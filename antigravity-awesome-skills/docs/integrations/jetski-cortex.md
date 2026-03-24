---
title: Jetski/Cortex + Gemini Integration Guide
description: "Come usare antigravity-awesome-skills con Jetski/Cortex evitando l’overflow di contesto con 1.309+ skill."
---

# Jetski/Cortex + Gemini: integrazione sicura con 1.309+ skill

Questa guida mostra come integrare il repository `antigravity-awesome-skills` con un agente basato su **Jetski/Cortex + Gemini** (o framework simili) **senza superare il context window** del modello.

L’errore tipico visto in Jetski/Cortex è:

> `TrajectoryChatConverter: could not convert a single message before hitting truncation`

Il problema non è nelle skill, ma **nel modo in cui vengono caricate**.

---

## 1. Antipattern da evitare

Non bisogna mai:

- leggere **tutte** le directory `skills/*/SKILL.md` all’avvio;
- concatenare il contenuto di tutte le `SKILL.md` in un singolo system prompt;
- reiniettare l’intera libreria per **ogni** richiesta.

Con oltre 1.309 skill, questo approccio riempie il context window prima ancora di aggiungere i messaggi dell’utente, causando l’errore di truncation.

---

## 2. Pattern raccomandato

Principi chiave:

- **Manifest leggero**: usare `data/skills_index.json` per sapere *quali* skill esistono, senza caricare i testi completi.
- **Lazy loading**: leggere `SKILL.md` **solo** per le skill effettivamente invocate in una conversazione (es. quando compare `@skill-id`).
- **Limiti espliciti**: imporre un massimo di skill/tokens caricati per turno, con fallback chiari.
- **Path safety**: verificare che i path del manifest restino dentro `SKILLS_ROOT` prima di leggere `SKILL.md`.

Il flusso consigliato è:

1. **Bootstrap**: all’avvio dell’agente leggere `data/skills_index.json` e costruire una mappa `id -> meta`.
2. **Parsing dei messaggi**: prima di chiamare il modello, estrarre tutti i riferimenti `@skill-id` dai messaggi utente/sistema.
3. **Risoluzione**: mappare gli id trovati in oggetti `SkillMeta` usando la mappa di bootstrap.
4. **Lazy load**: leggere i file `SKILL.md` solo per questi id (fino a un massimo configurabile).
5. **Prompt building**: costruire i system messages del modello includendo solo le definizioni delle skill selezionate.

---

## 3. Struttura di `skills_index.json`

Il file `data/skills_index.json` è un array di oggetti, ad esempio:

```json
{
  "id": "brainstorming",
  "path": "skills/brainstorming",
  "category": "planning",
  "name": "brainstorming",
  "description": "Use before any creative or constructive work.",
  "risk": "safe",
  "source": "official",
  "date_added": "2026-02-27"
}
```

Campi chiave:

- **`id`**: identificatore usato nelle menzioni `@id` (es. `@brainstorming`).
- **`path`**: directory che contiene la `SKILL.md` (es. `skills/brainstorming/`).

Per ottenere il percorso alla definizione della skill:

- `fullPath = path.join(SKILLS_ROOT, meta.path, "SKILL.md")`.

> Nota: `SKILLS_ROOT` è la directory radice dove avete installato il repository (es. `~/.agent/skills`).

---

## 4. Pseudo‑codice di integrazione (TypeScript)

> Esempio completo in: [`docs/integrations/jetski-gemini-loader/`](../../docs/integrations/jetski-gemini-loader/).

### 4.1. Tipi di base

```ts
type SkillMeta = {
  id: string;
  path: string;
  name: string;
  description?: string;
  category?: string;
  risk?: string;
};
```

### 4.2. Bootstrap: caricare il manifest

```ts
function loadSkillIndex(indexPath: string): Map<string, SkillMeta> {
  const raw = fs.readFileSync(indexPath, "utf8");
  const arr = JSON.parse(raw) as SkillMeta[];
  const map = new Map<string, SkillMeta>();
  for (const meta of arr) {
    map.set(meta.id, meta);
  }
  return map;
}
```

### 4.3. Parsing dei messaggi per trovare `@skill-id`

```ts
const SKILL_ID_REGEX = /@([a-zA-Z0-9-_./]+)/g;

function resolveSkillsFromMessages(
  messages: { role: string; content: string }[],
  index: Map<string, SkillMeta>,
  maxSkills: number
): SkillMeta[] {
  const found = new Set<string>();

  for (const msg of messages) {
    let match: RegExpExecArray | null;
    while ((match = SKILL_ID_REGEX.exec(msg.content)) !== null) {
      const id = match[1];
      if (index.has(id)) {
        found.add(id);
      }
    }
  }

  const metas: SkillMeta[] = [];
  for (const id of found) {
    const meta = index.get(id);
    if (meta) metas.push(meta);
    if (metas.length >= maxSkills) break;
  }

  return metas;
}
```

### 4.4. Lazy loading dei file `SKILL.md`

```ts
async function loadSkillBodies(
  skillsRoot: string,
  metas: SkillMeta[]
): Promise<string[]> {
  const bodies: string[] = [];

  for (const meta of metas) {
    const fullPath = path.join(skillsRoot, meta.path, "SKILL.md");
    const text = await fs.promises.readFile(fullPath, "utf8");
    bodies.push(text);
  }

  return bodies;
}
```

### 4.5. Costruzione del prompt Jetski/Cortex

Pseudocodice per la fase di pre‑processing, prima del `TrajectoryChatConverter`:

```ts
async function buildModelMessages(
  baseSystemMessages: { role: "system"; content: string }[],
  trajectory: { role: "user" | "assistant" | "system"; content: string }[],
  skillIndex: Map<string, SkillMeta>,
  skillsRoot: string,
  maxSkillsPerTurn: number,
  overflowBehavior: "truncate" | "error" = "truncate"
): Promise<{ role: string; content: string }[]> {
  const referencedSkills = resolveSkillsFromMessages(
    trajectory,
    skillIndex,
    Number.MAX_SAFE_INTEGER
  );
  if (
    overflowBehavior === "error" &&
    referencedSkills.length > maxSkillsPerTurn
  ) {
    throw new Error(
      `Too many skills requested in a single turn. Reduce @skill-id usage to ${maxSkillsPerTurn} or fewer.`
    );
  }

  const selectedMetas = resolveSkillsFromMessages(
    trajectory,
    skillIndex,
    maxSkillsPerTurn
  );

  const skillBodies = await loadSkillBodies(skillsRoot, selectedMetas);

  const skillMessages = skillBodies.map((body) => ({
    role: "system" as const,
    content: body,
  }));

  return [...baseSystemMessages, ...skillMessages, ...trajectory];
}
```

> Suggerimento: aggiungete una stima dei token per troncare o riassumere i `SKILL.md` se il context window si avvicina al limite.
> Il reference loader di questo repo supporta anche un fallback esplicito: `overflowBehavior: "error"`.

---

## 5. Gestione degli overflow di contesto

Per evitare errori difficili da capire per l’utente, impostate:

- una **soglia di sicurezza** (es. 70–80% del context window);
- un **limite massimo di skill per turno** (es. 5–10).

Strategie quando si supera la soglia:

- ridurre il numero di skill incluse (es. in base a recenza o priorità); oppure
- restituire un errore chiaro all’utente, ad esempio:

> "Sono state richieste troppe skill in un singolo turno. Riduci il numero di `@skill-id` nel messaggio o dividili in più passaggi."

---

## 6. Scenari di test raccomandati

- **Scenario 1 – Messaggio semplice ("hi")**
  - Nessun `@skill-id` → nessuna `SKILL.md` caricata → il prompt rimane piccolo → nessun errore.
- **Scenario 2 – Poche skill**
  - Messaggio con 1–2 `@skill-id` → solo le relative `SKILL.md` vengono caricate → nessun overflow.
- **Scenario 3 – Molte skill**
  - Messaggio con molte `@skill-id` → si attiva il limite `maxSkillsPerTurn` o il controllo di token → nessun overflow silenzioso.

---

## 7. Sottoinsiemi di skill e bundle

Per ulteriore controllo:

- spostate le skill non necessarie in `skills/.disabled/` per escluderle in certi ambienti;
- usate i **bundle** descritti in [`docs/users/bundles.md`](../users/bundles.md) per caricare solo gruppi tematici.

## 8. Recovery su Windows se siete gia in crash loop

Se l’host continua a riaprire la stessa trajectory corrotta dopo un errore di truncation:

- rimuovete la skill o il pacchetto problematico;
- cancellate Local Storage / Session Storage / IndexedDB usati da Antigravity;
- svuotate `%TEMP%`;
- riavviate con un loader lazy e limiti espliciti.

Guida completa:

- [`docs/users/windows-truncation-recovery.md`](../users/windows-truncation-recovery.md)

Per evitare che il problema si ripresenti:

- mantenete `overflowBehavior: "error"` quando preferite un fallimento esplicito;
- continuate a validare che i path risolti restino dentro `skillsRoot`.

---

## 9. Riepilogo

- Non concatenate mai tutte le `SKILL.md` in un singolo prompt.
- Usate `data/skills_index.json` come manifest leggero.
- Caricate le skill **on‑demand** in base a `@skill-id`.
- Impostate limiti chiari (max skill per turno, soglia di token).

Seguendo questo pattern, Jetski/Cortex + Gemini può usare l’intera libreria di `antigravity-awesome-skills` in modo sicuro, scalabile e compatibile con il context window dei modelli moderni.

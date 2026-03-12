import fs from "fs";
import path from "path";

export type SkillMeta = {
  id: string;
  path: string;
  name: string;
  description?: string;
  category?: string;
  risk?: string;
};

export type Message = {
  role: "system" | "user" | "assistant";
  content: string;
};

const SKILL_ID_REGEX = /@([a-zA-Z0-9-_./]+)/g;

export function loadSkillIndex(indexPath: string): Map<string, SkillMeta> {
  const raw = fs.readFileSync(indexPath, "utf8");
  const arr = JSON.parse(raw) as SkillMeta[];
  const map = new Map<string, SkillMeta>();

  for (const meta of arr) {
    map.set(meta.id, meta);
  }

  return map;
}

export function resolveSkillsFromMessages(
  messages: Message[],
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
    if (meta) {
      metas.push(meta);
    }
    if (metas.length >= maxSkills) {
      break;
    }
  }

  return metas;
}

export async function loadSkillBodies(
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

export async function buildModelMessages(options: {
  baseSystemMessages: Message[];
  trajectory: Message[];
  skillIndex: Map<string, SkillMeta>;
  skillsRoot: string;
  maxSkillsPerTurn?: number;
}): Promise<Message[]> {
  const {
    baseSystemMessages,
    trajectory,
    skillIndex,
    skillsRoot,
    maxSkillsPerTurn = 8,
  } = options;

  const selectedMetas = resolveSkillsFromMessages(
    trajectory,
    skillIndex,
    maxSkillsPerTurn
  );

  if (selectedMetas.length === 0) {
    return [...baseSystemMessages, ...trajectory];
  }

  const skillBodies = await loadSkillBodies(skillsRoot, selectedMetas);

  const skillMessages: Message[] = skillBodies.map((body) => ({
    role: "system",
    content: body,
  }));

  return [...baseSystemMessages, ...skillMessages, ...trajectory];
}


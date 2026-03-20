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

function collectReferencedSkillIds(
  messages: Message[],
  index: Map<string, SkillMeta>
): string[] {
  const referencedSkillIds = new Set<string>();

  for (const msg of messages) {
    for (const match of msg.content.matchAll(SKILL_ID_REGEX)) {
      const id = match[1];
      if (index.has(id)) {
        referencedSkillIds.add(id);
      }
    }
  }

  return [...referencedSkillIds];
}

function assertValidMaxSkills(maxSkills: number): number {
  if (!Number.isInteger(maxSkills) || maxSkills < 1) {
    throw new Error("maxSkills must be a positive integer.");
  }

  return maxSkills;
}

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
  const skillLimit = assertValidMaxSkills(maxSkills);
  const referencedSkillIds = collectReferencedSkillIds(messages, index);

  const metas: SkillMeta[] = [];
  for (const id of referencedSkillIds) {
    const meta = index.get(id);
    if (meta) {
      metas.push(meta);
    }
    if (metas.length >= skillLimit) {
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
  const rootPath = path.resolve(skillsRoot);
  const rootRealPath = await fs.promises.realpath(rootPath);

  for (const meta of metas) {
    const skillDirPath = path.resolve(rootPath, meta.path);
    const relativePath = path.relative(rootPath, skillDirPath);

    if (relativePath.startsWith("..") || path.isAbsolute(relativePath)) {
      throw new Error(`Skill path escapes skills root: ${meta.id}`);
    }

    const skillDirStat = await fs.promises.lstat(skillDirPath);
    if (!skillDirStat.isDirectory() || skillDirStat.isSymbolicLink()) {
      throw new Error(`Skill directory must be a regular directory inside the skills root: ${meta.id}`);
    }

    const fullPath = path.join(skillDirPath, "SKILL.md");
    const skillFileStat = await fs.promises.lstat(fullPath);
    if (!skillFileStat.isFile() || skillFileStat.isSymbolicLink()) {
      throw new Error(`SKILL.md must be a regular file inside the skills root: ${meta.id}`);
    }

    const realPath = await fs.promises.realpath(fullPath);
    const realRelativePath = path.relative(rootRealPath, realPath);
    if (realRelativePath.startsWith("..") || path.isAbsolute(realRelativePath)) {
      throw new Error(`SKILL.md resolves outside the skills root: ${meta.id}`);
    }

    const text = await fs.promises.readFile(realPath, "utf8");
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
  overflowBehavior?: "truncate" | "error";
}): Promise<Message[]> {
  const {
    baseSystemMessages,
    trajectory,
    skillIndex,
    skillsRoot,
    maxSkillsPerTurn = 8,
    overflowBehavior = "truncate",
  } = options;
  const skillLimit = assertValidMaxSkills(maxSkillsPerTurn);
  const referencedSkillIds = collectReferencedSkillIds(trajectory, skillIndex);

  if (
    overflowBehavior === "error" &&
    referencedSkillIds.length > skillLimit
  ) {
    throw new Error(
      `Too many skills requested in a single turn. Reduce @skill-id usage to ${skillLimit} or fewer.`
    );
  }

  const selectedMetas = resolveSkillsFromMessages(
    trajectory,
    skillIndex,
    skillLimit
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

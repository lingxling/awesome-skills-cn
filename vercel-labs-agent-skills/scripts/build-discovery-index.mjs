#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import {
  mkdirSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { join } from 'node:path';
import { parse } from 'yaml';

const schema = 'https://schemas.agentskills.io/discovery/0.2.0/schema.json';
const baseUrl = process.argv[2];
const outputDirectory = 'dist';
const archiveEnvironment = {
  ...process.env,
  GIT_AUTHOR_DATE: '2000-01-01T00:00:00Z',
  GIT_AUTHOR_EMAIL: 'agent-skills@vercel.com',
  GIT_AUTHOR_NAME: 'Agent Skills',
  GIT_COMMITTER_DATE: '2000-01-01T00:00:00Z',
  GIT_COMMITTER_EMAIL: 'agent-skills@vercel.com',
  GIT_COMMITTER_NAME: 'Agent Skills',
};

if (!baseUrl) {
  throw new Error(
    'Usage: node scripts/build-discovery-index.mjs <artifact-base-url>',
  );
}

const readMetadata = (directory) => {
  const path = `skills/${directory}/SKILL.md`;
  const source = execFileSync('git', ['show', `HEAD:${path}`], {
    encoding: 'utf8',
  });
  const frontmatter = source.match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1];
  if (!frontmatter) throw new Error(`Missing frontmatter in ${path}`);

  let metadata;
  try {
    metadata = parse(frontmatter);
  } catch (error) {
    throw new Error(`Invalid frontmatter in ${path}`, { cause: error });
  }

  if (!metadata || typeof metadata !== 'object') {
    throw new Error(`Invalid frontmatter in ${path}`);
  }

  const { name, description } = metadata;
  if (typeof name !== 'string' || typeof description !== 'string') {
    throw new Error(`Missing name or description in ${path}`);
  }

  if (
    name.length === 0 ||
    name.length > 64 ||
    !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) ||
    !description ||
    description.length > 1024
  ) {
    throw new Error(`Invalid name or description in ${path}`);
  }

  return { name, description };
};

const createArchive = (directory) => {
  const tree = execFileSync(
    'git',
    ['rev-parse', `HEAD:skills/${directory}`],
    { encoding: 'utf8' },
  ).trim();
  const commit = execFileSync('git', ['commit-tree', tree], {
    encoding: 'utf8',
    env: archiveEnvironment,
    input: 'Agent Skills archive\n',
  }).trim();
  const tar = execFileSync('git', ['archive', '--format=tar', commit]);
  return execFileSync('gzip', ['-n', '-9', '-c'], { input: tar });
};

const createArtifact = (directory) => {
  const entries = execFileSync(
    'git',
    ['ls-tree', '-r', `HEAD:skills/${directory}`],
    { encoding: 'utf8' },
  )
    .trim()
    .split('\n');
  if (entries.some((entry) => !/^100(?:644|755) blob /.test(entry))) {
    throw new Error(`Unsupported archive entry in skills/${directory}`);
  }

  const files = entries.map((entry) => entry.slice(entry.indexOf('\t') + 1));

  if (files.length === 1 && files[0] === 'SKILL.md') {
    return {
      content: execFileSync('git', [
        'show',
        `HEAD:skills/${directory}/SKILL.md`,
      ]),
      extension: 'md',
      type: 'skill-md',
    };
  }

  return {
    content: createArchive(directory),
    extension: 'tar.gz',
    type: 'archive',
  };
};

rmSync(outputDirectory, { force: true, recursive: true });
mkdirSync(outputDirectory);

const directories = execFileSync(
  'git',
  ['ls-tree', '-d', '--name-only', 'HEAD:skills'],
  { encoding: 'utf8' },
)
  .trim()
  .split('\n');

const skills = directories
  .map((directory) => {
    const metadata = readMetadata(directory);
    const artifact = createArtifact(directory);
    const filename = `${metadata.name}.${artifact.extension}`;
    writeFileSync(join(outputDirectory, filename), artifact.content);

    return {
      ...metadata,
      type: artifact.type,
      url: `${baseUrl.replace(/\/$/, '')}/${filename}`,
      digest: `sha256:${createHash('sha256')
        .update(artifact.content)
        .digest('hex')}`,
    };
  })
  .sort((a, b) => a.name.localeCompare(b.name));

if (new Set(skills.map(({ name }) => name)).size !== skills.length) {
  throw new Error('Skill names must be unique');
}

writeFileSync(
  join(outputDirectory, 'index.json'),
  `${JSON.stringify({ $schema: schema, skills }, null, 2)}\n`,
);

console.log(`Published ${skills.length} skills to ${outputDirectory}`);

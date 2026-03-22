import { act, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi, type Mock } from 'vitest';

import { getSkillsIndexCandidateUrls, SkillProvider, useSkills } from '../SkillContext';

// Keep tests deterministic by skipping real Supabase requests.
vi.mock('../../lib/supabase', () => ({
  supabase: {
    from: vi.fn(() => ({
      select: vi.fn().mockResolvedValue({ data: [], error: null }),
    })),
  },
}));

function SkillsProbe() {
  const { skills, loading } = useSkills();

  return (
    <div>
      <span data-testid="loading">{loading ? 'loading' : 'ready'}</span>
      <span data-testid="count">{skills.length}</span>
    </div>
  );
}

describe('getSkillsIndexCandidateUrls', () => {
  it('keeps stable candidates for gh-pages base path', () => {
    expect(
      getSkillsIndexCandidateUrls({
        baseUrl: '/antigravity-awesome-skills/',
        origin: 'https://sickn33.github.io',
        pathname: '/antigravity-awesome-skills/skill/some-id',
        documentBaseUrl: 'https://sickn33.github.io/antigravity-awesome-skills/',
      }),
    ).toEqual([
      'https://sickn33.github.io/antigravity-awesome-skills/skills.json',
      'https://sickn33.github.io/antigravity-awesome-skills/skills.json.backup',
      'https://sickn33.github.io/skills.json',
      'https://sickn33.github.io/skills.json.backup',
      'https://sickn33.github.io/antigravity-awesome-skills/skill/skills.json',
      'https://sickn33.github.io/antigravity-awesome-skills/skill/skills.json.backup',
      'https://sickn33.github.io/antigravity-awesome-skills/skill/some-id/skills.json',
      'https://sickn33.github.io/antigravity-awesome-skills/skill/some-id/skills.json.backup',
    ]);
  });

  it('normalizes dot-relative BASE_URL values', () => {
    expect(
      getSkillsIndexCandidateUrls({
        baseUrl: './',
        origin: 'https://sickn33.github.io',
        pathname: '/antigravity-awesome-skills/',
        documentBaseUrl: 'https://sickn33.github.io/antigravity-awesome-skills/',
      }),
    ).toEqual([
      'https://sickn33.github.io/antigravity-awesome-skills/skills.json',
      'https://sickn33.github.io/antigravity-awesome-skills/skills.json.backup',
      'https://sickn33.github.io/skills.json',
      'https://sickn33.github.io/skills.json.backup',
    ]);
  });
});

describe('SkillProvider', () => {
  beforeEach(() => {
    (global.fetch as Mock).mockReset();
    (global.fetch as Mock).mockImplementation(() => Promise.reject(new Error('unexpected fetch')));
    window.history.pushState({}, '', '/antigravity-awesome-skills/');
  });

  it('loads skills from a fallback candidate when the first URL fails', async () => {
    const mockSkills = [
      {
        id: 'skill-sample',
        path: 'skills/skill-sample',
        category: 'core',
        name: 'Sample skill',
        description: 'Sample description',
      },
    ];

    (global.fetch as Mock)
      .mockResolvedValueOnce({
        ok: false,
        status: 404,
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 404,
      })
      .mockResolvedValueOnce({
        ok: true,
        headers: {
          get: () => 'application/json',
        },
        text: async () => JSON.stringify(mockSkills),
      });

    render(
      <SkillProvider>
        <SkillsProbe />
      </SkillProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('loading').textContent).toBe('ready');
      expect(screen.getByTestId('count').textContent).toBe('1');
    });

    await act(async () => {
      await Promise.resolve();
    });
  });

  it('falls back to the bundled backup catalog when the primary index is invalid', async () => {
    const mockSkills = [
      {
        id: 'skill-backup',
        path: 'skills/skill-backup',
        category: 'core',
        name: 'Backup skill',
        description: 'Loaded from backup',
      },
    ];

    (global.fetch as Mock)
      .mockResolvedValueOnce({
        ok: true,
        headers: {
          get: () => 'text/html',
        },
        text: async () => '<!doctype html><html></html>',
      })
      .mockResolvedValueOnce({
        ok: true,
        headers: {
          get: () => 'application/json',
        },
        text: async () => JSON.stringify(mockSkills),
      });

    render(
      <SkillProvider>
        <SkillsProbe />
      </SkillProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('loading').textContent).toBe('ready');
      expect(screen.getByTestId('count').textContent).toBe('1');
    });
  });
});

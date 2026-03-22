import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';

const maybeSingle = vi.fn().mockResolvedValue({ data: null, error: null });
const upsert = vi.fn().mockResolvedValue({ error: null });
const select = vi.fn(() => ({ eq: vi.fn(() => ({ maybeSingle })) }));
const from = vi.fn(() => ({ select, upsert }));

vi.mock('../../lib/supabase', () => ({
  supabase: {
    from,
  },
}));

describe('useSkillStars shared writes', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
    from.mockReturnValue({ select, upsert });
    select.mockReturnValue({ eq: vi.fn(() => ({ maybeSingle })) });
    maybeSingle.mockResolvedValue({ data: null, error: null });
    upsert.mockResolvedValue({ error: null });
  });

  it('does not upsert shared star counts when frontend writes are disabled', async () => {
    const { useSkillStars } = await import('../useSkillStars');
    const { result } = renderHook(() => useSkillStars('shared-stars-disabled'));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.handleStarClick();
    });

    expect(upsert).not.toHaveBeenCalled();
    expect(result.current.hasStarred).toBe(true);
    expect(result.current.starCount).toBe(1);
  });
});

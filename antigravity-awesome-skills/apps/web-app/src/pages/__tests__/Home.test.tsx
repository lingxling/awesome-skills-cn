import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { screen, waitFor, fireEvent } from '@testing-library/react';
import { Home } from '../Home';
import { renderWithRouter } from '../../utils/testUtils';
import { createMockSkill } from '../../factories/skill';
import { useSkills } from '../../context/SkillContext';

// Mock lodash.debounce to execute immediately
vi.mock('lodash.debounce', () => ({
  default: vi.fn((fn) => {
    const mockedFn: any = (...args: any[]) => fn(...args);
    mockedFn.cancel = vi.fn();
    return mockedFn;
  }),
}));

// Mock useSkills hook
vi.mock('../../context/SkillContext', async (importOriginal) => {
  const actual = await importOriginal<any>();
  return { ...actual, useSkills: vi.fn() };
});

// Mock VirtuosoGrid to render items normally for easier testing
vi.mock('react-virtuoso', () => ({
  VirtuosoGrid: ({ totalCount, itemContent }: any) => (
    <div data-testid="virtuoso-grid">
      {Array.from({ length: totalCount || 0 }).map((_, index) => (
        <div key={index} data-testid="skill-item">
          {itemContent(index)}
        </div>
      ))}
    </div>
  ),
}));

describe('Home', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  describe('Rendering', () => {
    it('should show loading spinner when loading is true', () => {
      (useSkills as Mock).mockReturnValue({
        skills: [],
        stars: {},
        loading: true,
      });

      renderWithRouter(<Home />, { useProvider: false });
      expect(screen.getByTestId('loader')).toBeInTheDocument();
    });

    it('should render skill cards when skills are loaded', async () => {
      const mockSkills = [
        createMockSkill({ id: 'skill-1', name: 'Skill 1' }),
        createMockSkill({ id: 'skill-2', name: 'Skill 2' }),
      ];

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: {},
        loading: false,
      });

      renderWithRouter(<Home />, { useProvider: false });

      await waitFor(() => {
        expect(screen.getByText('@Skill 1')).toBeInTheDocument();
        expect(screen.getByText('@Skill 2')).toBeInTheDocument();
      });
    });
  });

  describe('Search and Filtering', () => {
    it('should filter skills based on search term', async () => {
      const mockSkills = [
        createMockSkill({ id: 'react', name: 'React Patterns' }),
        createMockSkill({ id: 'vue', name: 'Vue Basics' }),
      ];

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: {},
        loading: false,
      });

      renderWithRouter(<Home />, { useProvider: false });

      const searchInput = screen.getByLabelText(/Search skills/i);
      fireEvent.change(searchInput, { target: { value: 'React' } });

      await waitFor(() => {
        expect(searchInput).toHaveValue('React');
        expect(screen.getByText('@React Patterns')).toBeInTheDocument();
        expect(screen.queryByText('@Vue Basics')).not.toBeInTheDocument();
      });
    });

    it('should filter skills by category', async () => {
      const mockSkills = [
        createMockSkill({ id: 's1', category: 'frontend', name: 'Frontend Skill' }),
        createMockSkill({ id: 's2', category: 'backend', name: 'Backend Skill' }),
      ];

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: {},
        loading: false,
      });

      renderWithRouter(<Home />, { useProvider: false });

      const categorySelect = screen.getByLabelText(/Filter by category/i);
      fireEvent.change(categorySelect, { target: { value: 'frontend' } });

      await waitFor(() => {
        expect(categorySelect).toHaveValue('frontend');
        expect(screen.getByText('@Frontend Skill')).toBeInTheDocument();
        expect(screen.queryByText('@Backend Skill')).not.toBeInTheDocument();
      });
    });
  });

  describe('User Settings and Sync', () => {
    it('should sync local stars when sync button is clicked', async () => {
      const mockSkills = [createMockSkill({ id: 'skill-1' })];
      const refreshSkills = vi.fn().mockResolvedValue(undefined);

      (useSkills as Mock).mockReturnValue({
        skills: mockSkills,
        stars: { 'skill-1': 5 },
        loading: false,
        refreshSkills,
      });

      renderWithRouter(<Home />, { useProvider: false });

      const syncButton = screen.getByRole('button', { name: /Sync/i });

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ success: true, count: 1 })
      });

      fireEvent.click(syncButton);

      await waitFor(() => {
        expect(refreshSkills).toHaveBeenCalled();
      });
    });
  });
});

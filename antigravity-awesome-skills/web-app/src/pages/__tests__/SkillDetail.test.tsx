import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { screen, waitFor, fireEvent } from '@testing-library/react';
import { SkillDetail } from '../SkillDetail';
import { renderWithRouter } from '../../utils/testUtils';
import { createMockSkill } from '../../factories/skill';
import { useSkills } from '../../context/SkillContext';

// Mock the SkillStarButton component
vi.mock('../../components/SkillStarButton', () => ({
  SkillStarButton: ({ skillId, initialCount }: { skillId: string; initialCount?: number }) => (
    <button data-testid="star-button" data-skill-id={skillId} data-count={initialCount}>
      {initialCount || 0} Upvotes
    </button>
  ),
}));

// Mock useSkills hook
vi.mock('../../context/SkillContext', async (importOriginal) => {
  const actual = await importOriginal<any>();
  return {
    ...actual,
    useSkills: vi.fn(),
  };
});

// Mock react-markdown to avoid lazy loading issues in tests
vi.mock('react-markdown', () => ({
  default: ({ children }: { children: string }) => <div data-testid="markdown-content">{children}</div>,
}));

describe('SkillDetail', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  describe('Loading state', () => {
    it('should show loading spinner when context is loading', async () => {
      (useSkills as Mock).mockReturnValue({
        skills: [],
        stars: {},
        loading: true,
      });

      renderWithRouter(<SkillDetail />, {
        route: '/skill/test-skill',
        path: '/skill/:id',
        useProvider: false
      });

      expect(screen.getByTestId('loader')).toBeInTheDocument();
    });

    it('should show loading spinner when markdown is loading', async () => {
      const mockSkill = createMockSkill({ id: 'test-skill' });
      (useSkills as Mock).mockReturnValue({
        skills: [mockSkill],
        stars: {},
        loading: false,
      });

      // Mock fetch for markdown content to never resolve
      global.fetch = vi.fn().mockReturnValue(new Promise(() => { }));

      renderWithRouter(<SkillDetail />, {
        route: '/skill/test-skill',
        path: '/skill/:id',
        useProvider: false
      });

      await waitFor(() => {
        expect(screen.getByTestId('loader')).toBeInTheDocument();
      });
    });
  });

  describe('Skill rendering', () => {
    it('should render skill details correctly', async () => {
      const mockSkill = createMockSkill({
        id: 'react-patterns',
        name: 'react-patterns',
        description: 'React design patterns and best practices',
        category: 'frontend',
      });

      (useSkills as Mock).mockReturnValue({
        skills: [mockSkill],
        stars: { 'react-patterns': 5 },
        loading: false,
      });

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        text: async () => '# React Patterns\n\nThis is the skill content.',
      });

      renderWithRouter(<SkillDetail />, {
        route: '/skill/react-patterns',
        path: '/skill/:id',
        useProvider: false
      });

      await waitFor(() => {
        expect(screen.getByText('@react-patterns')).toBeInTheDocument();
        expect(screen.getByText('React design patterns and best practices')).toBeInTheDocument();
        expect(screen.getByTestId('markdown-content')).toHaveTextContent('This is the skill content.');
      });
    });

    it('should show skill not found when id does not exist', async () => {
      (useSkills as Mock).mockReturnValue({
        skills: [],
        stars: {},
        loading: false,
      });

      renderWithRouter(<SkillDetail />, {
        route: '/skill/nonexistent',
        path: '/skill/:id',
        useProvider: false
      });

      await waitFor(() => {
        expect(screen.getByText(/Error Loading Skill/i)).toBeInTheDocument();
        expect(screen.getByText(/Skill not found in registry/i)).toBeInTheDocument();
      });
    });
  });

  describe('Copy functionality', () => {
    it('should copy skill name to clipboard when clicked', async () => {
      const mockSkill = createMockSkill({ id: 'click-test', name: 'click-test' });

      (useSkills as Mock).mockReturnValue({
        skills: [mockSkill],
        stars: {},
        loading: false,
      });

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        text: async () => 'Content',
      });

      renderWithRouter(<SkillDetail />, {
        route: '/skill/click-test',
        path: '/skill/:id',
        useProvider: false
      });

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Copy @Skill/i })).toBeInTheDocument();
      });

      const copyButton = screen.getByRole('button', { name: /Copy @Skill/i });
      fireEvent.click(copyButton);

      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('Use @click-test');
    });
  });

  describe('Star button integration', () => {
    it('should render star button component with correct count', async () => {
      const mockSkill = createMockSkill({ id: 'star-integration' });

      (useSkills as Mock).mockReturnValue({
        skills: [mockSkill],
        stars: { 'star-integration': 10 },
        loading: false,
      });

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        text: async () => 'Content',
      });

      renderWithRouter(<SkillDetail />, {
        route: '/skill/star-integration',
        path: '/skill/:id',
        useProvider: false
      });

      await waitFor(() => {
        const starBtn = screen.getByTestId('star-button');
        expect(starBtn).toBeInTheDocument();
        expect(starBtn).toHaveAttribute('data-count', '10');
      });
    });
  });
});

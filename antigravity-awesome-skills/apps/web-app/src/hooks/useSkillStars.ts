import { useState, useEffect, useCallback } from 'react';
import { supabase } from '../lib/supabase';

const STORAGE_KEY = 'user_stars';

interface UserStars {
  [skillId: string]: boolean;
}

interface UseSkillStarsReturn {
  starCount: number;
  hasStarred: boolean;
  handleStarClick: () => Promise<void>;
  isLoading: boolean;
}

/**
 * Safely parse localStorage data with error handling
 */
function getUserStarsFromStorage(): UserStars {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return {};
    const parsed = JSON.parse(stored);
    return typeof parsed === 'object' && parsed !== null ? parsed : {};
  } catch (error) {
    console.warn('Failed to parse user_stars from localStorage:', error);
    return {};
  }
}

/**
 * Safely save to localStorage with error handling
 */
function saveUserStarsToStorage(stars: UserStars): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(stars));
  } catch (error) {
    console.warn('Failed to save user_stars to localStorage:', error);
  }
}

/**
 * Hook to manage skill starring functionality
 * Handles localStorage persistence, optimistic UI updates, and Supabase sync
 */
export function useSkillStars(skillId: string | undefined): UseSkillStarsReturn {
  const [starCount, setStarCount] = useState<number>(0);
  const [hasStarred, setHasStarred] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Initialize star count from Supabase and check if user has starred
  useEffect(() => {
    if (!skillId) return;

    const initializeStars = async () => {
      // Check localStorage for user's starred status
      const userStars = getUserStarsFromStorage();
      setHasStarred(!!userStars[skillId]);

      // Fetch star count from Supabase if available
      if (supabase) {
        try {
          const { data, error } = await supabase
            .from('skill_stars')
            .select('star_count')
            .eq('skill_id', skillId)
            .maybeSingle();

          if (!error && data) {
            setStarCount(data.star_count + (userStars[skillId] ? 1 : 0));
          }
        } catch (err) {
          console.warn('Failed to fetch star count:', err);
        }
      }
    };

    initializeStars();
  }, [skillId]);

  /**
   * Handle star button click
   * Prevents double-starring, updates optimistically, persists local state
   */
  const handleStarClick = useCallback(async () => {
    if (!skillId || isLoading) return;

    // Check if user has already starred (prevent spam)
    const userStars = getUserStarsFromStorage();
    if (userStars[skillId]) return;

    setIsLoading(true);

    try {
      // Optimistically update UI
      setStarCount(prev => prev + 1);
      setHasStarred(true);

      // Persist to localStorage
      const updatedStars = { ...userStars, [skillId]: true };
      saveUserStarsToStorage(updatedStars);
    } catch (error) {
      console.error('Failed to star skill:', error);
    } finally {
      setIsLoading(false);
    }
  }, [skillId, isLoading]);

  return {
    starCount,
    hasStarred,
    handleStarClick,
    isLoading
  };
}

export default useSkillStars;

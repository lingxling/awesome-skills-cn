import React from 'react';
import { Star } from 'lucide-react';
import { useSkillStars } from '../hooks/useSkillStars';

interface SkillStarButtonProps {
  skillId: string;
  communityCount?: number;
  onSaveClick?: () => void;
  variant?: 'default' | 'compact';
}

/**
 * Local-save button for skills with an optional read-only community count.
 */
export function SkillStarButton({
  skillId,
  communityCount = 0,
  onSaveClick,
  variant = 'default'
}: SkillStarButtonProps): React.ReactElement {
  const { hasSaved, handleSaveClick, isSaving } = useSkillStars(skillId);
  const actionLabel = hasSaved ? 'Saved locally' : 'Save locally';
  const communityLabel = communityCount > 0
    ? `${communityCount.toLocaleString('en-US')} community saves`
    : null;

  const handleClick = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (hasSaved || isSaving) return;

    await handleSaveClick();
    onSaveClick?.();
  };

  if (variant === 'compact') {
    return (
      <div className="flex flex-wrap items-center gap-2">
        {communityLabel && (
          <span className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs font-medium text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">
            {communityLabel}
          </span>
        )}
        <button
          onClick={handleClick}
          className="flex items-center space-x-1.5 px-3 py-1 bg-yellow-50 dark:bg-yellow-900/10 hover:bg-yellow-100 dark:hover:bg-yellow-900/30 text-yellow-700 dark:text-yellow-500 rounded-full text-xs font-bold border border-yellow-200 dark:border-yellow-700/50 transition-colors disabled:opacity-50"
          disabled={hasSaved || isSaving}
          title={hasSaved ? 'Saved in this browser' : 'Save this skill in this browser'}
        >
          <Star className={`h-3.5 w-3.5 ${hasSaved ? 'fill-yellow-500 stroke-yellow-500' : ''}`} />
          <span>{actionLabel}</span>
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-end gap-2 z-10">
      {communityLabel && (
        <span className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-[11px] font-medium text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">
          {communityLabel}
        </span>
      )}
      <button
        onClick={handleClick}
        className="flex items-center space-x-1 px-2.5 py-1.5 rounded-md bg-slate-50 dark:bg-slate-800/50 hover:bg-yellow-50 dark:hover:bg-yellow-900/20 text-slate-500 hover:text-yellow-600 dark:hover:text-yellow-500 transition-colors border border-slate-200 dark:border-slate-800 disabled:opacity-50"
        disabled={hasSaved || isSaving}
        title={hasSaved ? 'Saved in this browser' : 'Save this skill in this browser'}
      >
        <Star className={`h-4 w-4 ${hasSaved ? 'fill-yellow-400 stroke-yellow-400' : ''} ${isSaving ? 'animate-pulse' : ''}`} />
        <span className="text-xs font-semibold">{actionLabel}</span>
      </button>
    </div>
  );
}

export default SkillStarButton;

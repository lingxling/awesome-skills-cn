import React from 'react';
import { Link } from 'react-router-dom';
import { Book, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { SkillStarButton } from './SkillStarButton';
import type { Skill } from '../types';

interface SkillCardProps {
    skill: Skill;
    starCount: number;
}

export const SkillCard = React.memo(({ skill, starCount }: SkillCardProps) => {
    return (
        <motion.div
            layout
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="h-full"
        >
            <Link
                to={`/skill/${skill.id}`}
                className="group flex flex-col h-full rounded-lg border border-slate-200 bg-white p-6 shadow-sm transition-all hover:bg-slate-50 hover:shadow-md dark:border-slate-800 dark:bg-slate-900 dark:hover:border-indigo-500/50"
            >
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                        <div className="p-2 bg-indigo-50 dark:bg-indigo-950/30 rounded-md">
                            <Book className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
                        </div>
                        <span className="text-xs font-medium px-2 py-1 rounded-full bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400">
                            {skill.category || 'Uncategorized'}
                        </span>
                    </div>
                    <SkillStarButton
                        skillId={skill.id}
                        initialCount={starCount}
                        variant="default"
                    />
                </div>

                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-50 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors mb-2 line-clamp-1">
                    @{skill.name}
                </h3>

                <p className="text-sm text-slate-500 dark:text-slate-400 line-clamp-3 mb-4 flex-grow">
                    {skill.description}
                </p>

                <div className="flex items-center justify-between text-xs text-slate-400 dark:text-slate-500 mb-3 pb-3 border-b border-slate-100 dark:border-slate-800">
                    <span>Risk: <span className="font-semibold text-slate-600 dark:text-slate-300">{skill.risk || 'unknown'}</span></span>
                    {skill.date_added && (
                        <span className="ml-2">📅 {skill.date_added}</span>
                    )}
                </div>

                <div className="flex items-center text-sm font-medium text-indigo-600 dark:text-indigo-400 pt-2 mt-auto group-hover:translate-x-1 transition-transform">
                    Read Skill <ArrowRight className="ml-1 h-4 w-4" />
                </div>
            </Link>
        </motion.div>
    );
});

SkillCard.displayName = 'SkillCard';

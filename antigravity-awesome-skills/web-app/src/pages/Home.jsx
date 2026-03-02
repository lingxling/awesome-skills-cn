import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Book, AlertCircle, ArrowRight, Star } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { supabase } from '../lib/supabase';

export function Home() {
    const [skills, setSkills] = useState([]);
    const [filteredSkills, setFilteredSkills] = useState([]);
    const [search, setSearch] = useState('');
    const [categoryFilter, setCategoryFilter] = useState('all');
    const [loading, setLoading] = useState(true);
    const [displayCount, setDisplayCount] = useState(24);
    const [stars, setStars] = useState({});

    useEffect(() => {
        const fetchSkillsAndStars = async () => {
            try {
                const res = await fetch('/skills.json');
                const data = await res.json();

                setSkills(data);
                setFilteredSkills(data);

                if (supabase) {
                    const { data: starData, error } = await supabase
                        .from('skill_stars')
                        .select('skill_id, star_count');

                    if (!error && starData) {
                        const starMap = {};
                        starData.forEach(item => {
                            starMap[item.skill_id] = item.star_count;
                        });
                        setStars(starMap);
                    }
                }
            } catch (err) {
                console.error("Failed to load skills", err);
            } finally {
                setLoading(false);
            }
        };

        fetchSkillsAndStars();
    }, []);

    const handleStarClick = async (e, skillId) => {
        e.preventDefault();

        const storedStars = JSON.parse(localStorage.getItem('user_stars') || '{}');
        if (storedStars[skillId]) return;

        setStars(prev => ({
            ...prev,
            [skillId]: (prev[skillId] || 0) + 1
        }));

        localStorage.setItem('user_stars', JSON.stringify({
            ...storedStars,
            [skillId]: true
        }));

        if (supabase) {
            const { data } = await supabase
                .from('skill_stars')
                .select('star_count')
                .eq('skill_id', skillId)
                .single();

            if (data) {
                await supabase
                    .from('skill_stars')
                    .update({ star_count: data.star_count + 1 })
                    .eq('skill_id', skillId);
            } else {
                await supabase
                    .from('skill_stars')
                    .insert({ skill_id: skillId, star_count: 1 });
            }
        }
    };

    const calculateScore = (skill, terms) => {
        let score = 0;
        const nameLower = skill.name.toLowerCase();
        const descLower = (skill.description || '').toLowerCase();
        const catLower = (skill.category || '').toLowerCase();

        for (const term of terms) {
            if (nameLower === term) score += 100;
            else if (nameLower.startsWith(term)) score += 50;
            else if (nameLower.includes(term)) score += 30;
            else if (catLower.includes(term)) score += 20;
            else if (descLower.includes(term)) score += 10;
        }
        return score;
    };

    useEffect(() => {
        let result = skills;

        if (search) {
            const terms = search.toLowerCase().trim().split(/\s+/).filter(t => t.length > 0);
            if (terms.length > 0) {
                result = result
                    .map(skill => ({ ...skill, _score: calculateScore(skill, terms) }))
                    .filter(skill => skill._score > 0)
                    .sort((a, b) => b._score - a._score);
            }
        }

        if (categoryFilter !== 'all') {
            result = result.filter(skill => skill.category === categoryFilter);
        }

        setFilteredSkills(result);
    }, [search, categoryFilter, skills]);

    useEffect(() => {
        setDisplayCount(24);
    }, [search, categoryFilter]);

    const categoryStats = {};
    skills.forEach(skill => {
        categoryStats[skill.category] = (categoryStats[skill.category] || 0) + 1;
    });

    const categories = ['all', ...Object.keys(categoryStats)
        .filter(cat => cat !== 'uncategorized')
        .sort((a, b) => categoryStats[b] - categoryStats[a]),
        ...(categoryStats['uncategorized'] ? ['uncategorized'] : [])
    ];

    return (
        <div className="space-y-8">
            <div className="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mb-2">Explore Skills</h1>
                    <p className="text-slate-500 dark:text-slate-400">
                        {search || categoryFilter !== 'all'
                            ? `Showing ${filteredSkills.length} of ${skills.length} skills`
                            : `Discover ${skills.length} agentic capabilities for your AI assistant.`}
                    </p>
                </div>
            </div>

            <div className="flex flex-col space-y-4 md:flex-row md:items-center md:space-x-4 md:space-y-0 bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm sticky top-20 z-40">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
                    <input
                        type="text"
                        placeholder="Search skills (e.g., 'react', 'security', 'python', 'testing')..."
                        className="w-full rounded-md border border-slate-200 bg-slate-50 px-9 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50 pr-9"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                    {search && (
                        <button
                            onClick={() => setSearch('')}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                            title="Clear search"
                        >
                            ×
                        </button>
                    )}
                </div>
                <div className="flex items-center space-x-2 overflow-x-auto pb-2 md:pb-0 scrollbar-hide">
                    <Filter className="h-4 w-4 text-slate-500 shrink-0" />
                    <select
                        className="h-9 rounded-md border border-slate-200 bg-slate-50 px-3 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50 min-w-[150px]"
                        value={categoryFilter}
                        onChange={(e) => setCategoryFilter(e.target.value)}
                    >
                        {categories.map(cat => (
                            <option key={cat} value={cat}>
                                {cat === 'all'
                                    ? 'All Categories'
                                    : `${cat.charAt(0).toUpperCase() + cat.slice(1)} (${categoryStats[cat] || 0})`
                                }
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                <AnimatePresence>
                    {loading ? (
                        [...Array(8)].map((_, i) => (
                            <div key={i} className="animate-pulse rounded-lg border border-slate-200 p-6 h-48 bg-slate-100 dark:border-slate-800 dark:bg-slate-900">
                            </div>
                        ))
                    ) : filteredSkills.length === 0 ? (
                        <div className="col-span-full py-12 text-center">
                            <AlertCircle className="mx-auto h-12 w-12 text-slate-400" />
                            <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100">No skills found</h3>
                            <p className="mt-2 text-slate-500 dark:text-slate-400">Try adjusting your search or filter.</p>
                        </div>
                    ) : (
                        filteredSkills.slice(0, displayCount).map((skill) => (
                            <motion.div
                                key={skill.id}
                                layout
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                transition={{ duration: 0.2 }}
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
                                        <button
                                            onClick={(e) => handleStarClick(e, skill.id)}
                                            className="flex items-center space-x-1 px-2 py-1 rounded-md bg-slate-50 dark:bg-slate-800/50 hover:bg-yellow-50 dark:hover:bg-yellow-900/20 text-slate-500 hover:text-yellow-600 dark:hover:text-yellow-500 transition-colors border border-slate-200 dark:border-slate-800 z-10"
                                            title="Upvote skill"
                                        >
                                            <Star className={`h-4 w-4 ${JSON.parse(localStorage.getItem('user_stars') || '{}')[skill.id] ? 'fill-yellow-400 stroke-yellow-400' : ''}`} />
                                            <span className="text-xs font-semibold">{stars[skill.id] || 0}</span>
                                        </button>
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
                        ))
                    )}
                </AnimatePresence>

                {!loading && filteredSkills.length > displayCount && (
                    <div className="col-span-full flex justify-center py-8">
                        <button
                            onClick={() => setDisplayCount(prev => prev + 24)}
                            className="flex items-center space-x-2 px-6 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors shadow-sm"
                        >
                            <span>Load More</span>
                            <span className="text-sm text-slate-500 dark:text-slate-400">
                                ({filteredSkills.length - displayCount} remaining)
                            </span>
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

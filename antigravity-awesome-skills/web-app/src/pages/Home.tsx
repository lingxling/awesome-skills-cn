import { useState, useEffect, useMemo, useCallback } from 'react';
import { Search, Filter, AlertCircle, RefreshCw, ArrowUpDown } from 'lucide-react';
import { VirtuosoGrid } from 'react-virtuoso';
import debounce from 'lodash.debounce';
import { useSkills } from '../context/SkillContext';
import { SkillCard } from '../components/SkillCard';
import type { SyncMessage, CategoryStats } from '../types';

export function Home(): React.ReactElement {
  const { skills, stars, loading, refreshSkills } = useSkills();
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [sortBy, setSortBy] = useState('default');
  const [syncing, setSyncing] = useState(false);
  const [syncMsg, setSyncMsg] = useState<SyncMessage | null>(null);

  // Debounce search input to avoid excessive filtering on every keystroke
  const debouncedSetSearch = useCallback(
    debounce((value: string) => {
      setDebouncedSearch(value);
    }, 300),
    []
  );

  useEffect(() => {
    debouncedSetSearch(search);
  }, [search, debouncedSetSearch]);

  const filteredSkills = useMemo(() => {
    let result = [...skills];

    if (debouncedSearch) {
      const lowerSearch = debouncedSearch.toLowerCase();
      result = result.filter(skill =>
        skill.name.toLowerCase().includes(lowerSearch) ||
        skill.description.toLowerCase().includes(lowerSearch)
      );
    }

    if (categoryFilter !== 'all') {
      result = result.filter(skill => skill.category === categoryFilter);
    }

    // Apply sorting
    if (sortBy === 'stars') {
      result = [...result].sort((a, b) => (stars[b.id] || 0) - (stars[a.id] || 0));
    } else if (sortBy === 'newest') {
      result = [...result].sort((a, b) => (b.date_added || '').localeCompare(a.date_added || ''));
    } else if (sortBy === 'az') {
      result = [...result].sort((a, b) => a.name.localeCompare(b.name));
    }

    return result;
  }, [debouncedSearch, categoryFilter, sortBy, skills, stars]);

  // Sort categories by count (most skills first), with 'uncategorized' at the end
  const { categories, categoryStats } = useMemo(() => {
    const stats: CategoryStats = {};
    skills.forEach(skill => {
      stats[skill.category] = (stats[skill.category] || 0) + 1;
    });

    const cats = ['all', ...Object.keys(stats)
      .filter(cat => cat !== 'uncategorized')
      .sort((a, b) => stats[b] - stats[a]),
      ...(stats['uncategorized'] ? ['uncategorized'] : [])
    ];

    return { categories: cats, categoryStats: stats };
  }, [skills]);

  const handleSync = async () => {
    setSyncing(true);
    setSyncMsg(null);
    try {
      const res = await fetch('/api/refresh-skills');
      const data = await res.json();
      if (data.success) {
        if (data.upToDate) {
          setSyncMsg({ type: 'info', text: 'ℹ️ Skills are already up to date!' });
        } else {
          setSyncMsg({ type: 'success', text: `✅ Synced ${data.count} skills!` });
          await refreshSkills();
        }
      } else {
        setSyncMsg({ type: 'error', text: `❌ ${data.error}` });
      }
    } catch (err) {
      setSyncMsg({ type: 'error', text: '❌ Network error' });
    } finally {
      setSyncing(false);
      setTimeout(() => setSyncMsg(null), 5000);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div className="space-y-8 mb-8">
        <div className="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mb-2">Explore Skills</h1>
            <p className="text-slate-500 dark:text-slate-400">Discover {skills.length} agentic capabilities for your AI assistant.</p>
          </div>
          <div className="flex items-center gap-3">
            {syncMsg && (
              <span className={`text-sm font-medium px-3 py-1.5 rounded-full ${syncMsg.type === 'success'
                ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                : syncMsg.type === 'info'
                  ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                  : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                }`}>
                {syncMsg.text}
              </span>
            )}
            <button
              onClick={handleSync}
              disabled={syncing}
              className="flex items-center space-x-2 px-4 py-2.5 rounded-lg font-medium text-sm bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50 disabled:cursor-wait transition-colors shadow-sm"
            >
              <RefreshCw className={`h-4 w-4 ${syncing ? 'animate-spin' : ''}`} />
              <span>{syncing ? 'Syncing...' : 'Sync Skills'}</span>
            </button>
          </div>
        </div>

        <div className="flex flex-col space-y-4 md:flex-row md:items-center md:space-x-4 md:space-y-0 bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm sticky top-0 z-40">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              placeholder="Search skills (e.g., 'react', 'security', 'python')..."
              aria-label="Search skills"
              className="w-full rounded-md border border-slate-200 bg-slate-50 px-9 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="flex items-center space-x-2 overflow-x-auto pb-2 md:pb-0 scrollbar-hide">
            <Filter className="h-4 w-4 text-slate-500 shrink-0" />
            <select
              aria-label="Filter by category"
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
            <ArrowUpDown className="h-4 w-4 text-slate-500 shrink-0 ml-2" />
            <select
              aria-label="Sort skills"
              className="h-9 rounded-md border border-slate-200 bg-slate-50 px-3 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50 min-w-[130px]"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="default">Default</option>
              <option value="stars">⭐ Most Stars</option>
              <option value="newest">🆕 Newest</option>
              <option value="az">🔤 A → Z</option>
            </select>
          </div>
        </div>
      </div>

      <div className="flex-1 min-h-0 -mx-4">
        {loading ? (
          <div data-testid="loader" className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 px-4">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="animate-pulse rounded-lg border border-slate-200 p-6 h-48 bg-slate-100 dark:border-slate-800 dark:bg-slate-900">
              </div>
            ))}
          </div>
        ) : filteredSkills.length === 0 ? (
          <div className="py-12 text-center px-4 sm:px-6 lg:px-8">
            <AlertCircle className="mx-auto h-12 w-12 text-slate-400" />
            <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100">No skills found</h3>
            <p className="mt-2 text-slate-500 dark:text-slate-400">Try adjusting your search or filter.</p>
          </div>
        ) : (
          <VirtuosoGrid
            style={{ height: '100%' }}
            totalCount={filteredSkills.length}
            listClassName="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 pb-8 px-4"
            itemContent={(index) => {
              const skill = filteredSkills[index];
              return <SkillCard key={skill.id} skill={skill} starCount={stars[skill.id] || 0} />;
            }}
          />
        )}
      </div>
    </div>
  );
}

export default Home;

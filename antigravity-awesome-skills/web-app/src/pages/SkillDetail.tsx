import { useState, useEffect, useMemo, lazy, Suspense } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Copy, Check, FileCode, AlertTriangle, Loader2 } from 'lucide-react';
import { SkillStarButton } from '../components/SkillStarButton';
import { useSkills } from '../context/SkillContext';

// Lazy load heavy markdown component
const Markdown = lazy(() => import('react-markdown'));

interface RouteParams {
  id: string;
  [key: string]: string | undefined;
}

export function SkillDetail(): React.ReactElement {
  const { id } = useParams<RouteParams>();
  const { skills, stars, loading: contextLoading } = useSkills();
  const [content, setContent] = useState('');
  const [contentLoading, setContentLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [copiedFull, setCopiedFull] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [customContext, setCustomContext] = useState('');

  const skill = useMemo(() => skills.find(s => s.id === id), [skills, id]);
  const starCount = useMemo(() => (id ? stars[id] || 0 : 0), [stars, id]);

  useEffect(() => {
    if (contextLoading || !skill) return;

    const loadMarkdown = async () => {
      setContentLoading(true);
      try {
        const cleanPath = skill.path.startsWith('skills/')
          ? skill.path.replace('skills/', '')
          : skill.path;

        const mdRes = await fetch(`/skills/${cleanPath}/SKILL.md`);
        if (!mdRes.ok) throw new Error('Skill file not found');

        const text = await mdRes.text();
        setContent(text);
      } catch (err) {
        console.error('Failed to load skill content', err);
        setError(err instanceof Error ? err.message : 'Could not load skill content.');
      } finally {
        setContentLoading(false);
      }
    };

    loadMarkdown();
  }, [skill, contextLoading]);

  const copyToClipboard = () => {
    if (!skill) return;

    const basePrompt = `Use @${skill.name}`;
    const finalPrompt = customContext.trim()
      ? `${basePrompt}\n\nContext:\n${customContext}`
      : basePrompt;

    navigator.clipboard.writeText(finalPrompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const copyFullToClipboard = () => {
    const finalPrompt = customContext.trim()
      ? `${content}\n\nContext:\n${customContext}`
      : content;

    navigator.clipboard.writeText(finalPrompt);
    setCopiedFull(true);
    setTimeout(() => setCopiedFull(false), 2000);
  };

  if (!contextLoading && !skill) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] text-center px-4">
        <h2 className="text-xl font-bold mb-2">Error Loading Skill</h2>
        <p className="text-slate-600 dark:text-slate-400">Skill not found in registry.</p>
        <Link to="/" className="mt-4 text-indigo-600 hover:underline">Back to Catalog</Link>
      </div>
    );
  }

  if (contextLoading || (contentLoading && !error)) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]" data-testid="loader">
        <Loader2 className="animate-spin h-8 w-8 text-indigo-600" />
      </div>
    );
  }

  // If we're here, contextLoading is false, skill is defined, and content loading is finished (or errored)
  if (error || !skill) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">Failed to Load Content</h2>
        <p className="text-slate-500 mt-2">{error || 'Skill details could not be loaded.'}</p>
        <Link to="/" className="mt-8 inline-flex items-center text-indigo-600 font-medium hover:underline">
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to Catalog
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <Link to="/" className="inline-flex items-center text-sm font-medium text-slate-500 hover:text-indigo-600 transition-colors mb-4 group">
          <ArrowLeft className="mr-1 h-4 w-4 transform group-hover:-translate-x-1 transition-transform" />
          Back to Catalog
        </Link>

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2 flex-wrap gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-400 uppercase tracking-wide">
                {skill.category}
              </span>
              {skill.source && (
                <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400">
                  {skill.source}
                </span>
              )}
              {skill.date_added && (
                <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-400">
                  📅 Added {skill.date_added}
                </span>
              )}
            </div>
            <div className="flex items-center gap-3">
              <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
                @{skill.name}
              </h1>
              <SkillStarButton skillId={skill.id} initialCount={starCount} variant="compact" />
            </div>
            <p className="mt-2 text-lg text-slate-600 dark:text-slate-400">
              {skill.description}
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-2">
            <button
              onClick={copyToClipboard}
              className="flex items-center justify-center space-x-2 bg-slate-100 hover:bg-slate-200 text-slate-900 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700 px-4 py-2.5 rounded-lg font-medium transition-colors min-w-[140px] border border-slate-200 dark:border-slate-700"
            >
              {copied ? <Check className="h-4 w-4 text-green-600 dark:text-green-400" /> : <Copy className="h-4 w-4" />}
              <span>{copied ? 'Copied!' : 'Copy @Skill'}</span>
            </button>
            <button
              onClick={copyFullToClipboard}
              className="flex items-center justify-center space-x-2 bg-slate-900 hover:bg-slate-800 text-white dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-200 px-4 py-2.5 rounded-lg font-medium transition-colors min-w-[140px]"
            >
              {copiedFull ? <Check className="h-4 w-4 text-green-400" /> : <FileCode className="h-4 w-4" />}
              <span>{copiedFull ? 'Copied Content!' : 'Copy Full Content'}</span>
            </button>
          </div>
        </div>

        <div className="mt-6 bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <label htmlFor="context" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            Interactive Prompt Builder (Optional)
          </label>
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-3">
            Add specific details below (e.g. &quot;Use React 19 and Tailwind&quot;). The &quot;Copy Prompt&quot; button will automatically attach your context.
          </p>
          <textarea
            id="context"
            rows={3}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-4 py-3 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all resize-y"
            placeholder="Type your specific task requirements here..."
            value={customContext}
            onChange={(e) => setCustomContext(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div className="p-6 sm:p-8">
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <Suspense fallback={<div className="h-24 animate-pulse bg-slate-100 dark:bg-slate-800 rounded-lg"></div>}>
              <Markdown>{content}</Markdown>
            </Suspense>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SkillDetail;

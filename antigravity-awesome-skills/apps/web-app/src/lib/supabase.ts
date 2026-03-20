import { createClient, SupabaseClient } from '@supabase/supabase-js'

// Public Supabase credentials for the shared community stars database.
// The anon key is a public key by design — security is enforced via RLS policies.
// .env values override these defaults if provided.
const supabaseUrl =
  (import.meta as ImportMeta & { env: Record<string, string> }).env.VITE_SUPABASE_URL
  || 'https://gczhgcbtjbvfrgfmpbmv.supabase.co'

const supabaseAnonKey =
  (import.meta as ImportMeta & { env: Record<string, string> }).env.VITE_SUPABASE_ANON_KEY
  || 'sb_publishable_CyVwHGbtT80AuDFmXNkc9Q_YNcamTGg'

// Create a single supabase client for interacting with the database
export const supabase: SupabaseClient = createClient(supabaseUrl, supabaseAnonKey)

// Type for star data in the database
export interface SkillStarData {
  skill_id: string
  star_count: number
}

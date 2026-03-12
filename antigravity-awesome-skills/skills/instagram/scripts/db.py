"""
Camada de persistência SQLite para a skill Instagram.

Uso:
    from db import Database
    db = Database()
    db.init()
    db.upsert_account({...})
    db.insert_post({...})
    stats = db.get_stats()
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import DB_PATH

DDL = """
-- Contas Instagram (multi-conta ready)
CREATE TABLE IF NOT EXISTS accounts (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    ig_user_id        TEXT    UNIQUE NOT NULL,
    username          TEXT,
    account_type      TEXT,
    access_token      TEXT    NOT NULL,
    token_expires_at  TEXT,
    facebook_page_id  TEXT,
    app_id            TEXT,
    app_secret        TEXT,
    is_active         INTEGER DEFAULT 1,
    created_at        TEXT    DEFAULT (datetime('now'))
);

-- Pipeline de conteúdo: draft → approved → scheduled → container_created → published | failed
CREATE TABLE IF NOT EXISTS posts (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id        INTEGER REFERENCES accounts(id),
    media_type        TEXT,
    media_url         TEXT,
    local_path        TEXT,
    caption           TEXT,
    hashtags          TEXT,
    template_id       INTEGER REFERENCES templates(id),
    status            TEXT    DEFAULT 'draft',
    scheduled_at      TEXT,
    published_at      TEXT,
    ig_media_id       TEXT,
    ig_container_id   TEXT,
    permalink         TEXT,
    error_msg         TEXT,
    created_at        TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS comments (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id        INTEGER REFERENCES accounts(id),
    ig_comment_id     TEXT    UNIQUE,
    ig_media_id       TEXT,
    username          TEXT,
    text              TEXT,
    timestamp         TEXT,
    replied           INTEGER DEFAULT 0,
    reply_text        TEXT,
    hidden            INTEGER DEFAULT 0,
    fetched_at        TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS insights (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id        INTEGER REFERENCES accounts(id),
    ig_media_id       TEXT,
    metric_name       TEXT,
    metric_value      REAL,
    period            TEXT,
    fetched_at        TEXT    DEFAULT (datetime('now')),
    raw_json          TEXT
);

CREATE TABLE IF NOT EXISTS user_insights (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id        INTEGER REFERENCES accounts(id),
    metric_name       TEXT,
    metric_value      REAL,
    period            TEXT,
    end_time          TEXT,
    fetched_at        TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS templates (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT    UNIQUE NOT NULL,
    caption_template  TEXT,
    hashtag_set       TEXT,
    default_schedule_time TEXT,
    created_at        TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS hashtag_searches (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id        INTEGER REFERENCES accounts(id),
    hashtag           TEXT,
    ig_hashtag_id     TEXT,
    searched_at       TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS action_log (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id        INTEGER,
    action            TEXT    NOT NULL,
    params            TEXT,
    result            TEXT,
    confirmed         INTEGER,
    rate_remaining    TEXT,
    created_at        TEXT    DEFAULT (datetime('now'))
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_posts_status       ON posts (status);
CREATE INDEX IF NOT EXISTS idx_posts_account       ON posts (account_id);
CREATE INDEX IF NOT EXISTS idx_posts_scheduled     ON posts (scheduled_at);
CREATE INDEX IF NOT EXISTS idx_comments_media      ON comments (ig_media_id);
CREATE INDEX IF NOT EXISTS idx_comments_account    ON comments (account_id);
CREATE INDEX IF NOT EXISTS idx_insights_media      ON insights (ig_media_id);
CREATE INDEX IF NOT EXISTS idx_insights_account    ON insights (account_id);
CREATE INDEX IF NOT EXISTS idx_user_insights_acct  ON user_insights (account_id);
CREATE INDEX IF NOT EXISTS idx_action_log_action   ON action_log (action);
CREATE INDEX IF NOT EXISTS idx_action_log_time     ON action_log (created_at);
CREATE INDEX IF NOT EXISTS idx_hashtag_searched    ON hashtag_searches (searched_at);
"""


_POSTS_COLUMNS = frozenset({
    "account_id", "media_type", "media_url", "local_path", "caption",
    "hashtags", "template_id", "status", "scheduled_at", "published_at",
    "ig_media_id", "ig_container_id", "permalink", "error_msg", "created_at",
})


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def init(self) -> None:
        """Cria tabelas e índices se não existirem."""
        with self._connect() as conn:
            conn.executescript(DDL)

    # ── Accounts ──────────────────────────────────────────────────────────────

    def upsert_account(self, data: Dict[str, Any]) -> int:
        """Insere ou atualiza conta. Retorna o id da conta."""
        sql = """
        INSERT INTO accounts (ig_user_id, username, account_type, access_token,
                              token_expires_at, facebook_page_id, app_id, app_secret)
        VALUES (:ig_user_id, :username, :account_type, :access_token,
                :token_expires_at, :facebook_page_id, :app_id, :app_secret)
        ON CONFLICT(ig_user_id) DO UPDATE SET
            username = excluded.username,
            account_type = excluded.account_type,
            access_token = excluded.access_token,
            token_expires_at = excluded.token_expires_at,
            facebook_page_id = excluded.facebook_page_id,
            app_id = excluded.app_id,
            app_secret = excluded.app_secret,
            is_active = 1
        """
        with self._connect() as conn:
            conn.execute(sql, data)
            row = conn.execute(
                "SELECT id FROM accounts WHERE ig_user_id = ?",
                [data["ig_user_id"]]
            ).fetchone()
            return row["id"]

    def get_active_account(self) -> Optional[Dict[str, Any]]:
        """Retorna a conta ativa (primeira ativa encontrada)."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM accounts WHERE is_active = 1 ORDER BY id LIMIT 1"
            ).fetchone()
        return dict(row) if row else None

    def get_account_by_id(self, account_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM accounts WHERE id = ?", [account_id]
            ).fetchone()
        return dict(row) if row else None

    def update_token(self, account_id: int, access_token: str, expires_at: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE accounts SET access_token = ?, token_expires_at = ? WHERE id = ?",
                [access_token, expires_at, account_id],
            )

    # ── Posts (Pipeline) ──────────────────────────────────────────────────────

    def insert_post(self, data: Dict[str, Any]) -> int:
        """Cria um novo post (draft por padrão). Retorna o id."""
        keys = [k for k in data.keys() if k != "id" and k in _POSTS_COLUMNS]
        if not keys:
            raise ValueError("No valid columns provided for insert_post")
        placeholders = ", ".join("?" for _ in keys)
        columns = ", ".join(keys)
        values = [data[k] for k in keys]
        sql = f"INSERT INTO posts ({columns}) VALUES ({placeholders})"
        with self._connect() as conn:
            cursor = conn.execute(sql, values)
            return cursor.lastrowid

    def update_post_status(self, post_id: int, status: str, **extra) -> None:
        """Atualiza status de um post e campos adicionais."""
        sets = ["status = ?"]
        params: list = [status]
        for k, v in extra.items():
            if k not in _POSTS_COLUMNS:
                raise ValueError(f"Invalid column name for update_post_status: {k}")
            sets.append(f"{k} = ?")
            params.append(v)
        params.append(post_id)
        sql = f"UPDATE posts SET {', '.join(sets)} WHERE id = ?"
        with self._connect() as conn:
            conn.execute(sql, params)

    def get_posts(
        self,
        account_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        conditions = []
        params: list = []
        if account_id:
            conditions.append("account_id = ?")
            params.append(account_id)
        if status:
            conditions.append("status = ?")
            params.append(status)
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"SELECT * FROM posts {where} ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def get_posts_for_publishing(self, account_id: int) -> List[Dict[str, Any]]:
        """Posts aprovados/agendados prontos para publicar."""
        now = datetime.now(timezone.utc).isoformat()
        sql = """
        SELECT * FROM posts
        WHERE account_id = ? AND (
            status = 'approved'
            OR (status = 'scheduled' AND scheduled_at <= ?)
            OR status = 'container_created'
        )
        ORDER BY scheduled_at ASC, created_at ASC
        """
        with self._connect() as conn:
            rows = conn.execute(sql, [account_id, now]).fetchall()
        return [dict(r) for r in rows]

    def get_post_by_id(self, post_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM posts WHERE id = ?", [post_id]).fetchone()
        return dict(row) if row else None

    # ── Comments ──────────────────────────────────────────────────────────────

    def upsert_comments(self, comments: List[Dict[str, Any]]) -> int:
        sql = """
        INSERT INTO comments (account_id, ig_comment_id, ig_media_id, username, text, timestamp)
        VALUES (:account_id, :ig_comment_id, :ig_media_id, :username, :text, :timestamp)
        ON CONFLICT(ig_comment_id) DO UPDATE SET
            text = excluded.text,
            timestamp = excluded.timestamp
        """
        with self._connect() as conn:
            conn.executemany(sql, comments)
            return len(comments)

    def get_comments(
        self,
        ig_media_id: Optional[str] = None,
        account_id: Optional[int] = None,
        unreplied_only: bool = False,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        conditions = []
        params: list = []
        if ig_media_id:
            conditions.append("ig_media_id = ?")
            params.append(ig_media_id)
        if account_id:
            conditions.append("account_id = ?")
            params.append(account_id)
        if unreplied_only:
            conditions.append("replied = 0")
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"SELECT * FROM comments {where} ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    # ── Insights ──────────────────────────────────────────────────────────────

    def insert_insights(self, records: List[Dict[str, Any]]) -> int:
        sql = """
        INSERT INTO insights (account_id, ig_media_id, metric_name, metric_value, period, raw_json)
        VALUES (:account_id, :ig_media_id, :metric_name, :metric_value, :period, :raw_json)
        """
        with self._connect() as conn:
            conn.executemany(sql, records)
            return len(records)

    def insert_user_insights(self, records: List[Dict[str, Any]]) -> int:
        sql = """
        INSERT INTO user_insights (account_id, metric_name, metric_value, period, end_time)
        VALUES (:account_id, :metric_name, :metric_value, :period, :end_time)
        """
        with self._connect() as conn:
            conn.executemany(sql, records)
            return len(records)

    # ── Templates ─────────────────────────────────────────────────────────────

    def upsert_template(self, data: Dict[str, Any]) -> int:
        sql = """
        INSERT INTO templates (name, caption_template, hashtag_set, default_schedule_time)
        VALUES (:name, :caption_template, :hashtag_set, :default_schedule_time)
        ON CONFLICT(name) DO UPDATE SET
            caption_template = excluded.caption_template,
            hashtag_set = excluded.hashtag_set,
            default_schedule_time = excluded.default_schedule_time
        """
        with self._connect() as conn:
            conn.execute(sql, data)
            row = conn.execute("SELECT id FROM templates WHERE name = ?", [data["name"]]).fetchone()
            return row["id"]

    def get_templates(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM templates ORDER BY name").fetchall()
        return [dict(r) for r in rows]

    def get_template_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM templates WHERE name = ?", [name]).fetchone()
        return dict(row) if row else None

    def delete_template(self, name: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM templates WHERE name = ?", [name])
            return cursor.rowcount > 0

    # ── Hashtag Searches ──────────────────────────────────────────────────────

    def insert_hashtag_search(self, data: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO hashtag_searches (account_id, hashtag, ig_hashtag_id)
        VALUES (:account_id, :hashtag, :ig_hashtag_id)
        """
        with self._connect() as conn:
            conn.execute(sql, data)

    def count_hashtag_searches_last_week(self, account_id: int) -> int:
        sql = """
        SELECT COUNT(DISTINCT hashtag) FROM hashtag_searches
        WHERE account_id = ? AND searched_at >= datetime('now', '-7 days')
        """
        with self._connect() as conn:
            return conn.execute(sql, [account_id]).fetchone()[0]

    # ── Action Log ────────────────────────────────────────────────────────────

    def log_action(self, data: Dict[str, Any]) -> None:
        sql = """
        INSERT INTO action_log (account_id, action, params, result, confirmed, rate_remaining)
        VALUES (:account_id, :action, :params, :result, :confirmed, :rate_remaining)
        """
        with self._connect() as conn:
            conn.execute(sql, data)

    def get_recent_actions(self, limit: int = 20, action: Optional[str] = None) -> List[Dict[str, Any]]:
        if action:
            sql = "SELECT * FROM action_log WHERE action = ? ORDER BY created_at DESC LIMIT ?"
            params = [action, limit]
        else:
            sql = "SELECT * FROM action_log ORDER BY created_at DESC LIMIT ?"
            params = [limit]
        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    # ── Stats ─────────────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais do banco."""
        with self._connect() as conn:
            accounts = conn.execute("SELECT COUNT(*) FROM accounts WHERE is_active = 1").fetchone()[0]
            posts_total = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
            posts_published = conn.execute("SELECT COUNT(*) FROM posts WHERE status = 'published'").fetchone()[0]
            posts_draft = conn.execute("SELECT COUNT(*) FROM posts WHERE status = 'draft'").fetchone()[0]
            posts_scheduled = conn.execute("SELECT COUNT(*) FROM posts WHERE status = 'scheduled'").fetchone()[0]
            comments_total = conn.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
            comments_unreplied = conn.execute("SELECT COUNT(*) FROM comments WHERE replied = 0").fetchone()[0]
            templates = conn.execute("SELECT COUNT(*) FROM templates").fetchone()[0]
            actions_today = conn.execute(
                "SELECT COUNT(*) FROM action_log WHERE created_at >= date('now')"
            ).fetchone()[0]

        return {
            "accounts_active": accounts,
            "posts": {
                "total": posts_total,
                "published": posts_published,
                "draft": posts_draft,
                "scheduled": posts_scheduled,
            },
            "comments": {
                "total": comments_total,
                "unreplied": comments_unreplied,
            },
            "templates": templates,
            "actions_today": actions_today,
        }

    def count_requests_last_hour(self) -> int:
        """Conta requests na última hora (para rate limiting)."""
        sql = """
        SELECT COUNT(*) FROM action_log
        WHERE created_at >= datetime('now', '-1 hour')
        """
        with self._connect() as conn:
            return conn.execute(sql).fetchone()[0]

    def count_publishes_today(self) -> int:
        """Conta publicações hoje (para rate limiting)."""
        sql = """
        SELECT COUNT(*) FROM action_log
        WHERE action LIKE 'publish_%' AND created_at >= date('now')
        """
        with self._connect() as conn:
            return conn.execute(sql).fetchone()[0]


# ── CLI rápido para verificação ──────────────────────────────────────────────
if __name__ == "__main__":
    db = Database()
    db.init()
    stats = db.get_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

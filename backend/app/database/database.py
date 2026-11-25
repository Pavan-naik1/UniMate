import sqlite3
import json
from datetime import datetime
from backend.app.core.config import settings

def get_db_connection():
    conn = sqlite3.connect(str(settings.DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        original_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        page_count INTEGER NOT NULL,
        chunk_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'processed',
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Chat conversations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Chat messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL,
        sender TEXT NOT NULL,
        content TEXT NOT NULL,
        sources TEXT, -- JSON array of citation objects
        model_used TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
    )
    """)
    
    # Quizzes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        subject TEXT NOT NULL,
        document_id TEXT,
        difficulty TEXT NOT NULL,
        total_questions INTEGER NOT NULL,
        score INTEGER DEFAULT 0,
        questions_json TEXT NOT NULL,
        user_answers_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    )
    """)
    
    # Study plans table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_plans (
        id TEXT PRIMARY KEY,
        subject TEXT NOT NULL,
        exam_date TEXT NOT NULL,
        daily_hours REAL NOT NULL,
        difficulty TEXT NOT NULL,
        topics_json TEXT NOT NULL,
        schedule_json TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Study topics completion tracking table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_topics (
        id TEXT PRIMARY KEY,
        plan_id TEXT NOT NULL,
        topic_name TEXT NOT NULL,
        day INTEGER NOT NULL,
        completed INTEGER DEFAULT 0,
        completed_at TIMESTAMP,
        FOREIGN KEY (plan_id) REFERENCES study_plans(id) ON DELETE CASCADE
    )
    """)
    
    # User activity log for analytics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL,
        description TEXT NOT NULL,
        metadata_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

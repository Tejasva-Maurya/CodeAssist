import sqlite3
import json
from typing import List, Dict, Any, Optional
from .graph_base import GraphStorage

class SQLiteStorage(GraphStorage):
    def __init__(self, db_path: str = "code_graph.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                label TEXT NOT NULL,
                properties TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS edges (
                source_id TEXT,
                target_id TEXT,
                relationship_type TEXT,
                properties TEXT,
                FOREIGN KEY(source_id) REFERENCES nodes(id),
                FOREIGN KEY(target_id) REFERENCES nodes(id),
                UNIQUE(source_id, target_id, relationship_type)
            )
        """)
        # Indexes for fast lookup
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id)")
        self.conn.commit()

    def add_node(self, node_id: str, label: str, properties: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO nodes (id, label, properties) VALUES (?, ?, ?)",
            (node_id, label, json.dumps(properties))
        )

    def add_edge(self, source_id: str, target_id: str, relationship_type: str, properties: Dict[str, Any] = None):
        if properties is None:
            properties = {}
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO edges (source_id, target_id, relationship_type, properties) VALUES (?, ?, ?, ?)",
            (source_id, target_id, relationship_type, json.dumps(properties))
        )

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, label, properties FROM nodes WHERE id = ?", (node_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "label": row["label"],
                "properties": json.loads(row["properties"])
            }
        return None

    def get_edges(self, node_id: str, direction: str = "both") -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        edges = []
        
        if direction in ("out", "both"):
            cursor.execute("SELECT source_id, target_id, relationship_type, properties FROM edges WHERE source_id = ?", (node_id,))
            for row in cursor.fetchall():
                edges.append({
                    "source_id": row["source_id"],
                    "target_id": row["target_id"],
                    "relationship_type": row["relationship_type"],
                    "properties": json.loads(row["properties"])
                })
                
        if direction in ("in", "both"):
            cursor.execute("SELECT source_id, target_id, relationship_type, properties FROM edges WHERE target_id = ?", (node_id,))
            for row in cursor.fetchall():
                edges.append({
                    "source_id": row["source_id"],
                    "target_id": row["target_id"],
                    "relationship_type": row["relationship_type"],
                    "properties": json.loads(row["properties"])
                })
                
        return edges

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

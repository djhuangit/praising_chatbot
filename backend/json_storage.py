import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import asyncio
from pathlib import Path

class JSONStorage:
    """Simple JSON-based storage for chat history and cost tracking"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.chat_history_file = self.data_dir / "chat_history.json"
        self.token_usage_file = self.data_dir / "token_usage.json"

        # Initialize files if they don't exist
        self._init_storage()

    def _init_storage(self):
        """Initialize JSON files if they don't exist"""
        if not self.chat_history_file.exists():
            self._write_json(self.chat_history_file, {})

        if not self.token_usage_file.exists():
            self._write_json(self.token_usage_file, {
                "total_cost": 0.0,
                "total_tokens": 0
            })

    def _read_json(self, file_path: Path) -> dict:
        """Read JSON file with error handling"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_json(self, file_path: Path, data: dict):
        """Write JSON file with pretty formatting"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    # Chat History Methods
    async def get_chat_history(self, session_id: str) -> List[Dict]:
        """Get chat history for a specific session"""
        data = self._read_json(self.chat_history_file)
        session_data = data.get(session_id, [])
        return session_data

    async def add_message(self, session_id: str, role: str, content: str):
        """Add a message to the chat history"""
        data = self._read_json(self.chat_history_file)

        if session_id not in data:
            data[session_id] = []

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }

        data[session_id].append(message)
        self._write_json(self.chat_history_file, data)

    # Cost Tracking Methods
    async def get_cost_tracking(self) -> Dict[str, float]:
        """Get current cost tracking data"""
        data = self._read_json(self.token_usage_file)
        return {
            "total_cost": data.get("total_cost", 0.0),
            "total_tokens": data.get("total_tokens", 0)
        }

    async def update_cost_tracking(self, total_cost: float, total_tokens: int):
        """Update cost tracking data"""
        data = {
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "last_updated": datetime.utcnow().isoformat()
        }
        self._write_json(self.token_usage_file, data)

# Global storage instance
storage = JSONStorage()

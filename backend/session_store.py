from collections import defaultdict
from threading import Lock
from typing import Dict, List

from models import ChatMessage


class SessionStore:
    def __init__(self, max_history_messages: int = 8):
        self._store: Dict[str, List[ChatMessage]] = defaultdict(list)
        self._lock = Lock()
        self.max_history_messages = max_history_messages

    def get_history(self, session_id: str) -> List[ChatMessage]:
        with self._lock:
            return list(self._store.get(session_id, []))

    def append_turn(self, session_id: str, user_message: str, assistant_message: str) -> None:
        with self._lock:
            history = self._store[session_id]
            history.append(ChatMessage(role="user", text=user_message))
            history.append(ChatMessage(role="assistant", text=assistant_message))
            self._store[session_id] = history[-self.max_history_messages :]

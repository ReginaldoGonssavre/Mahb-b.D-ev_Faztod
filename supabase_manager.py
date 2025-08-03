import os
from typing import Dict, Any, List, Optional

class SupabaseManager:
    def __init__(self):
        print("SupabaseManager initialized in mock mode (in-memory database).")
        self.mock_tasks_db: Dict[str, Dict[str, Any]] = {}
        self.mock_agents_db: Dict[str, Dict[str, Any]] = {}
        self.mock_memory_db: List[Dict[str, Any]] = []
        self.mock_conversations_db: Dict[str, Dict[str, Any]] = {}

    # --- Agent Definitions (e.g., 'agents' table) ---
    def get_agent_definition(self, agent_id: str) -> Dict[str, Any] | None:
        return self.mock_agents_db.get(agent_id)

    def create_agent_definition(self, agent_data: Dict[str, Any]) -> Dict[str, Any] | None:
        agent_id = agent_data.get("id")
        if agent_id:
            self.mock_agents_db[agent_id] = agent_data
            return agent_data
        return None

    def update_agent_definition(self, agent_id: str, updates: Dict[str, Any]) -> Dict[str, Any] | None:
        if agent_id in self.mock_agents_db:
            self.mock_agents_db[agent_id].update(updates)
            return self.mock_agents_db[agent_id]
        return None

    # --- Agent Memory (e.g., 'agent_memory' table) ---
    def get_agent_memory(self, agent_id: str, user_id: str) -> List[Dict[str, Any]]:
        return [entry for entry in self.mock_memory_db if entry.get("agent_id") == agent_id and entry.get("user_id") == user_id]

    def add_to_agent_memory(self, memory_data: Dict[str, Any]) -> Dict[str, Any] | None:
        self.mock_memory_db.append(memory_data)
        return memory_data

    # --- Conversation State (e.g., 'conversations' table) ---
    def get_conversation_state(self, conversation_id: str) -> Dict[str, Any] | None:
        return self.mock_conversations_db.get(conversation_id)

    def update_conversation_state(self, conversation_id: str, updates: Dict[str, Any]) -> Dict[str, Any] | None:
        if conversation_id in self.mock_conversations_db:
            self.mock_conversations_db[conversation_id].update(updates)
            return self.mock_conversations_db[conversation_id]
        return None

    def create_conversation_state(self, conversation_data: Dict[str, Any]) -> Dict[str, Any] | None:
        conversation_id = conversation_data.get("id")
        if conversation_id:
            self.mock_conversations_db[conversation_id] = conversation_data
            return conversation_data
        return None

    # --- Task Management (e.g., 'tasks' table) ---
    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any] | None:
        task_id = task_data.get("task_id")
        if task_id:
            self.mock_tasks_db[task_id] = task_data
            return task_data
        return None

    def get_task(self, task_id: str) -> Dict[str, Any] | None:
        return self.mock_tasks_db.get(task_id)

    def update_task(self, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any] | None:
        if task_id in self.mock_tasks_db:
            self.mock_tasks_db[task_id].update(updates)
            return self.mock_tasks_db[task_id]
        return None

    def get_pending_tasks_for_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        pending_tasks = []
        for task_id, task_data in self.mock_tasks_db.items():
            if task_data.get("assigned_to") == agent_id and task_data.get("status") == "pending":
                pending_tasks.append(task_data)
        return pending_tasks

    def get_unassigned_pending_tasks(self) -> List[Dict[str, Any]]:
        unassigned_tasks = []
        for task_id, task_data in self.mock_tasks_db.items():
            if task_data.get("assigned_to") is None and task_data.get("status") == "pending":
                unassigned_tasks.append(task_data)
        return unassigned_tasks
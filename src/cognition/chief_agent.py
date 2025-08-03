from refactored_agent import IntelligentAgent
from supabase_manager import SupabaseManager
from src.cognition.agent_tools import AVAILABLE_TOOLS
from input_data import InputData
from typing import Dict, Any, Optional, List
import uuid

class Task:
    def __init__(self, task_id: str, description: str, assigned_to: Optional[str] = None, status: str = "pending", tool_name: Optional[str] = None, tool_parameters: Optional[Dict[str, Any]] = None):
        self.task_id = task_id
        self.description = description
        self.assigned_to = assigned_to
        self.status = status
        self.tool_name = tool_name
        self.tool_parameters = tool_parameters

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "tool_name": self.tool_name,
            "tool_parameters": self.tool_parameters
        }

class ChiefAgent(IntelligentAgent):
    def __init__(self, agent_id: str, supabase_manager: Optional[SupabaseManager] = None):
        super().__init__(agent_id, supabase_manager, tools=AVAILABLE_TOOLS) # ChiefAgent also has access to all tools
        self.task_queue: List[Task] = []
        print(f"ChiefAgent '{agent_id}' initialized. Ready to orchestrate.")

    def perceive(self, environment: InputData):
        # ChiefAgent perceives high-level goals or new tasks
        print(f"ChiefAgent perceived: {environment.text}")
        # In a real scenario, this would parse the environment to create new tasks
        # For now, we'll manually add tasks to the queue for demonstration
        pass

    def act(self, intention: str, rag_context: str = "") -> str:
        # ChiefAgent's act method focuses on task orchestration
        print(f"ChiefAgent acting with intention: {intention}")
        if intention == "orchestrate_tasks":
            return self._orchestrate_tasks()
        return f"ChiefAgent: Unrecognized intention: {intention}"

    def _orchestrate_tasks(self) -> str:
        if not self.task_queue and not self.supabase_manager:
            return "ChiefAgent: No tasks in queue to orchestrate."

        task_data = None
        if self.supabase_manager:
            # In a real scenario, ChiefAgent would query for tasks it needs to orchestrate
            # For this PoC, we'll assume it's orchestrating a task it just added or found.
            # We'll simulate popping from a queue for simplicity here, but real logic would be more complex.
            # For now, we'll just update the status of a task that was previously added.
            # This part needs more sophisticated logic for a true distributed system.
            print("ChiefAgent: Simulating orchestration of a task from Supabase.")
            unassigned_tasks = self.supabase_manager.get_unassigned_pending_tasks()
            if unassigned_tasks:
                task_data = unassigned_tasks[0] # Pega a primeira tarefa não atribuída
                task = Task(**task_data)
            else:
                return "ChiefAgent: No unassigned pending tasks found in Supabase."
        else:
            if not self.task_queue:
                return "ChiefAgent: No tasks in in-memory queue to orchestrate."
            task = self.task_queue.pop(0)
            task_data = task.to_dict()

        print(f"ChiefAgent: Orchestrating task '{task_data["task_id"]}': {task_data["description"]}")

        # In a real system, the ChiefAgent would decide which worker agent to assign to
        # For this PoC, we'll simulate assigning it to a generic worker (e.g., MyAgent)
        task_data["assigned_to"] = "worker_agent_1" # Placeholder
        task_data["status"] = "assigned"

        if self.supabase_manager:
            self.supabase_manager.update_task(task_data["task_id"], {"assigned_to": task_data["assigned_to"], "status": task_data["status"]})
            return f"ChiefAgent: Task '{task_data["task_id"]}' assigned to {task_data["assigned_to"]} in Supabase. Details: {task_data}"
        else:
            return f"ChiefAgent: Task '{task_data["task_id"]}' assigned to {task_data["assigned_to"]}. Details: {task_data}"

    def add_task(self, description: str, tool_name: Optional[str] = None, tool_parameters: Optional[Dict[str, Any]] = None):
        new_task = Task(str(uuid.uuid4()), description, tool_name=tool_name, tool_parameters=tool_parameters)
        if self.supabase_manager:
            self.supabase_manager.create_task(new_task.to_dict())
            print(f"ChiefAgent: Added new task to Supabase: {new_task.description}")
        else:
            self.task_queue.append(new_task)
            print(f"ChiefAgent: Added new task to in-memory queue: {new_task.description}")

    # Placeholder for abstract methods from IntelligentAgent
    def _update_desires(self):
        return "" # Simplified for example

    def _form_intention(self):
        return "" # Simplified for example

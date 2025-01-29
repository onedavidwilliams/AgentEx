from abc import ABC, abstractmethod
import uuid

class BaseTask(ABC):
    def __init__(self, task_type: str, payload: dict, retries: int = 0):
        self.task_id = str(uuid.uuid4())
        self.task_type = task_type
        self.payload = payload
        self.retries = retries
        self.status = "pending"  # pending, in_progress, completed, failed
        self.result = None  # Store success result or error message

    async def mark_in_progress(self):
        """Mark the task as in progress."""
        self.status = "in_progress"
        print(f"Task '{self.task_type}' with ID: {self.task_id} is now in progress.")

    async def mark_completed(self, result):
        """Mark the task as completed and store the result."""
        self.status = "completed"
        self.result = result
        print(f"Task '{self.task_type}' with ID: {self.task_id} completed successfully: {result}")

    async def mark_failed(self, error_message):
        """Mark the task as failed and store the error message."""
        self.status = "failed"
        self.result = error_message
        print(f"Task '{self.task_type}' with ID: {self.task_id} failed: {error_message}")

    @abstractmethod
    async def execute(self):
        """
        This method should be overridden by subclasses to define task-specific logic.
        """
        pass


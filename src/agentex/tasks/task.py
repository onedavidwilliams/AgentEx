import uuid

class Task:
    def __init__(self, task_type: str, payload: dict):
        """
        Initialize a Task object.
        :param task_type: The type of task (e.g., 'data_processing', 'analysis').
        :param payload: The data needed to complete the task.
        """
        self.task_id = str(uuid.uuid4())  # Unique ID for tracking
        self.task_type = task_type
        self.payload = payload
        self.status = "pending"  # Status: pending, in_progress, completed

    def mark_in_progress(self):
        """Mark the task as in progress."""
        self.status = "in_progress"

    def mark_completed(self):
        """Mark the task as completed."""
        self.status = "completed"

    def __repr__(self):
        return f"<Task {self.task_id} - {self.task_type} - {self.status}>"
    
    def register_task_type(self, task_type: str, task_class):
        """
        Register a custom task type.
        :param task_type: The name of the task type.
        :param task_class: The class implementing the task logic.
        """
        if task_type in self.task_registry:
            raise ValueError(f"Task type '{task_type}' is already registered.")
        self.task_registry[task_type] = task_class
        print(f"Task type '{task_type}' registered successfully.")

    async def add_task(self, task_type: str, payload: dict, retries: int = 0):
        """
        Create a task instance dynamically and add it to the appropriate queue.
        """
        task_class = self.task_registry.get(task_type)
        if task_class is None:
            raise ValueError(f"Unknown task type: {task_type}. Please register it first.")

        task = task_class(task_type, payload, retries)
        await self.task_queues[task_type].put(task)
        print(f"Task '{task_type}' added to queue with payload: {payload}")
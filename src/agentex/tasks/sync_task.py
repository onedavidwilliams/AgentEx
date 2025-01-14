from abc import ABC, abstractmethod
from exlog import ExLog

class AgentTask(ABC):
    def __init__(self, task_name, description, logger=None):
        self.task_name = task_name
        self.description = description
        self.result = None
        self.logger = logger or ExLog(log_level=1)

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def run_task(self, *args, **kwargs):
        try:
            self.execute(*args, **kwargs)
        except Exception as e:
            self.logger.dprint(f"[ERROR] Task '{self.task_name}' failed: {str(e)}", level="error")
        else:
            self.logger.dprint(f"[SYNC] Task '{self.task_name}' completed successfully.", level="info")

    def get_result(self):
        self.logger.dprint(f"[SYNC] Result of task '{self.task_name}': {self.result}", level="debug")
        return self.result

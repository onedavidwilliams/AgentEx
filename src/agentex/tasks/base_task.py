from abc import ABC, abstractmethod
from exlog import ExLog
from ..logging.logger import LoggerWrapper

class BaseTask(ABC):
    """
    Base class for shared attributes and logging.
    """
    def __init__(self, task_name, description, logger=None, silent=False):
        """
        :param task_name: Name of the task.
        :param description: Description of the task.
        :param logger: Logger instance (ExLog or standard logger).
        :param silent: Whether to suppress logging only within this task's `.log` method.
        """
        self.task_name = task_name
        self.description = description
        self.logger = logger or LoggerWrapper(log_level=1)
        self.result = None
        self.silent = silent  # Add silent mode specific to the `BaseTask.log()`

    def log(self, message, level="info"):
        """
        Log a message if `silent` is False.
        """
        if self.silent:  # Check if this specific task should suppress logs
            return  # Do nothing if silent mode is enabled

        if self.logger:
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(f"---{self.task_name}: {message}")

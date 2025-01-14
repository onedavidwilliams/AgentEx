from .base_task import BaseTask
from abc import ABC, abstractmethod

class AsyncAgentTask(BaseTask):
    
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass

    async def run_task(self, *args, **kwargs):
        """
        Runs the asynchronous task and waits for the result.
        """
        try:
            self.result = await self.execute(*args, **kwargs)
            self.log("Async task completed successfully.", level="info")
        except Exception as e:
            self.log(f"Async task failed: {str(e)}", level="error")
            raise

    def get_result(self):
        """
        Retrieve the result for async tasks.
        """
        self.log(f"Result: {self.result}", level="debug")
        return self.result

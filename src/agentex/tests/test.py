import aiohttp  # For data fetching
import os
import asyncio
from agentex import Swarm, CentralHub, Agent, AsyncAgentTask
from agentex.logging.logger import LoggerWrapper

# --------- Task Implementations --------- #

# 1. Asynchronous I/O Simulation Task (with file printing)
class IOTask(AsyncAgentTask):
    async def execute(self, file_name="sample.txt"):
        """Simulates an async I/O-bound task (file reading) and prints contents."""
        self.logger.dprint(f"[ASYNC I/O TASK] Reading file: {file_name}", level="info")  # ExLog's dprint

        # Check if file exists
        if not os.path.exists(file_name):
            self.logger.dprint(f"[ERROR] File '{file_name}' not found.", level="error")
            self.result = f"File '{file_name}' not found."
            return self.result

        await asyncio.sleep(1.5)  # Simulate I/O delay

        # Read file content
        with open(file_name, "r") as f:
            contents = f.read()

        self.result = contents
        self.logger.dprint(f"[ASYNC I/O TASK] File contents: {contents}", level="debug")
        print(f"[FILE CONTENTS]: {contents}")
        self.log(f"Finished reading file '{file_name}'.", level="info")
        return self.result


# 2. Asynchronous Data Fetch Task (fetches data from a URL)
class DataFetchTask(AsyncAgentTask):
    def __init__(self, task_name, description, url, logger=None):
        super().__init__(task_name, description, logger)
        self.url = url  # Store the URL

    async def execute(self):
        """Fetches data asynchronously from a URL."""
        if not self.url:
            self.logger.dprint(f"[DATA FETCH TASK] No URL provided!", level="error")
            self.result = "No URL provided!"
            return self.result

        self.logger.dprint(f"[DATA FETCH TASK] Fetching data from {self.url}...", level="info")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status == 200:
                        self.result = await response.text()
                        self.logger.dprint(f"[DATA FETCH TASK] Success! Data fetched from {self.url}.", level="debug")
                        #print(f"[FETCHED DATA]: {self.result[:200]}...")
                        self.log(f"Data fetch successful for {self.url}.", level="info")
                        return self.result
                    else:
                        self.result = f"Failed to fetch data (status code: {response.status})"
                        self.logger.dprint(f"[ERROR] Failed to fetch data from {self.url}", level="error")
                        return self.result
        except Exception as e:
            self.result = f"Error fetching data: {str(e)}"
            self.logger.dprint(f"[ERROR] Exception during data fetch: {str(e)}", level="error")
            return self.result


# --------- Test Functions --------- #

# 1. Test async I/O task (file reading)
async def test_async_io_task():
    logger = LoggerWrapper(log_level="info", use_exlog=True)
    silent_logger = LoggerWrapper(log_level=0, use_exlog=True)  # Silent mode for `log`

    central_hub = CentralHub(logger=logger)  # Create CentralHub instance
    swarm = Swarm(name="TestSwarm_IO", central_hub=central_hub, logger=logger)
    agent = Agent("Agent_IO", logger=logger)
    agent.set_swarm(swarm)

    # Task with silent logger (no BaseTask.log output)
    task = IOTask("async_io_task", "Asynchronous file reading task", logger=silent_logger)
    await agent.async_assign_task(task)
    logger.dprint


# 2. Test async data fetch task
async def test_data_fetch_task():
    logger = LoggerWrapper(log_level="debug", use_exlog=True)
    silent_logger = LoggerWrapper(log_level=0, use_exlog=True)

    central_hub = CentralHub(logger=logger)
    swarm = Swarm(name="TestSwarm_DataFetch", central_hub=central_hub, logger=logger)
    agent = Agent("Agent_DataFetch", logger=logger)
    agent.set_swarm(swarm)

    # Pass URL during creation
    test_url = "https://jsonplaceholder.typicode.com/posts/1"
    task = DataFetchTask("data_fetch_task", "Asynchronous data fetching task", url=test_url, logger=silent_logger)

    await agent.async_assign_task(task)
    result = task.get_result()
    if result:
        print(f"[TEST RESULT] Data Fetch Task result: {result[:200]}...")
    else:
        print("[ERROR] No result was fetched from the URL!")


# --------- Main Test Execution --------- #
def run_tests():
    print("[RUNNING ASYNC I/O TASK TEST (FILE READING)]")
    asyncio.run(test_async_io_task())

    print("\n[RUNNING DATA FETCH TASK TEST (API FETCH)]")
    asyncio.run(test_data_fetch_task())


if __name__ == "__main__":
    run_tests()

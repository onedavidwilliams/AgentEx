from exlog import ExLog  # Import ExLog as a mandatory dependency
import logging  # For fallback if user prefers standard logging

class LoggerWrapper:
    """
    A unified logging class that allows the user to choose between ExLog and standard logging.
    Provides an optional `silent` parameter to suppress specific log levels for convenience.
    """

    def __init__(self, log_level=1, use_exlog=True):
        """
        Initialize the logger with the specified log level and logging backend.
        :param log_level: The logging level (0 for silent, 1 for standard output, etc.).
                          Can be an int or a string ("info", "debug", etc.).
        :param use_exlog: Whether to use ExLog (True) or standard logging (False).
        """
        self.log_level = self._convert_log_level(log_level)
        self.use_exlog = use_exlog  # User choice only, no availability check

        if self.use_exlog:
            if self.log_level == 0:
                self.logger = ExLog(log_level=0)  # Silent mode
                self.logger.log_level = 0
            else:
                self.logger = ExLog(log_level=self.log_level)
        else:
            self.logger = self._setup_standard_logger(self.log_level)

        # Expose logging methods directly on the LoggerWrapper instance for convenience
        for method_name in ["info", "debug", "warning", "error", "critical"]:
            setattr(self, method_name, getattr(self.logger, method_name))

    def _convert_log_level(self, log_level):
        """
        Converts a string or integer log level to a numerical format.
        """
        if isinstance(log_level, str):
            log_level = log_level.lower()
            level_map = {
                "notset": 0,
                "info": 1,
                "debug": 2,
                "warning": 3,
                "error": 4,
                "critical": 5
            }
            return level_map.get(log_level, 1)  # Default to INFO if unrecognized
        return log_level

    def _setup_standard_logger(self, log_level):
        """
        Set up a Python standard logger.
        """
        logger = logging.getLogger("AgentExLogger")
        if log_level == 0:
            logger.disabled = True  # Disable all logging output
        else:
            logger.setLevel(self._map_log_level(log_level))
            if not logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
                handler.setFormatter(formatter)
                logger.addHandler(handler)
        return logger

    def _map_log_level(self, log_level):
        """
        Map ExLog-style log levels to standard Python logging levels.
        :param log_level: Custom log level.
        :return: Corresponding Python logging level.
        """
        return {
            0: logging.NOTSET,  # No output (silent)
            1: logging.INFO,  # Standard output
            2: logging.DEBUG,  # Detailed debug output
            3: logging.WARNING,  # Warnings only
            4: logging.ERROR,  # Errors only
            5: logging.CRITICAL  # Critical errors only
        }.get(log_level, logging.INFO)

    def dprint(self, message, level="info", silent=False):
        """
        Unified debug print method that works across ExLog and standard logging.
        :param message: The message to be logged.
        :param level: The logging level as a string ("info", "debug", "error", etc.).
        :param silent: If True, suppresses logging for this specific call.
        """
        if self.log_level == 0 or silent:
            return  # No output if log level is 0 (silent) or if silent=True

        level_method_map = {
            "info": self.logger.info,
            "debug": self.logger.debug,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "critical": self.logger.critical
        }

        log_method = level_method_map.get(level.lower(), self.logger.info)
        log_method(message)

    def set_log_level(self, log_level):
        """
        Update the logging level dynamically.
        :param log_level: The new logging level.
        """
        self.log_level = self._convert_log_level(log_level)
        if self.use_exlog:
            self.logger.log_level = self.log_level
        else:
            if self.log_level == 0:
                self.logger.disabled = True
            else:
                self.logger.disabled = False
                self.logger.setLevel(self._map_log_level(self.log_level))

# Usage Example: Using LoggerWrapper like standard logging without needing to do logger.logger.method()
logger = LoggerWrapper(log_level="info", use_exlog=False)  # Uses standard logging
logger.info("This is an info message (standard logging).")
logger.debug("This debug message shows standard logging usage.")
logger.warning("This is a warning (standard logging).")
logger.set_log_level("error")  # Change to error-level logging
logger.error("This is an error message.")
logger.critical("This is a critical error message.")

# Logging with ExLog-like interface
log = LoggerWrapper(log_level="debug", use_exlog=True)
log.dprint("This is a debug message with ExLog.", level="debug")

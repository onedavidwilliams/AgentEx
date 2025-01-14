from exlog import ExLog  # Import ExLog as a mandatory dependency
import logging  # For fallback if user prefers standard logging

class LoggerWrapper:
    """
    A unified logging class that allows the user to choose between ExLog and standard logging.
    """

    def __init__(self, log_level=1, use_exlog=True):
        """
        Initialize the logger with the specified log level and logging backend.
        """
        self.log_level = self._convert_log_level(log_level)
        self.use_exlog = use_exlog

        if self.use_exlog:
            self.logger = ExLog(log_level=self.log_level)
        else:
            self.logger = self._setup_standard_logger(self.log_level)

    def _convert_log_level(self, log_level):
        """
        Converts a string or integer log level to a numerical format.
        """
        if isinstance(log_level, str):
            level_map = {
                "notset": 0,
                "info": 1,
                "debug": 2,
                "warning": 3,
                "error": 4,
                "critical": 5
            }
            return level_map.get(log_level.lower(), 1)  # Default to INFO if unrecognized
        return log_level

    def _setup_standard_logger(self, log_level):
        """
        Set up a standard Python logger.
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
        """
        return {
            0: logging.NOTSET,
            1: logging.INFO,
            2: logging.DEBUG,
            3: logging.WARNING,
            4: logging.ERROR,
            5: logging.CRITICAL
        }.get(log_level, logging.INFO)

    def dprint(self, message, **kwargs):
        """
        Pass-through for ExLog's dprint. If using standard logging, defaults to info().
        """
        if self.use_exlog:
            # Direct pass-through to ExLog's dprint
            self.logger.dprint(message, **kwargs)
        else:
            # Default to 'info' level if not provided
            level = kwargs.get("level", "info").lower()
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(message)

    def log(self, message, level="info", **kwargs):
        """
        Unified logging method for ExLog and standard logging.
        """
        if self.log_level == 0:
            return  # Silent mode, do not log anything

        if self.use_exlog:
            # Call ExLog's dprint with all arguments
            self.logger.dprint(message, level=level, **kwargs)
        else:
            # Standard logging: dynamically call the method (e.g., .info(), .debug())
            log_method = getattr(self.logger, level.lower(), self.logger.info)
            log_method(message)

    def info(self, message, **kwargs):
        """Standard logging: info-level log or ExLog equivalent."""
        self.log(message, level="info", **kwargs)

    def debug(self, message, **kwargs):
        """Standard logging: debug-level log or ExLog equivalent."""
        self.log(message, level="debug", **kwargs)

    def warning(self, message, **kwargs):
        """Standard logging: warning-level log or ExLog equivalent."""
        self.log(message, level="warning", **kwargs)

    def error(self, message, **kwargs):
        """Standard logging: error-level log or ExLog equivalent."""
        self.log(message, level="error", **kwargs)

    def critical(self, message, **kwargs):
        """Standard logging: critical-level log or ExLog equivalent."""
        self.log(message, level="critical", **kwargs)

    def set_log_level(self, log_level):
        """
        Update the logging level dynamically.
        """
        self.log_level = self._convert_log_level(log_level)
        if self.use_exlog:
            self.logger.log_level = self.log_level
        else:
            self.logger.disabled = (self.log_level == 0)
            if self.log_level != 0:
                self.logger.setLevel(self._map_log_level(self.log_level))



# Usage Example: Using LoggerWrapper like standard logging without needing to do logger.logger.method()
# logger = LoggerWrapper(log_level="info", use_exlog=False)  # Uses standard logging
# logger.info("This is an info message (standard logging).")
# logger.debug("This debug message shows standard logging usage.")
# logger.warning("This is a warning (standard logging).")
# logger.set_log_level("error")  # Change to error-level logging
# logger.error("This is an error message.")
# logger.critical("This is a critical error message.")

# # Logging with ExLog-like interface
# log = LoggerWrapper(log_level="debug", use_exlog=True)
# log.dprint("This is a debug message with ExLog.", level="critical")

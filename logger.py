import os
import time

INFO = 0
WARNING = 1
ERROR = 2
FATAL = 3

_levelToName = {INFO: "Info: ", WARNING: "Warning: ", ERROR: "Error: ", FATAL: "Fatal: "}


class Logger:

    _DEFAULT_PATH = "log.txt"
    _s_logger_instance = None

    def __init__(self, log_file_path):
        self._log_file_path = log_file_path
        if log_file_path in os.listdir("."):  # os.path is unavailable
            os.remove(log_file_path)

    def log_msg(self, level, msg):
        """
        Logs the msg to file and serial
        :param level: Can be LOG_INFO / LOG_WARNING / LOG_ERROR / LOG_FATAL
        :param msg: Log txt
        """
        level_str = _levelToName.get(level, "Unknown")
        time_str = "{}:{}:{} - ".format(*Logger.get_up_time())
        # Also print to serial
        print(time_str, level_str, msg)
        with open(self._log_file_path, "a") as f:
            f.write(time_str)
            f.write(level_str)
            f.write(msg)

    @staticmethod
    def get_up_time():
        up_time_secs = time.time()
        up_time_hours = up_time_secs // 3600
        up_time_mins = (up_time_secs - up_time_hours*3600) // 60
        return up_time_hours, up_time_mins, up_time_secs

    @staticmethod
    def get_logger():
        if not Logger._s_logger_instance:
            Logger._s_logger_instance = Logger(Logger._DEFAULT_PATH)
        return Logger._s_logger_instance


def get_logger():
    return Logger.get_logger()
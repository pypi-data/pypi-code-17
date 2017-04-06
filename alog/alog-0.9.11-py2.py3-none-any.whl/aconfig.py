import sys
in_python2_runtime = sys.version_info[0] == 2


def default_alog_config():
    return {
        "custom_format": None,
        "showing_thread_name": False,
        "showing_process_id": False,
        "default_format":
            "%(asctime)s %(levelname)-5.5s %(pathname)s%(lineno)s%(message)s",
        "default_thread_format": (
            "%(asctime)s %(levelname)-5.5s %(threadName)s "
            "%(pathname)s%(lineno)s%(message)s"),
        "default_process_format": (
            "%(asctime)s %(levelname)-5.5s PID:%(process)d "
            "%(pathname)s%(lineno)s%(message)s"),
        "default_process_thread_format": (
            "%(asctime)s %(levelname)-5.5s PID:%(process)d:"
            "%(threadName)s %(pathname)s%(lineno)s%(message)s"
        )
    }

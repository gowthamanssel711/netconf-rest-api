import logging

def init_loggers(server_log,error_log):

    logger = logging.getLogger("request_log")
    logger.setLevel(logging.DEBUG)
    handle = logging.FileHandler(server_log)
    log_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    handle.setFormatter(log_format)
    logger.addHandler(handle)

    err_log = logging.getLogger("error_logger")
    err_handle = logging.FileHandler(error_log)
    log_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    err_handle.setFormatter(log_format)
    err_log.addHandler(err_handle)
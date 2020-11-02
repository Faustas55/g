import logging

def set_logging(name, level,logfile):
    # set logging up
    logger = logging.getLogger(name)
    logger.setLevel(level)
    filelog = logging.FileHandler(logfile)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    filelog.setFormatter(formatter)
    logger.addHandler(filelog)
    return logger
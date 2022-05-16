import logging


# simple log
logger_name = 'app'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# location w.r.t. working directory that calls this Flask app
hdler = logging.FileHandler(f'{logger_name}.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hdler.setFormatter(formatter)
logger.addHandler(hdler)
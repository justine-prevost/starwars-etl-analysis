import logging
import logging.config

def setup_logging(config):
        logging.config.dictConfig(config["logging"]) # I created key 'logging' in yaml because it waited for everything not only the loggers
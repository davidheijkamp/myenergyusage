import configparser
from utils import log

configfilename = 'config.ini'


def get(setting, section='default'):
    config = configparser.RawConfigParser()
    try:
        config.read(configfilename)
    except Exception as e:
        log.logger.critical('Reading from ' + configfilename)
        log.logger.debug(str(e))
        raise Exception
    try:
        cfg_data = config.get(section, setting)
        return cfg_data
    except Exception as e:
        log.logger.critical('Getting setting ' + setting + ' from ' + configfilename)
        log.logger.debug(str(e))
        raise Exception

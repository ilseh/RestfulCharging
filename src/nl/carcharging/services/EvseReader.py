
import logging
import os
import sys

from nl.carcharging.services.EvseReaderProd import EvseReaderProd, EvseState
from nl.carcharging.utils.GenericUtil import GenericUtil
try:
    from mfrc522 import SimpleMFRC522
except RuntimeError:
    logging.debug('Assuming dev env')

LOGGER_PATH = "nl.carcharging.service.EvseReader"


class EvseReaderDev(object):
    def __init__(self):
        self.logger = logging.getLogger(LOGGER_PATH + 'Dev')

    def loop(self, cb_until, cb_result):
        while not cb_until():
            self.logger.debug('Fake run Evse Read loop')
            cb_result(EvseState.EVSE_STATE_UNKNOWN)


class EvseReader(object):

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_PATH)
        if GenericUtil.isProd():
            self.logger.debug("Using production Evse reader")
            self.reader = EvseReaderProd()
        else:
            self.logger.debug("Using fake Evse reader")
            self.reader = EvseReaderDev()

    def loop(self, cb_until, cb_result):
        try:
            self.reader.loop(cb_until, cb_result)
        except Exception as ex:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.error('Could not start EvseReader loop: %s', ex)
            self.logger.error(exc_type, fname, exc_tb.tb_lineno)
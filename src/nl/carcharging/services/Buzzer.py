import threading
import time
import logging

from nl.carcharging.config.WebAppConfig import WebAppConfig
from nl.carcharging.utils.GenericUtil import GenericUtil

GPIO = GenericUtil.importGpio()


class BuzzerDev(object):

    def __init__(self):
        self.logger = logging.getLogger('nl.carcharging.services.BuzzerDev')

    def buzz(self, buzz_duration_s, iterations=1):
        for i in range(iterations):
            self.logger.debug("Fake buzzzzzzzz!!!!!!!")
            time.sleep(buzz_duration_s)

    def buzz_other_thread(self, buzz_duration_s, iterations=1):
        self.logger.debug("Starting buzzer in fake other thread")

    def cleanup(self):
        self.logger.debug("Fake cleanup")


class BuzzerProd(object):
    logger = logging.getLogger('nl.carcharging.services.BuzzerProd')

    def buzz(self, buzz_duration_s, iterations=1):
        global WebAppConfig

        self.logger.debug("Buzzing. Iteration %d, duration %.2f" % (iterations, buzz_duration_s))

        GPIO.setup(WebAppConfig.pinBuzzer, GPIO.OUT, initial=GPIO.LOW)

        for i in range(iterations):
            GPIO.output(WebAppConfig.pinBuzzer, GPIO.HIGH)  # Turn on
            time.sleep(buzz_duration_s)
            GPIO.output(WebAppConfig.pinBuzzer, GPIO.LOW)  # Turn off
            time.sleep(.05)

    def cleanup(self):
        global WebAppConfig

        GPIO.output(WebAppConfig.pinBuzzer, GPIO.LOW)  # Turn off
        self.logger.debug("GPIO cleanup done for %s" % self.color_desc())


    def buzz_other_thread(self, buzz_duration_s, iterations=1):
        self.logger.debug("Starting buzzer in other thread")
        thread_for_pulse = threading.Thread(target=self.buzz, name="BuzzerThread", args=(buzz_duration_s, iterations))
        thread_for_pulse.start()


class Buzzer(object):

    def __init__(self):
        self.logger = logging.getLogger('nl.carcharging.services.Buzzer')

        if GenericUtil.isProd():
            self.buzzer = BuzzerProd()
        else:
            self.buzzer = BuzzerDev()

    def buzz(self, buzz_duration_s, iterations=1):
        self.buzzer.buzz(buzz_duration_s, iterations)

    def buzz_other_thread(self, buzz_duration_s, iterations=1):
        self.buzzer.buzz_other_thread(buzz_duration_s, iterations)

    def cleanup(self):
        self.buzzer.cleanup()

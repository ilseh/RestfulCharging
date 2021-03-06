# https://raspberrytips.nl/kaarslicht-pwm-raspberry-pi/

import logging

from .LedLightDev import LedLightDev

from nl.oppleo.utils.GenericUtil import GenericUtil
from .LedLightPulseProd import LedLightPulseProd

try:
    from .LedLightProd import LedLightProd
except NameError:
    print('Assuming dev env')


class LedLight(object):

    def __init__(self, *colors, intensity, pulse=False, services=None):
        self.logger = logging.getLogger('nl.oppleo.services.LedLight')
        if services is None:
            services = []
        self.services = services

        for color in colors:
            if GenericUtil.isProd():
                self.services.append(LedLightPulseProd(color, intensity=intensity) if pulse else LedLightProd(color, intensity=intensity))
            else:
                self.services.append(LedLightDev(color, intensity=intensity))

        self.logger.debug('Initialize with %d ledlights %s' % (len(self.services), "to pulse" if pulse else "no pulse"))

    def on(self):
        for service in self.services:
            service.on()

    def off(self):
        for service in self.services:
            service.off()

    def cleanup(self):
        for service in self.services:
            service.cleanup()

from artiq.experiment import *
from artiq.coredevice.ad9910 import *
from artiq.coredevice.urukul import CPLD


class SVDemo(EnvExperiment):

    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_cpld")
        self.setattr_device("urukul0_ch0")

        self.dds = self.urukul0_ch0  # type: AD9910
        self.cpld = self.urukul0_cpld  # type: CPLD

    @kernel
    def run(self):
        self.core.break_realtime()

        # Initialize both CPLD and DDS channel
        self.cpld.init()
        self.dds.init()

        # function set sets generation parameters AND pulses IO_UPDATE
        self.dds.set(frequency=1*MHz)
        # setting attenuation does not require IO_UPDATE pulse as it is related
        # to the different chip
        self.dds.set_att(12.0)
        # turn RF switch on
        self.dds.sw.on()

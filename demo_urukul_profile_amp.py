from artiq.experiment import *
from artiq.coredevice.ad9910 import *
from artiq.coredevice.urukul import CPLD
from numpy import sin, pi


class SVDemo(EnvExperiment):

    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_cpld")
        self.setattr_device("urukul0_ch0")

        self.dds = self.urukul0_ch0  # type: AD9910
        self.cpld = self.urukul0_cpld  # type: CPLD

        self.amp = [sin(x/1024*pi/2) for x in range(1024)]
        self.amp_ram = [0]*len(self.amp)

    @kernel
    def run(self):
        self.core.break_realtime()

        self.cpld.init()
        self.dds.init()

        self.dds.amplitude_to_ram(self.amp, self.amp_ram)

        self.dds.set_frequency(10*MHz)
        self.dds.set_att(12.0)
        self.dds.sw.on()
        self.dds.set_cfr1(ram_enable=0)
        self.cpld.io_update.pulse_mu(8)

        self.dds.set_profile_ram(
            start=0, 
            end=len(self.amp_ram) - 1,
            step=1,
            profile=0, 
            mode=RAM_MODE_CONT_BIDIR_RAMP)
        self.cpld.set_profile(0)
        self.cpld.io_update.pulse_mu(8)

        delay(1 * ms)
        self.dds.write_ram(self.amp_ram)

        self.dds.set_cfr1(ram_enable=1, ram_destination=RAM_DEST_ASF)
        self.cpld.io_update.pulse_mu(8)

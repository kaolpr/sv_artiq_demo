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

        self.freq = [(x/1024*10)*MHz for x in range(1024)]
        self.freq_ram = [0]*len(self.freq)

    @kernel
    def run(self):
        self.core.break_realtime()

        self.cpld.init()
        self.dds.init()

        self.dds.frequency_to_ram(self.freq, self.freq_ram)

        self.dds.set_amplitude(1.0)
        self.dds.set_frequency(0*MHz)
        self.dds.set_att(12.0)
        self.dds.set_cfr1(ram_enable=0)
        self.cpld.io_update.pulse_mu(8)

        self.dds.set_profile_ram(
            start=0, 
            end=len(self.freq_ram) - 1,
            step=1,
            profile=0, 
            mode=RAM_MODE_CONT_BIDIR_RAMP)
        self.cpld.set_profile(0)
        self.cpld.io_update.pulse_mu(8)

        delay(1 * ms)
        self.dds.write_ram(self.freq_ram)

        self.dds.set_cfr1(ram_enable=1, ram_destination=RAM_DEST_FTW, osk_enable=1)
        self.dds.sw.on()
        self.cpld.io_update.pulse_mu(8)

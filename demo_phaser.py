from artiq.experiment import *
from artiq.coredevice.phaser import *


class SVDemo(EnvExperiment):

    def build(self):
        self.setattr_device("core")
        self.setattr_device("phaser0")
        self.phaser0 = self.phaser0  # type: Phaser

    @kernel
    def set_phaser_frequencies(self, phaser, duc, osc):
        phaser.channel[0].set_duc_frequency(duc)
        phaser.channel[0].set_duc_cfg()
        phaser.channel[0].set_att(6*dB)
        phaser.channel[1].set_duc_frequency(-duc)
        phaser.channel[1].set_duc_cfg()
        phaser.channel[1].set_att(6*dB)
        phaser.duc_stb()
        delay(1*ms)
        for i in range(len(osc)):
            phaser.channel[0].oscillator[i].set_frequency(osc[i])
            phaser.channel[0].oscillator[i].set_amplitude_phase(.2)
            phaser.channel[1].oscillator[i].set_frequency(-osc[i])
            phaser.channel[1].oscillator[i].set_amplitude_phase(.2)
            delay(1*ms)

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()

        self.phaser0.init()

        self.phaser0.channel[0].set_att(12.0)
        self.phaser0.channel[1].set_att(12.0)

        duc = 10*MHz
        osc = [i*1*MHz for i in range(5)]
        self.set_phaser_frequencies(self.phaser0, duc, osc)

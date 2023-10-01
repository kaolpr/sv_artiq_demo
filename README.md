# SV ARTIQ Demo

This repository uses [direnv](https://direnv.net/). For installation instruction
please refer to direnv [documentation](https://direnv.net/#docs).

## Crates

The system consists of two crates. One is acting as a master (SV001M), the other 
as a satellite (SV002S). Master crate can be used without satellite. Satellite 
must be used with master.

Master crate consists of the following modules:

* Sampler
* Urukul AD9910
* Phaser BB

Satellite create consists of the following modules:

* DIO BNC
* Zotino with BNC adapter

## Examples

Examples in this repository covers basic use of Urukul and Phaser modules and 
is intended to be a starting point for further development. For detalied 
information on the programming interface please refer to:

* [ARTIQ documentation on Urukul](https://m-labs.hk/artiq/manual/core_drivers_reference.html#module-artiq.coredevice.urukul)
* [ARTIQ coredevice for Urukul](https://github.com/m-labs/artiq/blob/master/artiq/coredevice/urukul.py)
* [ARTIQ coredevice for AD9910](https://github.com/m-labs/artiq/blob/master/artiq/coredevice/ad9910.py)
* [ARTIQ documentation on Phaser](https://m-labs.hk/artiq/manual/core_drivers_reference.html#module-artiq.coredevice.phaser)
* [ARTIQ coredevice for Phaser](https://github.com/m-labs/artiq/blob/master/artiq/coredevice/phaser.py)

Examples master crate to be availabe under IP `192.168.1.70` (preprogrammed).
Satellite crate may remain unconnected.

### `demo_phaser.py`

This experiment starts RF generation on Phaser with specified digital 
upconverter frequency and set of oscillators 5 numerically controlled 
oscillators.

### `demo_urukul.py`

This experiment starts RF generation on Urukul with specified frequency and 
output signal level.

### `demo_urukul_profile_amp.py`

This example demonstrates use of AD9910 profile feature for modulating output
signal amplitude.

### `demo_urukul_profile_freq.py`

This example demonstrates use of AD9910 profile feature for modulating output
signal frequency.

## Running examples

1. Clone repository:

```bash
clone https://github.com/kaolpr/sv_artiq_demo.git
```

2. Enter cloned repository and allow direnv profile:

```bash
cd sv_artiq_demo
direnv allow
```

3. Run demo experiment (adjust file name for the experiment of your choice):

```bash
artiq_run ./demo_phaser.py
```

:warning: Master crate must be available to the host PC under `192.168.1.70` 
address. To ensure that you can connect Ethernet cable directly to your PC 
and set network to manual with PC IP `192.168.1.1` and subnet mask 
`255.255.255.0`. 
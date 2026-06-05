from source.laser import CWLaser

from modulators.awg import (
    AWGController
)

from modulators.intensity_modulator import (
    MachZehnderIM
)

from synchronization.optical_delay_line import (
    OpticalDelayLine
)

from synchronization.synchronization import (
    SyncSystem
)

laser = CWLaser()

awg = AWGController()

im = MachZehnderIM()

odl = OpticalDelayLine()

sync = SyncSystem()

waveform = awg.generate_z_basis(
    dimension=8,
    state_index=3
)

duration = (
    len(waveform.time_axis)
    / awg.fs
)

alice = laser.generate_field(
    duration_s=duration,
    sampling_rate_hz=awg.fs
)

alice = im.modulate(
    optical_field=alice,
    drive_voltage=waveform.intensity_voltage,
    sampling_rate_hz=awg.fs
)

bob = alice.copy()

#
# Inject timing mismatch
#

bob = odl.apply_delay(
    bob,
    delay_ps=250
)

aligned_bob, metrics = (
    sync.synchronize(
        alice,
        bob
    )
)

print()
print(metrics)
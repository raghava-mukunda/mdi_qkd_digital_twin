import numpy as np

from source.laser import CWLaser
from modulators.awg import AWGController
from modulators.intensity_modulator import MachZehnderIM

laser = CWLaser()

awg = AWGController()

im = MachZehnderIM()

waveform = awg.generate_z_basis(
    dimension=8,
    state_index=3
)

field = laser.generate_field(
    duration_s=len(
        waveform.time_axis
    ) / awg.fs,
    sampling_rate_hz=awg.fs
)

output = im.modulate(
    optical_field=field,
    drive_voltage=waveform.intensity_voltage,
    sampling_rate_hz=awg.fs
)

metrics = im.evaluate(
    output
)

print("\nIntensity Modulator Test")
print("-" * 40)

print(
    "Average Power:",
    metrics.average_power
)

print(
    "Peak Power:",
    metrics.peak_power
)

print(
    "Extinction Ratio:",
    metrics.extinction_ratio_db,
    "dB"
)

print(
    "Insertion Loss:",
    metrics.insertion_loss_db,
    "dB"
)
"""
test_odl_with_pulses.py

Tests Optical Delay Line using actual
time-bin pulses instead of CW laser.

Chain:

Laser
↓
AWG
↓
Intensity Modulator
↓
ODL
"""

import numpy as np

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


print("\nGenerating pulse train...")

laser = CWLaser()

awg = AWGController()

im = MachZehnderIM()

odl = OpticalDelayLine()


#
# Generate d=8 Z-basis state |t3>
#

waveform = awg.generate_z_basis(
    dimension=8,
    state_index=3
)

duration = (
    len(waveform.time_axis)
    / awg.fs
)

field = laser.generate_field(
    duration_s=duration,
    sampling_rate_hz=awg.fs
)

pulse_train = im.modulate(
    optical_field=field,
    drive_voltage=waveform.intensity_voltage,
    sampling_rate_hz=awg.fs
)

print("Pulse train generated")

#
# Apply known delay
#

TRUE_DELAY_PS = 250

delayed = odl.apply_delay(
    pulse_train,
    delay_ps=TRUE_DELAY_PS
)

#
# Attempt recovery
#

corrected, metrics = odl.auto_align(
    pulse_train,
    delayed
)

print("\nODL Results")
print("-" * 50)

print(
    f"Applied Delay      : {TRUE_DELAY_PS:.2f} ps"
)

print(
    f"Recovered Delay    : {metrics.delay_ps:.2f} ps"
)

print(
    f"Recovered Samples  : "
    f"{metrics.delay_samples:.2f}"
)

print(
    f"Peak Correlation   : "
    f"{metrics.peak_correlation:.4f}"
)

#
# Alignment error
#

error_ps = abs(
    TRUE_DELAY_PS
    -
    metrics.delay_ps
)

print(
    f"Alignment Error    : "
    f"{error_ps:.2f} ps"
)

#
# Power check
#

power_before = np.mean(
    np.abs(
        pulse_train
    ) ** 2
)

power_after = np.mean(
    np.abs(
        corrected
    ) ** 2
)

print(
    f"Power Before Align : "
    f"{power_before:.6e}"
)

print(
    f"Power After Align  : "
    f"{power_after:.6e}"
)

print("\nDone.")
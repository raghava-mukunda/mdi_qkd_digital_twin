from source.laser import CWLaser
from modulators.awg import AWGController
from modulators.phase_modulator import (
    PhaseModulator
)

laser = CWLaser()

awg = AWGController()

pm = PhaseModulator()

waveform = awg.generate_x_basis(
    dimension=8,
    state_index=3
)

field = laser.generate_field(
    duration_s=len(
        waveform.time_axis
    ) / awg.fs,
    sampling_rate_hz=awg.fs
)

output = pm.modulate(
    optical_field=field,
    drive_voltage=waveform.phase_voltage,
    sampling_rate_hz=awg.fs
)

metrics = pm.evaluate(
    waveform.phase_voltage
)

print("\nPhase Modulator Test")
print("-" * 40)

print(
    "RMS Phase:",
    metrics.rms_phase_rad
)

print(
    "Max Phase:",
    metrics.max_phase_rad
)

print(
    "Vpi:",
    metrics.v_pi
)
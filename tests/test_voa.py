from source.laser import CWLaser
from channel.voa import (
    VariableOpticalAttenuator
)

laser = CWLaser()

voa = VariableOpticalAttenuator()

field = laser.generate_field(
    duration_s=1e-6,
    sampling_rate_hz=20e9
)

signal = voa.set_signal_state(
    field
)

decoy = voa.set_decoy_state(
    field
)

vacuum = voa.set_vacuum_state(
    field
)

print()

print(
    "Signal mu:",
    voa.mean_photon_number(
        signal
    )
)

print(
    "Decoy mu:",
    voa.mean_photon_number(
        decoy
    )
)

print(
    "Vacuum mu:",
    voa.mean_photon_number(
        vacuum
    )
)
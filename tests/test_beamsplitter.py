from source.laser import CWLaser

from interference.beam_splitter import (
    BeamSplitter
)

laser = CWLaser()

bs = BeamSplitter()

alice = laser.generate_field(
    duration_s=1e-6,
    sampling_rate_hz=20e9
)

bob = alice.copy()

c, d, metrics = bs.interfere(
    alice,
    bob,
    timing_offset_ps=0,
    phase_offset_rad=0,
    polarization_offset_deg=0
)

print()
print(metrics)
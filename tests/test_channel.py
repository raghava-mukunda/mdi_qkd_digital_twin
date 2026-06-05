from source.laser import CWLaser

from channel.fiber_channel import (
    FiberChannel
)

laser = CWLaser()

field = laser.generate_field(
    duration_s=1e-6,
    sampling_rate_hz=20e9
)

channel = FiberChannel(
    length_km=25
)

output, metrics = (
    channel.propagate(
        field
    )
)

print()
print(metrics)
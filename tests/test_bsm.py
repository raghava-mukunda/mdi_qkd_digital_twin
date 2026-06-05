from detectors.tcspc import (
    TimestampEvent
)

from bsm.bell_state_measurement import (
    BellStateMeasurement
)

bsm = BellStateMeasurement()

e1 = TimestampEvent(

    timestamp_ps=1000,

    channel=1,

    photon_number=0.4
)

e2 = TimestampEvent(

    timestamp_ps=1060,

    channel=4,

    photon_number=0.4
)

result = bsm.analyze_pair(
    e1,
    e2
)

print()
print(result)
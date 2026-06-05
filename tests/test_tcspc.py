from detectors.tcspc import (
    TCSPCModule
)

tcspc = TCSPCModule()

tcspc.add_event(
    100,
    1,
    0.4
)

tcspc.add_event(
    90,
    4,
    0.4
)

tcspc.add_event(
    110,
    2,
    0.4
)

print()

for event in tcspc.get_events():

    print(event)

print()

print(
    "Total Events:",
    tcspc.event_count()
)
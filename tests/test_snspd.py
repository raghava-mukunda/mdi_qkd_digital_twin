from detectors.spad import (
    SNSPDDetector
)

detector = SNSPDDetector(
    channel_id=1
)

print()
print(
    detector.metrics()
)

N = 10000

clicks = 0

for k in range(N):

    event = detector.detect(

        mu=0.4,

        timestamp_ps=k*50000
    )

    if event.detected:

        clicks += 1

print()

print(
    "Measured Click Probability:",
    clicks/N
)

print(
    "Expected Probability:",
    detector.click_probability(
        0.4
    )
)
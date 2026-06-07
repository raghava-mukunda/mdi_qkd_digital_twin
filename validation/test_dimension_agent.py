import time
import joblib

from adaptive.channel_state import (
    ChannelState
)

model = joblib.load(
    "validation/dimension_agent.pkl"
)

sample = [[

    5,
    0.1,
    20,
    2
]]

N = 10000

start = time.perf_counter()

for _ in range(N):

    model.predict(sample)

end = time.perf_counter()

latency = (

    end - start

) / N

print()
print("="*80)
print("AGENT LATENCY")
print("="*80)

print()

print(
    "Average Prediction Time:"
)

print(
    latency * 1e6,
    "microseconds"
)
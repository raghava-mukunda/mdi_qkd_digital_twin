"""
test_laser.py
"""
from source.laser import CWLaser
import numpy as np

laser = CWLaser()

field = laser.generate_field(
    duration_s=1e-6,
    sampling_rate_hz=20e9
)

print("Field shape:", field.shape)

power = np.abs(field)**2

print("Mean power:", np.mean(power))
print("Max power :", np.max(power))

print(laser.metrics())
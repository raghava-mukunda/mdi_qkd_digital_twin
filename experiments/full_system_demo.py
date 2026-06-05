"""
full_system_demo.py

HD-MDI-QKD Full System Demonstration

Generates:

1. Pulse waveform
2. Phase waveform
3. HOM visibility vs dimension
4. Q11 vs dimension
5. SKR vs dimension
6. Adaptive scheduler decisions
7. Throughput comparison

Author:
MDI-QKD Digital Twin
"""

import numpy as np
import matplotlib.pyplot as plt

from config.system_params import (
    SystemParameters
)

from bsm.quantum_state import (
    QuantumStateFactory
)

from interference.beam_splitter import (
    BeamSplitter
)

from statistics.physical_q11 import (
    PhysicalQ11
)

from statistics.x_basis_error import (
    XBasisErrorModel
)

from skr.secret_key_rate import (
    SecretKeyRate
)

from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)


params = SystemParameters()

beam_splitter = BeamSplitter()

q11_model = PhysicalQ11()

xerr = XBasisErrorModel()

skr_model = SecretKeyRate()

scheduler = RealScheduler()

# ============================================================
# 1. Pulse Train
# ============================================================

d = 8

pulse_width = params.pulse_width_ps
bin_spacing = params.time_bin_spacing_ps

time_ps = np.arange(
    0,
    d * bin_spacing,
    1
)

pulse_train = np.zeros_like(
    time_ps,
    dtype=float
)

for i in range(d):

    start = i * bin_spacing

    pulse_train[
        (time_ps >= start)
        &
        (
            time_ps <
            start + pulse_width
        )
    ] = 1.0

plt.figure(figsize=(10,4))
plt.plot(
    time_ps,
    pulse_train
)
plt.title(
    "Time-Bin Pulse Train (d=8)"
)
plt.xlabel(
    "Time (ps)"
)
plt.ylabel(
    "Normalized Power"
)
plt.grid()

# ============================================================
# 2. Phase Pattern
# ============================================================

phase_pattern = np.zeros(d)

phase_pattern[d//2:] = np.pi

plt.figure(figsize=(10,4))
plt.step(
    np.arange(d),
    phase_pattern,
    where="mid"
)

plt.title(
    "X-Basis Phase Encoding"
)

plt.xlabel(
    "Time Bin"
)

plt.ylabel(
    "Phase (rad)"
)

plt.grid()

# ============================================================
# 3. HOM Visibility
# ============================================================

dimensions = [2,4,8,16]

visibilities = []

for d in dimensions:

    a = QuantumStateFactory.create(
        d,
        "X",
        0
    )

    b = QuantumStateFactory.create(
        d,
        "X",
        0
    )

    hom = beam_splitter.interfere(
        a,
        b
    )

    visibilities.append(
        hom.total_visibility
    )

plt.figure(figsize=(8,4))
plt.plot(
    dimensions,
    visibilities,
    marker="o"
)

plt.title(
    "HOM Visibility vs Dimension"
)

plt.xlabel(
    "Dimension"
)

plt.ylabel(
    "Visibility"
)

plt.grid()

# ============================================================
# 4. Q11
# ============================================================

q11_values = []

for d in dimensions:

    q = q11_model.estimate(

        dimension=d,

        loss_db=5,

        phase_offset_rad=0.1,

        timing_offset_ps=20,

        polarization_offset_deg=2,

        trials=3000

    )

    q11_values.append(
        q.q11
    )

plt.figure(figsize=(8,4))
plt.plot(
    dimensions,
    q11_values,
    marker="o"
)

plt.title(
    "Q11 vs Dimension"
)

plt.xlabel(
    "Dimension"
)

plt.ylabel(
    "Q11"
)

plt.grid()

# ============================================================
# 5. SKR
# ============================================================

skr_values = []

for d in dimensions:

    q = q11_model.estimate(

        dimension=d,

        loss_db=5,

        phase_offset_rad=0.1,

        timing_offset_ps=20,

        polarization_offset_deg=2,

        trials=3000
    )

    xerr.params.phase_noise_std_rad = 0.1

    e = xerr.calculate(
        dimension=d,
        visibility=0.95
    )

    s = skr_model.calculate(

        dimension=d,

        q11_z=q.q11,

        ex11=e.error_rate,

        leak_ec=1e-4*q.q11
    )

    skr_values.append(
        s.secret_key_rate
    )

plt.figure(figsize=(8,4))
plt.plot(
    dimensions,
    skr_values,
    marker="o"
)

plt.title(
    "SKR vs Dimension"
)

plt.xlabel(
    "Dimension"
)

plt.ylabel(
    "SKR"
)

plt.grid()

# ============================================================
# 6. Adaptive Timeline
# ============================================================

N = 1000

selected_dimensions = []

adaptive_skr = 0

fixed_skr = {

    2:0,
    4:0,
    8:0,
    16:0
}

rng = np.random.default_rng(
    42
)

for _ in range(N):

    state = ChannelState(

        loss_db=rng.uniform(
            0,
            20
        ),

        phase_noise_rad=rng.uniform(
            0.02,
            0.30
        ),

        timing_jitter_ps=rng.uniform(
            10,
            50
        ),

        polarization_drift_deg=rng.uniform(
            0,
            5
        )
    )

    best, results = (
        scheduler.choose_dimension(
            state
        )
    )

    selected_dimensions.append(
        best
    )

    adaptive_skr += (
        results[best]
    )

    for d in dimensions:

        fixed_skr[d] += (
            results[d]
        )

plt.figure(figsize=(12,4))

plt.plot(
    selected_dimensions
)

plt.title(
    "Adaptive Dimension Selection Timeline"
)

plt.xlabel(
    "Frame Number"
)

plt.ylabel(
    "Selected Dimension"
)

plt.grid()

# ============================================================
# 7. Throughput Comparison
# ============================================================

labels = [

    "d=2",
    "d=4",
    "d=8",
    "d=16",
    "Adaptive"
]

values = [

    fixed_skr[2],
    fixed_skr[4],
    fixed_skr[8],
    fixed_skr[16],
    adaptive_skr
]

plt.figure(figsize=(8,4))

plt.bar(
    labels,
    values
)

plt.title(
    "Total SKR Comparison"
)

plt.ylabel(
    "Accumulated SKR"
)

plt.grid()

# ============================================================
# Summary
# ============================================================

best_fixed = max(
    fixed_skr.values()
)

improvement = (

    adaptive_skr
    -
    best_fixed

) / best_fixed * 100

print()
print("="*80)
print("FULL SYSTEM SUMMARY")
print("="*80)

print()

for d in dimensions:

    print(
        f"Fixed d={d}: "
        f"{fixed_skr[d]:.4f}"
    )

print()

print(
    f"Adaptive : {adaptive_skr:.4f}"
)

print()

print(
    f"Improvement : "
    f"{improvement:.2f}%"
)

plt.show()
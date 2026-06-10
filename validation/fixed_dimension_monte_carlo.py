"""
fixed_dimension_monte_carlo.py

Monte Carlo comparison of fixed HD-MDI-QKD modes.

Compares:

d=2 @ 500 MHz
d=2 @ 250 MHz
d=2 @ 125 MHz

d=4 @ 250 MHz
d=4 @ 125 MHz

d=8 @ 125 MHz

Uses exactly the same physics as the
digital twin.

Author:
MDI-QKD Digital Twin
"""

import numpy as np
import matplotlib.pyplot as plt

from channel.dynamic_fiber_channel import (
    DynamicFiberChannel
)

from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)


# ==========================================================
# Monte Carlo Settings
# ==========================================================

RUNS = 1000

FRAMES = 1000

LENGTH_KM = 100


# ==========================================================
# Fixed Configurations
# ==========================================================

CONFIGS = {

    "d=2 @ 500 MHz": {

        "d": 2,

        "rate_hz": 500e6
    },

    "d=2 @ 250 MHz": {

        "d": 2,

        "rate_hz": 250e6
    },

    "d=2 @ 125 MHz": {

        "d": 2,

        "rate_hz": 125e6
    },

    "d=4 @ 250 MHz": {

        "d": 4,

        "rate_hz": 250e6
    },

    "d=4 @ 125 MHz": {

        "d": 4,

        "rate_hz": 125e6
    },

    "d=8 @ 125 MHz": {

        "d": 8,

        "rate_hz": 125e6
    }
}


# ==========================================================
# Results Container
# ==========================================================

results = {

    name: []

    for name in CONFIGS
}


availability = {

    name: []

    for name in CONFIGS
}


# ==========================================================
# Helper Functions
# ==========================================================

def throughput_kbps(

    skr_per_pulse,

    rate_hz
):

    """
    Convert:

    bits/pulse

    →

    kbps
    """

    return (

        skr_per_pulse

        *np.log2(d)*

        rate_hz

        /

        1000.0
    )


def confidence_interval(

    values
):

    values = np.array(values)

    mean = np.mean(values)

    std = np.std(values)

    ci95 = (

        1.96

        *

        std

        /

        np.sqrt(

            len(values)
        )
    )

    return (

        mean,

        std,

        ci95
    )


print()

print("=" * 80)

print("FIXED DIMENSION MONTE CARLO")

print("=" * 80)

print()

print(

    f"Runs   : {RUNS}"
)

print(

    f"Frames : {FRAMES}"
)

print(

    f"Fiber  : {LENGTH_KM} km"
)

print()

print("Configurations:")

for name in CONFIGS:

    print(

        f"  {name}"
    )

print()
# ==========================================================
# Monte Carlo Engine
# ==========================================================

for run in range(RUNS):

    if (run + 1) % 50 == 0:

        print(
            f"Monte Carlo Run "
            f"{run+1}/{RUNS}"
        )

    #
    # Fresh channel and scheduler
    #

    channel = DynamicFiberChannel(
        length_km=LENGTH_KM
    )

    scheduler = RealScheduler(fast_mode=True)

    #
    # One realization
    #

    total_skr = {

        name: 0.0

        for name in CONFIGS
    }

    available_frames = {

        name: 0

        for name in CONFIGS
    }

    for frame in range(FRAMES):

        #
        # Same channel for ALL configs
        #

        metrics = channel.step()

        phi = metrics.phase_rad

        timing = metrics.timing_ps

        pol = metrics.polarization_deg

        #
        # Evaluate every fixed mode
        #

        for name, config in CONFIGS.items():

            d = config["d"]

            rate = config["rate_hz"]

            state = ChannelState(

                loss_db=LENGTH_KM * 0.2,

                phase_noise_rad=abs(phi),

                timing_jitter_ps=timing,

                polarization_drift_deg=pol

            )

            #
            # Evaluate ONLY this d
            #

            skr_pulse = scheduler.evaluate_dimension(

                d,

                state

            )

            #
            # Convert to kbps
            #

            skr_kbps = throughput_kbps(

                skr_pulse,

                rate

            )

            total_skr[name] += skr_kbps

            #
            # Availability
            #

            if skr_kbps > 0:

                available_frames[name] += 1

    #
    # Mean SKR for this run
    #

    for name in CONFIGS:

        mean_run_skr = (

            total_skr[name]

            /

            FRAMES

        )

        results[name].append(

            mean_run_skr

        )

        availability[name].append(

            available_frames[name]

            /

            FRAMES

        )
# ==========================================================
# Statistics
# ==========================================================

print()
print("=" * 80)
print("FINAL RESULTS")
print("=" * 80)

summary = {}

for name in CONFIGS:

    mean_skr, std_skr, ci_skr = confidence_interval(
        results[name]
    )

    mean_avail = np.mean(
        availability[name]
    )

    summary[name] = {

        "mean": mean_skr,

        "std": std_skr,

        "ci": ci_skr,

        "avail": mean_avail

    }

#
# Sort by throughput
#

sorted_configs = sorted(

    summary.keys(),

    key=lambda x: summary[x]["mean"],

    reverse=True

)

baseline = summary["d=4 @ 250 MHz"]["mean"]

print()

print(
    f"{'Configuration':<20}"
    f"{'Mean (kbps)':>15}"
    f"{'95% CI':>15}"
    f"{'Availability':>15}"
    f"{'Gain':>12}"
)

print("-" * 77)

for name in sorted_configs:

    mean = summary[name]["mean"]

    ci = summary[name]["ci"]

    avail = summary[name]["avail"]

    gain = (

        (mean - baseline)

        /

        baseline

        * 100

    )

    if name == "d=4 @ 250 MHz":

        gain_str = "---"

    else:

        gain_str = f"{gain:.2f}%"

    print(

        f"{name:<20}"

        f"{mean:>15.3f}"

        f"{ci:>15.3f}"

        f"{avail*100:>14.2f}%"

        f"{gain_str:>12}"

    )
    # ==========================================================
# Throughput Plot
# ==========================================================

names = sorted_configs

means = [

    summary[x]["mean"]

    for x in names

]

cis = [

    summary[x]["ci"]

    for x in names

]

plt.figure(figsize=(10, 6))

plt.bar(

    range(len(names)),

    means,

    yerr=cis,

    capsize=5

)

plt.xticks(

    range(len(names)),

    names,

    rotation=30

)

plt.ylabel(
    "Throughput (kbps)"
)

plt.title(
    "Fixed Dimension Monte Carlo"
)

plt.grid(True)

plt.tight_layout()

plt.show()
# ==========================================================
# Availability Plot
# ==========================================================

availabilities = [

    summary[x]["avail"] * 100

    for x in names

]

plt.figure(figsize=(10, 6))

plt.bar(

    range(len(names)),

    availabilities

)

plt.xticks(

    range(len(names)),

    names,

    rotation=30

)

plt.ylabel(
    "Availability (%)"
)

plt.title(
    "Link Availability"
)

plt.ylim(0, 100)

plt.grid(True)

plt.tight_layout()

plt.show()
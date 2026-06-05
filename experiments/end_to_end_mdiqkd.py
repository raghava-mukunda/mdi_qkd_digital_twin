"""
end_to_end_mdiqkd.py

Full HD-MDI-QKD Experiment
"""

import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler

from bsm.quantum_state import QuantumStateFactory
from bsm.charlie_receiver import CharlieReceiver

from skr.secret_key_rate import SecretKeyRate


N_FRAMES = 1000

scheduler = RealScheduler()
charlie = CharlieReceiver()
skr_model = SecretKeyRate()

rng = np.random.default_rng(42)

adaptive_key = 0.0
fixed8_key = 0.0

adaptive_history = []
fixed_history = []

dimension_history = []

bsm_success_history = []
sifted_history = []
qber_history = []

correct_events = 0
error_events = 0

for frame in range(N_FRAMES):

    state = ChannelState(
        loss_db=rng.uniform(0, 20),
        phase_noise_rad=rng.uniform(0.02, 0.30),
        timing_jitter_ps=rng.uniform(10, 50),
        polarization_drift_deg=rng.uniform(0, 5)
    )

    selected_d, predicted = scheduler.choose_dimension(
        state
    )

    dimension_history.append(
        selected_d
    )

    #
    # Alice
    #

    alice_basis = rng.choice(
        ["Z", "X"]
    )

    if alice_basis == "Z":

        alice_symbol = rng.integers(
            selected_d
        )

    else:

        alice_symbol = rng.integers(
            2
        )

    #
    # Bob
    #

    bob_basis = rng.choice(
        ["Z", "X"]
    )

    if bob_basis == "Z":

        bob_symbol = rng.integers(
            selected_d
        )

    else:

        bob_symbol = rng.integers(
            2
        )

    alice_state = QuantumStateFactory.create(
        selected_d,
        alice_basis,
        int(alice_symbol)
    )

    bob_state = QuantumStateFactory.create(
        selected_d,
        bob_basis,
        int(bob_symbol)
    )

    result = charlie.process_trial(
        alice_state,
        bob_state,
        timing_offset_ps=state.timing_jitter_ps,
        phase_offset_rad=state.phase_noise_rad,
        polarization_offset_deg=state.polarization_drift_deg
    )

    bsm_success_history.append(
        int(result.psi_minus)
    )

    #
    # Sifting
    #

    if (
        result.psi_minus
        and
        alice_basis == bob_basis
    ):

        sifted_history.append(1)

        #
        # Error generation
        #

        if rng.random() < (
            state.phase_noise_rad
            /
            np.pi
        ):

            error_events += 1

        else:

            correct_events += 1

        total = (
            correct_events
            +
            error_events
        )

        qber = (
            error_events
            /
            total
            if total > 0
            else 0.0
        )

        qber_history.append(
            qber
        )

        #
        # Adaptive dimension SKR
        #

        adaptive_skr = (
            skr_model.calculate(
                dimension=selected_d,
                q11_z=1.0,
                ex11=qber,
                leak_ec=1e-4
            ).secret_key_rate
        )

        adaptive_key += max(
            0.0,
            adaptive_skr
        )

        #
        # Fixed d=8 SKR
        #

        fixed_skr = (
            skr_model.calculate(
                dimension=8,
                q11_z=1.0,
                ex11=qber,
                leak_ec=1e-4
            ).secret_key_rate
        )

        fixed8_key += max(
            0.0,
            fixed_skr
        )

    else:

        sifted_history.append(
            0
        )

        if len(qber_history):

            qber_history.append(
                qber_history[-1]
            )

        else:

            qber_history.append(
                0.0
            )

    adaptive_history.append(
        adaptive_key
    )

    fixed_history.append(
        fixed8_key
    )

#
# Results
#

print()
print("=" * 80)
print("END TO END HD-MDI-QKD")
print("=" * 80)

print()
print("Frames:", N_FRAMES)
print("BSM Success:", sum(bsm_success_history))
print("Sifted Events:", sum(sifted_history))
print("Final QBER:", qber_history[-1])

print()
print("Adaptive Key:", adaptive_key)
print("Fixed d=8:", fixed8_key)

if fixed8_key > 0:

    print(
        "Improvement (%):",
        (
            adaptive_key
            -
            fixed8_key
        )
        /
        fixed8_key
        *
        100
    )

#
# Figure 1
#

plt.figure(figsize=(12,4))
plt.plot(dimension_history)
plt.title(
    "Adaptive Dimension Selection"
)
plt.xlabel("Frame")
plt.ylabel("Dimension")
plt.grid()

#
# Figure 2
#

plt.figure(figsize=(12,4))
plt.plot(
    np.cumsum(
        bsm_success_history
    )
)
plt.title(
    "Accumulated BSM Events"
)
plt.xlabel("Frame")
plt.ylabel("BSM Events")
plt.grid()

#
# Figure 3
#

plt.figure(figsize=(12,4))
plt.plot(
    np.cumsum(
        sifted_history
    )
)
plt.title(
    "Sifted Key Growth"
)
plt.xlabel("Frame")
plt.ylabel("Sifted Events")
plt.grid()

#
# Figure 4
#

plt.figure(figsize=(12,4))
plt.plot(
    qber_history
)
plt.title(
    "Running QBER"
)
plt.xlabel("Frame")
plt.ylabel("QBER")
plt.grid()

#
# Figure 5
#

plt.figure(figsize=(12,4))

plt.plot(
    adaptive_history,
    label="Adaptive"
)

plt.plot(
    fixed_history,
    label="Fixed d=8"
)

plt.title(
    "Accumulated Secret Key"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "Secret Key"
)

plt.legend()
plt.grid()

plt.show()
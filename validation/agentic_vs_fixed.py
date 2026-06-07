import joblib
import numpy as np
import matplotlib.pyplot as plt

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler


print()
print("=" * 80)
print("LOADING MODEL")
print("=" * 80)

model = joblib.load(
    "validation/dimension_agent.pkl"
)

scheduler = RealScheduler()

TOTAL_SYMBOLS = 10000

BLOCK_SIZE = 500

N_BLOCKS = TOTAL_SYMBOLS // BLOCK_SIZE

#
# FPGA timing assumptions
#

FPGA_DECISION_TIME_S = 100e-9

RECONFIG_TIME_S = 1e-6

SYMBOL_TIME_S = 8e-9

fixed_bits = {
    2: 0.0,
    4: 0.0,
    8: 0.0,
    16: 0.0
}

fixed_time = {
    2: 0.0,
    4: 0.0,
    8: 0.0,
    16: 0.0
}

oracle_bits = 0.0
oracle_time = 0.0

tree_bits = 0.0
tree_time = 0.0

previous_tree_d = None

print()
print("=" * 80)
print("RUNNING CHANNEL EVOLUTION")
print("=" * 80)

for block in range(N_BLOCKS):

    #
    # same scenario used in your successful demo
    #

    if block < 7:

        loss = 2.0
        phase = 0.03

    elif block < 14:

        loss = 8.0
        phase = 0.08

    else:

        loss = 18.0
        phase = 0.25

    state = ChannelState(

        loss_db=loss,

        phase_noise_rad=phase,

        timing_jitter_ps=20.0,

        polarization_drift_deg=2.0
    )

    best_d, scores = scheduler.choose_dimension(
        state
    )

    #
    # Fixed dimensions
    #

    for d in [2,4,8,16]:

        secret_bits = (

            scores[d]

            *

            BLOCK_SIZE

            *

            np.log2(d)
        )

        fixed_bits[d] += secret_bits

        fixed_time[d] += (

            BLOCK_SIZE

            *

            SYMBOL_TIME_S
        )

    #
    # Oracle
    #

    oracle_bits += (

        scores[best_d]

        *

        BLOCK_SIZE

        *

        np.log2(best_d)
    )

    oracle_time += (

        BLOCK_SIZE

        *

        SYMBOL_TIME_S
    )

    #
    # Decision Tree
    #

    features = [[

        state.loss_db,

        state.phase_noise_rad,

        state.timing_jitter_ps,

        state.polarization_drift_deg

    ]]

    tree_d = int(

        model.predict(
            features
        )[0]
    )

    tree_bits += (

        scores[tree_d]

        *

        BLOCK_SIZE

        *

        np.log2(tree_d)
    )

    tree_time += (

        BLOCK_SIZE

        *

        SYMBOL_TIME_S
    )

    #
    # FPGA decision overhead
    #

    tree_time += FPGA_DECISION_TIME_S

    #
    # reconfiguration overhead
    #

    if (

        previous_tree_d is not None

        and

        previous_tree_d != tree_d

    ):

        tree_time += RECONFIG_TIME_S

    previous_tree_d = tree_d

    print(

        f"Block {block+1:02d}/{N_BLOCKS}"

        f" | Oracle={best_d}"

        f" | Tree={tree_d}"
    )

#
# Effective SKR
#

results = {

    "d=2":

        fixed_bits[2] / fixed_time[2],

    "d=4":

        fixed_bits[4] / fixed_time[4],

    "d=8":

        fixed_bits[8] / fixed_time[8],

    "d=16":

        fixed_bits[16] / fixed_time[16],

    "Oracle":

        oracle_bits / oracle_time,

    "Tree FPGA":

        tree_bits / tree_time
}

print()
print("=" * 80)
print("RESULTS")
print("=" * 80)

for k,v in results.items():

    print(
        f"{k:<12} {v:.3e}"
    )

plt.figure(
    figsize=(10,6)
)

plt.bar(

    list(results.keys()),

    list(results.values())

)

plt.ylabel(
    "Effective SKR (bits/s)"
)

plt.title(
    "Agentic vs Fixed-D HD-MDI-QKD"
)

plt.grid(
    axis="y"
)

plt.tight_layout()

plt.show()
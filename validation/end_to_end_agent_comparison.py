import time
import joblib
import numpy as np
import pandas as pd

from adaptive.channel_state import ChannelState
from adaptive.real_scheduler import RealScheduler

# ============================================================
# CONFIG
# ============================================================

TOTAL_SYMBOLS = 10000

BLOCK_SIZE = 500

N_BLOCKS = TOTAL_SYMBOLS // BLOCK_SIZE

TREE_OVERHEAD = 290e-6      # measured CPU latency

FPGA_OVERHEAD = 100e-9      # projected FPGA latency

BIN_WIDTH = 1e-9            # 1 ns

# ============================================================
# LOAD MODEL
# ============================================================

print()
print("="*80)
print("LOADING DECISION TREE")
print("="*80)

model = joblib.load(
    "validation/dimension_agent.pkl"
)

scheduler = RealScheduler()

rng = np.random.default_rng(42)

# ============================================================
# INITIAL CHANNEL
# ============================================================

loss = 10.0

phase = 0.15

timing = 20.0

pol = 2.0

# ============================================================
# STORAGE
# ============================================================

fixed_results = {}

for d in [2,4,8,16]:

    fixed_results[d] = {

        "secret_bits":0.0,

        "time":0.0

    }

oracle_secret = 0.0
oracle_time = 0.0

tree_secret = 0.0
tree_time = 0.0

fpga_secret = 0.0
fpga_time = 0.0

# ============================================================
# SIMULATION
# ============================================================

print()
print("="*80)
print("RUNNING 10000 SYMBOL TRANSMISSION")
print("="*80)

for block in range(N_BLOCKS):

    # --------------------------------------------------------
    # Channel drift
    # --------------------------------------------------------

    # =====================================================
    # Controlled Channel Evolution
    # =====================================================

    if block < 7:

        loss = 2.0

        phase = 0.03

    elif block < 14:

        loss = 8.0

        phase = 0.08

    else:

        loss = 18.0

        phase = 0.25

    timing = 20.0

    pol = 2.0

    loss = np.clip(loss,0,20)

    phase = np.clip(phase,0.02,0.30)

    timing = np.clip(timing,10,50)

    pol = np.clip(pol,0,5)

    state = ChannelState(

        loss_db=float(loss),

        phase_noise_rad=float(phase),

        timing_jitter_ps=float(timing),

        polarization_drift_deg=float(pol)

    )

    # --------------------------------------------------------
    # Full physics scheduler
    # --------------------------------------------------------

    best_d, scores = scheduler.choose_dimension(
        state
    )

    # --------------------------------------------------------
    # Fixed dimensions
    # --------------------------------------------------------

    for d in [2,4,8,16]:

        skr = scores[d]

        secret = (

            skr

            * np.log2(d)

            * BLOCK_SIZE

        )

        tx_time = (

            BLOCK_SIZE

            * d

            * BIN_WIDTH

        )

        fixed_results[d]["secret_bits"] += secret

        fixed_results[d]["time"] += tx_time

    # --------------------------------------------------------
    # Oracle
    # --------------------------------------------------------

    oracle_secret += (

        scores[best_d]

        * np.log2(best_d)

        * BLOCK_SIZE

    )

    oracle_time += (

        BLOCK_SIZE

        * best_d

        * BIN_WIDTH

    )

    # --------------------------------------------------------
    # Decision Tree
    # --------------------------------------------------------

    sample = pd.DataFrame({

        "loss_db":[loss],

        "phase_noise_rad":[phase],

        "timing_jitter_ps":[timing],

        "polarization_drift_deg":[pol]

    })

    pred_d = int(

        model.predict(sample)[0]

    )

    tree_secret += (

        scores[pred_d]

        * np.log2(pred_d)

        * BLOCK_SIZE

    )

    tree_time += (

        BLOCK_SIZE

        * pred_d

        * BIN_WIDTH

        + TREE_OVERHEAD

    )

    fpga_secret += (

        scores[pred_d]

        * np.log2(pred_d)

        * BLOCK_SIZE

    )

    fpga_time += (

        BLOCK_SIZE

        * pred_d

        * BIN_WIDTH

        + FPGA_OVERHEAD

    )

    print(

        f"Block {block+1}/{N_BLOCKS}"

        f" | Loss={loss:.2f}"

        f" | Phase={phase:.3f}"

        f" | Oracle d={best_d}"

        f" | Tree d={pred_d}"

    )

# ============================================================
# RESULTS
# ============================================================

print()
print("="*80)
print("END-TO-END COMPARISON")
print("="*80)

print()

print(
    f"{'Mode':<20}"
    f"{'Secret Bits':>15}"
    f"{'Time(ms)':>15}"
    f"{'Eff SKR':>20}"
)

print("-"*70)

for d in [2,4,8,16]:

    secret = fixed_results[d]["secret_bits"]

    t = fixed_results[d]["time"]

    eff = secret / t

    print(

        f"{f'Fixed d={d}':<20}"

        f"{secret:>15.2f}"

        f"{t*1000:>15.6f}"

        f"{eff:>20.2f}"

    )

print()

oracle_eff = oracle_secret / oracle_time

print(

    f"{'Oracle':<20}"

    f"{oracle_secret:>15.2f}"

    f"{oracle_time*1000:>15.6f}"

    f"{oracle_eff:>20.2f}"

)

tree_eff = tree_secret / tree_time

print(

    f"{'Tree CPU':<20}"

    f"{tree_secret:>15.2f}"

    f"{tree_time*1000:>15.6f}"

    f"{tree_eff:>20.2f}"

)

fpga_eff = fpga_secret / fpga_time

print(

    f"{'Tree FPGA':<20}"

    f"{fpga_secret:>15.2f}"

    f"{fpga_time*1000:>15.6f}"

    f"{fpga_eff:>20.2f}"

)

print()
print("="*80)

print(

    "Tree vs Oracle Secret Bit Gap:",

    100 *

    (

        oracle_secret

        - tree_secret

    )

    /

    oracle_secret,

    "%"

)

best_fixed = max(

    fixed_results.values(),

    key=lambda x:x["secret_bits"]

)

adaptive_gain = (

    tree_secret

    - best_fixed["secret_bits"]

) / best_fixed["secret_bits"] * 100

print()

print(

    "Adaptive Gain over Best Fixed:",

    adaptive_gain,

    "%"

)

print("="*80)
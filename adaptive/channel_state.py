from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class ChannelState:

    loss_db: float

    phase_noise_rad: float

    timing_jitter_ps: float

    polarization_drift_deg: float

    residual_phase_rad: Optional[float] = None
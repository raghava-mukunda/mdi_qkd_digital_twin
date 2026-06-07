"""
beam_splitter.py

Dimension-Aware HOM Interference

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np

from config.system_params import (
    SystemParameters
)

from bsm.quantum_state import (
    QuantumState
)


@dataclass(slots=True)
class HOMMetrics:

    state_overlap: float

    timing_visibility: float

    phase_visibility: float

    polarization_visibility: float

    coherence_visibility: float

    total_visibility: float

    coincidence_probability: float


class BeamSplitter:

    def __init__(
        self,
        params: Optional[
            SystemParameters
        ] = None
    ):

        self.params = (
            params
            if params is not None
            else SystemParameters()
        )

        self.coherence_time_ps = (
            self.params.coherence_time_ps
        )

        self.bin_width_ps = (
            self.params.time_bin_spacing_ps
        )

        self.linewidth_hz = (
            self.params.laser_linewidth_hz
        )

    def timing_visibility(
        self,
        delay_ps: float
    ):

        sigma = 250.0

        return float(

            np.exp(

                -(delay_ps**2)

                /

                (2*sigma**2)

            )

        )

    def phase_visibility(
        self,
        phase_offset_rad: float
    ):

        return float(

            np.cos(
                phase_offset_rad/2
            )**2
        )

    def polarization_visibility(
        self,
        pol_offset_deg: float
    ):

        theta = np.deg2rad(
            pol_offset_deg
        )

        return float(
            np.cos(theta)**2
        )

    def coherence_visibility(
        self,
        dimension: int
    ):

        frame_duration_ps = (

            (dimension - 1)

            *

            self.bin_width_ps

        )

        #
        # Effective coherence window
        # representing accumulated phase
        # instability across long frames.
        #

        effective_coherence_ps = 30000.0

        return float(

            np.exp(

                -frame_duration_ps

                /

                effective_coherence_ps

            )

        )

    def interfere(

        self,

        alice_state: QuantumState,

        bob_state: QuantumState,

        timing_offset_ps: float = 0,

        phase_offset_rad: float = 0,

        polarization_offset_deg: float = 0

    ):

        overlap = (
            alice_state.overlap(
                bob_state
            )
        )

        vt = (
            self.timing_visibility(
                timing_offset_ps
            )
        )

        vp = (
            self.phase_visibility(
                phase_offset_rad
            )
        )

        vpol = (
            self.polarization_visibility(
                polarization_offset_deg
            )
        )

        vcoh = (
            self.coherence_visibility(
                alice_state.dimension
            )
        )

        visibility = (

            overlap

            *

            vt

            *

            vp

            *

            vpol

            *

            vcoh
        )

        visibility = np.clip(
            visibility,
            0.0,
            1.0
        )

        coincidence = (

            0.5

            *

            (
                1
                -
                visibility
            )
        )

        return HOMMetrics(

            state_overlap=float(
                overlap
            ),

            timing_visibility=float(
                vt
            ),

            phase_visibility=float(
                vp
            ),

            polarization_visibility=float(
                vpol
            ),

            coherence_visibility=float(
                vcoh
            ),

            total_visibility=float(
                visibility
            ),

            coincidence_probability=float(
                coincidence
            )
        )
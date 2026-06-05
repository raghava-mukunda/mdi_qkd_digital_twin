"""
full_system.py

Unified HD-MDI-QKD Simulator

Author:
MDI-QKD Digital Twin
"""

from collections import Counter

import numpy as np

from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)

from mdiqkd_system.results import (
    SimulationResult
)


class FullMDIQKDSystem:

    def __init__(self):

        self.scheduler = RealScheduler()

        self.rng = np.random.default_rng(
            42
        )

    def random_channel_state(self):

        return ChannelState(

            loss_db=self.rng.uniform(
                0,
                20
            ),

            phase_noise_rad=self.rng.uniform(
                0.02,
                0.30
            ),

            timing_jitter_ps=self.rng.uniform(
                10,
                50
            ),

            polarization_drift_deg=self.rng.uniform(
                0,
                5
            )
        )

    def run_adaptive(

        self,

        frames=1000

    ):

        total_skr = 0.0

        dimensions = []

        skr_history = []

        channels = []

        for _ in range(frames):

            state = (
                self.random_channel_state()
            )

            best, scores = (

                self.scheduler
                .choose_dimension(
                    state
                )
            )

            total_skr += (
                scores[best]
            )

            dimensions.append(
                best
            )

            channels.append(
                state
            )

            skr_history.append(
                total_skr
            )

        usage = dict(
            Counter(dimensions)
        )

        return SimulationResult(

            frames=frames,

            total_skr=total_skr,

            dimension_usage=usage,

            selected_dimensions=dimensions,

            skr_history=skr_history,

            channel_history=channels
        )

    def run_fixed(

        self,

        dimension,

        frames=1000

    ):

        total_skr = 0.0

        dimensions = []

        skr_history = []

        channels = []

        for _ in range(frames):

            state = (
                self.random_channel_state()
            )

            _, scores = (

                self.scheduler
                .choose_dimension(
                    state
                )
            )

            total_skr += (
                scores[dimension]
            )

            dimensions.append(
                dimension
            )

            channels.append(
                state
            )

            skr_history.append(
                total_skr
            )

        usage = {
            dimension: frames
        }

        return SimulationResult(

            frames=frames,

            total_skr=total_skr,

            dimension_usage=usage,

            selected_dimensions=dimensions,

            skr_history=skr_history,

            channel_history=channels
        )

    def compare(

        self,

        frames=1000

    ):

        adaptive = self.run_adaptive(
            frames
        )

        fixed2 = self.run_fixed(
            2,
            frames
        )

        fixed4 = self.run_fixed(
            4,
            frames
        )

        fixed8 = self.run_fixed(
            8,
            frames
        )

        fixed16 = self.run_fixed(
            16,
            frames
        )

        return {

            "adaptive": adaptive,

            "fixed2": fixed2,

            "fixed4": fixed4,

            "fixed8": fixed8,

            "fixed16": fixed16
        }
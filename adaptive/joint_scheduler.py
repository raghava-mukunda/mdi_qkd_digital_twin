from adaptive.real_scheduler import RealScheduler
from adaptive.mode_library import MODES
import numpy as np

class JointScheduler:

    def __init__(self):

        self.scheduler = RealScheduler()

    def choose_mode(

        self,

        state

    ):

        results = {}

        for mode in MODES:

            #
            # SKR per symbol
            #
            skr_symbol = (

                self.scheduler.evaluate_dimension(

                    mode.dimension,

                    state

                )

            )

            #
            # Secure throughput
            #
            dead_ns = (

                self.scheduler
                .q11_model
                .params
                .detector_dead_time_ns
            )

            symbol_spacing_ns = (

                1e9
                /
                mode.frequency_hz
            )

            recovery = (

                1

                -

                np.exp(

                    -symbol_spacing_ns
                    /
                    dead_ns

                )

            )

            throughput = (

                skr_symbol

                *

                mode.frequency_hz

                *

                recovery

            )

            

            results[mode] = throughput

        best = max(

            results,

            key=results.get

        )

        return best, results
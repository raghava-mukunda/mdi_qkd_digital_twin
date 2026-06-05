"""
fpga_buffer.py

Adaptive FPGA Buffer

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

from adaptive.channel_state import (
    ChannelState
)

from adaptive.real_scheduler import (
    RealScheduler
)


@dataclass(slots=True)
class BufferMetrics:

    transmitted_frames: int

    dropped_frames: int

    total_skr: float

    average_delay: float


class FPGABuffer:

    def __init__(

        self,

        max_size=50

    ):

        self.scheduler = (
            RealScheduler()
        )

        self.max_size = max_size

        self.queue = []

        self.total_skr = 0.0

        self.total_delay = 0.0

        self.transmitted = 0

        self.dropped = 0

    def enqueue(

        self,

        state: ChannelState,

        timestamp: int

    ):

        if len(self.queue) >= self.max_size:

            self.dropped += 1

            return

        self.queue.append(

            (state, timestamp)

        )

    def transmit_best(

        self,

        current_time

    ):

        if not self.queue:

            return

        #
        # choose frame with
        # highest predicted SKR
        #

        best_index = None

        best_skr = -1

        best_delay = 0

        for i, (

            state,

            arrival

        ) in enumerate(

            self.queue

        ):

            d, results = (

                self.scheduler
                .choose_dimension(
                    state
                )
            )

            skr = results[d]

            if skr > best_skr:

                best_skr = skr

                best_index = i

                best_delay = (

                    current_time
                    -
                    arrival
                )

        self.total_skr += (
            best_skr
        )

        self.total_delay += (
            best_delay
        )

        self.transmitted += 1

        self.queue.pop(
            best_index
        )

    def metrics(self):

        avg_delay = 0

        if self.transmitted > 0:

            avg_delay = (

                self.total_delay

                /

                self.transmitted
            )

        return BufferMetrics(

            transmitted_frames=
            self.transmitted,

            dropped_frames=
            self.dropped,

            total_skr=
            self.total_skr,

            average_delay=
            avg_delay
        )
"""
awg.py

Arbitrary Waveform Generator

Generates electrical drive signals for:

1. Intensity Modulator
2. Phase Modulator

Encoding follows the IISc
high-dimensional time-bin
MDI-QKD implementation.

Reference:

Figure 1:
f0 = [0 0 0 0]
f1 = [0 0 pi pi]

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

import numpy as np

from config.system_params import (
    SystemParameters
)


@dataclass(slots=True)
class AWGWaveform:

    time_axis: np.ndarray

    intensity_voltage: np.ndarray

    phase_voltage: np.ndarray


class AWGController:

    """
    Generates AWG waveforms
    used by Alice and Bob.
    """

    def __init__(
        self,
        params: SystemParameters | None = None
    ):

        self.params = (
            params
            if params is not None
            else SystemParameters()
        )

        self.fs = (
            self.params.awg_sampling_rate_hz
        )

        self.pulse_width_ps = (
            self.params.pulse_width_ps
        )

        self.bin_spacing_ps = (
            self.params.time_bin_spacing_ps
        )

    def _samples_per_bin(self):

        dt = 1 / self.fs

        return int(
            (
                self.bin_spacing_ps
                * 1e-12
            )
            / dt
        )

    def _pulse_samples(self):

        dt = 1 / self.fs

        return int(
            (
                self.pulse_width_ps
                * 1e-12
            )
            / dt
        )

    def generate_z_basis(
        self,
        dimension: int,
        state_index: int
    ) -> AWGWaveform:

        samples_per_bin = (
            self._samples_per_bin()
        )

        pulse_samples = (
            self._pulse_samples()
        )

        total_samples = (
            dimension
            *
            samples_per_bin
        )

        intensity = np.zeros(
            total_samples
        )

        phase = np.zeros(
            total_samples
        )

        start = (
            state_index
            *
            samples_per_bin
        )

        stop = (
            start
            +
            pulse_samples
        )

        intensity[start:stop] = (
            self.params.awg_voltage_max
        )

        time_axis = (
            np.arange(total_samples)
            / self.fs
        )

        return AWGWaveform(
            time_axis=time_axis,
            intensity_voltage=intensity,
            phase_voltage=phase
        )

    def _get_phase_pattern(
        self,
        dimension: int,
        state_index: int
    ):

        #
        # IISc phase basis
        #

        if dimension == 2:

            patterns = {

                0: [0, 0],

                1: [0, np.pi]
            }

        elif dimension == 4:

            patterns = {

                0: [0, 0, 0, 0],

                1: [0, 0, np.pi, np.pi]
            }

        elif dimension == 8:

            #
            # To be updated once
            # supplementary material
            # is available.
            #

            patterns = {

                0: [0]*8,

                1: [0,0,0,0,
                    np.pi,np.pi,
                    np.pi,np.pi]
            }

        elif dimension == 16:

            patterns = {

                0: [0]*16,

                1: (
                    [0]*8
                    +
                    [np.pi]*8
                )
            }

        else:

            raise ValueError(
                f"Unsupported dimension {dimension}"
            )

        if state_index not in patterns:

            raise ValueError(
                f"Invalid X basis state "
                f"{state_index}"
            )

        return patterns[
            state_index
        ]

    def generate_x_basis(
        self,
        dimension: int,
        state_index: int
    ) -> AWGWaveform:

        phase_pattern = (
            self._get_phase_pattern(
                dimension,
                state_index
            )
        )

        samples_per_bin = (
            self._samples_per_bin()
        )

        pulse_samples = (
            self._pulse_samples()
        )

        total_samples = (
            dimension
            *
            samples_per_bin
        )

        intensity = np.zeros(
            total_samples
        )

        phase = np.zeros(
            total_samples
        )

        for k in range(dimension):

            start = (
                k
                *
                samples_per_bin
            )

            stop = (
                start
                +
                pulse_samples
            )

            intensity[start:stop] = (
                self.params.awg_voltage_max
            )

            phase[start:stop] = (
                phase_pattern[k]
            )

        time_axis = (
            np.arange(total_samples)
            / self.fs
        )

        return AWGWaveform(
            time_axis=time_axis,
            intensity_voltage=intensity,
            phase_voltage=phase
        )

    def generate_random_state(
        self,
        dimension: int
    ):

        basis = np.random.choice(
            ["Z", "X"]
        )

        if basis == "Z":

            state_index = np.random.randint(
                0,
                dimension
            )

            waveform = (
                self.generate_z_basis(
                    dimension,
                    state_index
                )
            )

        else:

            #
            # IISc currently uses
            # only two phase states.
            #

            state_index = np.random.randint(
                0,
                2
            )

            waveform = (
                self.generate_x_basis(
                    dimension,
                    state_index
                )
            )

        return (
            basis,
            state_index,
            waveform
        )
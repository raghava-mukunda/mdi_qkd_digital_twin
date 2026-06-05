"""
phase_modulator.py
"""
"""
phase_modulator.py

Electro-Optic Phase Modulator

Models:

phi(V)
=
pi * V / Vpi

Used for:

- X basis generation
- Fourier basis generation
- Relative phase encoding

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np

from config.system_params import (
    SystemParameters
)


@dataclass(slots=True)
class PhaseModulatorMetrics:

    rms_phase_rad: float

    max_phase_rad: float

    v_pi: float


class PhaseModulator:

    """
    Electro-optic phase modulator.

    Phase shift:

        phi = pi * V / Vpi
    """

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

        self.v_pi = (
            self.params.pm_v_pi
        )

        self.bandwidth_hz = (
            self.params.pm_bandwidth_hz
        )

        self.phase_noise_std = (
            self.params.phase_noise_std_rad
        )

        self.rng = np.random.default_rng(
            self.params.random_seed
        )

    def voltage_to_phase(
        self,
        voltage: np.ndarray
    ) -> np.ndarray:

        return (
            np.pi
            *
            voltage
            /
            self.v_pi
        )

    def apply_bandwidth_limit(
        self,
        waveform: np.ndarray,
        sampling_rate_hz: float
    ) -> np.ndarray:

        fft_signal = np.fft.fft(
            waveform
        )

        freqs = np.fft.fftfreq(
            len(waveform),
            d=1/sampling_rate_hz
        )

        response = (
            1
            /
            (
                1
                +
                1j *
                freqs /
                self.bandwidth_hz
            )
        )

        filtered = np.fft.ifft(
            fft_signal * response
        )

        return np.real(
            filtered
        )

    def modulate(
        self,
        optical_field: np.ndarray,
        drive_voltage: np.ndarray,
        sampling_rate_hz: float
    ) -> np.ndarray:

        drive_voltage = (
            self.apply_bandwidth_limit(
                drive_voltage,
                sampling_rate_hz
            )
        )

        phase_shift = (
            self.voltage_to_phase(
                drive_voltage
            )
        )

        phase_shift += (
            self.rng.normal(
                0,
                self.phase_noise_std,
                len(
                    phase_shift
                )
            )
        )

        output = (
            optical_field
            *
            np.exp(
                1j *
                phase_shift
            )
        )

        return output

    def evaluate(
        self,
        voltage: np.ndarray
    ) -> PhaseModulatorMetrics:

        phase = (
            self.voltage_to_phase(
                voltage
            )
        )

        return (
            PhaseModulatorMetrics(
                rms_phase_rad=float(
                    np.sqrt(
                        np.mean(
                            phase**2
                        )
                    )
                ),
                max_phase_rad=float(
                    np.max(
                        np.abs(
                            phase
                        )
                    )
                ),
                v_pi=float(
                    self.v_pi
                )
            )
        )
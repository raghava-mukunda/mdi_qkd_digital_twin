"""
optical_delay_line.py
"""
"""
optical_delay_line.py

Optical Delay Line

Models:

E(t)
→
E(t - τ)

Supports:

- Continuous delay
- Fractional sample delay
- Automatic alignment

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
class DelayMetrics:

    delay_ps: float

    delay_samples: float

    peak_correlation: float


class OpticalDelayLine:

    """
    Optical Delay Line

    Implements continuous optical delay.

    Uses Fourier shift theorem:

        x(t-τ)

    ↔

        X(f)e^{-j2πfτ}
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

        self.fs = (
            self.params.sampling_rate_hz
        )

    def apply_delay(
        self,
        field: np.ndarray,
        delay_ps: float
    ) -> np.ndarray:

        delay_s = (
            delay_ps
            * 1e-12
        )

        n = len(field)

        freqs = np.fft.fftfreq(
            n,
            d=1/self.fs
        )

        spectrum = np.fft.fft(
            field
        )

        phase_shift = np.exp(
            -1j
            *
            2
            *
            np.pi
            *
            freqs
            *
            delay_s
        )

        delayed = np.fft.ifft(
            spectrum
            *
            phase_shift
        )

        return delayed

    def estimate_delay(
        self,
        reference: np.ndarray,
        target: np.ndarray
    ):

        correlation = np.correlate(
            np.abs(reference),
            np.abs(target),
            mode="full"
        )

        lag = (
            np.argmax(correlation)
            -
            (
                len(reference)
                - 1
            )
        )

        delay_s = (
            lag
            /
            self.fs
        )

        delay_ps = (
            delay_s
            *
            1e12
        )

        return (
            delay_ps,
            np.max(correlation)
        )

    def auto_align(
        self,
        reference: np.ndarray,
        target: np.ndarray
    ):

        estimated_delay_ps, peak = (
            self.estimate_delay(
                reference,
                target
            )
        )

        corrected = (
            self.apply_delay(
                target,
                -estimated_delay_ps
            )
        )

        metrics = DelayMetrics(

            delay_ps=float(
                estimated_delay_ps
            ),

            delay_samples=float(
                estimated_delay_ps
                *
                1e-12
                *
                self.fs
            ),

            peak_correlation=float(
                peak
            )
        )

        return (
            corrected,
            metrics
        )
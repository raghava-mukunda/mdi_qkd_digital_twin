"""
laser.py
"""
"""
laser.py

Continuous Wave (CW) Laser Model

Models:

1. Optical carrier generation
2. Phase noise (Wiener process)
3. Frequency drift
4. Lorentzian linewidth
5. Coherence time estimation

Reference:
1550 nm DFB laser used in HD-MDI-QKD setup

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
class LaserMetrics:

    coherence_time_s: float

    linewidth_hz: float

    wavelength_nm: float

    output_power_mw: float


class CWLaser:

    """
    Continuous Wave Laser

    Optical field:

    E(t)
    =
    E0 exp[j(phi(t))]

    where

    phi(t)

    follows a Wiener process

    dphi ~ N(0, 2*pi*linewidth*dt)
    """

    def __init__(
        self,
        params: Optional[SystemParameters] = None
    ):

        self.params = (
            params
            if params is not None
            else SystemParameters()
        )

        self.wavelength_nm = (
            self.params.wavelength_nm
        )

        self.linewidth_hz = (
            self.params.laser_linewidth_hz
        )

        self.output_power_mw = (
            self.params.laser_output_power_mw
        )

        self.rng = np.random.default_rng(
            self.params.random_seed
        )

    @property
    def wavelength_m(self):

        return (
            self.wavelength_nm
            * 1e-9
        )

    @property
    def output_power_w(self):

        return (
            self.output_power_mw
            * 1e-3
        )

    @property
    def field_amplitude(self):

        return np.sqrt(
            self.output_power_w
        )

    @property
    def coherence_time(self):

        """
        Lorentzian laser

        tc = 1/(pi*linewidth)
        """

        return (
            1
            /
            (
                np.pi
                *
                self.linewidth_hz
            )
        )

    def generate_phase_noise(
        self,
        duration_s: float,
        sampling_rate_hz: float
    ) -> np.ndarray:

        """
        Generate Wiener phase noise.

        sigma²
        =
        2*pi*linewidth*dt
        """

        n_samples = int(
            duration_s
            *
            sampling_rate_hz
        )

        dt = (
            1
            /
            sampling_rate_hz
        )

        sigma = np.sqrt(
            2
            *
            np.pi
            *
            self.linewidth_hz
            *
            dt
        )

        increments = (
            self.rng.normal(
                0,
                sigma,
                n_samples
            )
        )

        phase = np.cumsum(
            increments
        )

        return phase

    def generate_frequency_drift(
        self,
        duration_s: float,
        sampling_rate_hz: float,
        drift_hz: float = 1e3
    ) -> np.ndarray:

        """
        Slow thermal drift.

        Linear frequency drift.
        """

        n_samples = int(
            duration_s
            *
            sampling_rate_hz
        )

        t = (
            np.arange(n_samples)
            /
            sampling_rate_hz
        )

        phase_drift = (
            2
            *
            np.pi
            *
            drift_hz
            *
            t
        )

        return phase_drift

    def generate_field(
        self,
        duration_s: float,
        sampling_rate_hz: float,
        include_phase_noise: bool = True,
        include_drift: bool = True
    ) -> np.ndarray:

        """
        Generate complex optical field.

        Baseband representation.

        E(t)
        =
        A exp(j phi)
        """

        n_samples = int(
            duration_s
            *
            sampling_rate_hz
        )

        phase = np.zeros(
            n_samples
        )

        if include_phase_noise:

            phase += (
                self.generate_phase_noise(
                    duration_s,
                    sampling_rate_hz
                )
            )

        if include_drift:

            phase += (
                self.generate_frequency_drift(
                    duration_s,
                    sampling_rate_hz
                )
            )

        field = (
            self.field_amplitude
            *
            np.exp(
                1j
                *
                phase
            )
        )

        return field

    def metrics(self) -> LaserMetrics:

        return LaserMetrics(

            coherence_time_s=float(
                self.coherence_time
            ),

            linewidth_hz=float(
                self.linewidth_hz
            ),

            wavelength_nm=float(
                self.wavelength_nm
            ),

            output_power_mw=float(
                self.output_power_mw
            )
        )

    def __repr__(self):

        return (
            f"{self.__class__.__name__}("
            f"{self.wavelength_nm} nm, "
            f"{self.linewidth_hz/1e3:.1f} kHz)"
        )
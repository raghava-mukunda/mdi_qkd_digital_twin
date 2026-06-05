"""
voa.py
"""
"""
voa.py

Variable Optical Attenuator

Used to prepare:

Signal State
    mu_s

Decoy State
    mu_d

Vacuum State
    mu_v

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np

from config.system_params import (
    SystemParameters
)


PLANCK = 6.62607015e-34

LIGHT_SPEED = 299792458


@dataclass(slots=True)
class VOAMetrics:

    attenuation_db: float

    transmission: float

    mean_photon_number: float

    output_power_w: float


class VariableOpticalAttenuator:

    """
    Variable Optical Attenuator

    Pout
    =
    Pin * 10^(-A/10)
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

        self.wavelength_m = (
            self.params.wavelength_nm
            * 1e-9
        )

        self.pulse_width_s = (
            self.params.pulse_width_ps
            * 1e-12
        )

        self.frequency_hz = (
            LIGHT_SPEED
            /
            self.wavelength_m
        )

        self.photon_energy = (
            PLANCK
            *
            self.frequency_hz
        )

    def mean_photon_number(
        self,
        optical_field: np.ndarray
    ) -> float:

        power = np.mean(
            np.abs(
                optical_field
            ) ** 2
        )

        pulse_energy = (
            power
            *
            self.pulse_width_s
        )

        mu = (
            pulse_energy
            /
            self.photon_energy
        )

        return float(mu)

    def set_target_mu(
        self,
        optical_field: np.ndarray,
        target_mu: float
    ) -> np.ndarray:

        current_mu = (
            self.mean_photon_number(
                optical_field
            )
        )

        if current_mu <= 0:

            raise ValueError(
                "Current mu <= 0"
            )

        scale = np.sqrt(
            target_mu
            /
            current_mu
        )

        return (
            optical_field
            *
            scale
        )

    def set_signal_state(
        self,
        optical_field: np.ndarray
    ):

        return (
            self.set_target_mu(
                optical_field,
                self.params.signal_mu
            )
        )

    def set_decoy_state(
        self,
        optical_field: np.ndarray
    ):

        return (
            self.set_target_mu(
                optical_field,
                self.params.decoy_mu
            )
        )

    def set_vacuum_state(
        self,
        optical_field: np.ndarray
    ):

        return (
            self.set_target_mu(
                optical_field,
                self.params.vacuum_mu
            )
        )

    def evaluate(
        self,
        input_field: np.ndarray,
        output_field: np.ndarray
    ) -> VOAMetrics:

        pin = np.mean(
            np.abs(
                input_field
            ) ** 2
        )

        pout = np.mean(
            np.abs(
                output_field
            ) ** 2
        )

        transmission = (
            pout
            /
            pin
        )

        attenuation_db = (
            -10
            *
            np.log10(
                transmission
            )
        )

        return VOAMetrics(

            attenuation_db=float(
                attenuation_db
            ),

            transmission=float(
                transmission
            ),

            mean_photon_number=float(
                self.mean_photon_number(
                    output_field
                )
            ),

            output_power_w=float(
                pout
            )
        )
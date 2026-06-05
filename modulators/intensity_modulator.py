"""
intensity_modulator.py
"""
"""
intensity_modulator.py

Mach-Zehnder Intensity Modulator (MZM)

Models:

1. Electro-optic transfer function
2. Finite extinction ratio
3. Insertion loss
4. Finite modulation bandwidth
5. Pulse shaping

Reference:
IISc HD-MDI-QKD setup

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
class ModulatorMetrics:

    average_power: float

    peak_power: float

    extinction_ratio_db: float

    insertion_loss_db: float


class MachZehnderIM:

    """
    Mach-Zehnder Intensity Modulator

    Transfer function:

    P_out = P_in * cos²(pi*V/(2Vpi))

    where

    V = applied voltage
    Vpi = half-wave voltage

    Includes:

    - insertion loss
    - finite extinction ratio
    - bandwidth limitation
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

        self.v_pi = (
            self.params.im_v_pi
        )

        self.extinction_ratio_db = (
            self.params.im_extinction_ratio_db
        )

        self.insertion_loss_db = (
            self.params.im_insertion_loss_db
        )

        self.bandwidth_hz = (
            self.params.im_bandwidth_hz
        )

    @property
    def insertion_loss_linear(self):

        return (
            10
            **
            (
                -self.insertion_loss_db
                / 10
            )
        )

    @property
    def extinction_ratio_linear(self):

        return (
            10
            **
            (
                self.extinction_ratio_db
                / 10
            )
        )

    def transfer_function(
        self,
        voltage: np.ndarray
    ) -> np.ndarray:

        """
        Ideal MZM transfer function.

        P_out/P_in

        =
        cos²(piV/(2Vpi))
        """

        return np.cos(
            np.pi *
            voltage
            /
            (
                2 *
                self.v_pi
            )
        ) ** 2

    def apply_bandwidth_limit(
        self,
        waveform: np.ndarray,
        sampling_rate_hz: float
    ) -> np.ndarray:

        """
        First-order low-pass response.

        H(f)
        =
        1/(1+jf/fc)
        """

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
                freqs
                /
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

        """
        Main modulation function.

        Input:
        ------
        optical_field

        drive_voltage

        Output:
        -------
        intensity-modulated field
        """

        drive_voltage = (
            self.apply_bandwidth_limit(
                drive_voltage,
                sampling_rate_hz
            )
        )

        transmission = (
            self.transfer_function(
                drive_voltage
            )
        )

        output_field = (
            optical_field
            *
            np.sqrt(
                transmission
            )
        )

        output_field *= np.sqrt(
            self.insertion_loss_linear
        )

        er_floor = (
            1
            /
            self.extinction_ratio_linear
        )

        output_field += (
            er_floor
            *
            optical_field
        )

        return output_field

    def evaluate(
        self,
        optical_field: np.ndarray
    ) -> ModulatorMetrics:

        power = (
            np.abs(
                optical_field
            ) ** 2
        )

        return ModulatorMetrics(

            average_power=float(
                np.mean(power)
            ),

            peak_power=float(
                np.max(power)
            ),

            extinction_ratio_db=float(
                self.extinction_ratio_db
            ),

            insertion_loss_db=float(
                self.insertion_loss_db
            )
        )

    def __repr__(self):

        return (
            f"{self.__class__.__name__}("
            f"Vpi={self.v_pi}, "
            f"ER={self.extinction_ratio_db} dB, "
            f"IL={self.insertion_loss_db} dB)"
        )
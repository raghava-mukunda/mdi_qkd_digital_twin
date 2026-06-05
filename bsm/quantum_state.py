"""
quantum_state.py

High-Dimensional Time-Bin Quantum States

Supports:

d = 2
d = 4
d = 8
d = 16

Z basis

X basis

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class QuantumState:

    dimension: int

    basis: str

    state_index: int

    amplitudes: np.ndarray

    def overlap(
        self,
        other
    ):

        return float(

            np.abs(

                np.vdot(
                    self.amplitudes,
                    other.amplitudes
                )

            ) ** 2
        )

    def fidelity(
        self,
        other
    ):

        return self.overlap(
            other
        )

    def norm(self):

        return float(

            np.linalg.norm(
                self.amplitudes
            )
        )


class QuantumStateFactory:

    """
    Generates IISc HD-MDI-QKD states.
    """

    @staticmethod
    def z_basis(
        dimension: int,
        state_index: int
    ):

        psi = np.zeros(
            dimension,
            dtype=np.complex128
        )

        psi[state_index] = 1.0

        return QuantumState(

            dimension=dimension,

            basis="Z",

            state_index=state_index,

            amplitudes=psi
        )

    @staticmethod
    def x_basis(
        dimension: int,
        state_index: int
    ):

        #
        # f0
        #

        if state_index == 0:

            psi = np.ones(
                dimension,
                dtype=np.complex128
            )

        #
        # f1
        #

        elif state_index == 1:

            psi = np.ones(
                dimension,
                dtype=np.complex128
            )

            psi[
                dimension//2:
            ] *= -1

        else:

            raise ValueError(
                "Only f0/f1 supported"
            )

        psi = (
            psi
            /
            np.sqrt(
                dimension
            )
        )

        return QuantumState(

            dimension=dimension,

            basis="X",

            state_index=state_index,

            amplitudes=psi
        )

    @staticmethod
    def create(
        dimension: int,
        basis: str,
        state_index: int
    ):

        if basis == "Z":

            return (
                QuantumStateFactory
                .z_basis(
                    dimension,
                    state_index
                )
            )

        if basis == "X":

            return (
                QuantumStateFactory
                .x_basis(
                    dimension,
                    state_index
                )
            )

        raise ValueError(
            "Basis must be X or Z"
        )
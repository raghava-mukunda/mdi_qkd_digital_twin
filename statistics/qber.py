"""
qber.py
"""
"""
qber.py

Quantum Bit Error Rate

Author:
MDI-QKD Digital Twin
"""

from dataclasses import dataclass


@dataclass(slots=True)
class QBERMetrics:

    total_events: int

    correct_events: int

    error_events: int

    qber: float


class QBERCalculator:

    """
    QBER

    QBER =
        errors / total
    """

    def calculate(

        self,

        alice_bits,

        bob_bits,

        bsm_success

    ):

        total = 0

        errors = 0

        correct = 0

        for a, b, s in zip(

            alice_bits,

            bob_bits,

            bsm_success

        ):

            if not s:

                continue

            total += 1

            #
            # Psi-
            #
            # Alice and Bob
            # should be opposite
            #

            if a == b:

                errors += 1

            else:

                correct += 1

        if total == 0:

            qber = 0

        else:

            qber = errors / total

        return QBERMetrics(

            total_events=total,

            correct_events=correct,

            error_events=errors,

            qber=qber
        )
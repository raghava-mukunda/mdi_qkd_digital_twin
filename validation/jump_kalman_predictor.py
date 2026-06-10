"""
jump_kalman_predictor.py

Jump-Aware Kalman Predictor

Features
--------
1. 2-state model:
       x = [phase, phase_velocity]

2. Arbitrary FPGA prediction horizon

3. Innovation-based jump detection

4. Covariance inflation during phase slips

5. Compatible with the existing
   KalmanPredictor interface.

Author:
MDI-QKD Digital Twin
"""

import numpy as np


class JumpKalmanPredictor:

    def __init__(
        self,
        dt=1.0,
        velocity_decay=0.95,
        Q_phase=5e-5,
        Q_velocity=1e-4,
        R=1e-3,
        innovation_threshold=3.0,
        inflation_factor=20.0
    ):

        #
        # State:
        #
        # x[0] = phase
        # x[1] = phase velocity
        #

        self.x = np.zeros((2, 1))

        #
        # Covariance
        #

        self.P = np.eye(2)

        #
        # State transition
        #

        self.dt = dt

        self.F = np.array(
            [
                [1.0, dt],
                [0.0, velocity_decay]
            ],
            dtype=float
        )

        #
        # Measurement:
        #
        # z = phase
        #

        self.H = np.array(
            [[1.0, 0.0]],
            dtype=float
        )

        #
        # Process noise
        #

        self.Q = np.array(
            [
                [Q_phase, 0.0],
                [0.0, Q_velocity]
            ],
            dtype=float
        )

        #
        # Measurement noise
        #

        self.R = np.array(
            [[R]],
            dtype=float
        )

        #
        # Jump handling
        #

        self.innovation_threshold = innovation_threshold

        self.inflation_factor = inflation_factor

    def _wrap_phase(
        self,
        phase
    ):

        return np.angle(
            np.exp(1j * phase)
        )

    def update(
        self,
        measurement
    ):

        #
        # Prediction
        #

        x_pred = self.F @ self.x

        P_pred = (

            self.F
            @
            self.P
            @
            self.F.T

            +

            self.Q
        )

        #
        # Circular innovation
        #

        predicted_phase = x_pred[0, 0]

        innovation = self._wrap_phase(

            measurement
            -
            predicted_phase

        )

        innovation_vec = np.array(
            [[innovation]]
        )

        #
        # Innovation covariance
        #

        S = (

            self.H
            @
            P_pred
            @
            self.H.T

            +

            self.R
        )

        innovation_std = np.sqrt(
            S[0, 0]
        )

        #
        # Jump detection
        #

        if abs(innovation) > (

            self.innovation_threshold
            *
            innovation_std

        ):

            P_pred *= self.inflation_factor

            S = (

                self.H
                @
                P_pred
                @
                self.H.T

                +

                self.R
            )

        #
        # Kalman gain
        #

        K = (

            P_pred
            @
            self.H.T
            @
            np.linalg.inv(S)

        )

        #
        # Correction
        #

        self.x = (

            x_pred

            +

            K
            @
            innovation_vec

        )

        #
        # Wrap phase
        #

        self.x[0, 0] = self._wrap_phase(

            self.x[0, 0]

        )

        #
        # Covariance update
        #

        I = np.eye(2)

        self.P = (

            I

            -

            K
            @
            self.H

        ) @ P_pred

        return self.x[0, 0]

    def predict_ahead(
        self,
        steps=1
    ):

        x_future = self.x.copy()

        for _ in range(steps):

            x_future = (

                self.F
                @
                x_future

            )

            x_future[0, 0] = self._wrap_phase(

                x_future[0, 0]

            )

        return x_future[0, 0]

    @property
    def phase(self):

        return self.x[0, 0]

    @property
    def velocity(self):

        return self.x[1, 0]

    def reset(self):

        self.x = np.zeros((2, 1))

        self.P = np.eye(2)
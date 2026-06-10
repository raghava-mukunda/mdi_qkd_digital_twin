"""
kalman_predictor.py

3-State Kalman Predictor

State:
x = [phase,
     phase_velocity,
     phase_acceleration]

Author:
MDI-QKD Digital Twin
"""

import numpy as np


class KalmanPredictor:

    def __init__(
        self,
        dt=1.0,
        Q_phase=1e-6,
        Q_velocity=1e-6,
        Q_acceleration=1e-7,
        R=2.5e-3
    ):

        self.dt = dt
        self.R = R

        #
        # State:
        #
        # [phase,
        #  velocity,
        #  acceleration]
        #

        self.x = np.array([

            0.0,
            0.0,
            0.0

        ])

        #
        # Covariance
        #

        self.P = np.eye(3)

        #
        # Constant acceleration model
        #

        self.F = np.array([

            [
                1.0,
                dt,
                0.5 * dt**2
            ],

            [
                0.0,
                1.0,
                dt
            ],

            [
                0.0,
                0.0,
                1.0
            ]

        ])

        #
        # Measure phase only
        #

        self.H = np.array([

            [
                1.0,
                0.0,
                0.0
            ]

        ])

        #
        # Process noise
        #

        self.Q = np.array([

            [
                Q_phase,
                0.0,
                0.0
            ],

            [
                0.0,
                Q_velocity,
                0.0
            ],

            [
                0.0,
                0.0,
                Q_acceleration
            ]

        ])

    def update(
        self,
        measurement
    ):

        #
        # Predict
        #

        x_pred = (

            self.F
            @
            self.x

        )

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
        # Innovation
        #

        z = np.array([

            measurement

        ])

        y = (

            z

            -

            self.H
            @
            x_pred

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
        # Correct
        #

        self.x = (

            x_pred

            +

            (K @ y).flatten()

        )

        I = np.eye(3)

        self.P = (

            I

            -

            K @ self.H

        ) @ P_pred

        return float(

            self.x[0]

        )

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

        return float(

            x_future[0]

        )

    def phase(self):

        return float(

            self.x[0]

        )

    def velocity(self):

        return float(

            self.x[1]

        )

    def acceleration(self):

        return float(

            self.x[2]

        )
"""
system_params.py

Central configuration file for the
HD-MDI-QKD Digital Twin.

Reference:
IISc High-Dimensional Time-Bin MDI-QKD
"""

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class SystemParameters:

    # =====================================================
    # Simulation
    # =====================================================

    random_seed: int = 42

    sampling_rate_hz: float = 20e9

    simulation_time_s: float = 1e-6

    # =====================================================
    # Laser
    # =====================================================

    wavelength_nm: float = 1550.0

    laser_linewidth_hz: float = 100e3

    laser_output_power_mw: float = 10.0

    # =====================================================
    # AWG
    # =====================================================

    awg_sampling_rate_hz: float = 25e9

    awg_voltage_min: float = 0.0

    awg_voltage_max: float = 5.0

    #
    # IISc paper:
    # pulse width ≈ 1 ns
    #

    pulse_width_ps: float = 1000.0

    #
    # start with 1 ns spacing
    #

    time_bin_spacing_ps: float = 1000.0

    # =====================================================
    # Intensity Modulator
    # =====================================================

    im_v_pi: float = 4.0

    im_extinction_ratio_db: float = 30.0

    im_insertion_loss_db: float = 3.0

    im_bandwidth_hz: float = 20e9

    # =====================================================
    # Phase Modulator
    # =====================================================

    pm_v_pi: float = 3.5

    pm_bandwidth_hz: float = 20e9

    phase_noise_std_rad: float = 0.10

    # =====================================================
    # VOA
    # =====================================================

    signal_mu: float = 0.20

    decoy_mu: float = 0.12

    vacuum_mu: float = 1e-8

    # =====================================================
    # Optical Delay Line
    # =====================================================

    odl_range_ps: float = 1000.0

    synchronization_error_ps: float = 10.0

    # =====================================================
    # Fiber Channel
    # =====================================================

    fiber_loss_db_per_km: float = 0.2

    timing_jitter_ps: float = 20.0

    polarization_drift_deg: float = 1.0

    phase_drift_std_rad: float = 0.10

    # =====================================================
    # HOM
    # =====================================================

    #
    # Calculated automatically from linewidth
    #
    # tau_c = 1 / (pi * delta_nu)
    #

    @property
    def coherence_time_ps(self):

        return (

            1.0

            /

            (

                np.pi

                *

                self.laser_linewidth_hz

            )

        ) * 1e12

    # =====================================================
    # Beam Splitter
    # =====================================================

    beamsplitter_ratio: float = 0.5

    # =====================================================
    # SNSPD
    # =====================================================

    detector_efficiency: float = 0.95

    detector_dead_time_ns: float = 12.0

    detector_dark_count_rate_hz: float = 50.0

    detector_afterpulse_probability: float = 0.0

    detector_afterpulse_tau_ns: float = 0.0

    detector_jitter_ps: float = 20.0

    # =====================================================
    # TCSPC
    # =====================================================

    coincidence_window_ps: float = 200.0

    # =====================================================
    # Error Correction
    # =====================================================

    error_correction_efficiency: float = 1.16

    # =====================================================
    # Dimensions
    # =====================================================

    supported_dimensions = (
        2,
        4,
        8,
        16
    )

    # =====================================================
    # Validation
    # =====================================================

    validation_frames: int = 100000
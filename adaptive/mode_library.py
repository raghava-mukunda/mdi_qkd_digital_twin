from adaptive.operating_mode import OperatingMode

MODES = [

    #
    # 125 MHz mode
    #
    OperatingMode(
        frequency_hz=125e6,
        dimension=2
    ),

    OperatingMode(
        frequency_hz=125e6,
        dimension=4
    ),

    OperatingMode(
        frequency_hz=125e6,
        dimension=8
    ),

    #
    # 250 MHz mode
    #
    OperatingMode(
        frequency_hz=250e6,
        dimension=2
    ),

    OperatingMode(
        frequency_hz=250e6,
        dimension=4
    ),

    #
    # 500 MHz mode
    #
    OperatingMode(
        frequency_hz=500e6,
        dimension=2
    )
]
from dataclasses import dataclass

@dataclass(
    slots=True,
    frozen=True
)
class OperatingMode:

    frequency_hz: float

    dimension: int
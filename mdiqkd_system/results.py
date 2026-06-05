from dataclasses import dataclass

@dataclass(slots=True)
class SimulationResult:

    frames: int

    total_skr: float

    dimension_usage: dict

    selected_dimensions: list

    skr_history: list

    channel_history: list
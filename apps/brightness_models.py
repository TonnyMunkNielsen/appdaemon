from __future__ import annotations  # Add this import to enable forward references
from abc import ABC, abstractmethod
from enum import Enum

# Brightness Model Type Enum
class BrightnessModelType(Enum):
    ON_DIM = "on_dim"
    CIRCADIAN_RHYTHM = "circadian_rhythm"

# Brightness Model Factory
class BrightnessModelFactory:
    def get_brightness_model(self, model_type):
        """
        Get an instance of the specified brightness model.

        Args:
            model_type (BrightnessModelType): The type of brightness model to retrieve.

        Returns:
            BrightnessModel: An instance of the specified brightness model.
        """
        return self.model_mapping[model_type]

# --- Abstract Brightness Model (Moved to this file) ---
class BrightnessModel(ABC):
    """
    Abstract base class for defining the interface of a brightness model.

    Methods:
        dim_lights(light_entity, on_brightness, dim_brightness, dim_duration): Abstract method to dim the lights over a specified duration before turning them off.
    """

    @abstractmethod
    def dim_lights(self, light_entity, on_brightness, dim_brightness, dim_duration):
        """
        Dim the lights over a specified duration before turning them off.

        Args:
            light_entity (str): The entity ID of the light to dim.
            on_brightness (int): The brightness value to set the light when turned on.
            dim_brightness (int): The brightness value to dim the light to.
            dim_duration (int): Duration in seconds for the lights to dim before turning them off.
        """
        pass

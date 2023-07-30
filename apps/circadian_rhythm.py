from __future__ import annotations  # Add this import to enable forward references
from brightness_models import BrightnessModel

class CircadianRhythmBrightnessModel(BrightnessModel):

    def dim_lights(self, light_entity, on_brightness, dim_brightness, dim_duration):
        """
        Dim the lights over a specified duration before turning them off.

        Args:
            light_entity (str): The entity ID of the light to dim.
            on_brightness (int): The brightness value to set the light when turned on.
            dim_brightness (int): The brightness value to dim the light to.
            dim_duration (int): Duration in seconds for the lights to dim before turning them off.
        """
        # No dimming for circadian rhythm model
        # Turn on the light with the specified on_brightness
        self.turn_on(light_entity, brightness=on_brightness)

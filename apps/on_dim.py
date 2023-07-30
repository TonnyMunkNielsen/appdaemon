from __future__ import annotations  # Add this import to enable forward references
from brightness_models import BrightnessModel

# Time Constants
SECONDS_TO_MILLISECONDS = 1000

class OnDimBrightnessModel(BrightnessModel):

    def dim_lights(self, light_entity, on_brightness, dim_brightness, dim_duration):
        """
        Dim the lights over a specified duration before turning them off.

        Args:
            light_entity (str): The entity ID of the light to dim.
            on_brightness (int): The brightness value to set the light when turned on.
            dim_brightness (int): The brightness value to dim the light to.
            dim_duration (int): Duration in seconds for the lights to dim before turning them off.
        """
        # Calculate the transition time in milliseconds
        transition_time = dim_duration * SECONDS_TO_MILLISECONDS

        # Turn on the light with the specified on_brightness
        self.turn_on(light_entity, brightness=on_brightness, transition=transition_time)

        # Wait for the dim_duration before turning off the light
        self.run_in(self.turn_off_light, dim_duration, light_entity=light_entity, brightness=dim_brightness)

    def turn_off_light(self, kwargs):
        """
        Callback function to turn off the light after dim_duration.

        Args:
            kwargs (dict): Keyword arguments containing light_entity and brightness.
        """
        light_entity = kwargs["light_entity"]
        dim_brightness = kwargs["brightness"]
        self.turn_off(light_entity, brightness=dim_brightness)

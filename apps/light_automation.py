import hassapi as hass
from datetime import datetime, timedelta
from enum import Enum
from brightness_models import BrightnessModelFactory, BrightnessModelType
from circadian_rhythm import CircadianRhythmBrightnessModel
from on_dim import OnDimBrightnessModel

# Time Constants
SECONDS_TO_MILLISECONDS = 1000

# Event Constants
BUTTON_PUSH_VALUE = "1002"

# Door State Enum
class DoorState(Enum):
    CLOSED = "off"
    OPEN = "on"


class LightAutomation(hass.Hass):
    def initialize(self):
        # Mapping of brightness model types to their corresponding classes
        self.model_mapping = {
            BrightnessModelType.ON_DIM: OnDimBrightnessModel(),
            BrightnessModelType.CIRCADIAN_RHYTHM: CircadianRhythmBrightnessModel()
        }

        # Configuration
        self.motion_sensor = self.args["motion_sensor"]
        self.door_sensor = self.args.get(
            "door_sensor", None
        )  # Optional: Door sensor (if present)
        self.lights = self.args["lights"]
        self.manual_mode = self.args["manual_mode"]
        self.manual_mode_duration = int(self.args["manual_mode_duration"])
        self.dim_duration = int(self.args["dim_duration"])
        self.off_delay = int(self.args["off_delay"])
        self.button_unique_id = self.args["button_unique_id"]

        # Brightness Model Factory
        self.brightness_model_factory = BrightnessModelFactory()

        # State Variables
        self.is_person_inside = False

        # Optional: Door Sensor (if present)
        if self.door_sensor:
            self.listen_state(self.door_state_changed, self.door_sensor)

        # Motion Sensor
        if not self.get_state(self.manual_mode) == "on":
            self.listen_state(self.motion_triggered, self.motion_sensor)
        self.listen_event(
            self.manual_mode_activated,
            "deconz_event",
            unique_id=self.button_unique_id,
            value=BUTTON_PUSH_VALUE,
        )

        # Manual Mode Timer (will be started when manual mode is activated)
        self.manual_mode_timer = None

    # Configuration Parsing and Validation (New Feature: Validate Configuration)
    def parse_config(self):
        """
        Parse and validate the configuration parameters.

        Returns:
            bool: True if the configuration is valid, False otherwise.
        """
        if not isinstance(self.motion_sensor, str) or not self.motion_sensor.startswith(
            "binary_sensor."
        ):
            self.log(
                "Invalid motion_sensor configuration. Please provide a valid binary_sensor entity ID."
            )
            return False

        if self.door_sensor and (
            not isinstance(self.door_sensor, str)
            or not self.door_sensor.startswith("binary_sensor.")
        ):
            self.log(
                "Invalid door_sensor configuration. Please provide a valid binary_sensor entity ID."
            )
            return False

        if not isinstance(self.lights, list) or not all(
            isinstance(light, dict) and "entity" in light for light in self.lights
        ):
            self.log(
                "Invalid lights configuration. Please provide a list of dictionaries with 'entity' key."
            )
            return False

        for light in self.lights:
            if not isinstance(light["entity"], str) or not light["entity"].startswith(
                "light."
            ):
                self.log(
                    "Invalid 'entity' in lights configuration. Please provide a valid light entity ID."
                )
                return False

            on_brightness = light.get("on_brightness")
            if (
                not isinstance(on_brightness, int)
                or on_brightness < 0
                or on_brightness > 255
            ):
                self.log(
                    "Invalid 'on_brightness' in lights configuration. Please provide a valid integer (0-255)."
                )
                return False

            dim_brightness = light.get("dim_brightness", on_brightness)
            if (
                not isinstance(dim_brightness, int)
                or dim_brightness < 0
                or dim_brightness > 255
            ):
                self.log(
                    "Invalid 'dim_brightness' in lights configuration. Please provide a valid integer (0-255)."
                )
                return False

            brightness_model_type = light.get(
                "brightness_model", BrightnessModelType.ON_DIM
            )
            if brightness_model_type not in BrightnessModelType:
                self.log(
                    "Invalid 'brightness_model' in lights configuration. Please choose a valid brightness model."
                )
                return False

        if not isinstance(self.manual_mode, str) or not self.manual_mode.startswith(
            "input_boolean."
        ):
            self.log(
                "Invalid manual_mode configuration. Please provide a valid input_boolean entity ID."
            )
            return False

        if (
            not isinstance(self.manual_mode_duration, int)
            or self.manual_mode_duration < 0
        ):
            self.log(
                "Invalid manual_mode_duration configuration. Please provide a valid positive integer."
            )
            return False

        if not isinstance(self.dim_duration, int) or self.dim_duration < 0:
            self.log(
                "Invalid dim_duration configuration. Please provide a valid positive integer."
            )
            return False

        if not isinstance(self.off_delay, int) or self.off_delay < 0:
            self.log(
                "Invalid off_delay configuration. Please provide a valid positive integer."
            )
            return False

        if not isinstance(self.button_unique_id, str):
            self.log(
                "Invalid button_unique_id configuration. Please provide a valid string."
            )
            return False

        return True

    # Motion Sensor Triggered
    def motion_triggered(self, entity, attribute, old, new, kwargs):
        """
        Callback function when the motion sensor is triggered.

        Args:
            entity (str): The entity ID of the motion sensor.
            attribute (str): The attribute that triggered the callback.
            old (str): The previous state of the motion sensor.
            new (str): The new state of the motion sensor.
            kwargs (dict): Additional keyword arguments.
        """
        if new == "on":
            self.log("Motion detected!")
            if not self.is_blocked():
                self.log("Turning on lights...")
                for light in self.lights:
                    self.turn_on(light["entity"], brightness=light["on_brightness"])
                if self.door_sensor and self.get_state(self.door_sensor) == DoorState.CLOSED.value:
                    self.is_person_inside = True
                else:
                    self.dim_lights()
            else:
                self.log("Person in room, no changes until door opens")
        else:
            self.log("Motion cleared!")

    # Door Sensor State Changed (Optional: If door_sensor is present)
    def door_state_changed(self, entity, attribute, old, new, kwargs):
        """
        Callback function when the door sensor state changes.

        Args:
            entity (str): The entity ID of the door sensor.
            attribute (str): The attribute that triggered the callback.
            old (str): The previous state of the door sensor.
            new (str): The new state of the door sensor.
            kwargs (dict): Additional keyword arguments.
        """
        self.log(f"Door sensor {entity} state changed: {new}")
        if self.is_person_inside is True and new == DoorState.OPEN.value:
            self.is_person_inside = False
            self.dim_lights()

    # Manual Mode Activated
    def manual_mode_activated(self, event_name, data, kwargs):
        """
        Callback function when manual mode is activated.

        Args:
            event_name (str): The name of the event.
            data (dict): Data associated with the event.
            kwargs (dict): Additional keyword arguments.
        """
        self.log("Manual mode activated.")
        self.call_service("input_boolean/toggle", entity_id=self.manual_mode)

    # Set Manual Mode Off
    def set_manual_mode_off(self):
        """
        Set manual mode off and cancel the manual mode timer.
        """
        self.cancel_timer(self.manual_mode_timer)
        self.manual_mode_timer = self.run_in(
            self.manual_mode_timer_callback, self.manual_mode_duration
        )

    # Manual Mode Timer Callback
    def manual_mode_timer_callback(self, kwargs):
        """
        Callback function for the manual mode timer.

        Args:
            kwargs (dict): Additional keyword arguments.
        """
        self.log("Manual mode timer expired. Turning off manual mode.")
        self.call_service("input_boolean/turn_off", entity_id=self.manual_mode)

    # Dim Lights
    def dim_lights(self):
        """
        Dim the lights over a specified duration before turning them off.
        """

        if self.is_manual_mode_on():
            # Cancel turning off lights if manual mode is activated
            self.cancel_dimming_and_turn_off_lights()
        else:
            for light in self.lights:
                light_entity = light["entity"]
                on_brightness = light["on_brightness"]
                dim_brightness = light.get("dim_brightness", on_brightness)
                self.log(f"Dimming lights {light_entity} from {on_brightness} to {dim_brightness} over {self.dim_duration} seconds.")
                self.turn_on(
                    light_entity,
                    brightness=on_brightness,
                    transition=self.dim_duration * SECONDS_TO_MILLISECONDS,
                )
                self.run_in(
                    self.turn_off_lights,
                    self.dim_duration,
                    light_entity=light_entity,
                    on_brightness=on_brightness,
                    dim_brightness=dim_brightness,
                )

    # Turn Off Lights
    def turn_off_lights(self, kwargs):
        """
        Turn off the lights.

        Args:
            kwargs (dict): Additional keyword arguments.
        """
        if self.is_manual_mode_on():
            # Cancel turning off lights if manual mode is activated
            self.cancel_dimming_and_turn_off_lights()
        else:
            light_entity = kwargs["light_entity"]
            on_brightness = kwargs["on_brightness"]
            dim_brightness = kwargs["dim_brightness"]
            self.turn_on(light_entity, brightness=dim_brightness)
            self.run_in(self.check_off_delay, self.off_delay, light_entity=light_entity)

    # Check Off Delay
    def check_off_delay(self, kwargs):
        """
        Check if lights should be turned off after the off delay.

        Args:
            kwargs (dict): Additional keyword arguments.
        """
        light_entity = kwargs["light_entity"]
        if not self.is_blocked() and self.get_state(self.motion_sensor) == "off":
            self.log("Turning off lights.")
            self.turn_off(light_entity)

    # Check if Blocked (Is Person Inside Room)
    def is_blocked(self):
        """
        Check if the light automation is in a blocked state (is_person_inside).

        Returns:
            bool: True if the automation is in a blocked state, False otherwise.
        """
        return self.is_person_inside

    # Check if Manual Mode is On
    def is_manual_mode_on(self):
        """
        Check if manual mode is currently on.

        Returns:
            bool: True if manual mode is on, False otherwise.
        """
        return self.get_state(self.manual_mode) == "on"

    # Cancel Dimming and Turning Off Lights if Manual Mode is On
    def cancel_dimming_and_turn_off_lights(self):
        """
        Cancel scheduled dimming and turning off lightS.
        """
        for light in self.lights:
            light_entity = light["entity"]
            self.cancel_timer(self.manual_mode_timer)
            self.cancel_timer(f"{light_entity}_dim_timer")


# ... End of the Light Automation class ...

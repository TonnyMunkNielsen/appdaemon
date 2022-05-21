import hassapi as hass

from light_automation_helper import (
    get_rgb_int_tuple_from_hsv,
    kwarg_not_set,
    randint_from_list,
    randrange_from_list,
)

# from light_automation_helper import LightAutomationHelper

# Sensor State	    Description
# sunrise_start	    sunrise (top edge of the sun appears on the horizon)
# sunrise_end	    sunrise ends (bottom edge of the sun touches the horizon)
# golden_hour_1	    morning golden hour (soft light, the best time for photography)
# solar_noon	    solar noon (sun is in the highest position)
# golden_hour_2	    evening golden hour
# sunset_start	    sunset starts (bottom edge of the sun touches the horizon)
# sunset_end	    sunset (sun disappears below the horizon, evening civil twilight starts)
# dusk	            dusk (evening nautical twilight starts)
# nautical_dusk	    nautical dusk (evening astronomical twilight starts)
# night_start	    night starts (dark enough for astronomical observations)
# nadir	            nadir (darkest moment of the night, the sun is in the lowest position)
# night_end	        night ends (morning astronomical twilight starts)
# nautical_dawn	    nautical dawn (morning nautical twilight starts)
# dawn	            dawn (morning nautical twilight ends, morning civil twilight starts)


class AutomateLightsDaylight(hass.Hass):
    def initialize(self):
        # TODO TMN: Extract functionality into light_automation_helper after test suite is in place.
        # helpers = self.get_app("light_automation_helper")
        # self.listen_state(helpers.turn_lights_on, "sensor.daylight", new="dusk")
        self.listen_state(self.turn_lights_on, "sensor.daylight", new="dusk")
        self.listen_state(self.turn_lights_off, "sensor.daylight", new="dawn")

    def turn_lights_off(self, entity, attribute, old, new, kwargs):
        for light in self.args["lights"]:
            self.log(light.get("name") + ": Turning off light.")
            self.turn_off(light.get("name"))

    def turn_lights_on(self, entity, attribute, old, new, kwargs):
        for light in self.args["lights"]:
            kwargs = set_default_kwargs_if_empty(kwargs)
            self.turn_light_on_random_daylight(
                entity=light.get("name"),
                hue=kwargs["hue"],
                saturation=kwargs["saturation"],
                brightness_pct=kwargs["brightness_pct"],
            )

    def turn_light_on_random_daylight(self, **kwargs):
        entity = kwargs["entity"]
        brightness_percent = randint_from_list(kwargs["brightness_pct"])
        saturation = randrange_from_list(kwargs["saturation"])
        hue = randrange_from_list(kwargs["hue"])
        self.log_hsv(entity, brightness_percent, saturation, hue)
        rgb = get_rgb_int_tuple_from_hsv(brightness_percent, saturation, hue)
        self.log_rgb(entity, rgb)
        self.turn_on(entity, rgb_color=rgb)

    def log_rgb(self, entity, rgb):
        self.log(entity + ": RGB: " + str(rgb))

    def log_hsv(self, entity, brightness_percent, saturation, hue):
        self.log(
            entity
            + ": Turning on light. Hue: "
            + str(hue)
            + ", Saturation: "
            + str(saturation)
            + ", Brightness_percent: "
            + str(brightness_percent)
            + "."
        )


def set_default_kwargs_if_empty(kwargs):
    if kwarg_not_set(kwargs, "brightness_pct"):
        # brightness_pct = [from, to]
        kwargs["brightness_pct"] = [1, 100]
    if kwarg_not_set(kwargs, "hue"):
        # hue = [from, to (not including), step]
        kwargs["hue"] = [0, 360, 30]
    if kwarg_not_set(kwargs, "saturation"):
        # saturation = [from, to]
        kwargs["saturation"] = [1, 100]
    return kwargs

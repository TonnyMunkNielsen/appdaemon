import hassapi as hass

from light_automation_helper import (
    getRgbIntTupleFromHsv,
    kwargNotSet,
    randintFromList,
    randrangeFromList,
)

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
        self.listen_state(
            self.turnLightsOn,
            "sensor.daylight",
            new="dusk",
            brightness_pct=[100, 100],
            hue=[0, 360, 30],
            saturation=[80, 100],
        )
        self.listen_state(self.turnLightsOff, "sensor.daylight", new="dawn")

    def turnLightsOff(self, entity, attribute, old, new, kwargs):
        for light in self.args["lights"]:
            self.log(light.get("name") + ": Turning off light.")
            self.turn_off(light.get("name"))

    def turnLightsOn(self, entity, attribute, old, new, kwargs):
        for light in self.args["lights"]:
            lightName = light.get("name")
            kwargs = setDefaultKwargsIfEmpty(kwargs)
            self.turnLightOnRandomDaylight(
                entity=lightName,
                hue=kwargs["hue"],
                saturation=kwargs["saturation"],
                brightness_pct=kwargs["brightness_pct"],
            )

    def turnLightOnRandomDaylight(self, kwargs):
        entity = kwargs.get("entity")
        brightness_percent = randintFromList(kwargs["brightness_pct"])
        saturation = randrangeFromList(kwargs["saturation"])
        hue = randrangeFromList(kwargs["hue"])
        self.logHsv(entity, brightness_percent, saturation, hue)
        rgb = getRgbIntTupleFromHsv(brightness_percent, saturation, hue)
        self.logRgb(entity, rgb)
        self.turn_on(entity, rgb_color=rgb)

    def logRgb(self, entity, rgb):
        self.log(entity + ": RGB: " + str(rgb))

    def logHsv(self, entity, brightness_percent, saturation, hue):
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


def setDefaultKwargsIfEmpty(kwargs):
    if kwargNotSet(kwargs, "brightness_pct"):
        # brightness_pct = [from, to]
        kwargs["brightness_pct"] = [1, 100]
    if kwargNotSet(kwargs, "hue"):
        # hue = [from, to (not including), step]
        kwargs["hue"] = [0, 360, 30]
    if kwargNotSet(kwargs, "saturation"):
        # saturation = [from, to]
        kwargs["saturation"] = [1, 100]
    return kwargs

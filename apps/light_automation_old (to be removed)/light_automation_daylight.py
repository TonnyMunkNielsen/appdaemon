import hassapi as hass
import datetime
import distutils.util
import random
import colorsys

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
        self.api = self.get_app()
        self.listen_state(self.turnLightsOn, "sensor.daylight", new="dusk")
        self.listen_state(self.turnLightsOff, "sensor.daylight", new="dawn")

    def turnLightsOff(self, entity, attribute, old, new, kwargs):
        for light in self.args['lights']:
            self.log(light.get("name") + ": Turning off light.")
            self.turn_off(light.get("name"))

    def turnLightsOn(self, entity, attribute, old, new, kwargs):
        for light in self.args['lights']:
            brightness_percent = 100
            hue = random.randrange(0, 359, 30)
            saturation = random.randint(80, 100)
            self.log(light.get("name") + ": Turning on light. Hue: " + str(hue) + ", Saturation: " + str(saturation) + ", Brightness_percent: " + str(brightness_percent) + ".")
            rgb = colorsys.hsv_to_rgb(hue/360, saturation/100, brightness_percent/100)
            rgb = tuple([round(255*x) for x in rgb])
            self.log(light.get("name") + ": RGB: " + str(rgb))
            self.turn_on(light.get("name"), rgb_color = rgb)
import hassapi as hass
import random
import colorsys


class LightAutomationHelper(hass.Hass):
    def initialize(self):
        self.log("Do Nothing.")

    def turnLightOnRandom(self, entity, attribute, old, new, kwargs):
        kwargs = _setDefaultKwargsIfEmpty(kwargs)
        brightness_percent = random.randint(kwargs.get("brightness_pct")[0], kwargs.get("brightness_pct")[1])
        hue = random.randrange(kwargs.get("hue")[0], kwargs.get("hue")[1], kwargs.get("hue")[2])
        saturation = random.randint(kwargs.get("saturation")[0], kwargs.get("saturation")[1])
        self.log(entity + ": Turning on light. Hue: " + str(hue) + ", Saturation: " +
                 str(saturation) + ", Brightness_percent: " + str(brightness_percent) + ".")
        rgb = colorsys.hsv_to_rgb(
            hue/360, saturation/100, brightness_percent/100)
        rgb = tuple([round(255*x) for x in rgb])
        self.log(entity + ": RGB: " + str(rgb))
        self.turn_on(entity, rgb_color=rgb)


def _setDefaultKwargsIfEmpty(kwargs):
    if _kwargNotSet(kwargs, 'brightness_pct'):
        # brightness_pct = [from, to]
        kwargs['brightness_pct'] = [1, 100]
    if _kwargNotSet(kwargs, 'hue'):
        # hue = [from, to (not including), step]
        kwargs['hue'] = [0, 360, 30]
    if _kwargNotSet(kwargs, 'saturation'):
        # saturation = [from, to]
        kwargs['saturation'] = [1, 100]
    return kwargs


def _kwargNotSet(kwargs, name):
    return name not in kwargs

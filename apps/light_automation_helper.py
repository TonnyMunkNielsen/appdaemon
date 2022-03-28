import hassapi as hass
import random
import colorsys


class LightAutomationHelper(hass.Hass):
    def initialize(self):
        self.log("Do Nothing.")

    def turnLightOnRandom(self, entity, kwargs):
        tempKwargs = _setDefaultKwargsIfEmpty(kwargs)
        brightness_percent = random.randint(tempKwargs.get("brightness_pct")[0], tempKwargs.get("brightness_pct")[1])
        hue = random.randrange(tempKwargs.get("hue")[0], tempKwargs.get("hue")[1], tempKwargs.get("hue")[2])
        saturation = random.randint(tempKwargs.get("saturation")[0], tempKwargs.get("saturation")[1])
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

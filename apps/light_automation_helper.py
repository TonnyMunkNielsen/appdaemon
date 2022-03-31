import hassapi as hass
import random
import colorsys


class LightAutomationHelper(hass.Hass):
    def initialize(self):
        self.log("Do Nothing.")

    def turnLightOnRandom(self, **kwargs):
        entity = kwargs.get('entity')
        tempKwargs = self._setDefaultKwargsIfEmpty(*kwargs)
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


def kwargNotSet(kwargs, name):
    return name not in kwargs


def randintFromList(attr):
    return applyFunOnList(random.randint, attr)


def randrangeFromList(attr):
    return applyFunOnList(random.randrange, attr)


def applyFunOnList(fun, list):
    return fun(*list)


def getRgbIntTupleFromHsv(brightness_percent, saturation, hue):
    rgb = colorsys.hsv_to_rgb(
        hue/360, saturation/100, brightness_percent/100)
    return tuple([round(255*x) for x in rgb])

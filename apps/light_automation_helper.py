import appdaemon.plugins.hass.hassapi as hass

import colorsys
import random


class LightAutomationHelper(hass.Hass):
    def initialize(self):
        self.log("Do Nothing.")

    def turn_light_on_random(self, **kwargs):
        entity = kwargs.get("entity")
        tempKwargs = self._setDefaultKwargsIfEmpty(*kwargs)
        brightness_percent = random.randint(
            tempKwargs.get("brightness_pct")[0], tempKwargs.get("brightness_pct")[1]
        )
        hue = random.randrange(
            tempKwargs.get("hue")[0], tempKwargs.get("hue")[1], tempKwargs.get("hue")[2]
        )
        saturation = random.randint(
            tempKwargs.get("saturation")[0], tempKwargs.get("saturation")[1]
        )
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
        rgb = colorsys.hsv_to_rgb(hue / 360, saturation / 100, brightness_percent / 100)
        rgb = tuple([round(255 * x) for x in rgb])
        self.log(entity + ": RGB: " + str(rgb))
        self.turn_on(entity, rgb_color=rgb)


def kwarg_not_set(kwargs, name):
    return name not in kwargs


def randint_from_list(attr):
    return apply_fun_on_list(random.randint, attr)


def randrange_from_list(attr):
    return apply_fun_on_list(random.randrange, attr)


def apply_fun_on_list(fun, list):
    return fun(*list)


def get_rgb_int_tuple_from_hsv(brightness_percent, saturation, hue):
    rgb = colorsys.hsv_to_rgb(hue / 360, saturation / 100, brightness_percent / 100)
    return tuple([round(255 * x) for x in rgb])

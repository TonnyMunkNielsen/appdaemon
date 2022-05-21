import appdaemon.plugins.hass.hassapi as hass


from light_automation_helper import (
    get_rgb_int_tuple_from_hsv,
    kwarg_not_set,
    randint_from_list,
    randrange_from_list,
)

LIGHT_SEQUENCE = "LIGHT_SEQUENCE"


class LightSequence(hass.Hass):
    def initialize(self):
        self.listen_event(
            self.lights_cb,
            LIGHT_SEQUENCE,
            brightness_pct=[75, 100],
            hue=[0, 360, 30],
            saturation=[75, 100],
            entity="light.small_bathroom_mirror",
            delay=3,
            number_of_runs=10,
            turn_off=True,
        )
        self.listen_event(
            self.lights_cb,
            LIGHT_SEQUENCE,
            brightness_pct=[75, 100],
            hue=[0, 360, 30],
            saturation=[75, 100],
            entity="light.small_bathroom_shower",
            delay=3,
            number_of_runs=11,
            turn_off=True,
        )

    def lights_cb(self, event, data, kwargs):
        kwargs = set_default_kwargs_if_empty_light_sequence(kwargs)  # TODO: Test.
        turn_off = kwargs["turn_off"]
        if turn_off:
            self.turn_off(kwargs["entity"])
        number_of_runs = kwargs["number_of_runs"]
        for i in range(number_of_runs):
            multiplier = i + 1 if turn_off else i
            delay = multiplier * kwargs["delay"]
            self.log("Randomizing light at delay: " + str(delay))
            self.run_in(
                self.turn_light_on_random_light_sequence,
                delay,
                hue=kwargs["hue"],
                saturation=kwargs["saturation"],
                brightness_pct=kwargs["brightness_pct"],
                entity=kwargs["entity"],
            )

    def turn_light_on_random_light_sequence(self, kwargs):
        entity = kwargs.get("entity")
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


def set_default_kwargs_if_empty_light_sequence(kwargs):
    if kwarg_not_set(kwargs, "brightness_pct"):
        # brightness_pct = [from, to]
        kwargs["brightness_pct"] = [1, 100]
    if kwarg_not_set(kwargs, "hue"):
        # hue = [from, to (not including), step]
        kwargs["hue"] = [0, 360, 30]
    if kwarg_not_set(kwargs, "saturation"):
        # saturation = [from, to]
        kwargs["saturation"] = [1, 100]
    if kwarg_not_set(kwargs, "delay"):
        # delay in seconds between sequence progressions
        kwargs["delay"] = 3
    if kwarg_not_set(kwargs, "number_of_runs"):
        # number_of_runs is how many sequence progressions will take place.
        # TODO: Implement '-1' which means keeps looping until another event.
        kwargs["number_of_runs"] = 10
    if kwarg_not_set(kwargs, "turn_off"):
        # turn_off specifies if a turn_off-call should be prepended to the sequence.
        kwargs["turn_off"] = True
    return kwargs

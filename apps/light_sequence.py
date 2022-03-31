import hassapi as hass

from light_automation_helper import (getRgbIntTupleFromHsv, kwargNotSet,
                                     randintFromList, randrangeFromList)

LIGHT_SEQUENCE = "LIGHT_SEQUENCE"


class LightSequence(hass.Hass):
    def initialize(self):
        self.listen_event(self.lights_cb, LIGHT_SEQUENCE, brightness_pct=[75, 100], hue=[0, 360, 30], saturation=[75, 100], entity="light.office_ceiling_closet", delay=3, number_of_runs=10, turn_off=True)
        self.listen_event(self.lights_cb, LIGHT_SEQUENCE, brightness_pct=[75, 100], hue=[0, 360, 30], saturation=[75, 100], entity="light.office_ceiling_desktop", delay=3, number_of_runs=11, turn_off=True)

    def lights_cb(self, event, data, kwargs):
        kwargs = setDefaultKwargsIfEmptyLightSequence(kwargs)  # TODO: Test.
        turn_off = kwargs['turn_off']
        if(turn_off):
            self.turn_off(kwargs['entity'])
        number_of_runs = kwargs['number_of_runs']
        for i in range(number_of_runs):
            multiplier = i + 1 if turn_off else i
            delay = multiplier * kwargs['delay']
            self.log("Randomizing light at delay: " + str(delay))
            self.run_in(self.turnLightOnRandomLightSequence, delay, hue=kwargs['hue'], saturation=kwargs['saturation'], brightness_pct=kwargs['brightness_pct'], entity=kwargs['entity'])

    def turnLightOnRandomLightSequence(self, kwargs):
        entity = kwargs.get('entity')
        brightness_percent = randintFromList(kwargs['brightness_pct'])
        saturation = randrangeFromList(kwargs['saturation'])
        hue = randrangeFromList(kwargs['hue'])
        self.logHsv(entity, brightness_percent, saturation, hue)
        rgb = getRgbIntTupleFromHsv(brightness_percent, saturation, hue)
        self.logRgb(entity, rgb)
        self.turn_on(entity, rgb_color=rgb)

    def logRgb(self, entity, rgb):
        self.log(entity + ": RGB: " + str(rgb))

    def logHsv(self, entity, brightness_percent, saturation, hue):
        self.log(entity + ": Turning on light. Hue: " + str(hue) + ", Saturation: " +
                 str(saturation) + ", Brightness_percent: " + str(brightness_percent) + ".")


def setDefaultKwargsIfEmptyLightSequence(kwargs):
    if kwargNotSet(kwargs, 'brightness_pct'):
        # brightness_pct = [from, to]
        kwargs['brightness_pct'] = [1, 100]
    if kwargNotSet(kwargs, 'hue'):
        # hue = [from, to (not including), step]
        kwargs['hue'] = [0, 360, 30]
    if kwargNotSet(kwargs, 'saturation'):
        # saturation = [from, to]
        kwargs['saturation'] = [1, 100]
    if kwargNotSet(kwargs, 'delay'):
        # delay in seconds between sequence progressions
        kwargs['delay'] = 3
    if kwargNotSet(kwargs, 'number_of_runs'):
        # number_of_runs is how many sequence progressions will take place 
        # TODO: Implement '-1' which means keeps looping until another event.
        kwargs['number_of_runs'] = 10
    if kwargNotSet(kwargs, 'turn_off'):
        # turn_off specifies if a turn_off-call should be prepended to the sequence.
        kwargs['turn_off'] = True
    return kwargs

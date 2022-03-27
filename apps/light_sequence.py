import hassapi as hass

from light_automation_helper import LightAutomationHelper

LIGHT_SEQUENCE = "LIGHT_SEQUENCE"


class LightSequence(hass.Hass):
    def initialize(self):
        self.listen_event(self.lights_cb, LIGHT_SEQUENCE, brightness_pct=[75, 100], hue=[0, 360, 30], saturation=[75, 100])
        # self.listen_event(self.lights_cb, LIGHT_SEQUENCE, None, brightness_pct=[75, 100], hue=[0, 360, 30], saturation=[75, 100], entity="light.office_ceiling_desktop")

    def lights_cb(self, event, data, kwargs):
        self.turn_off("light.office_ceiling_closet")
        for i in range(0, 10):
            self.log("Randomizing light at delay: " + str(i))
            self.run_in(
                LightAutomationHelper.turnLightOnRandom, i, entity="light.office_ceiling_closet", attribute=None, old=None, new=None, kwargs=kwargs
            )

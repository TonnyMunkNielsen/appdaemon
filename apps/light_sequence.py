import hassapi as hass

LIGHT_SEQUENCE = "LIGHT_SEQUENCE"


class LightSequence(hass.Hass):
    def initialize(self):
        self.listen_event(self.lights_cb, LIGHT_SEQUENCE)

    def lights_cb(self, event, data, kwargs):
        self.turn_off("light.office_lights")

        self.run_in(
            self.turn_on_lights, 1, entity="light.office_ceiling_closet", brightness=128
        )
        self.run_in(
            self.turn_on_lights,
            2,
            entity="light.office_ceiling_desktop",
            brightness=128,
        )
        self.run_in(
            self.turn_on_lights, 3, entity="light.office_ceiling_closet", brightness=64
        )
        self.run_in(
            self.turn_on_lights, 4, entity="light.office_ceiling_desktop", brightness=64
        )
        self.run_in(
            self.turn_on_lights, 5, entity="light.office_lights", brightness=255
        )

    def turn_on_lights(self, kwargs):
        entity = kwargs["entity"]
        brightness = kwargs["brightness"]
        self.turn_on(entity, brightness=brightness)

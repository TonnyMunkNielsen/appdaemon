import hassapi as hass
from appdaemontestframework import automation_fixture
#from light_automation import AutomateLights


class AutomateLights(hass.Hass):
    def initialize(self):
        pass
    def turn_lights_off(self):
        pass

@automation_fixture(AutomateLights(hass))
def automate_lights():
    pass


# @automation_fixture(AutomateLights(hass.Hass))
# def automate_lights(given_that):
#     automate_lights = AutomateLights(hass.Hass)
#     automate_lights.initialize()
#     given_that.mock_functions_are_cleared()
#     given_that.passed_arg("sensor").is_set_to("binary_sensor.motion_sensor_hallway")
#     given_that.passed_arg("lights").is_set_to("light.hallway_lights")
#     given_that.passed_arg("timer_on_to_dim").is_set_to("7")
#     given_that.passed_arg("timer_dim_to_off").is_set_to("3")
#     given_that.passed_arg("brightness_on").is_set_to("100")
#     given_that.passed_arg("brightness_dim").is_set_to("33")
#     return automate_lights


# def test_motion_activates_light(given_that, automate_lights, assert_that):
#     automate_lights.turnLightsOn()
#     assert_that(automate_lights.args["lights"]).was.turned_on()


def test_motion_turns_light_on(self, automate_lights: AutomateLights, assert_that):
    self.turn_lights_off()

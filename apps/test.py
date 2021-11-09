from appdaemon_testing.pytest import automation_fixture
from light_automation import AutomateLights

@automation_fixture(AutomateLights)
def automate_lights(given_that):
  automate_lights = AutomateLights(None,None,None)
  automate_lights.initialize()
  given_that.mock_functions_are_cleared()
  given_that.passed_arg('sensor').is_set_to('binary_sensor.motion_sensor_hallway')
  given_that.passed_arg('lights').is_set_to('light.hallway_lights')
  given_that.passed_arg('timer_on_to_dim').is_set_to('7')
  given_that.passed_arg('timer_dim_to_off').is_set_to('3')
  given_that.passed_arg('brightness_on').is_set_to('100')
  given_that.passed_arg('brightness_dim').is_set_to('33')
  return automate_lights
  
def test_motion_activates_light(given_that, automate_lights, assert_that):
    automate_lights.turnLightsOn()
    assert_that(automate_lights.args["lights"]).was.turned_on()
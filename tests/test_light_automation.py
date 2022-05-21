from unittest import mock

from appdaemon_testing.pytest import automation_fixture
from apps.light_automation import AutomateLights


# TODO TMN: Add more tests.


def test_callbacks_are_registered(hass_driver, light_automation: AutomateLights):
    listen_state = hass_driver.get_mock("listen_state")
    listen_state.assert_has_calls(
        [
            mock.call(
                light_automation.turn_lights_on,
                "binary_sensor.motion_sensor_small_bathroom",
                new="on",
                old="off",
            ),
            mock.call(
                light_automation.dim_lights,
                "binary_sensor.motion_sensor_small_bathroom",
                new="off",
                old="on",
                duration=300,
            ),
        ]
    )


def test_lights_are_turned_on_when_motion_detected(
    hass_driver, light_automation: AutomateLights
):
    with hass_driver.setup():
        hass_driver.set_state("binary_sensor.motion_sensor_small_bathroom", "off")
        hass_driver.set_state("sensor.daylight", "nadir")

    hass_driver.set_state("binary_sensor.motion_sensor_small_bathroom", "on")

    turn_on = hass_driver.get_mock("turn_on")
    assert turn_on.call_count == 1
    turn_on.assert_called_once_with("light.small_bathroom_lights", brightness_pct=5)


@automation_fixture(
    AutomateLights,
    args={
        "lights": [
            {
                "name": "light.small_bathroom_lights",
                "brightness_on": 100,
                "brightness_dim": 33,
                "brightness_on_night_start": 66,
                "brightness_dim_night_start": 20,
                "brightness_on_nadir": 5,
                "brightness_dim_nadir": 5,
                "brightness_on_night_end": 25,
                "brightness_dim_night_end": 5,
            }
        ],
        "timer_on_to_dim": 300,
        "timer_dim_to_off": 5,
        "timer_manual_mode_off": 900,
        "sensor": "binary_sensor.motion_sensor_small_bathroom",
        "sensor_activate_value": "on",
        "sensor_deactivate_value": "off",
        "button_mac": "28:6d:97:00:01:11:6d:c7",
    },
)
def light_automation() -> AutomateLights:
    pass


# def test_callbacks_are_registered(hass_driver, light_automation: AutomateLights):
#     # listen_state = hass_driver.get_mock("listen_state")
#     # listen_state.assert_called_once_with(
#     # light_automation.turn_lights_on, "binary_sensor.motion_sensor_small_bathroom"
#     # )
#     pass


# @automation_fixture(AutomateLights(hass.Hass))
# def light_automation(given_that):
#     light_automation = AutomateLights(hass.Hass)
#     light_automation.initialize()
#     given_that.mock_functions_are_cleared()
#     given_that.passed_arg("sensor").is_set_to("binary_sensor.motion_sensor_hallway")
#     given_that.passed_arg("lights").is_set_to("light.hallway_lights")
#     given_that.passed_arg("timer_on_to_dim").is_set_to("7")
#     given_that.passed_arg("timer_dim_to_off").is_set_to("3")
#     given_that.passed_arg("brightness_on").is_set_to("100")
#     given_that.passed_arg("brightness_dim").is_set_to("33")
#     return light_automation


# def test_motion_activates_light(given_that, light_automation, assert_that):
#     light_automation.turnLightsOn()
#     assert_that(light_automation.args["lights"]).was.turned_on()


# def test_motion_turns_light_on(self, light_automation: AutomateLights, assert_that):
#     self.turn_lights_off()

from appdaemontestframework import automation_fixture
from apps.light_automation import AutomateLights


# TODO TMN: Add more tests
# TODO TMN:  - Different rooms and times of day.
# TODO TMN:  - Test of listen_state/listen_event being called at the correct times.
# TODO TMN:  - Better end-to-end testing - e.g. fix light_automation._button_event problems with recursive run_in's.
# TODO TMN: Extract magic numbers/strings


@automation_fixture(AutomateLights)
def light_automation_small_bathroom_nadir(given_that):
    # Passed parameters
    given_that.passed_arg("lights").is_set_to(
        [
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
        ]
    )
    given_that.passed_arg("timer_on_to_dim").is_set_to(300)
    given_that.passed_arg("timer_dim_to_off").is_set_to(5)
    given_that.passed_arg("timer_manual_mode_off").is_set_to(900)
    given_that.passed_arg("sensor").is_set_to(
        "binary_sensor.motion_sensor_small_bathroom"
    )
    given_that.passed_arg("sensor_activate_value").is_set_to("on")
    given_that.passed_arg("sensor_deactivate_value").is_set_to("off")
    given_that.passed_arg("button_mac").is_set_to("28:6d:97:00:01:11:6d:c7")

    # Initial conditions
    given_that.state_of("sensor.daylight").is_set_to("nadir")
    given_that.state_of("binary_sensor.motion_sensor_small_bathroom").is_set_to("on")


def test_turn_on_small_bathroom_nadir(
    light_automation_small_bathroom_nadir, assert_that, given_that
):
    light_automation_small_bathroom_nadir.turn_lights_on(None, None, None, None, None)
    assert_that("light.small_bathroom_lights").was.turned_on(brightness_pct=5)


def test_turn_off_small_bathroom_nadir(
    light_automation_small_bathroom_nadir, assert_that, time_travel
):
    light_automation_small_bathroom_nadir.dim_lights(None, None, None, None, None)
    assert_that("light.small_bathroom_lights").was.turned_on(brightness_pct=5)
    time_travel.fast_forward(4).seconds()
    assert_that("light.small_bathroom_lights").was_not.turned_off()
    time_travel.fast_forward(1).seconds()
    assert_that("light.small_bathroom_lights").was.turned_off()


def test_manual_mode_turn_on_small_bathroom_nadir(
    light_automation_small_bathroom_nadir, assert_that, given_that, time_travel
):
    assert_that("light.small_bathroom_lights").was_not.turned_on(brightness_pct=5)
    light_automation_small_bathroom_nadir._set_manual_mode({'value': True})
    light_automation_small_bathroom_nadir.turn_lights_on(None, None, None, None, None)
    assert_that("light.small_bathroom_lights").was_not.turned_on(brightness_pct=5)


def test_manual_mode_turn_off_small_bathroom_nadir(
    light_automation_small_bathroom_nadir, assert_that, time_travel, given_that
):
    light_automation_small_bathroom_nadir.turn_lights_on(None, None, None, None, None)
    assert_that("light.small_bathroom_lights").was.turned_on(brightness_pct=5)
    given_that.mock_functions_are_cleared()
    light_automation_small_bathroom_nadir._set_manual_mode({'value': True})
    light_automation_small_bathroom_nadir.dim_lights(None, None, None, None, None)
    assert_that("light.small_bathroom_lights").was_not.turned_on(brightness_pct=5)
    time_travel.fast_forward(10).seconds()
    assert_that("light.small_bathroom_lights").was_not.turned_off()

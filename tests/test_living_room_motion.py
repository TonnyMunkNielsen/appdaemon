from unittest import mock

from appdaemon_testing.pytest import automation_fixture
from apps.living_room_motion import LivingRoomMotion


def test_callbacks_are_registered(hass_driver, living_room_motion: LivingRoomMotion):
    listen_state = hass_driver.get_mock("listen_state")
    listen_state.assert_called_once_with(
        living_room_motion.on_motion_detected,
        "binary_sensor.motion_detected",
        old="off",
        new="on",
    )


def test_lights_are_turned_on_when_motion_detected(
    hass_driver, living_room_motion: LivingRoomMotion
):
    with hass_driver.setup():
        hass_driver.set_state("binary_sensor.motion_detected", "off")
        hass_driver.set_state("sensor.daylight", "nadir")

    hass_driver.set_state("binary_sensor.motion_detected", "on")

    turn_on = hass_driver.get_mock("turn_on")
    assert turn_on.call_count == 3
    turn_on.assert_has_calls(
        [
            mock.call("light.1", brightness_pct=None),
            mock.call("light.2", brightness_pct=None),
            mock.call("light.3", brightness_pct=None),
        ]
    )


@automation_fixture(
    LivingRoomMotion,
    args={
        "motion_entity": "binary_sensor.motion_detected",
        "lights": [
            {"name": "light.1"},
            {"name": "light.2"},
            {"name": "light.3"},
        ],
        "sensor_activate_value": "on",
        "sensor_deactivate_value": "off",
        "timer_on_to_dim": 5,
        "button_mac": "dsadsad"
    },
)
def living_room_motion() -> LivingRoomMotion:
    pass

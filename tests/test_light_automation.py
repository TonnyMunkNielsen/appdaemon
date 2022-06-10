from appdaemontestframework import automation_fixture
from apps.light_automation import AutomateLights

# EntityIds
ENTITY_ID_LIGHT_SMALL_BATHROOM = "light.small_bathroom_lights"
ENTITY_ID_MOTION_SENSOR_SMALL_BATHROOM = "binary_sensor.motion_sensor_small_bathroom"
ENTITY_ID_SENSOR_DAYLIGHT = "sensor.daylight"

# String constants
STRING_ON = "on"
STRING_OFF = "off"
STRING_NADIR = "nadir"
STRING_BUTTON_MAC = "28:6d:97:00:01:11:6d:c7"
STRING_OTHER_BUTTON_MAC = "29:6d:97:00:01:11:6d:c7"
STRING_OTHER_ENTITY_ID = "other.entity.id"
STRING_DECONZ_EVENT_NAME = "deconz_event"
STRING_BUTTON_SINGLE_VALUE = "1001"
STRING_BUTTON_HELD_VALUE = "1002"
STRING_BUTTON_DOUBLE_VALUE = "1004"

# Integer constants
INT_SECONDS_DIM_TO_OFF_SMALL_BATHROOM = 5
INT_SECONDS_ON_TO_DIM_SMALL_BATHROOM = 300
INT_SECONDS_MANUAL_MODE_OFF_SMALL_BATHROOM = 900
INT_DIM_BRIGHTNESS_NADIR_SMALL_BATHROOM = 5
INT_ON_BRIGHTNESS_NADIR_SMALL_BATHROOM = 5

# Dictionary constants
DICT_VALUE_TRUE = {"value": True}
DICT_VALUE_FALSE = {"value": False}

# TODO TMN: Add more tests
# TODO TMN:  - Different rooms and times of day.
# TODO TMN:  - Better end-to-end testing 
# TODO TMN:    - e.g. fix light_automation._button_event problems with recursive run_in's.


@automation_fixture(AutomateLights)
def light_automation_small_bathroom_nadir(given_that):
    # Passed parameters
    given_that.passed_arg("lights").is_set_to(
        [
            {
                "name": ENTITY_ID_LIGHT_SMALL_BATHROOM,
                "brightness_on": 100,
                "brightness_dim": 33,
                "brightness_on_night_start": 66,
                "brightness_dim_night_start": 20,
                "brightness_on_nadir": INT_ON_BRIGHTNESS_NADIR_SMALL_BATHROOM,
                "brightness_dim_nadir": INT_DIM_BRIGHTNESS_NADIR_SMALL_BATHROOM,
                "brightness_on_night_end": 25,
                "brightness_dim_night_end": 5,
            }
        ]
    )
    given_that.passed_arg("timer_on_to_dim").is_set_to(
        INT_SECONDS_ON_TO_DIM_SMALL_BATHROOM
    )
    given_that.passed_arg("timer_dim_to_off").is_set_to(
        INT_SECONDS_DIM_TO_OFF_SMALL_BATHROOM
    )
    given_that.passed_arg("timer_manual_mode_off").is_set_to(
        INT_SECONDS_MANUAL_MODE_OFF_SMALL_BATHROOM
    )
    given_that.passed_arg("sensor").is_set_to(ENTITY_ID_MOTION_SENSOR_SMALL_BATHROOM)
    given_that.passed_arg("sensor_activate_value").is_set_to(STRING_ON)
    given_that.passed_arg("sensor_deactivate_value").is_set_to(STRING_OFF)
    given_that.passed_arg("button_mac").is_set_to(STRING_BUTTON_MAC)

    # Initial conditions
    given_that.state_of(ENTITY_ID_SENSOR_DAYLIGHT).is_set_to(STRING_NADIR)
    given_that.state_of(ENTITY_ID_MOTION_SENSOR_SMALL_BATHROOM).is_set_to(STRING_ON)


# LIGHT TESTS #
def test_turn_on_small_bathroom_nadir(
    light_automation_small_bathroom_nadir, assert_that
):
    light_automation_small_bathroom_nadir.turn_lights_on(None, None, None, None, None)
    assert_that(ENTITY_ID_LIGHT_SMALL_BATHROOM).was.turned_on(
        brightness_pct=INT_ON_BRIGHTNESS_NADIR_SMALL_BATHROOM
    )


def test_turn_off_small_bathroom_nadir(
    light_automation_small_bathroom_nadir, assert_that, time_travel
):
    light_automation_small_bathroom_nadir.dim_lights(None, None, None, None, None)
    assert_that(ENTITY_ID_LIGHT_SMALL_BATHROOM).was.turned_on(
        brightness_pct=INT_ON_BRIGHTNESS_NADIR_SMALL_BATHROOM
    )
    time_travel.fast_forward(INT_SECONDS_DIM_TO_OFF_SMALL_BATHROOM - 1).seconds()
    assert_that(ENTITY_ID_LIGHT_SMALL_BATHROOM).was_not.turned_off()
    time_travel.fast_forward(1).seconds()
    assert_that(ENTITY_ID_LIGHT_SMALL_BATHROOM).was.turned_off()


def test_manual_mode_should_not_turn_on_small_bathroom_nadir(
    light_automation_small_bathroom_nadir, assert_that
):
    light_automation_small_bathroom_nadir._set_manual_mode(DICT_VALUE_TRUE)
    light_automation_small_bathroom_nadir.turn_lights_on(None, None, None, None, None)
    assert_that(ENTITY_ID_LIGHT_SMALL_BATHROOM).was_not.turned_on(
        brightness_pct=INT_ON_BRIGHTNESS_NADIR_SMALL_BATHROOM
    )


def test_manual_mode_should_not_turn_off_small_bathroom_nadir(
    light_automation_small_bathroom_nadir, assert_that, time_travel
):
    light_automation_small_bathroom_nadir._set_manual_mode(DICT_VALUE_TRUE)
    light_automation_small_bathroom_nadir.dim_lights(None, None, None, None, None)
    assert_that(ENTITY_ID_LIGHT_SMALL_BATHROOM).was_not.turned_on(
        brightness_pct=INT_DIM_BRIGHTNESS_NADIR_SMALL_BATHROOM
    )
    time_travel.fast_forward(INT_SECONDS_DIM_TO_OFF_SMALL_BATHROOM + 1).seconds()
    assert_that(ENTITY_ID_LIGHT_SMALL_BATHROOM).was_not.turned_off()


def test_manual_mode_deactivate_should_not_turn_off_small_bathroom_nadir(
    light_automation_small_bathroom_nadir, assert_that, time_travel, given_that
):
    light_automation_small_bathroom_nadir.turn_lights_on(None, None, None, None, None)
    given_that.mock_functions_are_cleared()
    light_automation_small_bathroom_nadir._set_manual_mode(DICT_VALUE_TRUE)
    time_travel.fast_forward(INT_SECONDS_ON_TO_DIM_SMALL_BATHROOM + 1).seconds()
    assert_that(ENTITY_ID_LIGHT_SMALL_BATHROOM).was_not.turned_on(
        brightness_pct=INT_DIM_BRIGHTNESS_NADIR_SMALL_BATHROOM
    )


# LISTEN STATE TESTS #
# TODO TMN: Add test that we do not listen to states if manual mode is on.
# TODO TMN: This is currently not the case, so implement with TDD.
def test_listen_state_motion_off(light_automation_small_bathroom_nadir, assert_that):
    assert_that(light_automation_small_bathroom_nadir).listens_to.state(
        ENTITY_ID_MOTION_SENSOR_SMALL_BATHROOM,
        old=STRING_ON,
        new=STRING_OFF,
        duration=INT_SECONDS_ON_TO_DIM_SMALL_BATHROOM,
    ).with_callback(light_automation_small_bathroom_nadir.dim_lights)


def test_listen_state_motion_on(light_automation_small_bathroom_nadir, assert_that):
    assert_that(light_automation_small_bathroom_nadir).listens_to.state(
        ENTITY_ID_MOTION_SENSOR_SMALL_BATHROOM,
        old=STRING_OFF,
        new=STRING_ON,
    ).with_callback(light_automation_small_bathroom_nadir.turn_lights_on)


def test_listen_state_motion_on_other_motion_sensor(
    light_automation_small_bathroom_nadir, assert_that
):
    try:
        assert_that(light_automation_small_bathroom_nadir).listens_to.state(
            STRING_OTHER_ENTITY_ID,
            old=STRING_OFF,
            new=STRING_ON,
        ).with_callback(light_automation_small_bathroom_nadir.turn_lights_on)
        assert False  # Exception is expected to be raised, if not the test fails.
    except AssertionError as e:  # Must be AssertionError
        if "call not found" not in str(e):
            raise e  # Exception is re-raised if it does not have "call not found" in its message.


def test_listen_state_motion_on_lights_on(
    light_automation_small_bathroom_nadir, assert_that
):
    light_automation_small_bathroom_nadir.turn_lights_on(None, None, None, None, None)
    try:
        assert_that(light_automation_small_bathroom_nadir).listens_to.state(
            ENTITY_ID_MOTION_SENSOR_SMALL_BATHROOM,
            old=STRING_OFF,
            new=STRING_ON,
        ).with_callback(light_automation_small_bathroom_nadir.turn_lights_on)
        assert False  # Exception is expected to be raised, if not the test fails.
    except AssertionError as e:  # Must be AssertionError
        if "call not found" not in str(e):
            raise e  # Exception is re-raised if it does not have "call not found" in its message.


def test_listen_state_motion_off_lights_on(
    light_automation_small_bathroom_nadir, assert_that
):
    light_automation_small_bathroom_nadir.turn_lights_on(None, None, None, None, None)
    assert_that(light_automation_small_bathroom_nadir).listens_to.state(
        ENTITY_ID_MOTION_SENSOR_SMALL_BATHROOM,
        old=STRING_ON,
        new=STRING_OFF,
        duration=INT_SECONDS_ON_TO_DIM_SMALL_BATHROOM,
    ).with_callback(light_automation_small_bathroom_nadir.dim_lights)


def test_listen_state_motion_on_lights_off(
    light_automation_small_bathroom_nadir, assert_that
):
    light_automation_small_bathroom_nadir.turn_lights_off(None)
    assert_that(light_automation_small_bathroom_nadir).listens_to.state(
        ENTITY_ID_MOTION_SENSOR_SMALL_BATHROOM,
        old=STRING_OFF,
        new=STRING_ON,
    ).with_callback(light_automation_small_bathroom_nadir.turn_lights_on)


def test_listen_state_motion_off_lights_off(
    light_automation_small_bathroom_nadir, assert_that, time_travel, given_that
):
    light_automation_small_bathroom_nadir.turn_lights_off(None)
    try:
        assert_that(light_automation_small_bathroom_nadir).listens_to.state(
            ENTITY_ID_MOTION_SENSOR_SMALL_BATHROOM,
            old=STRING_ON,
            new=STRING_OFF,
            duration=INT_SECONDS_ON_TO_DIM_SMALL_BATHROOM,
        ).with_callback(light_automation_small_bathroom_nadir.dim_lights)
        assert False  # Exception is expected to be raised, if not the test fails.
    except AssertionError as e:  # Must be AssertionError
        if "call not found" not in str(e):
            raise e  # Exception is re-raised if it does not have "call not found" in its message.


# LISTEN EVENT TESTS#
def test_listen_event(
    light_automation_small_bathroom_nadir, assert_that
):
    assert_that(light_automation_small_bathroom_nadir).listens_to.event(
        STRING_DECONZ_EVENT_NAME,
        value=STRING_BUTTON_SINGLE_VALUE,
        unique_id=STRING_BUTTON_MAC,
    ).with_callback(light_automation_small_bathroom_nadir._button_event)


def test_listen_event_other_button_mac(
    light_automation_small_bathroom_nadir, assert_that
):
    light_automation_small_bathroom_nadir.turn_lights_off(None)
    try:
        assert_that(light_automation_small_bathroom_nadir).listens_to.event(
            STRING_DECONZ_EVENT_NAME,
            value=STRING_BUTTON_SINGLE_VALUE,
            unique_id=STRING_OTHER_BUTTON_MAC,
        ).with_callback(light_automation_small_bathroom_nadir._button_event)
        assert False  # Exception is expected to be raised, if not the test fails.
    except AssertionError as e:  # Must be AssertionError
        if "call not found" not in str(e):
            raise e  # Exception is re-raised if it does not have "call not found" in its message.


def test_listen_event_double_click(
    light_automation_small_bathroom_nadir, assert_that
):
    light_automation_small_bathroom_nadir.turn_lights_off(None)
    try:
        assert_that(light_automation_small_bathroom_nadir).listens_to.event(
            STRING_DECONZ_EVENT_NAME,
            value=STRING_BUTTON_DOUBLE_VALUE,
            unique_id=STRING_BUTTON_MAC,
        ).with_callback(light_automation_small_bathroom_nadir._button_event)
        assert False  # Exception is expected to be raised, if not the test fails.
    except AssertionError as e:  # Must be AssertionError
        if "call not found" not in str(e):
            raise e  # Exception is re-raised if it does not have "call not found" in its message.
        
def test_listen_event_held(
    light_automation_small_bathroom_nadir, assert_that
):
    light_automation_small_bathroom_nadir.turn_lights_off(None)
    try:
        assert_that(light_automation_small_bathroom_nadir).listens_to.event(
            STRING_DECONZ_EVENT_NAME,
            value=STRING_BUTTON_HELD_VALUE,
            unique_id=STRING_BUTTON_MAC,
        ).with_callback(light_automation_small_bathroom_nadir._button_event)
        assert False  # Exception is expected to be raised, if not the test fails.
    except AssertionError as e:  # Must be AssertionError
        if "call not found" not in str(e):
            raise e  # Exception is re-raised if it does not have "call not found" in its message.

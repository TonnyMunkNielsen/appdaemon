import hassapi as hass
import datetime
import distutils.util


class AutomateLights(hass.Hass):
    on_off_timer = None
    manual_mode_timer = None
    on = None
    manual_mode = False

    def initialize(self):
        self.log(self.args["sensor"] + ": Sensor has been turned " +
                 format(self.get_state(self.args["sensor"])))
        if(self.on is None or self.on is False):
            self.listen_state(self.turn_lights_on,
                              self.args["sensor"], new=self.args["sensor_activate_value"], old=self.args["sensor_deactivate_value"])
        if(self.on is None or self.on is True):
            self.listen_state(
                self.dim_lights, self.args["sensor"], new=self.args["sensor_deactivate_value"], old=self.args["sensor_activate_value"], duration=self.args["timer_on_to_dim"])
        try:
            # 1001: held, 1002: push, 1004: double.
            self.listen_event(self._button_event, event="deconz_event",
                              value="1001", unique_id=self.args["button_mac"])
        except KeyError:
            pass

    def turn_lights_off(self, kwargs):
        for light in self.args['lights']:
            self.log(light.get("name") + ": Lights have been dimmed for " +
                     str(self.args["timer_dim_to_off"]) + " seconds, turning off")
            self.turn_off(light.get("name"))
        self.on = False

    def turn_lights_on(self, entity, attribute, old, new, kwargs):
        if(not self.manual_mode):
            self._cancel_timer(self.on_off_timer)
            __daylight_state = self.get_state('sensor.daylight')
            self.log("Daylight sensor state is " + __daylight_state)
            for light in self.args['lights']:
                __brightness = self._get_on_brightness(__daylight_state, light)
                # Log entry
                self.log(light.get("name") + ": Lights has been turned on. Brightness: " +
                         str(__brightness))
                # Action
                self.turn_on(light.get("name"),
                             brightness_pct=__brightness)
            self.on = True

    def dim_lights(self, entity, attribute, old, new, kwargs):
        if(not self.manual_mode):
            self._cancel_timer(self.on_off_timer)
            self.log(self.args["sensor"] + ": Sensor has been off for " +
                     str(self.args["timer_on_to_dim"]) + " seconds.")
            __daylight_state = self.get_state('sensor.daylight')
            for light in self.args['lights']:
                __brightness = self._get_dim_brightness(
                    __daylight_state, light)
                # Log entries
                self.log(light.get("name") + ": Lights has been dimmed. Brightness: " +
                         str(__brightness))
                self.log(light.get("name") + ": Turning lights off in " +
                         str(self.args["timer_dim_to_off"]) + " seconds.")
                # Action
                self.turn_on(light.get("name"),
                             brightness_pct=__brightness)
            self.on_off_timer = self.run_in(
                self.turn_lights_off, self.args["timer_dim_to_off"])

    def _get_on_brightness(self, daylight_state, light):
        __brightness_type = "on"
        return self._get_brightness(daylight_state, light, __brightness_type)

    def _get_dim_brightness(self, daylight_state, light):
        __brightness_type = "dim"
        return self._get_brightness(daylight_state, light, __brightness_type)

    def _get_brightness(self, daylight_state, light, brightness_type):
        # Validate brightness type.
        self._validate_brightness_type(brightness_type)
        # Default brightness - daytime.
        __brightness = light.get("brightness_{}".format(brightness_type))
        # If it's night, set brightness appripriately.
        if(daylight_state == "nadir" and light.get("brightness_{}_nadir".format(brightness_type)) is not None):
            __brightness = light.get(
                "brightness_{}_nadir".format(brightness_type))
        elif(daylight_state == "night_start" and light.get("brightness_{}_night_start".format(brightness_type)) is not None):
            __brightness = light.get(
                "brightness_{}_night_start".format(brightness_type))
        elif(daylight_state == "night_end" and light.get("brightness_{}_night_end".format(brightness_type)) is not None):
            __brightness = light.get(
                "brightness_{}_night_end".format(brightness_type))
        return __brightness

    def _validate_brightness_type(self, type):
        if(type != "on" and type != "dim"):
            raise ValueError("Unsupported brightness type: " + type)

    def _cancel_timer(self, handle):
        if(handle != None and self.timer_running(handle)):
            self.log("Active timer found, cancelling active timer.")
            self.cancel_timer(handle)

    def _button_event(self, event, data, kwargs):
        self.log("Button with MAC " +
                 self.args["button_mac"] + ": Button pressed.")
        # Toggling manual_mode.
        self.manual_mode = not self.manual_mode
        self._cancel_timer(self.on_off_timer)
        # self.cancelTimer(self.manual_mode_timer)
        # Call flashWarning if manual mode is true
        if(self.manual_mode):
            self.on = None
            self.log("Manual mode has been turned on, calling flashWarning.")
            self.flashcount = 0
            self.run_in(self._flash_warning, 1)
            # self.manual_mode_timer=self.run_in(self.setManualMode, int(
            # self.args["timer_manual_mode_off"]), value=False)

        if(not self.manual_mode and self.get_state(self.args["sensor"]) == 'on'):
            # TODO: Make this work, don't think it works?
            self.run_in(self.turn_lights_on, 1)

    # value = None --> Toggle manual mode.
    def _set_manual_mode(self, kwargs):
        if(kwargs["value"] == True):
            self.log("Setting manual mode from " + str(self.manual_mode) +
                     " to True.")
            self.manual_mode = True
        elif(kwargs["value"] == False):
            self.log("Setting manual mode from " + str(self.manual_mode) +
                     " to False.")
            self.manual_mode = False

    def _flash_warning(self, kwargs):
        for light in self.args['lights']:
            self.toggle(light.get("name"))
        self.flashcount += 1
        if self.flashcount < 4:
            self.run_in(self._flash_warning, 1)
            
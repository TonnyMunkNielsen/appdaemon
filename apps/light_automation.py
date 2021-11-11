import hassapi as hass
import datetime
import distutils.util


class AutomateLights(hass.Hass):
    on_off_timer = None
    manual_mode_timer = None
    on = None
    manual_mode = False

    def initialize(self):

        self.log("0Manual mode value: " + str(self.manual_mode))
        self.log(self.args["sensor"] + ": Sensor has been turned " +
                 format(self.get_state(self.args["sensor"])))
        if(self.on is None or self.on is False):
            self.listen_state(self.turnLightsOn,
                              self.args["sensor"], new=str(self.args["sensor_activate_value"]), old=str(self.args["sensor_deactivate_value"]))
        if(self.on is None or self.on is True):
            self.listen_state(
                self.dimLights, self.args["sensor"], new=self.args["sensor_deactivate_value"], old=self.args["sensor_activate_value"], duration=self.args["timer_on_to_dim"])
        try:
            # 1001: held, 1002: push, 1004: double.
            self.listen_event(self.buttonEvent, event="deconz_event",
                              value="1001", unique_id=self.args["button_mac"])
        except KeyError:
            pass
        self.log("2Manual mode value: " + str(self.manual_mode))

    def turnLightsOff(self, kwargs):
        for light in self.args['lights']:
            self.log("4Manual mode value: " + str(self.manual_mode))
            self.log(light.get("name") + ": Lights have been dimmed for " +
                     str(self.args["timer_dim_to_off"]) + " seconds, turning off")
            self.turn_off(light.get("name"))
        self.on = False

    def turnLightsOn(self, entity, attribute, old, new, kwargs):
        if(not self.manual_mode):
            self.log("5Manual mode value: " + str(self.manual_mode))
            self.cancelTimer(self.on_off_timer)
            for light in self.args['lights']:
                self.log(light.get("name") + ": Lights has been turned on. Brightness: " +
                         str(light.get("brightness_on")))
                self.turn_on(light.get("name"),
                             brightness_pct=light.get("brightness_on"))
            self.on = True

    def dimLights(self, entity, attribute, old, new, kwargs):
        if(not self.manual_mode):
            self.log("6Manual mode value: " + str(self.manual_mode))
            self.cancelTimer(self.on_off_timer)
            self.log(self.args["sensor"] + ": Sensor has been off for " +
                     str(self.args["timer_on_to_dim"]) + " seconds")
            for light in self.args['lights']:
                self.log(light.get("name") + ": Lights has been dimmed. Brightness: " +
                         str(light.get("brightness_dim")))
                self.log(light.get("name") + ": Turning lights off in " +
                         str(self.args["timer_dim_to_off"]) + " seconds.")
                self.turn_on(light.get("name"),
                             brightness_pct=light.get("brightness_dim"))
            self.on_off_timer = self.run_in(self.turnLightsOff, self.args["timer_dim_to_off"])

    def cancelTimer(self, handle):
        self.log("7Manual mode value: " + str(self.manual_mode))
        if(handle != None and self.timer_running(handle)):
            self.log("Active timer found, cancelling active timer.")
            self.cancel_timer(handle)

    def buttonEvent(self, event, data, kwargs):
        self.log("8Manual mode value: " + str(self.manual_mode))
        self.log("Button with MAC " + self.args["button_mac"] + ": Button pressed.")
        # Toggling manual_mode.
        self.manual_mode = not self.manual_mode
        self.cancelTimer(self.on_off_timer)
        # self.cancelTimer(self.manual_mode_timer)
        # Call flashWarning if manual mode is true
        if(self.manual_mode):
            self.on=None
            self.log("Manual mode has been turned on, calling flashWarning.")
            self.flashcount=0
            self.run_in(self.flashWarning, 1)
            # self.manual_mode_timer=self.run_in(self.setManualMode, int(
                # self.args["timer_manual_mode_off"]), value=False)

        if(not self.manual_mode and self.get_state(self.args["sensor"]) is 'on'):
            # TODO: Make this work, don't think it works?
            self.run_in(self.turnLightsOn, 1)

    # value = None --> Toggle manual mode.
    def setManualMode(self, kwargs):
        if(kwargs["value"] is True):
            self.log("Setting manual mode from " + str(self.manual_mode) + \
                     " to True.")
            self.manual_mode=True
        elif(kwargs["value"] is False):
            self.log("Setting manual mode from " + str(self.manual_mode) + \
                     " to False.")
            self.manual_mode=False

    def flashWarning(self, kwargs):
        self.log("9Manual mode value: " + str(self.manual_mode))
        for light in self.args['lights']:
            self.toggle(light.get("name"))
        self.flashcount += 1
        if self.flashcount < 4:
            self.run_in(self.flashWarning, 1)

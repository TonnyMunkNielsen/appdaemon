import hassapi as hass
import globals

class EventPublisher(hass.Hass):

    def initialize(self):
        __entity_id = self.args["sensor"]
        self.log(__entity_id + ": Sensor has been turned " + format(self.get_state(__entity_id)))
        self.listen_state(self.stateChangeEvent, __entity_id)

    def stateChangeEvent(self, entity, attribute, old, new, kwargs):
        if(new == 'on' and old == "off"):
            self.log(entity + ": Publishing 'turn on' event.")
            self.publishTurnOnEvent(entity, )
        elif(new == 'off' and old == 'on'):
            self.log(entity + ": Publishing 'turn off' event.")

    def publishTurnOnEvent(self, entity, state, kwargs):
        self.fire_event(globals.EVENT_STATE_CHANGE_ON, )

    def publishTurnOffEvent(self, entity, attribute, old, new, kwargs):
        
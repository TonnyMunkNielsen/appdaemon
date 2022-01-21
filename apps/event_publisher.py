import hassapi as hass
import globals

class EventPublisher(hass.Hass):

    def initialize(self):
        __entity_id = self.args["sensor"]
        self.log(__entity_id + ": Sensor has been turned " + format(self.get_state(__entity_id)))
        self.listen_state(self.stateChangeEvent, __entity_id)

    def stateChangeEvent(self, entity, attribute, old, new, kwargs):
        __event = None
        
        if(new == 'on' and old == "off"):
            self.log(entity + ": Publishing 'turn on' event.")
            __event = globals.EVENT_STATE_CHANGE_ON
        elif(new == 'off' and old == 'on'):
            self.log(entity + ": Publishing 'turn off' event.")
            __event = globals.EVENT_STATE_CHANGE_OFF
        
        self.publishEvent(entity, __event)

    def publishEvent(self, event, entity_id):
        if(event is not None):
            self.fire_event(event, entity_id=entity_id)
        else:
            self.warn(entity_id + ": PublishEvent was called with event = None.")
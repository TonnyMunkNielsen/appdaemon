import hassapi as hass
import globals

class EventHandler(hass.Hass):
    
    def initialize(self):
        __entity_id = self.args["entity_id"] # TODO: Refactor to use get_entity and align with Object Oriented design of Appdaemon.
        __event = self.args["event"]
        self.log(__entity_id + ": Event is being handled: " + __event)
        self.listen_event(self.handleEvent, __event, entity_id=__entity_id)

    def handleEvent(self, entity, attribute, old, new, kwargs):
        

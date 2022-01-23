import hassapi as hass
import globals


class EventHandler(hass.Hass):

    def initialize(self):
        # TODO: Refactor to use get_entity and align with Object Oriented design of Appdaemon.
        __entity_id = self.args["sensor"]
        __event = self.args["event"]
        self.log(__entity_id + ": Event is being handled: " + __event)
        self.listen_event(self.handle_event, __event, entity_id=__entity_id)

    def handle_event(self, event_name, data, kwargs):
        __device_id = self.args["device"]
        __device_type = extract_device_type(__device_id)
        if(__device_type == globals.DEVICE_TYPE_LIGHT):
            # handle_light_event
            if(event_name == globals.EVENT_STATE_CHANGE_ON):
                self.turn_on(__device_id)
            elif(event_name == globals.EVENT_STATE_CHANGE_OFF):
                self.turn_off(__device_id)
        else:
            raise NotImplementedError("No method to handle device type: " + __device_type)
    
    def handle_light_event(self, event_name, kwargs):



# device helpers
def extract_device_type(entity_id):
    __type = entity_id.split('.')[0]
    if(__type == "light"):
        return globals.DEVICE_TYPE_LIGHT
    elif(__type == "binary_sensor"):
        return globals.DEVICE_TYPE_BINARY_SENSOR
    else:
        raise ValueError("Unknown device type")

# event helpers
def extract_event_type(entity_id):
    __type = entity_id.split('.')[0]
    if(__type == "light"):
        return globals.DEVICE_TYPE_LIGHT
    elif(__type == "binary_sensor"):
        return globals.DEVICE_TYPE_BINARY_SENSOR
    else:
        raise ValueError("Unknown device type")
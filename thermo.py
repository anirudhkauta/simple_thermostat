#!/usr/bin/python
import web
import json

#The routes for the api calls
urls = (
    '/?', 'Index',
    '/thermostats/(\d+)/(\w+)/?', 'Thermostat',
    '/thermostats/?(\d+)?/?', 'Thermostat',
    '/thermostats/?', 'Thermostat',
)

#Thermostat items
thermostats = [
    {
        "id": 100,
        "name": "Living Room Thermostat",
        "current_temp": 65,
        "operating_mode": "heat",
        "cool_setPoint": 60,
        "heat_setPoint": 70,
        "fan_mode": "auto"
    },
    {
        "id": 101,
        "name": "Master Bedroom Thermostat",
        "current_temp": 65,
        "operating_mode": "heat",
        "cool_setPoint": 60,
        "heat_setPoint": 70,
        "fan_mode": "auto"
    }
]

#Thermostat settings
thermo_props = {"id","name","operating_mode","cool_setPoint","heat_setPoint","fan_mode"}
thermo_props_ro = {"id", "current_temp"}
operating_mode = {"cool", "heat", "off"}
fan_mode = {"off", "auto"}


#Index returns only 200 OK and does not accept any put or post requests
class Index:
    def GET(self):
        web.header('Content-Type', 'application/json')
        raise web.ok(data='200 OK')

#Thermostat that talks with the data
class Thermostat:

    #Checks if a value set is valid for the field
    def check_valid_value(self, thermo_property,setting_value):
        if thermo_property == 'operating_mode' and setting_value in operating_mode:
            return True
        elif thermo_property == 'fan_mode' and setting_value in fan_mode:
            return True
        elif (thermo_property == 'cool_setPoint' or thermo_property == 'heat_setPoint') and int(setting_value) <= 100 and int(setting_value) >= 30:
            return True

        return False

    #Returns the specific thermostat queried by id
    def get_thermostat(self, id):
        for thermostat in thermostats:
            if int(id) == thermostat['id']:
                return thermostat
        return None

    def GET(self, id = None, thermo_property = None):
        web.header('Content-Type', 'application/json')
        if id is None:
            return json.dumps(thermostats)

        info = self.get_thermostat(id)
        if info is None:
            raise web.notfound()

        if thermo_property is None:
            return json.dumps(info)

        return json.dumps({thermo_property: info[thermo_property]})

    def PUT(self, id = None, thermo_property = None):
        web.header('Content-Type', 'application/json')
        data = web.data()
        json_data = json.loads(data)

        if id is None or thermo_property is None:
            raise web.badrequest

        info = self.get_thermostat(id)
        if thermo_property in thermo_props_ro:
            raise web.forbidden
        if thermo_property not in thermo_props or not self.check_valid_value(thermo_property,json_data):
            raise web.badrequest()
        for thermostat in thermostats:
            if int(id) == thermostat['id']:
                thermostat[thermo_property] = json_data
                return json.dumps(thermostat)

        raise web.notfound()


app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()

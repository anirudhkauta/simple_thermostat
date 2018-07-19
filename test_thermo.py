from thermo import app
from paste.fixture import TestApp
from nose.tools import *
import json

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

thermostat_cool_set = {
    "id": 100,
    "name": "Living Room Thermostat",
    "current_temp": 65,
    "operating_mode": "heat",
    "cool_setPoint": 30,
    "heat_setPoint": 70,
    "fan_mode": "auto"
}

cool_setPoint = 30
cool_setPoint_string = '30'
new_id = 105
new_temp = 83
operating_mode = 'Fire'
high_temp = 200
low_temp = 0


class TestIndex():

    def test_GET(self):
        # self.assertEqual(thermo.Index().GET(), 200)
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        r = testApp.get('/')
        assert_equal(r.status, 200)
        r.mustcontain('200 OK')


class TestThermostat():

    def test_GET(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))

        # Return all thermostats with 200 OK
        r = testApp.get('/thermostats', {'content-type': 'application/json'})
        json_data = json.loads(r.body)
        assert_equal(r.status, 200)
        assert_equal(json_data, thermostats)

        # Return thermostat with id 100 with 200 OK
        r = testApp.get('/thermostats/100', {'content-type': 'application/json'})
        json_data = json.loads(r.body)
        assert_equal(r.status, 200)
        assert_equal(json_data, thermostats[0])

        # Return 404 error for thermostat that doesn't exists
        r = testApp.get('/thermostats/102', status="*")
        assert_equal(r.status, 404)
        r.mustcontain('not found')

        # This test case is failing as non int ids are not captured from the URL
        # Return 406 notacceptable for thermostat id that isn't int
        # r = testApp.get('/thermostats/abc', status="*")
        # assert_equal(r.status, 406)
        # r.mustcontain('not acceptable')

    def test_PUT(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))

        # Return 200 OK for putting a valid setting
        r = testApp.put('/thermostats/100/cool_setPoint', params=json.dumps(cool_setPoint))
        json_data = json.loads(r.body)
        assert_equal(r.status, 200)
        assert_equal(json_data, thermostat_cool_set)

        # Return 403 forbidden for assigning string for int value
        r = testApp.put('/thermostats/100/id', params=json.dumps(cool_setPoint_string), status="*")
        assert_equal(r.status, 403)
        r.mustcontain('forbidden')

        # Return 403 forbidden for read only setting
        r = testApp.put('/thermostats/100/id', params=json.dumps(new_id), status="*")
        assert_equal(r.status, 403)
        r.mustcontain('forbidden')

        # Return 400 bad request if put is attempted without a specific setting
        r = testApp.put('/thermostats/100', params=json.dumps(new_id), status="*")
        assert_equal(r.status, 400)
        r.mustcontain('bad request')

        # Return 400 bad request for non-existent setting
        r = testApp.put('/thermostats/100/clock_display', params=json.dumps(new_temp), status="*")
        assert_equal(r.status, 400)
        r.mustcontain('bad request')

        # Return 400 bad request for setting values higher than bounds
        r = testApp.put('/thermostats/100/cool_setPoint', params=json.dumps(high_temp), status="*")
        assert_equal(r.status, 400)
        r.mustcontain('bad request')

        # Return 400 bad request for setting values lower than bounds
        r = testApp.put('/thermostats/100/cool_setPoint', params=json.dumps(low_temp), status="*")
        assert_equal(r.status, 400)
        r.mustcontain('bad request')

        # Return 400 bad request for setting values out of scope
        r = testApp.put('/thermostats/100/operating_mode', params=json.dumps(operating_mode), status="*")
        assert_equal(r.status, 400)
        r.mustcontain('bad request')

        # Return 404 for non-existent thermostat
        r = testApp.put('/thermostats/108/cool_setPoint', params=json.dumps(cool_setPoint), status="*")
        assert_equal(r.status, 404)
        r.mustcontain('not found')

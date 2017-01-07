#!/usr/bin/env python

from datetime import datetime
from evohomeclient2 import EvohomeClient
from influxdb import InfluxDBClient
from utils import log
from utils import config

username = config.get('username', 'Honeywell')
password = config.get('password', 'Honeywell')
ec = EvohomeClient(username, password)

dbaddress = config.get('address', 'InfluxDB')
dbport = config.get('port', 'InfluxDB')
db = InfluxDBClient(dbaddress, dbport, 'root', 'root', 'energy')
db.create_database('energy')

for name, gateway in ec.locations[0].gateways.items():
    zones = gateway._control_systems[0].zones
    # gateway = client.locations[0].gateways['1885175']
    country = gateway.location.country.lower()
    city = gateway.location.city.lower()
    streetaddress = gateway.location.streetAddress.lower()
    street = streetaddress.rsplit(' ', 1)[0].replace(' ', '-')
    housenumber = streetaddress.rsplit(' ', 1)[1]

    for name, properties in zones.items():
        zone = name.lower()
        currenttemp = properties.temperatureStatus['temperature']
        targettemp = properties.heatSetpointStatus['targetTemperature']
        datapoint = [
            {'measurement': 'heating',
             'tags': {
                'country': country,
                'city': city,
                'street': street,
                'housenumber': housenumber,
                'zone': zone
             },
             'fields': {
                'currenttemperature': currenttemp,
                'targettemperature': targettemp
             },
             'time': datetime.utcnow()
             }
        ]
        db.write_points(datapoint)

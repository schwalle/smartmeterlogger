"""Smart Meter Logger

A simple tool to log smart electric meter values into an InfluxDB database.
The smart meter must use SML protocol over a serial connection.

Usage:
    smartmeterlogger.py [-c FILE | --influxconfig FILE] DEVICE

Options:
    -c File, --influxconfig FILE    InfluxDB configuration file in configperser format
                                    See https://github.com/influxdata/influxdb-client-python for details
    
    DEVICE                          Serial device used for getting SML messages from the smart electric meter
                                    
"""

import asyncio
from datetime import datetime
from functools import partial
from typing import Awaitable, Dict, List

import serial_asyncio
from docopt import docopt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi
from influxdb_client.domain.write_precision import WritePrecision
from smllib import SmlStreamReader
from smllib.sml_fields import SmlListEntry
from smllib.sml_frame import SmlFrame

from detail.helper import create_hex_dump, eprint
from detail.obis import ObisCode


class SmlFrameReceiver(asyncio.Protocol):

    def __init__(self, framehandler: Awaitable[SmlFrame]):
        super().__init__()

        self._smlstreamreader = SmlStreamReader()
        self._framehandler = framehandler

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)

    def data_received(self, data):        
        self._smlstreamreader.add(data)
        smlframe = self._smlstreamreader.get_frame()
        if smlframe is not None:                        
            self.transport.loop.create_task(self._framehandler(smlframe))
            self._smlstreamreader.clear()
                
    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

class Sml2InfluxHandler:

    def __init__(self, influx: InfluxDBClient, desired_obis: List[ObisCode], bucket: str, org: str, measurement: str) -> None:
        self._influxclient = influx
        self._write_api = influx.write_api()
        self._desired_obis = desired_obis
        self._bucket = bucket        
        self._org = org        
        self._measurement = measurement                
        pass


    async def __call__(self, smlframe: SmlFrame) -> None:
        get_first_smlentry_by_obis = lambda obis_code: next(smlentry for smlentry in smlframe.get_obis() if smlentry.obis == obis_code.obis)
        
        point = Point.measurement(self._measurement).time(datetime.utcnow())
        for oc, smlentry in ((oc, get_first_smlentry_by_obis(oc)) for oc in self._desired_obis):
            point.field(oc.name, smlentry.get_value())
    
        if len(point._fields) > 0:
            self._write_api.write(self._bucket,self._org, point)


def main(arguments):
    config_file = 'config.ini'
    if '-c' in arguments:
        config_file = arguments['-c']

    desired_obis_values = [ObisCode.ZAEHLERSTAND_TOTAL_BEZUG ,ObisCode.ZAEHLERSTAND_TOTAL_EINSPEISUNG]

    try:
        client = InfluxDBClient.from_config_file(config_file)
        loop = asyncio.get_event_loop()
        coro = serial_asyncio.create_serial_connection(
            loop, lambda: SmlFrameReceiver(Sml2InfluxHandler(client,desired_obis_values,'home','schwalle', 'mainelectricmeter')), arguments['DEVICE'], baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0)
        loop.run_until_complete(coro)
        loop.run_forever()
        loop.close()
        client.close()
    finally:
        pass

if __name__ == "__main__":
    arguments = docopt(__doc__, version='1.0')
    main(arguments)

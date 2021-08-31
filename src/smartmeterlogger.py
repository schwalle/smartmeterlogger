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
import serial_asyncio

from typing import Awaitable, List
from docopt import docopt
from datetime import datetime
from smllib import SmlStreamReader
from smllib.sml_fields import SmlListEntry
from smllib.sml_frame import SmlFrame
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi
from influxdb_client.domain.write_precision import WritePrecision

from detail.obis import Obis, ObisCode
from detail.helper import create_hex_dump, eprint

class SmlFrameReceiver(asyncio.Protocol):

    def __init__(self, framehandler: Awaitable[SmlFrame]):
        super().__init__()

        self._smlstreamreader = SmlStreamReader()
        self._framehandler = framehandler

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)

    def data_received(self, data):
        print('data received', repr(data))        
        self._smlstreamreader.add(data)
        smlframe = self._smlstreamreader.get_frame()
        if smlframe is not None:                        
            self.transport.loop.create_task(self._framehandler(smlframe))
            self._smlstreamreader.clear()
        else:
            print(f"Current buffer length {len(self._smlstreamreader.bytes)}")
            print(create_hex_dump(self._smlstreamreader.bytes))

    def extract_desired_values(self, smlframe: SmlFrame):
        extracted_values = {}
        sml_values: List[SmlListEntry] = list(filter(lambda smlentry: smlentry.obis in [o.obis for o in self.desired_obis]), smlframe.get_obis())
        for value in sml_values:
            extracted_values[ObisCode.by_obis(
                    value.obis)] = value.get_value()
                
        return extracted_values

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

class Sml2Influx:

    def __init__(self, influx: InfluxDBClient) -> None:
        self._influxclient = influx
        pass


    async def __call__(self, smlframe: SmlFrame) -> None:
        for smlentry in smlframe.get_obis():
            print(smlentry.format_msg())
        pass

    def __repr__(self) -> str:
        return f'Sml2Influx(influx={self._influxclient})'
        
    

async def insertValues(values, influxwriteapi: WriteApi):
    point = Point('mainelectricmeter')
    for oc, v in values:
        point.field(oc.name, v)
    point.time(int(datetime.now().timestamp()), write_precision=WritePrecision.S)
    influxwriteapi.write('electricmeter', org='schwalle', record=point)

def createInfluxInserter(client: InfluxDBClient):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return lambda values : insertValues(values, write_api)

def main(arguments):
    config_file = 'config.ini'
    if '-c' in arguments:
        config_file = arguments['-c']

    desired_obis_values = [ObisCode.TOTAL_ZAEHLERSTAND,ObisCode.AKTUELLE_WIRKLEISTUNG, 
                        ObisCode.WIRKLEISTUNG_L1, ObisCode.WIRKLEISTUNG_L2, ObisCode.WIRKLEISTUNG_L3]

    try:
        client = InfluxDBClient.from_config_file(config_file)
        loop = asyncio.get_event_loop()
        coro = serial_asyncio.create_serial_connection(
            loop, lambda: SmlFrameReceiver(Sml2Influx(client)), arguments['DEVICE'], baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0)
        loop.run_until_complete(coro)
        loop.run_forever()
        loop.close()
        client.close()
    finally:
        pass

if __name__ == "__main__":
    arguments = docopt(__doc__, version='1.0')
    main(arguments)
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

from typing import Callable, Dict, List, Any
from docopt import docopt
from datetime import datetime
from rx.core.typing import MapperIndexed
from smllib import SmlStreamReader
from smllib.sml_fields import SmlListEntry
from smllib.sml_frame import SmlFrame
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi
from influxdb_client.domain.write_precision import WritePrecision

from detail.obis import Obis, ObisCode
from detail.helper import create_hex_dump, eprint

class SmlValueReceiver(asyncio.Protocol):

    def __init__(self, desired_obis: List[ObisCode], value_receiver: Callable[[dict], Any]):
        super().__init__()

        self.smlstreamreader = SmlStreamReader()
        self.desired_obis = desired_obis
        self.value_receiver = value_receiver

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)

    def data_received(self, data):
        print('data received', repr(data))        
        self.smlstreamreader.add(data)
        smlframe = self.smlstreamreader.get_frame()
        if smlframe is not None:
            self.dump_sml_frame(smlframe)
            self.smlstreamreader.clear()
            pass
            extracted_values = self.extract_desired_values(smlframe)
            self.value_receiver(extracted_values)
        else:
            print(f"Current buffer length {len(self.smlstreamreader.bytes)}")
            print(create_hex_dump(self.smlstreamreader.bytes))

    def extract_desired_values(self, smlframe):
        extracted_values = {}
        sml_values: List[SmlListEntry] = list(filter(
                lambda smlentry: smlentry.obis in [o.obis for o in self.desired_obis]), smlframe.get_obis())
        for value in sml_values:
            extracted_values[ObisCode.by_obis(
                    value.obis)] = value.get_value()
                
        return extracted_values

    def dump_sml_frame(self, smlframe: SmlFrame):
        for msg in smlframe.parse_frame():
            print(msg.format_msg())

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')

def insertValues(values: Dict[ObisCode, Any], influxwriteapi: WriteApi):
    point = Point('electricmeter')
    point._tags.update((oc.name, v) for oc, v in values)
    point.time(int(datetime.now().timestamp()), write_precision=WritePrecision.S)
    influxwriteapi.write('', record=point)

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
            loop, lambda: SmlValueReceiver(desired_obis_values, createInfluxInserter(client)), arguments['DEVICE'], baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0)
        loop.run_until_complete(coro)
        loop.run_forever()
        loop.close()
        client.close()
    finally:
        pass

if __name__ == "__main__":
    arguments = docopt(__doc__, version='1.0')
    main(arguments)


from src.detail.obis import ObisCode

def test_get_obis_string():
    assert( ObisCode.ZAEHLERSTAND_TOTAL_BEZUG.obis == '0100010800ff')

def test_get_obis_description():
    assert( ObisCode.ZAEHLERSTAND_TOTAL_BEZUG.description == 'Zählerstand Total Bezug')

def test_get_obiscode_by_obis():
    assert(ObisCode.ZAEHLERSTAND_TOTAL_BEZUG == ObisCode.by_obis('0100010800ff'))

def test_get_obiscode_by_description():
    assert( ObisCode.ZAEHLERSTAND_TOTAL_BEZUG == ObisCode.by_description('Zählerstand Total Bezug'))
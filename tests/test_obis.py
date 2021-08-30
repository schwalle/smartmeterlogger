

from src.detail.obis import ObisCode

def test_get_obis_string():
    assert( ObisCode.AKTUELLE_WIRKLEISTUNG.obis == '0100100700ff')

def test_get_obis_description():
    assert( ObisCode.AKTUELLE_WIRKLEISTUNG.description == 'aktuelle Wirkleistung')

def test_get_obiscode_by_obis():
    assert(ObisCode.AKTUELLE_WIRKLEISTUNG == ObisCode.by_obis('0100100700ff'))

def test_get_obiscode_by_description():
    assert( ObisCode.AKTUELLE_WIRKLEISTUNG == ObisCode.by_description('aktuelle Wirkleistung'))
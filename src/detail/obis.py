import enum
from typing import NamedTuple
from collections import namedtuple

Obis = namedtuple('Obis', ['obis', 'description'])

class ObisCode(enum.Enum):
    GERAETEEINZELIDENTIFIKATION = Obis(
        '0100000009ff', 'Geräteeinzelidentifikation')
    ZAEHLERSTAND_TOTAL = Obis('0100010800ff', 'Zählerstand Total')
    ZAEHLERSTAND_TARIF_1 = Obis('0100010801ff', 'Zählerstand Tarif 1')
    ZAEHLERSTAND_TARIF_2 = Obis('0100010802ff', 'Zählerstand Tarif 2')
    TOTAL_ZAEHLERSTAND = Obis('0100011100ff', 'Total-Zählerstand')
    AKTUELLE_WIRKLEISTUNG = Obis('0100100700ff', 'aktuelle Wirkleistung')
    MOMENTANEBLINDLEISTUNG_L1 = Obis('0100170700ff', 'Momentanblindleistung L1')
    STROM_L1 = Obis('01001f0700ff', 'Strom L1')
    SPANNUNG_L1 = Obis('0100200700ff', 'Spannung L1')
    WIRKLEISTUNG_L1 = Obis('0100240700ff', 'Wirkleistung L1')
    MOMENTANBLINDLEISTUNG_L2 = Obis('01002b0700ff', 'Momentanblindleistung L2')
    STROM_L2 = Obis('0100330700ff', 'Strom L2')
    SPANNUNG_L2 = Obis('0100340700ff', 'Spannung L2')
    WIRKLEISTUNG_L2 = Obis('0100380700ff', 'Wirkleistung L2')
    MOMENTANBLINDLEISTUNG_L3 = Obis('01003f0700ff', 'Momentanblindleistung L3')
    STROM_L3 = Obis('0100470700ff', 'Strom L3')
    SPANNUNG_L3 = Obis('0100480700ff', 'Spannung L3')
    WIRKLEISTUNG_L3 = Obis('01004c0700ff', 'Wirkleistung L3')
    PHASENABWEICHUNG_SPANNUNGEN_L1L2 = Obis(
        '0100510701ff', 'Phasenabweichung Spannungen L1/L2')
    PHASENABWEICHUNG_SPANNUNGEN_L1L3 = Obis(
        '0100510702ff', 'Phasenabweichung Spannungen L1/L3')
    PHASENABWEICHUNG_STROM_SPANNUNG_L1 = Obis(
        '0100510704ff', 'Phasenabweichung Strom/Spannung L1')
    PHASENABWEICHUNG_STROM_SPANNUNG_L2 = Obis(
        '010051070fff', 'Phasenabweichung Strom/Spannung L2')
    PHASENABWEICHUNG_STROM_SPANNUNG_L3 = Obis(
        '010051071aff', 'Phasenabweichung Strom/Spannung L3')
    AKTUELLE_CHIPTEMPERATUR = Obis('010060320002', 'Aktuelle Chiptemperatur')
    MINIMALE_CHIPTEMPERATUR = Obis('010060320003', 'Minimale Chiptemperatur')
    MAXIMALE_CHIPTEMPERATUR = Obis('010060320004', 'Maximale Chiptemperatur')
    GEMITTELTE_CHIPTEMPERATUR = Obis('010060320005', 'Gemittelte Chiptemperatur')
    SPANNUNGSMINIMUM = Obis('010060320303', 'Spannungsminimum')
    SPANNUNGSMAXIMUM = Obis('010060320304', 'Spannungsmaximum')
    HERSTELLER_IDENTIFIKATION = Obis('8181c78203ff', 'Hersteller-Identifikation')
    OEFFENTLICHER_SCHLUESSEL = Obis('8181c78205ff', 'Öffentlicher Schlüssel')

    @property
    def obis(self) -> str:
        return self.value.obis

    @property
    def description(self) -> str:
        return self.value.description

    @classmethod
    def by_obis(cls, obis: str):
       return next((x for x in list(cls) if x.value.obis == obis), None)
    
    @classmethod
    def by_description(cls, description: str):
        return next((x for x in list(cls) if x.value.description == description), None)
import enum
from typing import NamedTuple
from collections import namedtuple

Obis = namedtuple('Obis', ['obis', 'description'])


class ObisCode(enum.Enum):
    GERAETEEINZELIDENTIFIKATION = Obis('0100000009ff', 'Geräteeinzelidentifikation')
    ZAEHLERSTAND_TOTAL_BEZUG = Obis('0100010800ff', 'Zählerstand Total Bezug')
    ZAEHLERSTAND_TARIF_1_BEZUG = Obis('0100010801ff', 'Zählerstand Tarif 1 Bezug')
    ZAEHLERSTAND_TARIF_2_BEZUG = Obis('0100010802ff', 'Zählerstand Tarif 2 Bezug')
    ZAEHLERSTAND_TOTAL_EINSPEISUNG = Obis('0100020800ff', 'Zählerstand Total Einspeisung')
    ZAEHLERSTAND_TARIF_1_EINSPEISUNG = Obis('0100020801ff', 'Zählerstand Tarif 1 Einspeisung')
    ZAEHLERSTAND_TARIF_2_EINSPEISUNG = Obis('0100020802ff', 'Zählerstand Tarif 2 Einspeisung')
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

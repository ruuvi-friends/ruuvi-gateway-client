from typing import Optional, TypedDict, Dict


class SensorPayload(TypedDict):
    rssi: int
    timestamp: str
    data: str


class PayloadData(TypedDict):
    coordinates: any
    timestamp: str
    gw_mac: str
    tags: Dict[str, SensorPayload]


class Payload(TypedDict):
    data: PayloadData


class SensorData(TypedDict):
    data_format: int
    humidity: float
    temperature: float
    pressure: float
    acceleration: float
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    battery: int
    tx_power: Optional[int]
    movement_counter:  Optional[int]
    measurement_sequence_number:  Optional[int]
    mac: Optional[str]
    rssi: Optional[int]


ParsedDatas = Dict[str, SensorData]

from pydantic import BaseModel
from typing import Optional,List



class Pageinfo(BaseModel):
    pageNo: int
    pageSize: int
    totalCount: int
    totalPage: int


class Track(BaseModel):
    return_code: int
    return_message: str
    data: list
    pageinfo: Pageinfo


class Parking(BaseModel):
    label: int
    start_time: str
    end_time: str
    park_time: str
    park_longitude: float
    park_latitude: float
    count: int

# 每一条数据对象
class Item(BaseModel):
    uuid: str
    company_id: Optional[str] = None
    gps_time: Optional[str] = None
    create_time: Optional[str] = None
    event_code: Optional[str] = None
    device_code: Optional[str] = None
    count: Optional[str] = None
    ShellDamageAlarm: Optional[str] = None
    locationStatus: Optional[int] = None
    LocationModuleStatus: Optional[str] = None
    Elevation: Optional[str] = None
    DeviceSwitchState: Optional[str] = None
    MotionSensorStatus: Optional[int] = None
    LongitudePosition: Optional[str] = None
    longitude: Optional[float] = None
    LatitudePosition: Optional[str] = None
    latitude: Optional[float] = None
    BatteryVoltage: Optional[str] = None
    Battery: Optional[str] = None
    Speed: Optional[str] = None
    BatteryLevel: Optional[str] = None
    ChargeStatus: Optional[str] = None
    NetworkMode: Optional[str] = None
    LockRodStatus: Optional[str] = None


# 表对象
class BulkData(BaseModel):
    items: list[Item]


class Points(BaseModel):
    latitude: float
    longitude:float


class PointsData(BaseModel):
    points: list[Points]
##########################################

# class DeviceStatus(BaseModel):
#     LockRodStatus: str
#     ChargeStatus: str
#     DeviceSwitchState: str
#     MotionSensorStatus: str
#     LinkMode: str
#     LongitudePosition: str
#     LatitudePosition: str
#     NetworkMode: str
#     LocationModuleStatus: str
#     SimMode: str
#     GPSPositionStatus: int

class DeviceWarning(BaseModel):
    ShellDamageAlarm: str

class DeviceData(BaseModel):
    deviceStatus: Optional[str]  # JSON 字符串
    gpsTime: Optional[int]
    deviceCode: Optional[str]
    deviceName: Optional[str]
    lat: Optional[str]
    lng: Optional[str]
    direction: Optional[int]
    speed: Optional[float]
    deviceWarning: Optional[str]  # JSON 字符串
    elevation: Optional[int]
    battery: Optional[float]
    eventId: Optional[str]
    protocolTypeEncode: Optional[str]
    gpsPositionStatus: Optional[str]
    shortVideoFile: Optional[str]
class RequestBody(BaseModel):
    data: List[DeviceData]


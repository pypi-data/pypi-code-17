from enum import Enum
from spynnaker_external_devices_plugin.pyNN.protocols\
    .munich_io_spinnaker_link_protocol import RetinaKey


class PushBotRetinaResolution(Enum):

    NATIVE_128_X_128 = RetinaKey.NATIVE_128_X_128
    DOWNSAMPLE_64_X_64 = RetinaKey.DOWNSAMPLE_64_X_64
    DOWNSAMPLE_32_X_32 = RetinaKey.DOWNSAMPLE_32_X_32
    DOWNSAMPLE_16_X_16 = RetinaKey.DOWNSAMPLE_16_X_16

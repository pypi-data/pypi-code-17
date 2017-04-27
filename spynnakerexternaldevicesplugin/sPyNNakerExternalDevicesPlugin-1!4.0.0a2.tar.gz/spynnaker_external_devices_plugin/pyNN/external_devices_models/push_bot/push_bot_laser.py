from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol
from data_specification.enums.data_type import DataType
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .abstract_push_bot_output_device import AbstractPushBotOutputDevice


class PushBotLaser(AbstractPushBotOutputDevice):

    LASER_TOTAL_PERIOD = (
        0,
        MunichIoSpiNNakerLinkProtocol.push_bot_laser_config_total_period_key,
        0, DataType.S1615.max, 20
    )

    LASER_ACTIVE_TIME = (
        1, MunichIoSpiNNakerLinkProtocol.push_bot_laser_config_active_time_key,
        0, DataType.S1615.max, 20
    )

    LASER_FREQUENCY = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_laser_set_frequency_key,
        0, DataType.S1615.max, 20
    )

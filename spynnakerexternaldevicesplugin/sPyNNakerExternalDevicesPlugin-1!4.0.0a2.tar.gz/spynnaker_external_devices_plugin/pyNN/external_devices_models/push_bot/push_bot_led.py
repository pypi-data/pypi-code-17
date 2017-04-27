from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .abstract_push_bot_output_device import AbstractPushBotOutputDevice
from data_specification.enums.data_type import DataType


class PushBotLED(AbstractPushBotOutputDevice):

    LED_TOTAL_PERIOD = (
        0, MunichIoSpiNNakerLinkProtocol.push_bot_led_total_period_key,
        0, DataType.S1615.max, 20
    )

    LED_FRONT_ACTIVE_TIME = (
        1, MunichIoSpiNNakerLinkProtocol.push_bot_led_front_active_time_key,
        0, DataType.S1615.max, 20
    )

    LED_BACK_ACTIVE_TIME = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_led_back_active_time_key,
        0, DataType.S1615.max, 20
    )

    LED_FREQUENCY = (
        3, MunichIoSpiNNakerLinkProtocol.push_bot_led_set_frequency_key,
        0, DataType.S1615.max, 20
    )

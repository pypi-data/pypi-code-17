from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .abstract_push_bot_output_device import AbstractPushBotOutputDevice
from data_specification.enums.data_type import DataType


class PushBotSpeaker(AbstractPushBotOutputDevice):

    SPEAKER_TOTAL_PERIOD = (
        0,
        MunichIoSpiNNakerLinkProtocol.push_bot_speaker_config_total_period_key,
        0, DataType.S1615.max, 20
    )

    SPEAKER_ACTIVE_TIME = (
        1,
        MunichIoSpiNNakerLinkProtocol.push_bot_speaker_config_active_time_key,
        0, DataType.S1615.max, 20
    )

    SPEAKER_TONE = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_speaker_set_tone_key,
        0, DataType.S1615.max, 20
    )

    SPEAKER_MELODY = (
        3, MunichIoSpiNNakerLinkProtocol.push_bot_speaker_set_melody_key,
        0, DataType.S1615.max, 20
    )

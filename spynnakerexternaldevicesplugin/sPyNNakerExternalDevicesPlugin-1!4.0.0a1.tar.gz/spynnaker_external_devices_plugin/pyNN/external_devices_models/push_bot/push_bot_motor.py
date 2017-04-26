from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .abstract_push_bot_output_device import AbstractPushBotOutputDevice


class PushBotMotor(AbstractPushBotOutputDevice):

    MOTOR_0_PERMANENT = (
        0, MunichIoSpiNNakerLinkProtocol.push_bot_motor_0_permanent_key,
        -100, 100, 20
    )

    MOTOR_0_LEAKY = (
        1,
        (MunichIoSpiNNakerLinkProtocol
         .push_bot_motor_0_leaking_towards_zero_key),
        -100, 100, 20
    )

    MOTOR_1_PERMANENT = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_motor_1_permanent_key,
        -100, 100, 20
    )

    MOTOR_1_LEAKY = (
        3,
        (MunichIoSpiNNakerLinkProtocol
         .push_bot_motor_1_leaking_towards_zero_key),
        -100, 100, 20
    )

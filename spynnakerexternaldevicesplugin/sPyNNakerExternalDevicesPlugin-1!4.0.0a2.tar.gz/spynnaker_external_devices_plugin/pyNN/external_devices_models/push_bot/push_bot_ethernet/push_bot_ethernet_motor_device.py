from spinn_front_end_common.abstract_models.impl.\
    provides_key_to_atom_mapping_impl import \
    ProvidesKeyToAtomMappingImpl
from spinn_front_end_common.abstract_models.\
    abstract_send_me_multicast_commands_vertex \
    import AbstractSendMeMulticastCommandsVertex
from spinn_front_end_common.utilities.exceptions import ConfigurationException

from pacman.model.decorators.overrides import overrides

from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_ethernet.push_bot_ethernet_device import PushBotEthernetDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_motor import PushBotMotor


class PushBotEthernetMotorDevice(
        AbstractSendMeMulticastCommandsVertex, ProvidesKeyToAtomMappingImpl,
        PushBotEthernetDevice):
    """ The motor of a PushBot
    """

    def __init__(self, motor, protocol, timesteps_between_send=None):
        """

        :param motor: a PushBotMotor value to indicate the motor to control
        :param protocol: The protocol used to control the device
        :param timesteps_between_send:\
            The number of timesteps between sending commands to the device,\
            or None to use the default
        """

        if not isinstance(motor, PushBotMotor):
            raise ConfigurationException(
                "motor parameter must be a PushBotMotor value")

        ProvidesKeyToAtomMappingImpl.__init__(self)
        PushBotEthernetDevice.__init__(
            self, protocol, motor, True, timesteps_between_send)
        self._command_protocol = protocol

    def set_command_protocol(self, command_protocol):
        self._command_protocol = command_protocol

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.start_resume_commands)
    def start_resume_commands(self):
        commands = list()

        # add mode command if not done already
        if not self.protocol.sent_mode_command():
            commands.append(self.protocol.set_mode())

        # device specific commands
        commands.append(self._command_protocol.generic_motor_enable())
        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.pause_stop_commands)
    def pause_stop_commands(self):
        return [self._command_protocol.generic_motor_disable()]

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.timed_commands)
    def timed_commands(self):
        return []

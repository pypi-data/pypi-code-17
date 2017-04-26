"""
The :py:mod:`spynnaker.pynn` package contains the front end specifications
and implementation for the PyNN High-level API
(http://neuralensemble.org/trac/PyNN)
"""

import logging
import os

from spinnman.messages.eieio.eieio_type import EIEIOType

from spinn_front_end_common.utilities import helpful_functions
from spinn_front_end_common.utility_models.live_packet_gather \
    import LivePacketGather
from spinn_front_end_common.abstract_models\
    .abstract_send_me_multicast_commands_vertex \
    import AbstractSendMeMulticastCommandsVertex
from spinn_front_end_common.utilities.notification_protocol.socket_address \
    import SocketAddress

from spynnaker.pyNN.spinnaker import executable_finder
from spynnaker.pyNN.utilities import conf
from spynnaker.pyNN.utilities import constants
from spynnaker import pyNN as p

from spynnaker_external_devices_plugin.pyNN.external_devices_models.\
    arbitrary_fpga_device import ArbitraryFPGADevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.\
    external_spinnaker_link_cochlea_device import ExternalCochleaDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.\
    external_spinnaker_link_fpga_retina_device import ExternalFPGARetinaDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.\
    munich_spinnaker_link_motor_device import MunichMotorDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.\
    munich_spinnaker_link_retina_device import MunichRetinaDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.\
    push_bot.push_bot_retina_viewer import PushBotRetinaViewer

# PushBot Parameters
from spynnaker_external_devices_plugin.pyNN.protocols\
    .munich_io_spinnaker_link_protocol import MunichIoSpiNNakerLinkProtocol
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_laser import PushBotLaser
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_led import PushBotLED
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_motor import PushBotMotor
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_speaker import PushBotSpeaker
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_retina_resolution import PushBotRetinaResolution

# PushBot Ethernet control
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_ethernet.push_bot_lif_ethernet import PushBotLifEthernet
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_ethernet.push_bot_ethernet_laser_device \
    import PushBotEthernetLaserDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_ethernet.push_bot_ethernet_led_device \
    import PushBotEthernetLEDDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_ethernet.push_bot_ethernet_motor_device \
    import PushBotEthernetMotorDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_ethernet.push_bot_ethernet_speaker_device \
    import PushBotEthernetSpeakerDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_ethernet.push_bot_ethernet_retina_device \
    import PushBotEthernetRetinaDevice

# PushBotSpiNNakerLink control
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link.push_bot_lif_spinnaker_link \
    import PushBotLifSpinnakerLink
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link.push_bot_spinnaker_link_laser_device \
    import PushBotSpiNNakerLinkLaserDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link.push_bot_spinnaker_link_led_device \
    import PushBotSpiNNakerLinkLEDDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link.push_bot_spinnaker_link_motor_device \
    import PushBotSpiNNakerLinkMotorDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link.push_bot_spinnaker_link_speaker_device \
    import PushBotSpiNNakerLinkSpeakerDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_spinnaker_link.push_bot_spinnaker_link_retina_device \
    import PushBotSpiNNakerLinkRetinaDevice

from spynnaker_external_devices_plugin.pyNN.\
    spynnaker_external_device_plugin_manager import \
    SpynnakerExternalDevicePluginManager
from spynnaker_external_devices_plugin.pyNN.utility_models.spike_injector \
    import SpikeInjector as SpynnakerExternalDeviceSpikeInjector
from spynnaker_external_devices_plugin.pyNN.external_devices_models\
    .abstract_ethernet_controller import AbstractEthernetController
from spynnaker_external_devices_plugin.pyNN.connections\
    .ethernet_control_connection import EthernetControlConnection
from spynnaker_external_devices_plugin.pyNN.connections\
    .ethernet_command_connection import EthernetCommandConnection
from spynnaker_external_devices_plugin.pyNN.external_devices_models\
    .abstract_ethernet_sensor import AbstractEthernetSensor
from spynnaker_external_devices_plugin.pyNN import model_binaries
from spynnaker_external_devices_plugin.pyNN.connections\
    .spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection

logger = logging.getLogger(__name__)

executable_finder.add_path(os.path.dirname(model_binaries.__file__))
spynnaker_external_devices = SpynnakerExternalDevicePluginManager()

__all__ = [
    "EIEIOType",

    # General Devices
    "ExternalCochleaDevice", "ExternalFPGARetinaDevice",
    "MunichRetinaDevice", "MunichMotorDevice",
    "ArbitraryFPGADevice", "PushBotRetinaViewer",

    # Pushbot Parameters
    "MunichIoSpiNNakerLinkProtocol",
    "PushBotLaser", "PushBotLED", "PushBotMotor", "PushBotSpeaker",
    "PushBotRetinaResolution",

    # Pushbot Ethernet Parts
    "PushBotLifEthernet", "PushBotEthernetLaserDevice",
    "PushBotEthernetLEDDevice", "PushBotEthernetMotorDevice",
    "PushBotEthernetSpeakerDevice", "PushBotEthernetRetinaDevice",

    # Pushbot SpiNNaker Link Parts
    "PushBotLifSpinnakerLink", "PushBotSpiNNakerLinkLaserDevice",
    "PushBotSpiNNakerLinkLEDDevice", "PushBotSpiNNakerLinkMotorDevice",
    "PushBotSpiNNakerLinkSpeakerDevice", "PushBotSpiNNakerLinkRetinaDevice",

    # Connections
    "SpynnakerLiveSpikesConnection",

    # Provided functions
    "activate_live_output_for",
    "activate_live_output_to",
    "SpikeInjector"

]


def add_database_socket_address(
        database_notify_host, database_notify_port_num, database_ack_port_num):

    if database_notify_port_num is None:
        database_notify_port_num = helpful_functions.read_config_int(
            conf.config, "Database", "notify_port")
    if database_notify_host is None:
        database_notify_host = helpful_functions.read_config(
            conf.config, "Database", "notify_hostname")
    elif database_notify_host == "0.0.0.0":
        database_notify_host = "localhost"
    if database_ack_port_num is None:
        database_ack_port_num = helpful_functions.read_config_int(
            conf.config, "Database", "listen_port")

    # build the database socket address used by the notification interface
    database_socket = SocketAddress(
        listen_port=database_ack_port_num,
        notify_host_name=database_notify_host,
        notify_port_no=database_notify_port_num)

    # update socket interface with new demands.
    spynnaker_external_devices.add_socket_address(database_socket)


def activate_live_output_for(
        population, database_notify_host=None, database_notify_port_num=None,
        database_ack_port_num=None, board_address=None, port=None,
        host=None, tag=None, strip_sdp=True, use_prefix=False, key_prefix=None,
        prefix_type=None, message_type=EIEIOType.KEY_32_BIT,
        right_shift=0, payload_as_time_stamps=True, notify=True,
        use_payload_prefix=True, payload_prefix=None,
        payload_right_shift=0, number_of_packets_sent_per_time_step=0):
    """ Output the spikes from a given population from SpiNNaker as they
        occur in the simulation

    :param population: The population to activate the live output for
    :type population: spynnaker.pyNN.models.pynn_population.Population
    :param database_notify_host: the hostname for the device which is\
            listening to the database notification.
    :type database_notify_host: str
    :param database_ack_port_num: the port number to which a external device\
            will acknowledge that they have finished reading the database and\
            are ready for it to start execution
    :type database_ack_port_num: int
    :param database_notify_port_num: The port number to which a external\
            device will receive the database is ready command
    :type database_notify_port_num: int
    :param board_address: A fixed board address required for the tag, or\
            None if any address is OK
    :type board_address: str
    :param key_prefix: the prefix to be applied to the key
    :type key_prefix: int or None
    :param prefix_type: if the prefix type is 32 bit or 16 bit
    :param message_type: if the message is a eieio_command message, or\
            eieio data message with 16 bit or 32 bit keys.
    :param payload_as_time_stamps:
    :param right_shift:
    :param use_payload_prefix:
    :param notify:
    :param payload_prefix:
    :param payload_right_shift:
    :param number_of_packets_sent_per_time_step:
    :param port: The UDP port to which the live spikes will be sent.  If not\
                specified, the port will be taken from the "live_spike_port"\
                parameter in the "Recording" section of the spynnaker cfg file.
    :type port: int
    :param host: The host name or IP address to which the live spikes will be\
                sent.  If not specified, the host will be taken from the\
                "live_spike_host" parameter in the "Recording" section of the\
                spynnaker cfg file.
    :type host: str
    :param tag: The IP tag to be used for the spikes.  If not specified, one\
                will be automatically assigned
    :type tag: int
    :param strip_sdp: Determines if the SDP headers will be stripped from the\
                transmitted packet.
    :type strip_sdp: bool
    :param use_prefix: Determines if the spike packet will contain a common\
                prefix for the spikes
    :type use_prefix: bool
    """

    # get default params if none set
    if port is None:
        port = conf.config.getint("Recording", "live_spike_port")
    if host is None:
        host = conf.config.get("Recording", "live_spike_host")

    # add new edge and vertex if required to spinnaker graph
    spynnaker_external_devices.add_edge_to_recorder_vertex(
        population._vertex, port, host, tag, board_address, strip_sdp,
        use_prefix, key_prefix, prefix_type, message_type, right_shift,
        payload_as_time_stamps, use_payload_prefix, payload_prefix,
        payload_right_shift, number_of_packets_sent_per_time_step)

    if notify:
        add_database_socket_address(
            database_notify_host, database_notify_port_num,
            database_ack_port_num)


def activate_live_output_to(population, device):
    """ Activate the output of spikes from a population to an external device.\
        Note that all spikes will be sent to the device.

    :param population: The pyNN population object from which spikes will be\
                sent.
    :param device: The pyNN population external device to which the spikes\
                will be sent.
    """
    spynnaker_external_devices.add_edge(
        population._get_vertex, device._get_vertex,
        constants.SPIKE_PARTITION_ID)


def SpikeInjector(
        n_neurons, label, port=None, notify=True,
        virtual_key=None, database_notify_host=None,
        database_notify_port_num=None, database_ack_port_num=None):
    """ Supports adding a spike injector to the application graph.

    :param n_neurons: the number of neurons the spike injector will emulate
    :type n_neurons: int
    :param notify: allows us to not bother with the database system
    :type notify: bool
    :param label: the label given to the population
    :type label: str
    :param port: the port number used to listen for injections of spikes
    :type port: int
    :param virtual_key: the virtual key used in the routing system
    :type virtual_key: int
    :param database_notify_host: the hostname for the device which is\
            listening to the database notification.
    :type database_notify_host: str
    :param database_ack_port_num: the port number to which a external device\
            will acknowledge that they have finished reading the database and\
            are ready for it to start execution
    :type database_ack_port_num: int
    :param database_notify_port_num: The port number to which a external\
            device will receive the database is ready command
    :type database_notify_port_num: int
    """
    if notify:
        add_database_socket_address(
            database_notify_host, database_notify_port_num,
            database_ack_port_num)
    return SpynnakerExternalDeviceSpikeInjector(
        n_neurons=n_neurons, label=label, port=port, virtual_key=virtual_key)


def EthernetControlPopulation(
        n_neurons, model, params, label=None, local_host=None, local_port=None,
        database_notify_port_num=None, database_ack_port_num=None):
    """ Create a PyNN population that can be included in a network to\
        control an external device which is connected to the host

    :param n_neurons: The number of neurons in the control population
    :param model: Class of a model that implements AbstractEthernetController
    :param params: The parameters of the model
    :param label: An optional label for the population
    :param local_host:\
            The optional local host IP address to listen on for commands
    :param lost_port: The optional local port to listen on for commands
    :param database_ack_port_num:\
            The optional port to which responses to the database notification\
            protocol are to be sent
    :param database_notify_port_num:\
            The optional port to which notifications from the database\
            notification protocol are to be sent
    :return:\
            A pyNN Population which can be used as the target of a Projection.\
            Note that the Population can also be used as the source of a\
            Projection, but it might not send spikes.
    """
    if not issubclass(model, AbstractEthernetController):
        raise Exception(
            "Model must be a subclass of AbstractEthernetController")
    population = p.Population(n_neurons, model, params, label=label)
    vertex = population._get_vertex
    translator = vertex.get_message_translator()
    ethernet_control_connection = EthernetControlConnection(
        translator, local_host, local_port)
    devices_with_commands = [
        device for device in vertex.get_external_devices()
        if isinstance(device, AbstractSendMeMulticastCommandsVertex)
    ]
    if len(devices_with_commands) > 0:
        ethernet_command_connection = EthernetCommandConnection(
            translator, devices_with_commands, local_host,
            database_notify_port_num)
        add_database_socket_address(
            ethernet_command_connection.local_ip_address,
            ethernet_command_connection.local_port, database_ack_port_num)
    live_packet_gather = LivePacketGather(
        ethernet_control_connection.local_ip_address,
        ethernet_control_connection.local_port,
        message_type=EIEIOType.KEY_PAYLOAD_32_BIT,
        payload_as_time_stamps=False, use_payload_prefix=False)
    spynnaker_external_devices.add_application_vertex(live_packet_gather)
    for partition_id in vertex.get_outgoing_partition_ids():
        spynnaker_external_devices.add_edge(
            vertex, live_packet_gather, partition_id)
    return population


def EthernetSensorPopulation(
        model, params, local_host=None,
        database_notify_port_num=None, database_ack_port_num=None):
    """ Create a pyNN population which can be included in a network to\
        receive spikes from a device connected to the host

    :param model: Class of a model that implements AbstractEthernetController
    :param params: The parameters of the model
    :param local_host:\
            The optional local host IP address to listen on for database\
            notification
    :param database_ack_port_num:\
            The optional port to which responses to the database notification\
            protocol are to be sent
    :param database_notify_port_num:\
            The optional port to which notifications from the database\
            notification protocol are to be sent
    :return:\
            A pyNN Population which can be used as the source of a Projection.\
            Note that the Population cannot be used as the target of a\
            Projection.
    """
    if not issubclass(model, AbstractEthernetSensor):
        raise Exception("Model must be a subclass of AbstractEthernetSensor")
    device = model(**params)
    injector_params = dict(device.get_injector_parameters())
    injector_params['notify'] = False

    population = p.Population(
        device.get_n_neurons(), SpikeInjector, injector_params,
        label=device.get_injector_label())
    if isinstance(device, AbstractSendMeMulticastCommandsVertex):
        ethernet_command_connection = EthernetCommandConnection(
            device.get_translator(), [device], local_host,
            database_notify_port_num)
        add_database_socket_address(
            ethernet_command_connection.local_ip_address,
            ethernet_command_connection.local_port, database_ack_port_num)
    database_connection = device.get_database_connection()
    if database_connection is not None:
        add_database_socket_address(
            database_connection.local_ip_address,
            database_connection.local_port, database_ack_port_num)
    return population

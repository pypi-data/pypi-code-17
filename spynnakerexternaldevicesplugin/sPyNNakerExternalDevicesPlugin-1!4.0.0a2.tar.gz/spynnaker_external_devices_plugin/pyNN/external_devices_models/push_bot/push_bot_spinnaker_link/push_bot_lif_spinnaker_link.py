from spynnaker_external_devices_plugin.pyNN.external_devices_models\
    .external_device_lif_control import ExternalDeviceLifControl
from spynnaker_external_devices_plugin.pyNN.protocols\
    .munich_io_spinnaker_link_protocol import MunichIoSpiNNakerLinkProtocol

import logging

logger = logging.getLogger(__name__)


class PushBotLifSpinnakerLink(ExternalDeviceLifControl):
    """ Control module for a pushbot connected to a SpiNNaker Link
    """

    def __init__(
            self, n_neurons, protocol, devices,
            spikes_per_second=None, ring_buffer_sigma=None, label=None,
            incoming_spike_buffer_size=None, constraints=None,
            board_address=None,

            # default params for the neuron model type
            tau_m=ExternalDeviceLifControl.default_parameters['tau_m'],
            cm=ExternalDeviceLifControl.default_parameters['cm'],
            v_rest=ExternalDeviceLifControl.default_parameters['v_rest'],
            v_reset=ExternalDeviceLifControl.default_parameters['v_reset'],
            tau_syn_E=ExternalDeviceLifControl.default_parameters['tau_syn_E'],
            tau_syn_I=ExternalDeviceLifControl.default_parameters['tau_syn_I'],
            tau_refrac=(
                ExternalDeviceLifControl.default_parameters['tau_refrac']
            ),
            i_offset=ExternalDeviceLifControl.default_parameters['i_offset'],
            v_init=None
    ):

        self._command_protocol = MunichIoSpiNNakerLinkProtocol(
            protocol.mode, uart_id=protocol.uart_id)
        for device in devices:
            device.set_command_protocol(self._command_protocol)

        # Initialise the abstract LIF class
        ExternalDeviceLifControl.__init__(
            self, n_neurons=n_neurons, devices=devices, create_edges=True,
            spikes_per_second=spikes_per_second, label=label,
            ring_buffer_sigma=ring_buffer_sigma,
            incoming_spike_buffer_size=incoming_spike_buffer_size,
            constraints=constraints,
            tau_m=tau_m, cm=cm, v_rest=v_rest, v_reset=v_reset,
            tau_syn_E=tau_syn_E, tau_syn_I=tau_syn_I,
            tau_refrac=tau_refrac, i_offset=i_offset, v_init=v_init
        )

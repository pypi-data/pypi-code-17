
from spynnaker_external_devices_plugin.pyNN.external_devices_models\
    .push_bot.push_bot_ethernet.push_bot_translator import PushBotTranslator
from spynnaker_external_devices_plugin.pyNN.external_devices_models\
    .external_device_lif_control import ExternalDeviceLifControl
from spynnaker_external_devices_plugin.pyNN.external_devices_models\
    .push_bot.push_bot_ethernet.push_bot_wifi_connection \
    import get_pushbot_wifi_connection


class PushBotLifEthernet(ExternalDeviceLifControl):
    """ Leaky integrate and fire neuron with an exponentially decaying \
        current input
    """

    def __init__(
            self, n_neurons, protocol, devices, pushbot_ip_address,
            pushbot_port=56000, spikes_per_second=None, ring_buffer_sigma=None,
            label=None, incoming_spike_buffer_size=None, constraints=None,

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
            v_init=None):

        translator = PushBotTranslator(
            protocol,
            get_pushbot_wifi_connection(pushbot_ip_address, pushbot_port))

        ExternalDeviceLifControl.__init__(
            self, n_neurons, devices, False, translator, spikes_per_second,
            label, ring_buffer_sigma, incoming_spike_buffer_size, constraints,
            tau_m, cm, v_rest, v_reset, tau_syn_E, tau_syn_I, tau_refrac,
            i_offset, v_init)

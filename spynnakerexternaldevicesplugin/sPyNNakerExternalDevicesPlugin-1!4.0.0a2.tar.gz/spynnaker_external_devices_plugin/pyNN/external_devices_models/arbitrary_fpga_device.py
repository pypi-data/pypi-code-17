# general imports
from six import add_metaclass
from spinn_utilities.abstract_base import AbstractBase

# pacman imports
from pacman.model.graphs.application.application_fpga_vertex \
    import ApplicationFPGAVertex
from spinn_front_end_common.abstract_models.impl\
    .provides_key_to_atom_mapping_impl import ProvidesKeyToAtomMappingImpl


@add_metaclass(AbstractBase)
class ArbitraryFPGADevice(
        ApplicationFPGAVertex, ProvidesKeyToAtomMappingImpl):

    def __init__(
            self, n_neurons, fpga_link_id, fpga_id, board_address=None,
            label=None):
        ApplicationFPGAVertex.__init__(
            self, n_neurons, fpga_id, fpga_link_id, board_address, label)
        ProvidesKeyToAtomMappingImpl.__init__(self)

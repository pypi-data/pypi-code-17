MODULE = {
    'configs': {
        'node': '/etc/corenode/config.py',
        'network': '/etc/corenetwork/config.py',
    },
    'hooks': {
        'vm.prepared': [],
        'vm.started': ['corenode.hooks.vm'],
        'vm.stopped': ['corenode.hooks.vm'],
        'network.started': ['corenode.hooks.network_vxlan'],
        'network.stopped': ['corenode.hooks.network_vxlan'],
    },
}

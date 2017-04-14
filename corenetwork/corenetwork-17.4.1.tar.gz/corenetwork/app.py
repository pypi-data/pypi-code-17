MODULE = {
    'configs': {'network': '/etc/corenetwork/config.py'},
    'drivers': {
        'NETWORK_ROUTED_DRIVER': 'corenetwork.drivers.network_quagga',
        'NETWORK_ISOLATED_DRIVER': 'corenetwork.drivers.network_vxlan',
        'CORE_DRIVER': 'corenetwork.drivers.core_default',
        'NODE_DRIVER': 'corenetwork.drivers.node_default',
        'VM_DRIVER': 'corenetwork.drivers.vm_default',
    },
    'hooks': {
        'cron.daily': ['corenetwork.hooks.logs_dump',],
    },
}

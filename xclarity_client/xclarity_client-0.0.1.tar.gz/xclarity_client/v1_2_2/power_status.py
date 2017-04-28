power_status_list = {
    0: 'unknown',
    5: 'off',
    8: 'on',
    18: 'standby'
}

power_status_action = {
    'POWER_ON': 'powerOn',  # powers on the server
    'POWER_OFF': 'powerOff',  # powers off the server immediately
    'POWER_CYCLE_SOFT': 'powerCycleSoft',  # restarts the server immediately
    'POWER_CYCLE_SOFT_GRACE': 'powerCycleSoftGrace',  # restarts the server gracefully
    # 'VIRTUAL_RESEAT': 'virtualReseat',  # calls the CMM function to simulate removing power from the bay
    # 'POWER_NMI': 'powerNMI',  # restarts the server with non-maskable interrupt (performs a diagnostic interrupt)
    # 'BOOT_TO_F1': 'bootToF1',  # (Lenovo endpoints only) Powers on to UEFI(F1)
}

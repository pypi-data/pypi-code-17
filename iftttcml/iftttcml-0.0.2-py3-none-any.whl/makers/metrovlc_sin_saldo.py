# -*- coding: utf-8 -*-

import metrovlc
from iftttcml import iftttmaker


def launch(key, param):

    limite = param['limite']
    bono = param['bono']
    event = 'metrovlc_sin_saldo'

    info = metrovlc.metrosaldo(bono)

    if float(info['saldo']) < limite:
        saldo_y_moneda = '{} {}'.format(info['saldo'], info['moneda'])
        values = {'value1': bono, 'value2': saldo_y_moneda}
        # llamo a ifttt
        iftttmaker.call_event(key, event, values)

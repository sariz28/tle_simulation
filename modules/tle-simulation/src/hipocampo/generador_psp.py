# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 23:58:29 2015

@author: sara
"""
from configs.variables_sim import TIPO_E

v_n = [1]


def calcula_psp(psp, pa, step):

    if psp.tipo == TIPO_E :
        for t in range(1, psp.tiempo):
            psp.t_psp.append(float(t * step))

            v = psp.v_psp[t - 1]
            if t < 2:
                nuevo_v = psp.coeficiente * v + 1 * psp.amplitud * ((pa.v_max - v) / pa.v_max)
            else:
                nuevo_v = psp.coeficiente * v
            psp.v_psp.append(nuevo_v)
    else:

        for t in range(1, psp.tiempo):
            psp.t_psp.append(float(t * step))
            v = psp.v_psp[t - 1]
            rango_ipsp = psp.const_ipsp
            suma = 0
            for j in range(0, rango_ipsp):
                if (t - 1 - j) < 0:
                    suma += 0
                else:
                    suma += v_n[t - 1 - j] * psp.amplitud[j]
            nuevo_v = psp.coeficiente * v + ((pa.v_min - v) / pa.v_min) * suma
            v_n.append(0)
            psp.v_psp.append(nuevo_v)

    return psp

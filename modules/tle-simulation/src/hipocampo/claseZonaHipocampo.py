__author__ = 'sara'

import numpy as np

from configs.variables_sim import TIEMPO_ITERA_SIM
from simulacion.modelo_ac import inicializaModeloAC


class ZonaHipocampo:
    def __init__(self, nombre_zona, parametros):
        self.nombre_zona= nombre_zona

        # AFERENCIAS EXTRINSECAS
        self.pulsos_entrada = np.random.poisson(parametros.TASA_AFERENCIAS, TIEMPO_ITERA_SIM)

        # AFERENCIAS INTRINSECAS_EX
        self.pulsos_entrada_int_ex = 0

        # SENIAL GENERADA
        self.senial_saludable = []

        # POTENCIALES DE ACCION
        self.num_potenciales_saludable = []

        # POTENCIALES DE ACCION
        self.num_potenciales_saludable_in = []

        # LATTICE DE NEUTONAS EXCITATORIAS E INHIBITORIAS
        self.lattice_ex, self.lattice_in, self.pulsos_entrada_int_ex, \
        self.perdida_neuronal_ex, self.perdida_neuronal_in = inicializaModeloAC(parametros, self.pulsos_entrada[0])

        # Parametros
        self.param = parametros

        #IMPULSOS POR SUBZONA
        self.impulsos_subzonas = {"dorsal_proximal": 0, "dorsal_intermedio": 0, "dorsal_distal": 0,
                                  "ventral_proximal": 0, "ventral_intermedio": 0, "ventral_distal": 0}

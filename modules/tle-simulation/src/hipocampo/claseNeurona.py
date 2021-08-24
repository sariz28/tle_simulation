__author__ = 'sara'

from configs.parametros import E_INACTIVO
from configs.variables_sim import TIPO_E

"""
Created on Mon Sep  7 18:25:18 2015

@author: sara

"""


class Neurona:
    def __init__(self,tipo,posx, posy, vecinos,parametros, sub_zona, es_muerta):
        # ID-NEURONA
        self.idneurona=tipo + "_" + str(posx)+ "_"+ str(posy)
        # PARAMETROS QUE SON ASIGNADOS DEPENDIENDO EL TIPO DE NEURONA
        if tipo == TIPO_E:
            self.pa = parametros.pa_ex
        else:
            self.pa = parametros.pa_in

        self.muerta= es_muerta

        # Tipo de sub zona a la que pernece la neurona
        self.sub_zona = sub_zona

        # Estados
        self.estado = [E_INACTIVO]

        # TIEMPO
        self.tiempo_estado=self.pa.t_inactivo

        # VOLTAJE (voltaje intracelular)
        self.volt_membrana = self.pa.v_inactivo

        # UMBRAL
        self.umbral=self.pa.u_inactivo

        # Vecinos
        self.aferencias=vecinos

        # EPSPs EXT-E
        self.epsp_ext_e = 0

        # NUMERO DE NEURONAS_EXCITADORAS
        self.n_ext_e  = 0

        # EPSPs EXT-E
        self.epsp_e_e = 0

        # NUMERO DE NEURONAS_EXCITADORAS
        self.n_e_e = 0

        # EPSPs E-I
        self.epsp_e_i = 0

        # NUMERO DE NEURONAS_EXITADORAS
        self.n_e_i = 0

        # IPSPs
        self.ipsp = 0
        # NUMERO DE NEURONAS INHIBIDORAS
        self.n_i=[0]

    def getEstado(self):
        return self.estado[-1]

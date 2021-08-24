__author__ = 'sara'


class Psp:
    def __init__(self, tipo, coeficiente, amplitud_voltaje, tiempo_duracion, constante_ipsp=None):

        # Tipo de psp (IPSP o EPSP)
        self.tipo = tipo

        # Coefieciente que determina el comportamiento de crecimiento o decremento de un PSP
        self.coeficiente = coeficiente

        # Amplitud en miliVoltios de un PSP
        self.amplitud = amplitud_voltaje

        # Tiempo que tiene efecto un PSP
        self.tiempo = tiempo_duracion

        # TIEMPOS DE SIMULACION DE PSP
        self.t_psp = [0]

        # VOLTAJES DE SIMULACION DE PSP
        self.v_psp = [0]

        self.const_ipsp = constante_ipsp

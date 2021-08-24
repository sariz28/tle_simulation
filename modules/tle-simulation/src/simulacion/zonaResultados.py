__author__ = 'sara'

class ZonaHipocampoResultados:
    def __init__(self, zonaHipocampo):
        self.zona = zonaHipocampo.nombre_zona

        self.pa_ex= zonaHipocampo.param .pa_ex
        # SENIAL GENERADA
        self.senial_saludable = zonaHipocampo.senial_saludable

        # POTENCIALES DE ACCION
        self.num_potenciales_saludable =zonaHipocampo.num_potenciales_saludable

        # POTENCIALES DE ACCION
        self.num_potenciales_saludable_in =  zonaHipocampo.num_potenciales_saludable_in

        # Parametros de subzonas para graficar
        self.sub_zonas = zonaHipocampo.param.subZonas

        self.is_recurrente = zonaHipocampo.param.is_recurrente
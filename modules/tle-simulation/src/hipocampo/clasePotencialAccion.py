__author__ = 'sara'


class PotencialAccion:
    def __init__(self, tiempo_activo, tiempo_refractario, tiempo_inactivo, umbral_activo, umbral_refractario,
                 umbral_inactivo, voltaje_max, voltaje_min, voltaje_inactivo):

        # TIEMPOS DE DURACION EN LA ETAPA ACTIVA DE UN POTENCIAL DE ACCION ( PERIODO ABSOLUTO)
        self.t_activo = tiempo_activo

        # TIEMPO DE DURACION EN LA ETAPA REFRACTARIA DE UN POTECIAL DE ACCION (PERIODO REFRACTARIO)
        self.t_refractario = tiempo_refractario

        # TIEMPO DE DURACION EN LA ETAPA DE INACTIVA DE LA NEURONA (PERIODO DE REPOSO)
        self.t_inactivo = tiempo_inactivo

        # UMBRAL EN LA ETAPA ACTIVA
        self.u_activo = umbral_activo

        # UMBRAL EN LA ETAPA REFRACTARIA
        self.u_refractario = umbral_refractario

        # UMBRAL EN LA ETAPA INACTIVA
        self.u_inactivo = umbral_inactivo

        # VOLTAJE MAXIMO DE PICO QUE TOMA UN POTENCIAL DE ACCION
        self.v_max = voltaje_max

        # VOLTAJE MINIMO EN HIPERPOLARIZACION QUE TOMA UN POTENCIAL DE ACCION
        self.v_min = voltaje_min

        # VOLTAJE EN REPOSO DE UNA NEURONA
        self.v_inactivo = voltaje_inactivo

__author__ = 'sara'

from generador_psp import calcula_psp


class SubZonaHipocampo:
    def __init__(self, nombre_sub_zona, rango_limite_nueronas_EX, rango_limite_nueronas_IN, psp_EXT_E, psp_E_E, psp_E_I,
                 psp_I_E, pa_ex, pa_in,step):
        # Nombre de la subzona del hipocampo
        self.nombre = nombre_sub_zona

        # Rango del limite del nueronas excitatorias pertenecientes a la subzona
        self.rango_ex = rango_limite_nueronas_EX

        # Rango del limite del nueronas inhibitorias  pertenecientes a la subzona
        self.rango_in = rango_limite_nueronas_IN

        # PSP generado de aferencias extrinsecas exitatorias a celulas exitatorias
        self.psp_EXT_E = calcula_psp(psp_EXT_E, pa_ex, step)

        # EPSP DE NEURONA PIRAMIDAL A NEURONA PIRAMIDAL
        self.psp_E_E = calcula_psp(psp_E_E, pa_ex, step)

        # EPSP DE NEURONA PIRAMIDAL A INTERNEURONA
        self.psp_E_I = calcula_psp(psp_E_I, pa_ex, step)

        # IPSP DE INTERNEURONA A NEURONA PIRAMIDAL

        self.psp_I_E = calcula_psp(psp_I_E, pa_in, step)


__author__ = 'sara'
import numpy as np

#ESTADOS
from configs.variables_sim import NUM_TOTAL_NEURONAS_EX, TIPO_E, TIPO_I, NUM_NEURONAS_EX, NUM_NEURONAS_IN
from hipocampo.clasePotencialAccion import PotencialAccion
from hipocampo.clasePsp import Psp
from hipocampo.claseSubzona import SubZonaHipocampo

E_INACTIVO = 0
E_ACTIVO = 1
E_REFRACTARIO = 2
TERMINO_ESTADO=0

# PARAMETROS NEUROFISIOLOGICOS DE LA NEURONA CA3

class parametrosCA3Class:
    def __init__(self):

        # PARAMETROS PARA SIMULACION DE UN POTENCIAL DE ACCION EN UN CELULA EXCITATORIA
        self.pa_ex = PotencialAccion(2, 3, 0, 37.1,[-43, -38.1, -23.0], -43, 37.1, -70.7,-60.5)

        # PARAMETROS PARA SIMULACION DE UN POTENCIAL DE ACCION EN UN CELULA EXCITATORIA
        self.pa_in = PotencialAccion(2, 7, 0, 12.8, [-50, -49.01, -48.03, -46.07, -42.15, -34.3, -18.6], -50, 12.8, -69.1, -58.3)

        # PARAMETROS PARA SIMULACION DE UN POTENCIAL DE ACCION EN UN CELULA EXCITATORIA
        #self.pa_ex = PotencialAccion(2, 3, 0, 30, [-54,-50.2,-33.4], -54, 30, -80, -60)

        # PARAMETROS PARA SIMULACION DE UN POTENCIAL DE ACCION EN UN CELULA EXCITATORIA
        #self.pa_in = PotencialAccion(2, 5, 0, 30, [-54,-53.71,-52.68, -48.75, -33.0], -54, 30, -80, -60)
        # VARIABLES PARA MANIPULAR LAS AFERENCIAS EXTRINCICAS
        self.TASA_AFERENCIAS= NUM_TOTAL_NEURONAS_EX * 0.12

        # VARIABLES PARA MANIPULAR LAS AFERENCIAS EXTRINCICAS
        self.TASA_AFERENCIAS_INT= round(NUM_TOTAL_NEURONAS_EX * 0.02)
        # CONTIENE SINAPSIS EX INTRINSECAS (RECURRENTES)
        self.is_recurrente = True

        # VARIABLES PARA LAS VECINDADES
        self.RADIO_IN_CELL = np.array([36,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,
                                       38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,36])
        self.AUX_1_RADIO_IN = 17
        self.AUX_2_RADIO_IN = 36
        self.AUX_3_RADIO_IN = 16
        self.AUX_4_RADIO_IN = 2

        self.RADIO_EX_CELL = np.array([12,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,12])
        self.AUX_1_RADIO_EX = 7
        self.AUX_2_RADIO_EX = 12
        self.AUX_3_RADIO_EX = 5
        self.AUX_4_RADIO_EX = 3

        # COLORES PARA EL DIBUJADO DE NEURONAS
        self.colores_neurona = {"EX-fill": '#E3CEF6', "IN-fill": "#CEE3F6", "EX-line": '#f97525', "IN-line": "#2E64FE"}
        self.tam_sub_zonas = [[["dorsal_proximal",30,50,"#000b10"],["dorsal_intermedio",40,50, "#00141e"],["dorsal_distal",30,50,"#001a28"]],
                             [["ventral_proximal",30,50, "#1e0012"],["ventral_intermedio",40,50 , "#2e001a"],["ventral_distal",30,50 , "#3b0022"]]]

        self.num_sub_zonas = [3,3]

        # INICIALIZA LOS PARAMETROS DE CADA SUBZONA DE LA CA3
        self.subZonas = self.inicializa_subzonas()

        self.perdida_neuronal= False

        #PORCENTAJES DE PERDIDA NEURONAL POR ZONA

        self.zonas_afectadas_ex = {"dorsal_proximal":0, "dorsal_intermedio":0, "dorsal_distal":0,
                                  "ventral_proximal":0, "ventral_intermedio":0, "ventral_distal":0, "all":0}

        self.zonas_afectadas_in = {"dorsal_proximal":0, "dorsal_intermedio":0, "dorsal_distal":0,
                                  "ventral_proximal":0, "ventral_intermedio":0, "ventral_distal":0, "all":0}

    def inicializa_subzonas(self):

        lista_rangos_ex = calculaDensidadNeuronas(self.tam_sub_zonas,self.num_sub_zonas,NUM_NEURONAS_EX)
        lista_rangos_in = calculaDensidadNeuronas(self.tam_sub_zonas,self.num_sub_zonas, NUM_NEURONAS_IN)

        sub_zonas = {}

        id_subzona= "dorsal_proximal"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8,np.random.randint(9,13), 11)
        psp_E_E = Psp(TIPO_E, 0.8, 0.8, 11)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "dorsal_intermedio"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8,np.random.randint(9,13), 11)
        psp_E_E = Psp(TIPO_E, 0.8, 0.8, 11)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "dorsal_distal"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8,np.random.randint(9,13), 11)
        psp_E_E = Psp(TIPO_E, 0.8, 0.8, 11)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "ventral_proximal"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8,np.random.randint(9,13), 11)
        psp_E_E = Psp(TIPO_E, 0.8, 0.8, 11)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "ventral_intermedio"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8,np.random.randint(9,13), 11)
        psp_E_E = Psp(TIPO_E, 0.8, 0.8, 11)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "ventral_distal"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8, np.random.randint(9,13), 11)
        psp_E_E = Psp(TIPO_E, 0.8, 0.8, 11)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona= "prueba_psp"
        rango_num_neuronas_ex = {"rango_x": [-1, -1], "rango_y": [-1,-1]}
        rango_num_neuronas_in = {"rango_x": [-1, -1], "rango_y": [-1,-1]}
        psp_EXT_E = Psp(TIPO_E, 0.8, 12, 21)
        psp_E_E = Psp(TIPO_E, 0.7, 0.8, 11)
        psp_E_I = Psp(TIPO_E, 0.6, 2, 11)
        psp_I_E = Psp(TIPO_I, 0.85, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in,1)
        sub_zonas[id_subzona] = sub_zona

        return sub_zonas




# PARAMETROS NEUROFISIOLOGICOS DE LA NEURONA CA1

class parametrosCA1Class:
    def __init__(self):

        #self.pa_ex = PotencialAccion(2, 3, 0, 22.6, [-49, -46.15 , -34.78], -49, 22.6, -70.2, -62.4)

        #self.pa_in = PotencialAccion(2, 7, 0, 12.8, [-50, -49.01, -48.03, -46.07, -42.15, -34.3, -18.6], -50, 12.8, -69.1, -58.3)

        # PARAMETROS PARA SIMULACION DE UN POTENCIAL DE ACCION EN UN CELULA EXCITATORIA
        self.pa_ex = PotencialAccion(2, 3, 0, 30, [-54,-50.2,-33.4], -54, 30, -80, -60)

        # PARAMETROS PARA SIMULACION DE UN POTENCIAL DE ACCION EN UN CELULA EXCITATORIA
        self.pa_in = PotencialAccion(2, 7, 0, 12.8, [-50, -49.01, -48.03, -46.07, -42.15, -34.3, -18.6], -50, 12.8, -69.1, -58.3)

        # VARIABLES PARA MANIPULAR LAS AFERENCIAS EXTRINSECAS
        self.TASA_AFERENCIAS= NUM_TOTAL_NEURONAS_EX * 0.06

        self.TASA_AFERENCIAS_INT= 0

        # CONTIENE SINAPSIS EX INTRINSECAS (RECURRENTES)
        self.is_recurrente = False

        # VARIABLES PARA LAS VECINDADES
        self.RADIO_IN_CELL = np.array([8,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,8])
        self.AUX_1_RADIO_IN = 8
        self.AUX_2_RADIO_IN = 8
        self.AUX_3_RADIO_IN = 3
        self.AUX_4_RADIO_IN = 5


        self.RADIO_EX_CELL = np.array([12,14,14,14,14,14,14,14,14,14,14,12])
        self.AUX_1_RADIO_EX = 5
        self.AUX_2_RADIO_EX = 12
        self.AUX_3_RADIO_EX = 5
        self.AUX_4_RADIO_EX = 0

        # COLORES PARA EL DIBUJADO DE NEURONAS
        self.colores_neurona = {"EX-fill": '#F6CEEC', "IN-fill": "#CEE3F6", "EX-line": '#FF0080', "IN-line": "#2E64FE"}
        self.tam_sub_zonas = [[["dorsal_proximal",30,50,"#000b10"],["dorsal_intermedio",40,50, "#00141e"],["dorsal_distal",30,50,"#001a28"]],
                             [["ventral_proximal",30,50, "#1e0012"],["ventral_intermedio",40,50 , "#2e001a"],["ventral_distal",30,50 , "#3b0022"]]]

        self.num_sub_zonas = [3,3]

        # INICIALIZA LOS PARAMETROS DE CADA SUBZONA DE LA CA3
        self.subZonas = self.inicializa_subzonas()

        self.perdida_neuronal= False
        #PORCENTAJES DE PERDIDA NEURONAL POR ZONA

        self.zonas_afectadas_ex = {"dorsal_proximal":0, "dorsal_intermedio":0, "dorsal_distal":0,
                                  "ventral_proximal":0, "ventral_intermedio":0, "ventral_distal":0, "all":0}

        self.zonas_afectadas_in = {"dorsal_proximal":0, "dorsal_intermedio":0, "dorsal_distal":0,
                                  "ventral_proximal":0, "ventral_intermedio":0, "ventral_distal":0, "all":0}

    def inicializa_subzonas(self):

        lista_rangos_ex = calculaDensidadNeuronas(self.tam_sub_zonas,self.num_sub_zonas,NUM_NEURONAS_EX)
        lista_rangos_in = calculaDensidadNeuronas(self.tam_sub_zonas,self.num_sub_zonas, NUM_NEURONAS_IN)

        sub_zonas = {}

        id_subzona= "dorsal_proximal"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8, 1.2, 11)
        psp_E_E = Psp(TIPO_E, 0, 0, 0)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "dorsal_intermedio"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8, 1.2, 11)
        psp_E_E = Psp(TIPO_E, 0, 0, 0)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "dorsal_distal"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8, 1.2, 11)
        psp_E_E = Psp(TIPO_E, 0, 0, 0)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "ventral_proximal"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8, 1.2, 11)
        psp_E_E = Psp(TIPO_E, 0, 0, 0)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "ventral_intermedio"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8, 1.2, 11)
        psp_E_E = Psp(TIPO_E, 0, 0, 0)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona = "ventral_distal"
        rango_num_neuronas_ex = lista_rangos_ex[id_subzona]
        rango_num_neuronas_in = lista_rangos_in[id_subzona]
        psp_EXT_E = Psp(TIPO_E, 0.8, 1.2, 11)
        psp_E_E = Psp(TIPO_E, 0, 0, 0)
        psp_E_I = Psp(TIPO_E, 0.7,2, 11)
        psp_I_E = Psp(TIPO_I, 0.95, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 4)
        sub_zonas[id_subzona] = sub_zona

        id_subzona= "prueba_psp"
        rango_num_neuronas_ex = {"rango_x": [-1, -1], "rango_y": [-1,-1]}
        rango_num_neuronas_in = {"rango_x": [-1, -1], "rango_y": [-1,-1]}
        psp_EXT_E = Psp(TIPO_E, 0.7, 1, 11)
        psp_E_E = Psp(TIPO_E, 0.8, 1, 11)
        psp_E_I = Psp(TIPO_E, 0.6, 2, 11)
        psp_I_E = Psp(TIPO_I, 0.85, [-1] * 1, 26, 1)
        sub_zona = SubZonaHipocampo(id_subzona, rango_num_neuronas_ex, rango_num_neuronas_in, psp_EXT_E,
                                    psp_E_E, psp_E_I, psp_I_E, self.pa_ex, self.pa_in, 1)
        sub_zonas[id_subzona] = sub_zona

        return sub_zonas


def calculaDensidadNeuronas(porcentajes_tam_sub_zonas, sub_areas, numero_neuronas):
    num_fila = 0
    limite_x = 0
    rangos_y = [0] * sub_areas[0]
    rangos_y_aux = []
    limites_sub_zonas = {}
    for num_columnas in sub_areas:
        for columna in range(num_columnas):
            sub_zona = porcentajes_tam_sub_zonas[num_fila][columna]
            num_neuronas_y = round((sub_zona[2] * numero_neuronas) / 100.0) -1
            num_neuronas_x = round((sub_zona[1] * numero_neuronas) / 100.0) -1
            rango_y =  int(num_neuronas_y + rangos_y[columna])
            rango_x =  int(num_neuronas_x + limite_x)
            rango_y =  rango_y if rango_y < numero_neuronas -1 else numero_neuronas -1
            rango_x =  rango_x if rango_x < numero_neuronas -1 else numero_neuronas -1
            limites_sub_zonas[sub_zona[0]]= {"rango_x": [limite_x, rango_x], "rango_y": [rangos_y[columna], rango_y]}
            rangos_y_aux.append(rango_y + 1)
            limite_x = rango_x + 1
        num_fila += 1
        limite_x = 0
        rangos_y = rangos_y_aux
        rangos_y_aux= []
    return limites_sub_zonas




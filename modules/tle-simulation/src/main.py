from graficos.graficos import grafica_resultados
from simulacion.modelo_ac import ejecutaModeloAC, salidasCA3
from configs.parametros import parametrosCA3Class, parametrosCA1Class
from configs.variables_sim import TIEMPO_INCREMENTO, TIEMPO_ITERA_SIM
from graficos.variables_graficos_sim import canvas_ca3, canvas_ca1
from hipocampo.claseZonaHipocampo import ZonaHipocampo

# SIMULACION
# EJECUTA EL MODELO
print("Iniciando simulacion ... ")
tiempo_sim = [float("{0:.3f}".format(TIEMPO_INCREMENTO * i)) for i in range(TIEMPO_ITERA_SIM - 1)]
parametrosCA3 = parametrosCA3Class()
parametrosCA1 = parametrosCA1Class()
zona_ca3 = ZonaHipocampo("CA3", parametrosCA3)
zona_ca1 = ZonaHipocampo("CA1", parametrosCA1)
zona_ca1.impulsos_subzonas = salidasCA3(zona_ca3)
zona_ca3, zona_ca1 = ejecutaModeloAC(zona_ca3, zona_ca1, canvas_ca3, canvas_ca1, tiempo_sim)
# guardaResultados(zona_ca3,zona_ca1, num_sim)
grafica_resultados(zona_ca3, zona_ca1, tiempo_sim)

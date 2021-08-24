__author__ = 'sara'

#PARAMETROS DE SIMULACION
AUMENTO_PARAMETROS = 1

NUM_NEURONAS_EX = 50 * AUMENTO_PARAMETROS
NUM_NEURONAS_IN = 16 * AUMENTO_PARAMETROS
NUM_TOTAL_NEURONAS_EX= NUM_NEURONAS_EX * NUM_NEURONAS_EX


TIPO_E="EX"
TIPO_I="IN"

TIEMPO_PSP=31
TIEMPO_ITERA_SIM = 3001
TIEMPO_INCREMENTO = 0.00333
TIEMPO_ACTUALIZACION = 1

FRECUENCIA_MUESTREO = round( 1 /  TIEMPO_INCREMENTO)
VALORES_FRECUENCIA = TIEMPO_ITERA_SIM / 2

RUTA_GRAFICOS_SIM = '/home/sara/Dropbox/TESIS/pruebas_modelo/IMAGENES/pruebas/normal_p/'
RUTA_MUESTREO_SIM = '/home/sara/Dropbox/TESIS/pruebas_modelo/seniales_pruebas/success/'
RUTA_MUESTREO_DISP_SIM = '/home/sara/Dropbox/TESIS/pruebas_modelo/seniales_pruebas/tasas_disparo/'
RUTA_MUESTREO_REAL = '/home/sara/Dropbox/TESIS/pruebas_modelo/seniales_reales/'
RUTA_MUESTREO_REAL_M = '/home/sara/Dropbox/TESIS/pruebas_modelo/seniales_reales/muestras1/'
RUTA_MUESTREO_REAL_I = '/home/sara/Dropbox/TESIS/pruebas_modelo/seniales_reales/muestras1_fig/'
RUTA_MUESTREO_REAL_D = '/home/sara/Dropbox/TESIS/pruebas_modelo/seniales_reales/muestras1_des/'
RUTA_GRAFICOS_SIM_P = '/home/sara/Dropbox/TESIS/pruebas_modelo/IMAGENES/pruebas/prueba_perdida_ca1/'
RUTA_MUESTREO_SIM_P = '/home/sara/Dropbox/TESIS/pruebas_modelo/seniales_pruebas/prueba_perdida_ca1/'



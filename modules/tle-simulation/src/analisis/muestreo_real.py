import os

__author__ = 'sara'
import matplotlib.pyplot as plt
import numpy as np

from analisis.filtro_pasa_bandas import filtra_signal
from analisis.herramientas_wavelet import normalizacion_datos, descomposicion_signal, plot_signal_decomp
from configs.variables_sim import TIEMPO_INCREMENTO, TIEMPO_ITERA_SIM, RUTA_MUESTREO_REAL_I, \
    FRECUENCIA_MUESTREO, RUTA_MUESTREO_REAL_D


def plot_datos_reales (ruta, nombre_arch):
    print nombre_arch
    tiempo_sim = [float("{0:.3f}".format(TIEMPO_INCREMENTO * i)) for i in range(TIEMPO_ITERA_SIM - 1)]
    senial = np.loadtxt(ruta + nombre_arch)
    plt.subplots_adjust(wspace=0.8, hspace= 0.5)
    plt.subplot(211)
    plt.title("Muestra", fontweight='bold')
    senial = normalizacion_datos(senial)
    plt.plot(tiempo_sim,senial, color="black")
    plt.xlabel("Segundos")
    plt.ylabel("miliVolts")
    plt.ylim(-8,8)
    plt.grid()
    plt.subplot(212)
    plt.title("Espectro de Frecuencia", fontweight='bold')
    f, a=filtra_signal(senial,FRECUENCIA_MUESTREO)
    plt.plot(f,a,color="black")
    plt.xlabel("Frecuencia")
    plt.ylabel("Amplitud")
    plt.xlim(0,50)
    plt.grid()
    plt.savefig(RUTA_MUESTREO_REAL_I + nombre_arch.replace(".dat","_img")+'.png')
    plt.clf()


def genera_ima_dat_real(ruta):
    for root, dirs, files in os.walk(ruta):
        for nombre_arch in  files:
            plot_datos_reales(ruta, nombre_arch)


def genera_descomposicion_dat_real(ruta):
    for root, dirs, files in os.walk(ruta):
        for nombre_arch in  files:
            senial = np.loadtxt(ruta + nombre_arch)
            rec_a, rec_d = descomposicion_signal(senial, 'sym9')
            fig = plot_signal_decomp(senial, rec_a, rec_d)
            fig.savefig(RUTA_MUESTREO_REAL_D + nombre_arch.replace(".dat","_des")+'.png')

def division_senial(ruta, archivo,frec_muestreo):
    senial = np.loadtxt(ruta + archivo)
    tam_archivo = len(senial)
    #MUESTRAS CON UN TIEMPO DE DURACION DE 10 SEGUNDOS
    muestras_totales = int (tam_archivo / (frec_muestreo * 10.0))
    tam_muestras_par = muestras_totales / 3
    rango_min = tam_muestras_par
    rango_max = tam_muestras_par * 2
    lista_muestras = []
    muestras = 100
    info = []
    carpeta = archivo.replace(".dat","")
    while (len(lista_muestras) < muestras):
        num_muestra = np.random.randint(rango_min,rango_max)
        if num_muestra not in lista_muestras :
            r_min = num_muestra *(frec_muestreo * 10.0)
            r_max = r_min + (frec_muestreo * 10.0)
            sub_muestra = senial[r_min: r_max ]
            info.append(" muestra "+ str (num_muestra) + "  rangos  " + str(r_min) + "  --  " + str (r_max) + "\n" )
            lista_muestras.append(num_muestra)
            np.savetxt(ruta + carpeta +"/muestra_"+ str(len(lista_muestras))+".dat", sub_muestra)

    archivo = open(ruta + "INFO.txt","r+")
    archivo.writelines(info)
    archivo.close()




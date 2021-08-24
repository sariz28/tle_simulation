from filtro_pasa_bandas import filtros_bandas, calcula_porcentaje_energia_fil, filtraSignal
from herramientas_wavelet import descomposicion_signal, plot_signal_decomp, calcula_porcentaje_energia, \
    normalizacion_datos
from variables_sim import RUTA_GRAFICOS_SIM, RUTA_MUESTREO_SIM, RUTA_MUESTREO_REAL_M, RUTA_MUESTREO_DISP_SIM, \
    RUTA_MUESTREO_SIM_P, RUTA_GRAFICOS_SIM_P, FRECUENCIA_MUESTREO, TIEMPO_INCREMENTO, TIEMPO_ITERA_SIM

__author__ = 'sara'
import os
import numpy as np
import matplotlib.pyplot as plt
import pywt
import pylab as plt1
import matplotlib.pylab

bandas_frecuencia = {"D1": "Higher Gamma", "D2": "Lower Gamma", "D3" : "Beta", "D4": "Alfa", "D5":"Theta", "A5":"Delta"}


def guardaResultados(zona_ca3, zona_ca1, num_sim):
    nombre_archivo_ca3 = RUTA_MUESTREO_SIM_P  + str(num_sim) + "_SIMULACION_CA3.dat"
    nombre_archivo_ca1 = RUTA_MUESTREO_SIM_P  + str(num_sim) + "_SIMULACION_CA1.dat"
    np.savetxt(nombre_archivo_ca3, zona_ca3.senial_saludable)
    np.savetxt(nombre_archivo_ca1, zona_ca1.senial_saludable)

def guarda_graficas (figura ,num_sim):
    figura.savefig(RUTA_GRAFICOS_SIM_P + str(num_sim)+'_SIMULACION.png')

def calcula_num_sim ():
    num_simulacion = []
    for root, dirs, files in os.walk(RUTA_MUESTREO_SIM):
        for file in files:
            num_sim = file.replace("_SIMULACION_CA3.dat", "").replace("_SIMULACION_CA1.dat", "")
            num_simulacion.append(int (num_sim))
    num_sim = 0 if len(num_simulacion) == 0 else max(num_simulacion)
    return num_sim

def calcula_num_graf ():
    num_grafica = []
    for root, dirs, files in os.walk(RUTA_GRAFICOS_SIM):
        for file in files:
            num_grafica.append(int (file.replace("_SIMULACION.png","")))
    num_graf = 0 if len(num_grafica) == 0 else max(num_grafica)
    return num_graf


def grafica_porcentajes_zona():
    porcentajes_banda = (prueba_frecuencia_dominante(RUTA_MUESTREO_SIM, "CA3", 100))
    porcentajes_banda2 = (prueba_frecuencia_dominante(RUTA_MUESTREO_REAL_M,"muestra_", 100))
    porcentajes_banda3 = (prueba_frecuencia_dominante(RUTA_MUESTREO_SIM, "CA1", 100))
    bandas_frecuencia = ["Delta", "Theta","Alfa","Beta","Gamma baja","Gamma alta"]
    porcentajes1 = regresa_arreglo(porcentajes_banda)
    porcentajes2 = regresa_arreglo(porcentajes_banda2)
    porcentajes3 = regresa_arreglo(porcentajes_banda3)
    N = 6
    ind = np.arange(N)
    width = 1.2
    plt1.figure()
    plt1.rc('font', size=12)
    plt1.bar(ind + 0.25,porcentajes2, width = 0.25, color='#086A87', label = r"""$Zona \; CA3 \;-\; Datos \;Reales$""" )
    plt1.bar(ind + 0.50,porcentajes1, width = 0.25, color='#688A08',label = r"""$Zona \; CA3 \;-\;  Simulaci\'on$""")
    plt1.bar(ind + 0.75,porcentajes3, width = 0.25, color='#8A0868',label = r"""$Zona \; CA1 \;-\;  Simulaci\'on$""")
    plt1.xticks(ind + width/2.,bandas_frecuencia, fontweight='bold', size=12)
    plt1.xlabel("Bandas de Frecuencia")
    plt1.ylabel("Porcentaje de Energia")
    plt1.margins(0.025)
    plt1.legend(bbox_to_anchor=(0.70, 0.95), loc=2, borderaxespad=0., fontsize='12')
    plt1.grid(True)
    plt1.show()

def prueba_unitaria(archivo):
    senial = np.loadtxt(archivo)
    rec_a, rec_d = descomposicion_signal(senial, 'sym9')
    p= calcula_porcentaje_energia(rec_a, rec_d,senial)
    grafica_porcentajes_prueba(p)

def prueba_frecuencia_dominante(ruta, zona, numero):
    bandas_frecuencia = {"Higher Gamma" : 0, "Lower Gamma": 0, "Beta":0,  "Alfa": 0, "Theta":0, "Delta":0}
    for root, dirs, files in os.walk(ruta):
        num_archivos = 0
        for archivo in  files:
            if zona in archivo:
                num_archivos += 1
                if zona == "muestra_":
                    senial = np.loadtxt(ruta + zona +str(num_archivos)+ ".dat")
                else:
                    senial = np.loadtxt(ruta +str(num_archivos)+ "_SIMULACION_"+ zona +".dat")
                rec_a, rec_d = descomposicion_signal(senial, 'sym9')
                porcentaje_bandas = calcula_porcentaje_energia(rec_a, rec_d,senial)
                for k,v in porcentaje_bandas.items():
                    bandas_frecuencia[k]+=v
            if num_archivos == numero:
                break

        for k,v in bandas_frecuencia.items():
            bandas_frecuencia[k] = v / num_archivos

    return  bandas_frecuencia

def grafica_funciones_ventana():

    plt.subplots_adjust(wspace=0.4, hspace= 0.6)
    plt.subplot(221)
    window = np.bartlett(51)
    plt.plot(window, color="black")
    plt.title("Ventana Bartlett", fontweight='bold', fontsize='11')
    plt.ylabel("Amplitud")
    plt.xlabel("Muestra")
    plt.grid(True)

    plt.subplot(222)
    window = np.blackman(51)
    plt.plot(window, color="black")
    plt.title("Ventana Blackman ", fontweight='bold', fontsize='11')
    plt.ylabel("Amplitud")
    plt.xlabel("Muestra")
    plt.grid(True)

    plt.subplot(223)
    window = np.hamming(51)
    plt.plot(window, color="black")
    plt.title("Ventana Hamming", fontweight='bold', fontsize='11')
    plt.ylabel("Amplitud")
    plt.xlabel("Muestra")
    plt.grid(True)

    plt.subplot(224)
    window = np.hanning(51)
    plt.plot(window, color="black")
    plt.title("Ventana Hanning", fontweight='bold', fontsize='11')
    plt.ylabel("Amplitud")
    plt.xlabel("Muestra")
    plt.grid(True)

    plt.show()



def grafica_resolucion():

    plt.subplots_adjust(wspace=0.4, hspace= 0.6)
    ax =plt.subplot(121)
    plt.title("Ventana Ancha", fontweight='bold', fontsize='28')
    plt.ylabel("Frecuencia",fontsize='20')
    plt.xlabel("Tiempo", fontsize='20')
    plt.xlim(0,10)
    plt.ylim(0,100)
    plt.yticks([i*5 for i in range(0,20)])
    gridlines = ax.get_xgridlines() + ax.get_ygridlines()
    for line in gridlines:
        line.set_linestyle('-')
    plt.grid(True)
    ax.set_yticklabels("")
    ax.set_xticklabels("")

    ax = plt.subplot(122)
    plt.title("Ventana Estrecha ", fontweight='bold', fontsize='28')
    plt.ylabel("Frecuencia",fontsize='20')
    plt.xlabel("Tiempo", fontsize='20')
    plt.ylim(0,10)
    plt.xlim(0,100)
    plt.xticks([i*5 for i in range(0,20)])
    gridlines = ax.get_xgridlines() + ax.get_ygridlines()
    for line in gridlines:
        line.set_linestyle('-')
    plt.grid(True)
    ax.set_yticklabels("")
    ax.set_xticklabels("")

    plt.show()


def dibuja_wavelet():
    wavelet = ["haar", 'db6', 'bior1.3', 'coif1', 'sym9', 'rbio1.5']
    i = 1
    iterations = 5
    plt.subplots_adjust(wspace=0.4, hspace= 0.4)
    for fun in wavelet:
            try:

                wavelet = pywt.Wavelet(fun)
            except StopIteration:
                    break
            if fun not in ["bior1.3", "rbio1.5"]:
                phi, psi, x = wavelet.wavefun(iterations)
            else:
                phi, psi, phi_r, psi_r, x = wavelet.wavefun(iterations)
            plt.subplot(2,3,i)
            plt.title("Ondeleta "+fun,fontweight='bold')
            plt.plot(x, phi,color="black" )
            plt.xlim(min(x), max(x))
            i += 1
            plt.grid(True)
    plt.show()

def regresa_arreglo(map):
    bandas_frecuencia = ["Delta", "Theta","Alfa","Beta","Lower Gamma","Higher Gamma"]
    porcentaje = [0]*6
    for k, v in map.items():
        indice = bandas_frecuencia.index(k)
        porcentaje[indice] = v
    return porcentaje

def grafica_porcentaje_muestras(ruta, zona):
    x = [1,2,3,4,5,6]
    bandas_frecuencia = ["Delta", "Theta","Alfa","Beta","Gamma baja","Gamma alta"]
    muestra_5 = regresa_arreglo(prueba_frecuencia_dominante(ruta, zona, 5))
    muestra_25 = regresa_arreglo(prueba_frecuencia_dominante(ruta, zona, 25))
    muestra_50 = regresa_arreglo(prueba_frecuencia_dominante(ruta, zona, 50))
    muestra_75 = regresa_arreglo(prueba_frecuencia_dominante(ruta, zona, 75))
    muestra_100 = regresa_arreglo(prueba_frecuencia_dominante(ruta, zona, 100))
    plt.figure()
    plt.rc('font', size=12)
    plt.ylabel("Porcentaje de Energia")
    plt.xlabel("Bandas de Frecuencia")
    plt.xlim(0.8,6.2)
    plt.ylim(0,50)
    ind = np.arange(1,7)
    width = 0.1
    plt.xticks(ind + width/2.,bandas_frecuencia, fontweight='bold', size=9)
    plt.plot(x,muestra_5,'p-', color="#08088A", label = "5 muestras")
    plt.plot(x,muestra_25,'o-', color="red", label = "25 muestras")
    plt.plot(x,muestra_50,'s-', color="green", label = "50 muestras")
    plt.plot(x,muestra_75,'*-', color="#DBA901", label = "75 muestras")
    plt.plot(x,muestra_100,'D-', color="#DF0174", label = "100 muestras")
    plt.legend(bbox_to_anchor=(0.70, 0.95), loc=2, borderaxespad=0., fontsize='12')
    plt.grid(True)
    plt.show()

def muestreo_spikes(ruta, zona):
    for root, dirs, files in os.walk(ruta):
        num_archivos = 0
        num_spikes=0
        for archivo in  files:
            if zona in archivo:
                num_archivos += 1
                spikes = np.loadtxt(ruta+ archivo)
                num_spikes += sum(spikes)

    promedio= num_spikes / num_archivos
    return promedio

def grafica_porcentajes_prueba(p):
    bandas_frecuencia = ["Delta", "Theta","Alfa","Beta","Gamma baja","Gamma alta"]
    porcentajes1 = regresa_arreglo(p)
    N = 6
    ind = np.arange(N)
    width = 1.2
    plt1.figure(1)
    plt1.rc('font', size=12)
    plt1.bar(ind,porcentajes1, color='#6E6E6E', label = r"""$Zona \; CA3 \;-\; Datos \;Reales$""" )
    plt1.xticks(ind + width/2.,bandas_frecuencia, fontweight='bold', size=12)
    plt1.xlabel("Bandas de Frecuencia")
    plt1.ylabel("Porcentaje de Energia")
    plt1.margins(0.025)
    plt1.legend(bbox_to_anchor=(0.70, 0.95), loc=2, borderaxespad=0., fontsize='12')
    plt1.grid(True)
    plt1.show()

def grafica_senial_por_filtros(senial_filtrada):
    fig = plt.figure()
    plt.rc('font', size=10)
    ax = plt.subplot(511)
    ax.plot(senial_filtrada[0],color="black")
    ax.set_xlabel("Segundos")
    ax.set_ylabel("Voltage (mV)")
    ax.set_title("Banda Delta",weight = 'bold')
    ax = plt.subplot(512)
    ax.plot(senial_filtrada[1],color="black")
    ax.set_xlabel("Segundos")
    ax.set_ylabel("Voltage (mV)")
    ax.set_title("Banda Theta",weight = 'bold')
    ax = plt.subplot(513)
    ax.plot(senial_filtrada[2],color="black")
    ax.set_xlabel("Segundos")
    ax.set_ylabel("Voltage (mV)")
    ax.set_title("Banda Alfa",weight = 'bold')
    ax = plt.subplot(514)
    ax.plot(senial_filtrada[3],color="black")
    ax.set_xlabel("Segundos")
    ax.set_ylabel("Voltage (mV)")
    ax.set_title("Banda Beta",weight = 'bold')
    ax = plt.subplot(515)
    ax.plot(senial_filtrada[4],color="black")
    ax.set_xlabel("Segundos")
    ax.set_ylabel("Voltage (mV)")
    ax.set_title("Banda Gamma",weight = 'bold')
    fig.subplots_adjust(top=0.95,bottom = 0.05 , right=0.90, left=0.1,hspace = 0.8, wspace = 0.99)
    plt.show()

def promedio_energia_muestras(ruta,zona, numero):
    bandas_frecuencia=[0] * 5
    for root, dirs, files in os.walk(ruta):
        num_archivos = 0
        for archivo in  files:
            if zona in archivo:
                num_archivos += 1
                if zona == "muestra_":
                    senial = np.loadtxt(ruta + zona +str(num_archivos)+ ".dat")
                else:
                    senial = np.loadtxt(ruta +str(num_archivos)+ "_SIMULACION_"+ zona +".dat")
                senial = normalizacion_datos(senial)
                senial_filtrada = filtros_bandas(senial,FRECUENCIA_MUESTREO)
                energias_bandas = calcula_porcentaje_energia_fil(senial,senial_filtrada)
                for i, energia in enumerate(energias_bandas):
                    bandas_frecuencia[i]+= energia
            if num_archivos == numero:
                break

        for i, energia in enumerate(energias_bandas):
            bandas_frecuencia[i] =  bandas_frecuencia[i] / num_archivos

    return  bandas_frecuencia

def grafica_porcentaje_muestras_fil(ruta, zona):
    x = [1,2,3,4,5]
    bandas_frecuencia = ["Delta", "Theta","Alfa","Beta","Gamma"]
    muestra_5 = promedio_energia_muestras(ruta, zona, 5)
    muestra_25 = promedio_energia_muestras(ruta, zona, 25)
    muestra_50 = promedio_energia_muestras(ruta, zona, 50)
    muestra_75 = promedio_energia_muestras(ruta, zona, 75)
    muestra_100 = promedio_energia_muestras(ruta, zona, 100)
    plt.figure()
    plt.rc('font', size=12)
    plt.ylabel("Porcentaje de Energia")
    plt.xlabel("Bandas de Frecuencia")
    plt.xlim(0.8,5.2)
    plt.ylim(0,50)
    ind = np.arange(1,7)
    width = 0.1
    plt.xticks(ind + width/2.,bandas_frecuencia, fontweight='bold', size=9)
    plt.plot(x,muestra_5,'p-', color="#08088A", label = "5 muestras")
    plt.plot(x,muestra_25,'o-', color="red", label = "25 muestras")
    plt.plot(x,muestra_50,'s-', color="green", label = "50 muestras")
    plt.plot(x,muestra_75,'*-', color="#DBA901", label = "75 muestras")
    plt.plot(x,muestra_100,'D-', color="#DF0174", label = "100 muestras")
    plt.legend(bbox_to_anchor=(0.70, 0.95), loc=2, borderaxespad=0., fontsize='12')
    plt.grid(True)
    plt.show()


def grafica_porcentajes_zona_fil():
    porcentajes_banda = promedio_energia_muestras(RUTA_MUESTREO_REAL_M,"muestra_", 100)
    porcentajes_banda2 = promedio_energia_muestras(RUTA_MUESTREO_SIM, "CA3", 100)
    porcentajes_banda3 = promedio_energia_muestras(RUTA_MUESTREO_SIM, "CA1", 100)
    bandas_frecuencia = ["Delta", "Theta","Alfa","Beta","Gamma"]
    N = 5
    ind = np.arange(N)
    width = 1.2
    plt1.figure()
    plt1.rc('font', size=12)
    plt1.bar(ind + 0.25,porcentajes_banda, width = 0.25, color='#6E6E6E', label = r"""$Zona \; CA3 \;-\; Datos \;Reales$""" )
    plt1.bar(ind + 0.50,porcentajes_banda2, width = 0.25, color='#0A122A',label = r"""$Zona \; CA3 \;-\;  Simulaci\'on$""")
    plt1.bar(ind + 0.75,porcentajes_banda3, width = 0.25, color='#3B0B39',label = r"""$Zona \; CA1 \;-\;  Simulaci\'on$""")
    plt1.xticks(ind + width/2.,bandas_frecuencia, fontweight='bold', size=12)
    plt1.xlabel("Bandas de Frecuencia")
    plt1.ylabel("Porcentaje de Energia")
    plt1.margins(0.025)
    plt1.legend(bbox_to_anchor=(0.70, 0.95), loc=2, borderaxespad=0., fontsize='12')
    plt1.grid(True)
    plt1.show()

def grafica_porcentajes_senial_epi_igual(ruta):
    x = [1,2,3,4,5,6]
    bandas_frecuencia = ["Delta", "Theta","Alfa","Beta","Gamma baja","Gamma alta"]
    fig = plt.figure(figsize = (15, 8))
    ax = plt.subplot(121)
    plt.rc('font', size=12)
    plt.title("Zona CA3")
    plt.ylabel("Porcentaje de Energia")
    plt.xlabel("Bandas de Frecuencia")
    ind = np.arange(1,7)
    width = 0.1
    plt.grid(True)
    plot_senial(ruta, "CA3", x, 0, 1)
    matplotlib.pylab.legend(loc='upper right',  fontsize='10')
    plt.xticks(ind + width/2.,bandas_frecuencia, fontweight='bold', size=9)
    plt.xlim(0.5,6.5)
    ax1 = plt.subplot(122)
    plt.rc('font', size=12)
    plt.title("Zona CA1")
    plt.ylabel("Porcentaje de Energia")
    plt.xlabel("Bandas de Frecuencia")
    ind = np.arange(1,7)
    width = 0.1
    plt.xticks(ind + width/2.,bandas_frecuencia, fontweight='bold', size=9)
    plt.grid(True)
    plot_senial(ruta, "CA1", x, 2 ,3)
    plt.xlim(0.5,6.5)
    fig.subplots_adjust(top=0.90,bottom = 0.1 , right=0.95, left=0.05,wspace = 0.2)
    matplotlib.pylab.legend(loc='upper right',  fontsize='10')
    matplotlib.pylab.show()


def plot_senial(ruta, zona, x, ind1, ind2):
    for root, dirs, files in os.walk(ruta):
        for archivo in  sorted(files):
            if zona in archivo:

                info = archivo.split("_")
                perdida_ex = info[ind1] if "G" not in archivo else info[ind1 + 1]
                perdida_in = info[ind2] if "G" not in archivo else info[ind2 + 1]
                senial = np.loadtxt(ruta + archivo)
                rec_a, rec_d = descomposicion_signal(senial, 'sym9')
                porcentaje_bandas = calcula_porcentaje_energia(rec_a, rec_d,senial)
                muestra = regresa_arreglo(porcentaje_bandas)
                etiqueta = "Muerte Neuronal (EX = " + str(perdida_ex) + "% , IN = "+ str(perdida_in) + "% )"
                matplotlib.pylab.plot(x,muestra,'o-', label=str(etiqueta) )

    muestra_100 = regresa_arreglo(prueba_frecuencia_dominante(RUTA_MUESTREO_SIM, zona, 100))
    matplotlib.pylab.plot(x,muestra_100,'o-', label= "Estado Saludable (sin muerte neuronal)" , linewidth=2.0, color="black")


def plot_datos_perdida(ruta, nombre_arch):
    tiempo_sim = [float("{0:.3f}".format(TIEMPO_INCREMENTO * i)) for i in range(TIEMPO_ITERA_SIM - 1)]
    senial = np.loadtxt(ruta + nombre_arch)
    plt.subplots_adjust(wspace=0.8, hspace= 0.5)
    plt.subplot(211)
    nombre_zona = nombre_arch.split("_")
    zona = nombre_zona[len(nombre_zona) - 1].replace(".dat","")
    plt.title("Zona " + str(zona), fontweight='bold')
    plt.plot(tiempo_sim,senial, color="black")
    plt.xlabel("Segundos")
    plt.ylabel("miliVolts")
    plt.ylim(-100,-30)
    plt.grid()
    plt.subplot(212)
    plt.title("Espectro de Frecuencia", fontweight='bold')
    f, a= filtraSignal(senial,FRECUENCIA_MUESTREO)
    plt.plot(f,a,color="black")
    plt.xlabel("Frecuencia")
    plt.ylabel("Amplitud")
    plt.xlim(0,50)
    plt.grid()
    plt.savefig(RUTA_GRAFICOS_SIM_P + "seniales/" + nombre_arch.replace(".dat","_img")+'.png')
    plt.clf()

def genera_ima_dat_perdida(ruta):
    for root, dirs, files in os.walk(ruta):
        for nombre_arch in  files:
            plot_datos_perdida(root + "/", nombre_arch)
import matplotlib.pyplot as plt
import pywt
import numpy as np


# mode = pywt.Modes.smooth
from configs.variables_sim import TIEMPO_ITERA_SIM, TIEMPO_INCREMENTO

bandas_frecuencias = {"D1": "Gamma Alta \n(150 - 75 hz)", "D2":
                     "Gamma Baja \n(75 - 37.5 hz)", "D3" : "Beta \n(37.5 - 18.7 hz)",
                     "D4": "Alfa \n(18.7 - 9.3 hz)", "D5":"Theta \n(9.3 - 4.6 hz)",
                     "A5":"Delta"}

bandas_frecuencia = {"D1": "Higher Gamma", "D2": "Lower Gamma", "D3" : "Beta", "D4": "Alfa", "D5":"Theta", "A5":"Delta"}


def normalizacion_datos(coefecientes):
    coefecientes = np.array(coefecientes)
    media = coefecientes.mean()
    desviacion = np.std(coefecientes)

    for x in range(len(coefecientes)):
      coefecientes[x] =  (coefecientes[x] - media) / desviacion

    return coefecientes


def calcula_energia(senial):
    energia = 0
    ts = TIEMPO_INCREMENTO
    for n in range(len(senial)):
        energia += abs(senial[n]) ** 2
    return ts * energia

def calcula_porcentaje_energia(rec_a, rec_d,senial):
    senial = normalizacion_datos(senial)
    total_energia_senial = calcula_energia(senial)
    porcentaje_energia_sub_bandas = {}
    porcentajes = []
    banda_domina = ""
    for i in range(1, len(rec_d) + 1):
        sub_banda = rec_d[i - 1][0:TIEMPO_ITERA_SIM - 1]
        energia_sub_banda =  calcula_energia(sub_banda)
        porcentaje = energia_sub_banda / total_energia_senial * 100
        porcentaje_energia_sub_bandas[bandas_frecuencia["D" + str(i)]] = porcentaje
        porcentajes.append(porcentaje)

    sub_banda = rec_a[4][0:TIEMPO_ITERA_SIM - 1]
    energia_sub_banda = calcula_energia(sub_banda)
    porcentaje = energia_sub_banda / total_energia_senial * 100
    porcentaje_energia_sub_bandas[bandas_frecuencia["A5"]] = porcentaje
    porcentajes.append(porcentaje)
    for k, v in porcentaje_energia_sub_bandas.items():
        if v == max(porcentajes):
            banda_domina= k

    #print "BANDA QUE DOMINA : ", banda_domina
    #print sum(porcentajes)
    return porcentaje_energia_sub_bandas


def descomposicion_signal(data, w):
    data = normalizacion_datos(data)
    w = pywt.Wavelet(w)
    a = data
    ca = []
    cd = []
    for i in range(5):
        (a, d) = pywt.dwt(a, w, 'db1')
        ca.append(a)
        cd.append(d)

    rec_a = []
    rec_d = []

    for i, coeff in enumerate(ca):
        coeff_list = [coeff, None] + [None] * i
        rec_a.append(pywt.waverec(coeff_list, w))

    for i, coeff in enumerate(cd):
        coeff_list = [None, coeff] + [None] * i
        rec_d.append(pywt.waverec(coeff_list, w))

    return rec_a, rec_d

def plot_signal_decomp(data,rec_a, rec_d):
    senial_norm = normalizacion_datos(data)
    plt.clf()
    fig = plt.figure(figsize = (15, 8))
    plt.rc('font', size=8)
    fig.subplots_adjust(top=0.95,bottom = 0.05 , right=0.90, left=0.05,hspace = 0.5, wspace = 0.99)
    ax_main = plt.subplot2grid((7, 8),  (0, 0), colspan=8)
    ax_main.set_title(r"""$Se\~nal\;Original$""",weight = 'bold',fontsize=14)
    ax_main.plot(data,color="black")
    ax_main.set_xlim(0, len(data) - 1)

    ax_main = plt.subplot2grid((7, 8),  (1, 0), colspan=8)
    ax_main.set_title(r"""$Se\~nal\;Normalizada$""",weight = 'bold',fontsize=14)
    ax_main.plot(senial_norm,color="black")
    ax_main.set_xlim(0, len(data) - 1)

    for i, y in enumerate(rec_a):
        ax = plt.subplot2grid((7, 8),  (i+2, 0) , colspan=4)
        ax.plot(y, color="black")
        ax.set_xlim(0, len(y) - 1)
        ax.set_ylabel("A%d" % (i + 1),weight = 'bold' ,fontsize=10)

    for i, y in enumerate(rec_d):
        ax = plt.subplot2grid((7, 8),  (i+2, 4), colspan=4)
        ax.plot(y, color="black")
        ax.set_xlim(0, len(y) - 1)
        ax.set_ylabel("D%d" % (i + 1),weight = 'bold',fontsize=10)
        axes2 = ax.twinx()
        axes2.set_yticklabels("")
        axes2.set_ylabel(bandas_frecuencias["D%d" % (i + 1)],
                                rotation=0,weight = 'bold', labelpad=50,fontsize=11)

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()
    #return fig


def analisis_tipos_wavelet(senial):

    resultados = {}
    plot_data = ['db','sym','coif', 'bior', 'rbio']

    for family in plot_data:
        print "Familia : " ,family

        wnames = pywt.wavelist(family)

        for wavelet in wnames:
            rec_a, rec_d= descomposicion_signal(senial, wavelet)
            energias_bandas, porcentajes = calcula_porcentaje_energia(rec_a, rec_d,senial)
            energia_total = sum(porcentajes)
            resultados[wavelet] = energia_total
            print "Wavelet madre :", wavelet, "PROMEDIO ",energia_total



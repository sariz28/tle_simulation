import numpy as np
from scipy import signal, arange
from herramientas_wavelet import normalizacion_datos, calcula_energia


def filtra_signal(s, freq_sample):
    freq_n = int(float(freq_sample) / float(2))
    orden_filtro = 5
    caida_freq = 34
    corte_inf = float(1) / float(freq_n)
    corte_sup = float(50) / float(freq_n)
    longitud_senal = len(s)
    filtro_recursivo_b_low, filtro_recursivo_a_low = signal.cheby2(orden_filtro, caida_freq, corte_sup, "low")
    filtro_recursivo_b_high, filtro_recursivo_a_high = signal.cheby2(orden_filtro, caida_freq, corte_inf, "high")
    t_filtrado = signal.lfilter(filtro_recursivo_b_low,filtro_recursivo_a_low,s)
    t_filtrado = signal.lfilter(filtro_recursivo_b_high,filtro_recursivo_a_high,t_filtrado)

    ventana= np.hamming(longitud_senal)
    w = np.fft.fft(t_filtrado * ventana)
    frecuencia = arange(0, freq_n, float(freq_sample)/float(longitud_senal))
    amplitud= abs(w[0:len(w) / 2])
    return frecuencia,amplitud

def filtraSignalAux (s,freq_sample):
    freq_n = int(float(freq_sample) / float(2))
    longitud_senal= len(s)
    ventana= np.hamming(longitud_senal)
    w = np.fft.fft(s * ventana)
    frecuencia = arange(0,freq_n,float(freq_sample)/float(longitud_senal))
    amplitud= abs(w[0:len(w) / 2])
    return frecuencia,amplitud

def filtros_bandas(senial,freq_sample):
    fn = float(freq_sample)/2
    orden = 5
    caida = 34

    corte_01_inf = float(0.5)/fn
    corte_01_sup = float(6)/fn
    corte_02_inf = float(3)/fn
    corte_02_sup = float(10)/fn
    corte_03_inf = float(7)/fn
    corte_03_sup = float(15)/fn
    corte_04_inf = float(11)/fn
    corte_04_sup = float(36)/fn
    corte_05_inf = float(25)/fn
    corte_05_sup = float(115)/fn
    senial_filtrada = []

    iir_b_delta_low, iir_a_delta_low = signal.cheby2(orden, caida, corte_01_sup, 'low')
    iir_b_delta_high,iir_a_delta_high = signal.cheby2(orden, caida, corte_01_inf, 'high')

    iir_b_theta, iir_a_theta = signal.cheby2(orden, caida, [corte_02_inf, corte_02_sup], 'bandpass')
    iir_b_alfa, iir_a_alfa = signal.cheby2(orden, caida, [corte_03_inf, corte_03_sup], 'bandpass')
    iir_b_beta, iir_a_beta = signal.cheby2(orden, caida, [corte_04_inf, corte_04_sup], 'bandpass')
    iir_b_gamma, iir_a_gamma = signal.cheby2(orden, caida, [corte_05_inf, corte_05_sup], 'bandpass')

    delta_filtrado = signal.lfilter( iir_b_delta_low, iir_a_delta_low ,senial)
    delta_filtrado = signal.lfilter(iir_b_delta_high,iir_a_delta_high, delta_filtrado)
    senial_filtrada.append(delta_filtrado)

    theta_filtrado = signal.lfilter(iir_b_theta, iir_a_theta,senial)
    senial_filtrada.append(theta_filtrado)

    alfa_filtrado = signal.lfilter(iir_b_alfa, iir_a_alfa,senial)
    senial_filtrada.append(alfa_filtrado)

    beta_filtrado = signal.lfilter(iir_b_beta, iir_a_beta,senial)
    senial_filtrada.append(beta_filtrado)

    gamma_filtrado = signal.lfilter(iir_b_gamma, iir_a_gamma,senial)
    senial_filtrada.append(gamma_filtrado)

    return senial_filtrada


def calcula_porcentaje_energia_fil(senial, senial_filtrada):
    senial = normalizacion_datos(senial)
    total_energia_senial = calcula_energia(senial)
    porcentaje_energia_sub_bandas = []
    for banda_frecuencia in senial_filtrada :
        energia_sub_banda =  calcula_energia(banda_frecuencia)
        porcentaje_energia_sub_bandas.append((energia_sub_banda / total_energia_senial) * 100)
    return porcentaje_energia_sub_bandas

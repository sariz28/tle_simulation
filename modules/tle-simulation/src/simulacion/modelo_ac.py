__author__ = 'sara'

from configs.parametros import E_ACTIVO, TERMINO_ESTADO, E_REFRACTARIO, E_INACTIVO
from configs.variables_sim import NUM_NEURONAS_EX, NUM_TOTAL_NEURONAS_EX, NUM_NEURONAS_IN, TIPO_I, TIPO_E, \
    TIEMPO_ITERA_SIM, TIEMPO_ACTUALIZACION
from graficos.graficos import dibujaAutomata, dibuja_senial
from hipocampo.claseNeurona import Neurona
from zonaResultados import ZonaHipocampoResultados
from Tkconstants import ALL
import numpy as np

def calculaIndice(numero):
    i=int(np.floor(numero/NUM_NEURONAS_EX))
    j=numero%NUM_NEURONAS_EX
    return [i,j]


def asignaPulsos(num_pulsos, perdida_ex, es_perdida):
    neuronas_ex_pulsos = [[0 for posy in range(NUM_NEURONAS_EX)] for posx in range(NUM_NEURONAS_EX)]
    num_pulsos_asignados = 0
    if es_perdida :
        while (num_pulsos_asignados < num_pulsos ):
            idNx = np.random.randint(NUM_NEURONAS_EX - 1)
            idNy = np.random.randint(NUM_NEURONAS_EX - 1)
            if [idNx, idNy] not in perdida_ex:
                neuronas_ex_pulsos[idNx][idNy]+=1
                num_pulsos_asignados += 1
    else :
        for i in range(num_pulsos):
            idNx, idNy=calculaIndice(np.random.randint(NUM_TOTAL_NEURONAS_EX - 1))
            neuronas_ex_pulsos[idNx][idNy]+=1
    return neuronas_ex_pulsos


def obtiene_vecinos_por_celula(x,y,aux1,listaCell,aux2, aux3,aux4 ):
    posx = NUM_NEURONAS_EX - aux1 if x==0 else x * 3 - aux1
    posy = NUM_NEURONAS_EX - aux3 if y==0 else y * 3 - aux1  + aux4
    posx = posx if posx >= 0 else NUM_NEURONAS_EX  + posx
    posy = posy if posy >=0 else NUM_NEURONAS_EX - 1
    vecinos = []
    for xi in listaCell:
        ny = posy if xi== aux2 else posy-1  if posy-1 >= 0 else NUM_NEURONAS_EX - 1
        for yi in range(xi):
            vecinos.append([posx,ny])
            ny= 0 if ny+1 == NUM_NEURONAS_EX else ny+1
        posx = 0 if posx+1 == NUM_NEURONAS_EX else posx+1
    return vecinos


def obtiene_vecinos(p):
    vecinos_in={}
    vecinos_ex={}
    for x in range(NUM_NEURONAS_IN):
        for y in range(NUM_NEURONAS_IN):
            vecinos_ex[x, y]=obtiene_vecinos_por_celula(x, y,p.AUX_1_RADIO_IN,p.RADIO_IN_CELL, p.AUX_2_RADIO_IN,p.AUX_3_RADIO_IN,p.AUX_4_RADIO_IN )
            vecinos_in[x, y]=obtiene_vecinos_por_celula(x, y,p.AUX_1_RADIO_EX, p.RADIO_EX_CELL, p.AUX_2_RADIO_EX,p.AUX_3_RADIO_EX,p.AUX_4_RADIO_EX)
    return vecinos_ex,vecinos_in

def obtieneAferenciasIn(x,y,vecinos):
    return vecinos[x,y]

def obtieneAferenciasEx(x,y,vecinos):
    aferencias=[]
    for celula, lista_vecinos in vecinos.iteritems():
        if [x,y] in lista_vecinos:
            aferencias.append(list(celula))
    return aferencias


def obtieneAferencias(x,y,tipo,vecinos):
    if tipo== TIPO_I:
        return obtieneAferenciasIn(x,y,vecinos)
    else:
        return obtieneAferenciasEx(x,y,vecinos)


def calcula_neuronas(limiteX, limiteY, porcentaje):
    num_total_neuronas_x= limiteX[1] - limiteX[0] + 1
    num_total_neuronas_y= limiteY[1] - limiteY[0] + 1
    total_neuronas_perdidas = int (round((num_total_neuronas_x * num_total_neuronas_y * porcentaje) / 100.0))
    lista_neuronas = []
    while (len(lista_neuronas) < total_neuronas_perdidas):
        idNx = np.random.randint(limiteX[0], limiteX[1] + 1)
        idNy = np.random.randint(limiteY[0], limiteY[1] + 1)
        if [idNy, idNx] not in lista_neuronas:
            lista_neuronas.append([idNy, idNx])
    return lista_neuronas

def calcula_neuronas_perdias_zonas (zonas_afectadas,subzonas, tipo):
    lista_neuronas = []
    num_neuronas = NUM_NEURONAS_EX - 1 if tipo == TIPO_E else NUM_NEURONAS_IN - 1
    if zonas_afectadas["all"] > 0 :
        lista_neuronas = calcula_neuronas([0,num_neuronas],[0,num_neuronas],zonas_afectadas["all"])
    else:
        zonas_afectadas.pop("all")
        for k,v in zonas_afectadas.items():
            limite_subzona = subzonas[k].rango_ex if tipo == TIPO_E  else  subzonas[k].rango_in
            lista_neuronas += calcula_neuronas(limite_subzona["rango_x"],limite_subzona["rango_y"], v)
    return lista_neuronas


def perdida_neuronal(param):
    zonas_afectadas_ex = calcula_neuronas_perdias_zonas(param.zonas_afectadas_ex, param.subZonas,TIPO_E)
    zonas_afectadas_in = calcula_neuronas_perdias_zonas(param.zonas_afectadas_in,param.subZonas, TIPO_I)
    return  zonas_afectadas_ex,  zonas_afectadas_in


def obtiene_sub_zona(fila, columna, listaSubZonas, tipo):
    nombre_sub_zona= ""
    for sub_zona_key, subzona  in listaSubZonas.items():
        rango_limites = subzona.rango_ex if tipo == TIPO_E else subzona.rango_in
        rango_x = rango_limites["rango_x"]
        rango_y = rango_limites["rango_y"]
        if columna >= rango_x[0] and columna <= rango_x[1]:
            if fila >= rango_y[0]  and fila <= rango_y[1]:
                nombre_sub_zona = sub_zona_key
                break
    return  nombre_sub_zona

def esNeuronaMuerta(x,y,neuronas_perdida):
    if [x,y] in neuronas_perdida:
        return True
    else:
        return False

def inicializaNeuronas(tipo,numNeuronas,listaVecinos,p, neuronas_perdidas):
    lattice = np.array([[Neurona(tipo,x,y,obtieneAferencias(x,y,tipo,listaVecinos), p,
                    obtiene_sub_zona(x, y, p.subZonas, tipo), esNeuronaMuerta(x,y,neuronas_perdidas))
                    for y in range(numNeuronas)] for x in range(numNeuronas)])
    return lattice


def generaCondicionesIniciales(lattice_ex,lattice_in, num_pulsos, perdida_ex, es_perdida):
     pulsos_ex_ext=asignaPulsos(num_pulsos, perdida_ex, es_perdida)
     num_ap_ex = 0
     for i in range (NUM_NEURONAS_EX):
        for j in range (NUM_NEURONAS_EX):
             neurona_ex = lattice_ex[i][j]
             if neurona_ex.muerta == False:
                 neurona_ex.n_ext_e = pulsos_ex_ext[i][j]
                 aplica_funcion_evolucion(neurona_ex, 0)
                 if neurona_ex.getEstado() == E_ACTIVO \
                    and neurona_ex.tiempo_estado== neurona_ex.pa.t_activo - 1:
                      num_ap_ex+=1

     for x in range(NUM_NEURONAS_IN):
        for y in range(NUM_NEURONAS_IN):
            neurona_in= lattice_in[x][y]
            if neurona_in.muerta == False:
                aplica_funcion_evolucion(neurona_in, 0)
     return lattice_ex,lattice_ex, num_ap_ex

def elimina_vecinos(vecinos, perdida_neuronal_ex, perdida_neuronal_in):
    for x in range(NUM_NEURONAS_IN):
        for y in range(NUM_NEURONAS_IN):
            if [x,y] in perdida_neuronal_in:
                vecinos[x,y]= []
            else:
                for vecino in vecinos[x,y]:
                    if vecino in perdida_neuronal_ex:
                        vecinos[x,y].remove(vecino)
    return vecinos

def aplica_perdida_neuronal(parametros, vecinos_ex, vecinos_in):
    perdida_neuronal_ex = []
    perdida_neuronal_in = []
    if parametros.perdida_neuronal:
        perdida_neuronal_ex, perdida_neuronal_in = perdida_neuronal(parametros)
        vecinos_ex = elimina_vecinos (vecinos_ex, perdida_neuronal_ex, perdida_neuronal_in)
        vecinos_in = elimina_vecinos (vecinos_in, perdida_neuronal_ex, perdida_neuronal_in)
    return  vecinos_ex, vecinos_in, perdida_neuronal_ex, perdida_neuronal_in

def inicializaModeloAC(parametros,pulsos):
    VECINOS_EX,VECINOS_IN = obtiene_vecinos(parametros)
    VECINOS_EX,VECINOS_IN, perdida_ex, perdida_in = aplica_perdida_neuronal(parametros, VECINOS_EX, VECINOS_IN)
    LATTICE_EX_CELL=inicializaNeuronas(TIPO_E,NUM_NEURONAS_EX,VECINOS_EX,parametros, perdida_ex)
    LATTICE_IN_CELL=inicializaNeuronas(TIPO_I,NUM_NEURONAS_IN,VECINOS_IN,parametros, perdida_in)
    LATTICE_EX_CELL,LATTICE_EX_CELL, num_ap_ex = generaCondicionesIniciales(LATTICE_EX_CELL,LATTICE_IN_CELL,pulsos, perdida_ex, parametros.perdida_neuronal)
    return LATTICE_EX_CELL, LATTICE_IN_CELL, num_ap_ex, perdida_ex, perdida_in


def calcula_ipsp(neurona,i,zona):
    pa = zona.param.pa_ex
    subZona =zona.param.subZonas[neurona.sub_zona]
    v= neurona.ipsp
    ipsp_i_e = subZona.psp_I_E
    rango_ipsp = ipsp_i_e.const_ipsp
    suma = 0
    for j in range(0, rango_ipsp):
        if (i - 1 - j) < 0:
            suma += 0
        else:
            n = neurona.n_i[i - j]
            suma += n * ipsp_i_e.amplitud[j]
    nuevo_ipsp = ipsp_i_e.coeficiente * v + ((pa.v_min - v) / pa.v_min) * suma
    return nuevo_ipsp


def calcula_vol_ex_ext(neurona, zona):
    v = neurona.epsp_ext_e
    n_ext_e = neurona.n_ext_e
    pa = zona.param.pa_ex
    subZona =zona.param.subZonas[neurona.sub_zona]
    epsp_ext_e = subZona.psp_EXT_E
    if zona.nombre_zona == "CA3":
        epsp_ext_e.amplitud = np.random.randint(9,13)
    v_epsp_nuevo = epsp_ext_e.coeficiente * v +(((pa.v_max - v) / pa.v_max ) * n_ext_e * epsp_ext_e.amplitud)
    return v_epsp_nuevo


def calcula_vol_e_e(neurona, zona):
     v = neurona.epsp_e_e
     n_e_e = neurona.n_e_e
     pa = zona.param.pa_in
     subZona =zona.param.subZonas[neurona.sub_zona]
     epsp_e_e = subZona.psp_E_E
     v_epsp_nuevo = epsp_e_e.coeficiente * v + (((pa.v_max - v) / pa.v_max) * n_e_e * epsp_e_e.amplitud)
     return v_epsp_nuevo

def calcula_vol_ex_i(neurona, zona):
     v = neurona.epsp_e_i
     n_e_i=neurona.n_e_i
     pa = zona.param.pa_in
     subZona =zona.param.subZonas[neurona.sub_zona]
     epsp_e_i = subZona.psp_E_I
     v_epsp_nuevo = epsp_e_i.coeficiente * v + (((pa.v_max - v) / pa.v_max) * n_e_i * epsp_e_i.amplitud)
     return v_epsp_nuevo



def calculaNeuronasActivas(lista,lattice,i):
    num_neuronas_act=0
    for aferencia in lista:
        neurona = lattice[aferencia[0]][aferencia[1]]
        if neurona.muerta == False and neurona.estado[i] == E_ACTIVO \
                    and neurona.tiempo_estado == neurona.pa.t_activo - 1:
                num_neuronas_act+=1
    return num_neuronas_act


 # EN ESTE METODO SE IMPLEMENTAN LA FUNCION DE EVOLUCION DEL AC

def aplica_funcion_evolucion(neurona, t_i):
        neurona.tiempo_estado = 0 if neurona.tiempo_estado - 1 < 0 else neurona.tiempo_estado - 1
        suma = neurona.pa.v_inactivo  + neurona.epsp_e_i + neurona.ipsp + neurona.epsp_ext_e + neurona.epsp_e_e
        neurona.volt_membrana = suma
        estado_actual = neurona.estado[t_i]
        umbral_actual = neurona.umbral
        num_estados = len(neurona.estado)
        if neurona.tiempo_estado  == TERMINO_ESTADO:
            if (estado_actual == E_INACTIVO or estado_actual == E_REFRACTARIO) and suma > umbral_actual:
                neurona.estado.append(E_ACTIVO)
                neurona.tiempo_estado = neurona.pa.t_activo
                neurona.umbral = neurona.pa.u_activo
            elif estado_actual == E_ACTIVO and suma <= umbral_actual:
                neurona.estado.append(E_REFRACTARIO)
                neurona.tiempo_estado =neurona.pa.t_refractario
                neurona.umbral = neurona.pa.u_refractario[-1]
            elif estado_actual == E_REFRACTARIO and suma <= umbral_actual:
                neurona.estado.append(E_INACTIVO)
                neurona.tiempo_estado = neurona.pa.t_inactivo
                neurona.umbral = neurona.pa.u_inactivo
        elif estado_actual == E_REFRACTARIO and suma > umbral_actual:
            neurona.estado.append(E_ACTIVO)
            neurona.tiempo_estado = neurona.pa.t_activo
            neurona.umbral = neurona.pa.u_activo
        elif estado_actual !=E_ACTIVO:
            neurona.umbral = neurona.pa.u_refractario[neurona.tiempo_estado -1]
        else:
            neurona.umbral = neurona.pa.u_activo

        if num_estados  == len(neurona.estado) :
            neurona.estado.append(neurona.estado[-1])


def aplica_fun_evo_lattice_ex(zona,t_i):
    potencial_membrana=0
    num_ap_ti=0
    for i in range (NUM_NEURONAS_EX):
        for j in range (NUM_NEURONAS_EX):
             neurona_ex = zona.lattice_ex[i][j]
             if neurona_ex.muerta == False:
                 neurona_ex.epsp_ext_e = calcula_vol_ex_ext(neurona_ex, zona)
                 neurona_ex.epsp_e_e = calcula_vol_e_e(neurona_ex, zona)
                 neurona_ex.ipsp = calcula_ipsp(neurona_ex,t_i - 1,zona)
                 aplica_funcion_evolucion(neurona_ex, t_i)
                 potencial_membrana+= neurona_ex.volt_membrana
                 if neurona_ex.getEstado() == E_ACTIVO \
                        and neurona_ex.tiempo_estado== neurona_ex.pa.t_activo - 1:
                    num_ap_ti+=1
    #num_ap_ti = num_ap_ti if num_ap_ti < 150 else 150
    return potencial_membrana, num_ap_ti


def aplica_fun_evo_lattice_in(zona,t_i):
    num_ap_ti_in=0
    for i in range(NUM_NEURONAS_IN):
        for j in range(NUM_NEURONAS_IN):
            neurona_in= zona.lattice_in[i][j]
            if neurona_in.muerta == False:
                neurona_in.epsp_ext_e = 0
                neurona_in.epsp_e_i = calcula_vol_ex_i(neurona_in,zona)
                aplica_funcion_evolucion(neurona_in, t_i)
                cell_ex_activas=calculaNeuronasActivas(neurona_in.aferencias,zona.lattice_ex,t_i)
                neurona_in.n_e_i = cell_ex_activas
                neurona_in.n_ext_e = 0
                if neurona_in.getEstado() == E_ACTIVO \
                        and neurona_in.tiempo_estado== neurona_in.pa.t_activo - 1:
                    num_ap_ti_in+=1

def agregar_num_cell_act(zona, t_i):
    if zona.nombre_zona == "CA3":
        pulsos_ex_ext = asignaPulsos(zona.pulsos_entrada[t_i], zona.perdida_neuronal_ex, zona.param.perdida_neuronal)
    else :
        pulsos_ex_ext = asignaPulsosCA3(zona)
    if zona.param.is_recurrente and zona.pulsos_entrada_int_ex > 0:
        pulsos_ex_int = asignaPulsos(int(zona.pulsos_entrada_int_ex * zona.param.TASA_AFERENCIAS_INT), zona.perdida_neuronal_ex, zona.param.perdida_neuronal)
    for i in range (NUM_NEURONAS_EX):
        for j in range (NUM_NEURONAS_EX):
            neurona_ex = zona.lattice_ex[i][j]
            if neurona_ex.muerta == False:
                neurona_ex.n_ext_e = pulsos_ex_ext[i][j]
                if zona.param.is_recurrente and zona.pulsos_entrada_int_ex > 0:
                    neurona_ex.n_e_e = pulsos_ex_int[i][j]
                cell_in_activas=calculaNeuronasActivas(neurona_ex.aferencias,zona.lattice_in,t_i)
                neurona_ex.n_i.append(cell_in_activas)


def aplicaFuncionEvolucion(zona,t_i):
    potencial_membrana, num_ap_ti = aplica_fun_evo_lattice_ex(zona, t_i)
    zona.pulsos_entrada_int_ex = num_ap_ti
    num_ap_ti_in = aplica_fun_evo_lattice_in(zona, t_i)
    agregar_num_cell_act(zona, t_i)
    zona.senial_saludable.append(potencial_membrana / (NUM_TOTAL_NEURONAS_EX - len(zona.perdida_neuronal_ex)))
    zona.num_potenciales_saludable.append(num_ap_ti)
    zona.num_potenciales_saludable_in.append(num_ap_ti_in)
    return zona

def empaquetaResultados(zona_ca3, zona_ca1):
    resul_zona_ca3 = ZonaHipocampoResultados(zona_ca3)
    resul_zona_ca1 = ZonaHipocampoResultados(zona_ca1)
    return resul_zona_ca3, resul_zona_ca1

def salidasCA3(zona):
    zona.impulsos_subzonas={"dorsal_proximal": 0, "dorsal_intermedio":0, "dorsal_distal":0,
                                  "ventral_proximal":0, "ventral_intermedio":0, "ventral_distal":0}
    for x in range(0,NUM_NEURONAS_EX):
        for y in range(0,NUM_NEURONAS_EX):
            neurona = zona.lattice_ex[x][y]
            if neurona.muerta == False and neurona.getEstado() == E_ACTIVO \
                    and neurona.tiempo_estado== neurona.pa.t_activo - 1:
                zona.impulsos_subzonas[neurona.sub_zona] += 1
    return zona.impulsos_subzonas

def asignaPulsosCA3(zona):
    neuronas_ex_pulsos = [[0 for posy in range(NUM_NEURONAS_EX)] for posx in range(NUM_NEURONAS_EX)]
    sub_zonas = zona.param.subZonas
    for k,v in zona.impulsos_subzonas.items():
        k = k.replace("distal","proximal") if "distal" in k else  k.replace("proximal","distal") if  "proximal" in k else k
        if k != "all" :
            limite_subzona= sub_zonas[k].rango_ex
        limite_x= [0, NUM_NEURONAS_EX - 1] if k== "all" else limite_subzona["rango_x"]
        limite_y= [0, NUM_NEURONAS_EX - 1] if k== "all" else limite_subzona["rango_y"]
        num_pulsos = int(v * zona.param.TASA_AFERENCIAS)
        if zona.param.perdida_neuronal :
            num_pulsos_asignados = 0
            while (num_pulsos_asignados < num_pulsos):
                idNx = np.random.randint(limite_x[0], limite_x[1] + 1)
                idNy = np.random.randint(limite_y[0], limite_y[1] + 1)
                if [idNy, idNx] not in zona.perdida_neuronal_ex:
                    neuronas_ex_pulsos[idNy][idNx]+=1
                    num_pulsos_asignados += 1
        else:
            for i in range(num_pulsos):
                idNx = np.random.randint(limite_x[0], limite_x[1] + 1)
                idNy = np.random.randint(limite_y[0], limite_y[1] + 1)
                neuronas_ex_pulsos[idNy][idNx]+=1

    return neuronas_ex_pulsos


def ejecutaModeloAC (zona_ca3, zona_ca1, wS_ca3, wS_ca1,tiempo_sim):
    for t in range(1,TIEMPO_ITERA_SIM):
        print("Tiempo simulacion : {}  milisegundos".format(t * 300))
        wS_ca3.delete(ALL)
        wS_ca1.delete(ALL)
        dibujaAutomata (zona_ca3.lattice_ex, zona_ca3.lattice_in, wS_ca3, zona_ca3.param)
        dibujaAutomata (zona_ca1.lattice_ex, zona_ca1.lattice_in, wS_ca1, zona_ca1.param)
        zona_ca3 = aplicaFuncionEvolucion(zona_ca3, t)
        zona_ca1 = aplicaFuncionEvolucion(zona_ca1, t)
        zona_ca1.impulsos_subzonas = salidasCA3(zona_ca3)
        dibuja_senial(zona_ca3, zona_ca1,tiempo_sim[0:t])
        wS_ca3.after(TIEMPO_ACTUALIZACION)
        wS_ca1.after(TIEMPO_ACTUALIZACION)
        wS_ca3.update()
        wS_ca1.update()
    return empaquetaResultados(zona_ca3, zona_ca1)

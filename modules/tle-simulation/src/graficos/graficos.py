__author__ = 'sara'
import matplotlib.pyplot as plt
from matplotlib import gridspec

from analisis.filtro_pasa_bandas import filtra_signal
from configs.parametros import E_ACTIVO
from configs.variables_sim import NUM_NEURONAS_EX, NUM_NEURONAS_IN, TIPO_E, TIPO_I, FRECUENCIA_MUESTREO, \
    VALORES_FRECUENCIA
from variables_graficos_sim import TAMANIO_CANVAS, SEPARACION_CELL_EX, SEPARCACION_CELL_IN, ACA3, \
    canvas_figCA3, ACA1, canvas_figCA1
from hipocampo.clasePsp import Psp
from hipocampo.generador_psp import calcula_psp


def dibujaLattice(lattice, num_neuronas, tipo, separacion, ventana, colores_celulas):
    inicio_cell = separacion[0]
    fin_cell = separacion[1]
    for x in range(num_neuronas):
        incrementoY = (x * inicio_cell) + fin_cell * x
        for y in range(num_neuronas):
            incrementoX = y * fin_cell + inicio_cell * y
            if lattice[x][y].getEstado() == E_ACTIVO:
            #if [x,y] in l:
                ventana.create_oval(inicio_cell + incrementoX, inicio_cell + incrementoY,
                                    fin_cell + incrementoX, fin_cell + incrementoY,
                                    fill=colores_celulas[tipo + "-line"],
                                    outline=colores_celulas[tipo + "-line"], width=2)
            else:
                if lattice[x][y].muerta:
                    ventana.create_oval(inicio_cell + incrementoX, inicio_cell + incrementoY,
                                    fin_cell + incrementoX, fin_cell + incrementoY,
                                    fill="#000000")
                else:
                    ventana.create_oval(inicio_cell + incrementoX, inicio_cell + incrementoY,
                                    fin_cell + incrementoX, fin_cell + incrementoY,
                                    outline="#585858")


def dibuja_limites_sub_zonas(lista_sub_zonas, num_sub_zonas,  ventana):
     num_fila = 0
     x_init = 0
     y_init = [0] * num_sub_zonas[0]
     y_fin = 0
     y_init_aux= []
     for num_columnas in num_sub_zonas:
        for columna in range(num_columnas):
            conf_zona = lista_sub_zonas[num_fila][columna]
            x_fin = TAMANIO_CANVAS * (conf_zona[1] / 100.0) + x_init
            y_fin = TAMANIO_CANVAS * (conf_zona[2] / 100.0) + y_init[columna]
            color = conf_zona[3]
            ventana.create_rectangle(x_init, y_init[columna] , x_fin , y_fin, fill=color)
            x_init = x_fin
            y_init_aux.append(y_fin)
        x_init = 0
        y_init = y_init_aux
        y_init_aux = []
        num_fila += 1


def dibujaAutomata(lattice_ex, lattice_in, ventana, param):
    dibuja_limites_sub_zonas(param.tam_sub_zonas,param.num_sub_zonas, ventana)
    dibujaLattice(lattice_ex, NUM_NEURONAS_EX, TIPO_E, SEPARACION_CELL_EX, ventana, param.colores_neurona)
    dibujaLattice(lattice_in, NUM_NEURONAS_IN, TIPO_I, SEPARCACION_CELL_IN, ventana, param.colores_neurona)


def dibuja_senial(zona_ca3, zona_ca1,tiempo):
    ACA3.clear()
    ACA3.plot(tiempo,zona_ca3.senial_saludable, color='#25fa04')
    #ACA3.set_ylim(-100, -45)
    ACA3.set_xlim(0, 10)
    canvas_figCA3.draw()
    ACA1.clear()
    ACA1.plot(tiempo,zona_ca1.senial_saludable, color='#25fa04')
    ACA1.set_ylim(-85, -45)
    ACA1.set_xlim(0, 10)
    canvas_figCA1.draw()


def grafica_resultados_zona(zona, tiempo_sim, fig, gs, y):

    zona1 = zona.sub_zonas["prueba_psp"]

    if zona.is_recurrente:
        ax1 = fig.add_subplot(gs[0, 2 + y])
        ax1.plot(zona1.psp_E_E.t_psp, zona1.psp_E_E.v_psp, color="black")
        ax1.set_title("EPSP E - E")
        ax1.set_xlabel("milisegundos")
        ax1.set_ylabel("miliVolts")
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 2)

    ax2 = fig.add_subplot(gs[0, 0 + y])
    ax2.plot(zona1.psp_E_I.t_psp, zona1.psp_E_I.v_psp, color="black")
    ax2.set_title("EPSP E - I")
    ax2.set_xlabel("milisegundos")
    ax2.set_ylabel("miliVolts")
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 2.6)

    ax3 = fig.add_subplot(gs[0, 1 + y])
    ax3.plot(zona1.psp_I_E.t_psp, zona1.psp_I_E.v_psp, color="black")
    ax3.set_title("IPSP I - E")
    ax3.set_xlabel("milisegundos")
    ax3.set_ylabel("miliVolts")
    ax3.set_xlim(0, 20)
    ax3.set_ylim(-1.05, 0)

    ax8 = fig.add_subplot(gs[1, 0 + y: 3 + y])
    ax8.plot(zona1.psp_EXT_E.t_psp,zona1.psp_EXT_E.v_psp, color="black")
    if zona.is_recurrente:
        psp_EXT_E = Psp(TIPO_E, 0.8, 9, 21)
        psp2 = calcula_psp(psp_EXT_E, zona.pa_ex,1)
        ax8.plot(psp2.t_psp,psp2.v_psp, color="black")
        psp_EXT_E = Psp(TIPO_E, 0.8, 11, 21)
        psp2 = calcula_psp(psp_EXT_E, zona.pa_ex,1)
        ax8.plot(psp2.t_psp,psp2.v_psp, color="black")
    ax8.set_title("EPSP E - EXT")
    ax8.set_xlabel("milisegundos")
    ax8.set_ylabel("miliVolts")
    ax8.set_xlim(0, zona1.psp_EXT_E.t_psp[-1] + 0.2)
    ax8.set_ylim(0, max(zona1.psp_EXT_E.v_psp) + 0.5)

    ax4 = fig.add_subplot(gs[2, 0 + y: 3 + y])
    ax4.plot(tiempo_sim, zona.senial_saludable, color="black")
    ax4.set_title("Onda en " + zona.zona)
    ax4.set_xlabel("Segundos")
    ax4.set_ylabel("Voltage (mV)")
    if zona.zona == "CA3":
        ax4.set_ylim(-100, -30)
    else:
        ax4.set_ylim(-75, -40)

    ax6 = fig.add_subplot(gs[3, 0 + y:2 + y])
    ax6.plot(tiempo_sim, zona.num_potenciales_saludable, color="black")
    ax6.set_title("NUMERO DE POTENCIALES DE ACCION")
    ax6.set_xlabel("TIEMPO")
    ax6.set_ylabel("No. potenciales")

    ax7 = fig.add_subplot(gs[3, 2 + y])
    plt.hist(zona.num_potenciales_saludable, bins=20, color="black")
    ax7.set_title("DISTRIBUCION")
    ax7.set_ylabel("No.")
    #ax7.set_xlim(0, 25)

    fre, am = filtra_signal(zona.senial_saludable, FRECUENCIA_MUESTREO)
    ax5 = fig.add_subplot(gs[4, 0 + y:3 + y])
    ax5.plot(fre[0:VALORES_FRECUENCIA], am, color="black")
    ax5.set_title("FRECUENCIA")
    ax5.set_xlabel("Frecuencia (Hz)")
    ax5.set_ylabel("Amplitud")
    ax5.set_xlim(0, 50)

    gs.update(wspace=0.5, hspace=1.2)

    return fig


def grafica_resultados(zona_ca3, zona_ca1, tiempo_sim, num_sim=""):
    fig = plt.figure("RESULTADOS", figsize=(15, 8))
    gs = gridspec.GridSpec(5, 7)
    plt.rc('font', size=10)
    fig = grafica_resultados_zona(zona_ca3, tiempo_sim, fig, gs, 0)
    fig = grafica_resultados_zona(zona_ca1, tiempo_sim, fig, gs, 4)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    # guarda_graficas(fig, num_sim)
    plt.show()


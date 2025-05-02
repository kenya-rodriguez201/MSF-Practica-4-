"""
Práctica 5: Sistema cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Kenya Fernanda Rodriguez Castro
Número de control: 20213058
Correo institucional: kenya.rodriguez201@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control 
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np 
import math as m 
import matplotlib.pyplot as plt 
import control as ctrl

# Parámetros de simulación
x0, t0, tF, dt, w, h = 0, 0, 10, 1E-3, 10, 5
N = round((tF - t0) / dt) + 1
t = np.linspace(t0, tF, N) 
u = np.sin(2 * m.pi * 95 / 60 * t) + 0.8

# Función del sistema cardiovascular
def sys_cardio(Z, C, R, L):    
    num = [L * R, R * Z]
    den = [C * L * R * Z, L * R + L * Z, R * Z]
    return ctrl.tf(num, den)

#Funcion de transferencia: Individuo saludable [control]
Z,R,L,C = 0.033,0.950,0.010,1.5
sysN = sys_cardio(Z,C,R,L)
print('Individuo sano [control]: ')
print(sysN)

#Funcion de transferencia: Individuo enfermo [Caso: Hipertenso]
Z,R,L,C = 0.050,1.40,0.020,2.5
sysE1 = sys_cardio(Z,C,R,L)
print('Individuo enfermo [Caso: Hipertenso]: ')
print(sysE1)

#Funcion de transferencia: Individuo enfermo [Caso: Hipotenso]
Z,R,L,C = 0.020,0.600,0.005,0.250
sysE2 = sys_cardio(Z,C,R,L)
print('Individuo enfermo [Caso: Hipotenso]: ')
print(sysE2)

# Colores
Morado = [70/255, 53/255, 177/255]
Verde = [62/255, 123/255, 39/255]
Rosa = [255/255, 116/255, 139/255]
Azul = [7/255, 71/255, 153/255]

def plotsignals(u, sysN, sysE1, sysE2, signal):
    fig = plt.figure()
    
    ts, Ve = ctrl.forced_response(sysE2, t, u, x0)
    plt.plot(t, u, '-', linewidth=0.5, color= Azul, label='$P_a(t)$')
    
    ts, Vs = ctrl.forced_response(sysN, t, u, x0)
    plt.plot(t, Vs, "-", linewidth=1, color= Morado, label='$P_P(t): Sano$')
    
    ts, Vs = ctrl.forced_response(sysE1, t, u, x0)
    plt.plot(t, Vs, ":", linewidth=2, color= Verde, label='$P_P(t): Hipertenso$')
    
    ts, Vs = ctrl.forced_response(sysE2, t, u, x0)
    plt.plot(t, Vs, ":", linewidth=2, color= Rosa, label='$P_P(t): Hipotenso$')
    
    plt.grid(False)
    plt.xlim(0, 10)
    plt.ylim(-0.5, 2)
    plt.xticks(np.arange(0, 11, 2))
    plt.yticks(np.arange(-0.5, 2.1, 0.5))
    plt.xlabel("$t$ [s]")
    plt.ylabel("$PA(t)$ [V]")
    plt.legend(bbox_to_anchor=(0.5, -0.3), loc="center", ncol=4, fontsize=8, frameon=False)
    plt.show()
    
    fig.set_size_inches(w, h)
    fig.tight_layout()
    fig.savefig(f'python_{signal}.png', dpi=600, bbox_inches="tight")
    fig.savefig(f'python_{signal}.pdf', bbox_inches="tight")

plotsignals(u, sysN, sysE1, sysE2, 'Sin')

def control_plot(sysE, sysN, u, t, x0, case_name, color_disease, color_control, file_name):
    Cr = 1E-6
    Re = 249.586
    Rr = 2.495E7 
    numPI = [Rr * Cr, 1]
    denPI = [Re * Cr, 0]
    PI = ctrl.tf(numPI, denPI)

    open_loop = ctrl.series(PI, sysE)
    sysPI = ctrl.feedback(open_loop, 1, sign=-1)

    fig = plt.figure()
    plt.plot(t, u, '-', linewidth=0.5, color = Azul, label='$P_a(t)$')

    ts, y_enfermo = ctrl.forced_response(sysE, t, u, x0)
    plt.plot(t, y_enfermo, '-', linewidth=0.5, color= color_disease, label=f'$P_p(t): {case_name}$')

    ts, y_sano = ctrl.forced_response(sysN, t, u, x0)
    plt.plot(t, y_sano, '-', linewidth=0.5, color= color_control, label='$P_p(t): Control$')

    ts, y_tratado = ctrl.forced_response(sysPI, t, y_sano, x0)
    plt.plot(t, y_tratado, ':', linewidth=2, color= color_disease, label='$P_p(t): Tratamiento$')

    plt.grid(False)
    plt.xlim(0, 10)
    plt.ylim(-0.5, 2)
    plt.xticks(np.arange(0, 11, 1))
    plt.xlabel("$t$ $[s]$")
    plt.ylabel("$PA(t)$ [V]")
    plt.legend(bbox_to_anchor=(0.5, -0.23), loc='center', ncol=4)
    plt.show()

    fig.set_size_inches(w, h)
    fig.tight_layout()
    fig.savefig(file_name + '.png', dpi=600, bbox_inches='tight')
    fig.savefig(file_name + '.pdf', dpi=600, bbox_inches='tight')

control_plot(sysE2, sysN, u, t, x0, 'Hipotenso',
             color_disease= Rosa,
             color_control= Morado,
             file_name='sistema_hipotenso')

control_plot(sysE1, sysN, u, t, x0, 'Hipertenso',
             color_disease= Verde,
             color_control= Morado,
             file_name='sistema_hipertenso')
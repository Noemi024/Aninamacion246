import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, CheckButtons, TextBox

puntos_originales = np.array([
    [0, -2, 2, 0],  # eje de x
    [2, -1, -1, 2]  # eje de las y
])

estado = {
    "angulo": 0,
    "escala": 1.0,
    "ver_coordenadas": True
}

def obtener_matriz_rotacion(angulo_grados):
    angulo_rad = np.radians(angulo_grados)
    cos_a = np.cos(angulo_rad)
    sin_a = np.sin(angulo_rad)
    return np.array([
        [cos_a, -sin_a],
        [sin_a, cos_a]
    ])

def obtener_matriz_escala(factor):
    return np.array([
        [factor, 0],
        [0, factor]
    ])

def actualizar_grafico():
    T_rot = obtener_matriz_rotacion(estado["angulo"])
    T_esc = obtener_matriz_escala(estado["escala"])
    puntos_escalados = T_esc @ puntos_originales
    puntos_transformados = T_rot @ puntos_escalados
    ax.clear()
    
    ax.plot(puntos_originales[0], puntos_originales[1], 'r--', label="original", alpha=0.6)
    ax.plot(puntos_transformados[0], puntos_transformados[1], 'b-', linewidth=2, label=f"Transformada")
    
    if estado["ver_coordenadas"]:
        # ✅ CORREGIDO: puntos originales son ROJOS (eran azules) y formato de texto
        for x, y in zip(puntos_originales[0], puntos_originales[1]):
            ax.plot(x, y, 'ro', markersize=4)
            ax.text(x + 0.08, y + 0.08, f"({x:.1f},{y:.1f})", color="red", fontsize=8)
        
        for x, y in zip(puntos_transformados[0], puntos_transformados[1]):
            ax.plot(x, y, 'bo', markersize=4)
            ax.text(x + 0.08, y + 0.08, f"({x:.1f},{y:.1f})", color="blue", fontsize=8)
    
    ax.axhline(0, color='black', linewidth=1)  # linea de ejes en x
    ax.axvline(0, color='black', linewidth=1)   # linea de ejes en y
    ax.grid(True, linestyle=':')
    ax.axis("equal")
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.legend(loc="upper right")
    
    # ✅ CORREGIDO: faltaban comillas en las claves del diccionario
    ax.set_title(
        f"Rotacion:{estado['angulo']}° | Escala:x{estado['escala']:.1f}",
        fontsize=12, fontweight="bold"
    )
    fig.canvas.draw_idle()

def actualizar_coordenadas(event):
    global puntos_originales
    try:
        texto_x = text_box_x.text
        texto_y = text_box_y.text  # ✅ CORREGIDO: faltaba el .text aquí
        
        x = list(map(float, texto_x.strip().split(',')))
        y = list(map(float, texto_y.strip().split(',')))
        
        if len(x) != len(y):
            print("Error debe ingresar la misma cantidad de valores en x como en y")
            return
        
        puntos_originales = np.array([x, y])
        estado["angulo"] = 0
        estado["escala"] = 1.0
        actualizar_grafico()
        print("coordenadas actualizadas con exito") # ✅ corregido error de escritura
    except Exception as e:
        print(f"error verificar el formato de los numeros deben ser seguidos con comas :{e}")

def rotar_izq(event):
    estado["angulo"] = (estado["angulo"] + 90) % 360
    actualizar_grafico()

def rotar_der(event):
    estado["angulo"] = (estado["angulo"] - 90) % 360
    actualizar_grafico()

def ampliar(event):
    # ✅ CORREGIDO: condición mal escrita
    if estado["escala"] < 3.0:
        estado["escala"] += 0.5
    actualizar_grafico()

def reducir(event): # ✅ CORREGIDO: nombre del parámetro (era evemt)
    # ✅ CORREGIDO: condición mal escrita
    if estado["escala"] > 0.3:
        estado["escala"] -= 0.5
    actualizar_grafico()

def resetear(event): # ✅ CORREGIDO: nombre del parámetro (era evemt)
    estado["angulo"] = 0
    estado["escala"] = 1.0
    text_box_x.set_val(",".join(map(str, puntos_originales[0])))
    text_box_y.set_val(",".join(map(str, puntos_originales[1])))
    actualizar_grafico()

def togglew_coordenadas(label):
    estado["ver_coordenadas"] = not estado["ver_coordenadas"]
    actualizar_grafico()

# ---------------------- INTERFAZ ----------------------
fig, ax = plt.subplots(figsize=(8, 8))
fig.subplots_adjust(bottom=0.32)

# caja de para la x
ax_text_x = plt.axes([0.12, 0.24, 0.75, 0.04])
text_box_x = TextBox(ax_text_x, "Fila 0 - Coordenadas X:", textalignment="left") # ✅ nombre corregido
text_box_x.set_val(",".join(map(str, puntos_originales[0])))

# caja de para la y ✅ CORREGIDO: posición y nombre correcto
ax_text_y = plt.axes([0.12, 0.18, 0.75, 0.04])
text_box_y = TextBox(ax_text_y, "Fila 1 - Coordenadas Y:", textalignment="left")
text_box_y.set_val(",".join(map(str, puntos_originales[1])))

ax_boton_actualizar = plt.axes([0.42, 0.12, 0.16, 0.05])
btn_actualizar = Button(ax_boton_actualizar, "actualizar figura", color="#f0f0f0", hovercolor="#d0d0d0")
btn_actualizar.on_clicked(actualizar_coordenadas)

ax_rot_izq = plt.axes([0.05, 0.05, 0.18, 0.05])
btn_rot_izq = Button(ax_rot_izq, "rotar a la izquierda", color="#2d9746", hovercolor="#61db72")
btn_rot_izq.on_clicked(rotar_izq)

ax_rot_der = plt.axes([0.26, 0.05, 0.18, 0.05])
btn_rot_der = Button(ax_rot_der, "rotar a la derecha", color="#216bd2", hovercolor="#8691d9")
btn_rot_der.on_clicked(rotar_der)

ax_amp = plt.axes([0.47, 0.05, 0.18, 0.05])
btn_amp = Button(ax_amp, "ampliar", color="#ac2e71", hovercolor="#845374")
btn_amp.on_clicked(ampliar)

ax_red = plt.axes([0.68, 0.05, 0.18, 0.05])
btn_red = Button(ax_red, "reducir", color="#eb803d", hovercolor="#c5851f") # ✅ texto corregido
btn_red.on_clicked(reducir)

ax_check = plt.axes([0.05, 0.12, 0.22, 0.05])
check_coords = CheckButtons(ax_check, ["ver coordenadas"], [True])
check_coords.on_clicked(togglew_coordenadas)

ax_reset = plt.axes([0.72, 0.12, 0.18, 0.05])
btn_reset = Button(ax_reset, "resetear", color="#ac2e71", hovercolor="#845374")
btn_reset.on_clicked(resetear)

actualizar_grafico()
plt.show()
from tkinter import *
import time
from PIL import Image, ImageTk
import pygame
import os
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Inicialitzar Pygame per a àudio
try:
    pygame.mixer.init()
    musica_disponible = True
except:
    musica_disponible = False

def generar_so_crash():
    """Genera un so de crash sintetitzat"""
    if not musica_disponible:
        return None
    try:
        from scipy.io import wavfile

        sample_rate = 22050
        duracio = 0.3  # 300ms
        muestras = int(sample_rate * duracio)

        temps = np.linspace(0, duracio, muestras)
        frecuencia = 800 - (700 * temps / duracio)
        fase = 2 * np.pi * np.cumsum(frecuencia) / sample_rate
        onda = np.sin(fase)
        envoltoria = np.exp(-5 * temps)
        onda = onda * envoltoria

        onda_int16 = np.int16(onda * 32767 / 2)
        wavfile.write("crash_temp.wav", sample_rate, onda_int16)
        so = pygame.mixer.Sound("crash_temp.wav")
        return so
    except Exception as e:
        return None

def generar_musica_fons():
    """Genera música de fons simple"""
    if not musica_disponible:
        return None
    try:
        from scipy.io import wavfile

        sample_rate = 22050
        duracio = 4  # 4 segons
        muestras = int(sample_rate * duracio)
        temps = np.linspace(0, duracio, muestras)

        # Melodia simple repetida
        onda = np.zeros(muestras)
        notes = [262, 294, 330, 349]  # Do, Re, Mi, Fa
        notes_duracio = int(sample_rate * 0.5)  # 0.5s per nota

        for i, freq in enumerate(notes * 2):
            start = i * notes_duracio
            end = min((i + 1) * notes_duracio, muestras)
            t = temps[start:end]
            onda[start:end] = np.sin(2 * np.pi * freq * t)

        onda_int16 = np.int16(onda * 32767 / 3)
        wavfile.write("musica_fons_temp.wav", sample_rate, onda_int16)
        so = pygame.mixer.Sound("musica_fons_temp.wav")
        return so
    except Exception as e:
        return None

def generar_so_victoria():
    """Genera so de victoria (notes altes)"""
    if not musica_disponible:
        return None
    try:
        from scipy.io import wavfile

        sample_rate = 22050
        duracio = 0.6
        muestras = int(sample_rate * duracio)
        temps = np.linspace(0, duracio, muestras)

        # Dues notes altes
        onda = np.sin(2 * np.pi * 523 * temps[:muestras//2])  # Do alt
        onda_part2 = np.sin(2 * np.pi * 659 * temps[muestras//2:])  # Mi alt
        onda = np.concatenate([onda, onda_part2])

        envoltoria = np.exp(-3 * temps)
        onda = onda * envoltoria

        onda_int16 = np.int16(onda * 32767 / 2)
        wavfile.write("victoria_temp.wav", sample_rate, onda_int16)
        so = pygame.mixer.Sound("victoria_temp.wav")
        return so
    except Exception as e:
        return None

def generar_so_gameover():
    """Genera so de game over (notes baixes tristes)"""
    if not musica_disponible:
        return None
    try:
        from scipy.io import wavfile

        sample_rate = 22050
        duracio = 0.8
        muestras = int(sample_rate * duracio)
        temps = np.linspace(0, duracio, muestras)

        # Dues notes baixes que baixen
        onda = np.sin(2 * np.pi * 262 * temps[:muestras//2])  # Do
        onda_part2 = np.sin(2 * np.pi * 196 * temps[muestras//2:])  # Sol baix
        onda = np.concatenate([onda, onda_part2])

        envoltoria = np.exp(-2 * temps)
        onda = onda * envoltoria

        onda_int16 = np.int16(onda * 32767 / 2)
        wavfile.write("gameover_temp.wav", sample_rate, onda_int16)
        so = pygame.mixer.Sound("gameover_temp.wav")
        return so
    except Exception as e:
        return None

# Carregar/generar sons
sons = {}
if musica_disponible:
    # Generar sons
    so_crash = generar_so_crash()
    if so_crash:
        sons['xoc'] = so_crash

    so_fons = generar_musica_fons()
    if so_fons:
        sons['fons'] = so_fons

    so_victoria = generar_so_victoria()
    if so_victoria:
        sons['victoria'] = so_victoria

    so_gameover = generar_so_gameover()
    if so_gameover:
        sons['gameover'] = so_gameover

tk = Tk()
tk.title("Joc de la Granota - Edicio Avancada")
f = Canvas(tk, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="green")
f.pack()

# Dades granota
granota = {'x': 400, 'y': 550, 'amp': 40, 'al': 40, 'v': 8}
vides = 3

# Carregar imatge granota
try:
    imatge_granota = Image.open("ranita.png")
    imatge_granota = imatge_granota.resize((granota['amp'], granota['al']))
    imatge_granota_tk = ImageTk.PhotoImage(imatge_granota)
except:
    imatge_granota_tk = None

# Control de tecles
tecles = {"up": False, "down": False, "left": False, "right": False}
reiniciar_joc_flag = False

def tecla_premuda(event):
    global reiniciar_joc_flag
    tecla = event.keysym.lower()
    if tecla in tecles: tecles[tecla] = True
    if tecla == "space": reiniciar_joc_flag = True

def tecla_amollada(event):
    tecla = event.keysym.lower()
    if tecla in tecles: tecles[tecla] = False

def tecla_especial_premuda(event, nom_tecla):
    tecles[nom_tecla] = True

def tecla_especial_amollada(event, nom_tecla):
    tecles[nom_tecla] = False

tk.bind("<KeyPress>", tecla_premuda)
tk.bind("<KeyRelease>", tecla_amollada)
tk.bind("<Up>", lambda e: tecla_especial_premuda(e, "up"))
tk.bind("<Down>", lambda e: tecla_especial_premuda(e, "down"))
tk.bind("<Left>", lambda e: tecla_especial_premuda(e, "left"))
tk.bind("<Right>", lambda e: tecla_especial_premuda(e, "right"))
tk.bind("<KeyRelease-Up>", lambda e: tecla_especial_amollada(e, "up"))
tk.bind("<KeyRelease-Down>", lambda e: tecla_especial_amollada(e, "down"))
tk.bind("<KeyRelease-Left>", lambda e: tecla_especial_amollada(e, "left"))
tk.bind("<KeyRelease-Right>", lambda e: tecla_especial_amollada(e, "right"))

def reiniciar():
    granota['x'] = 400
    granota['y'] = 550

def reiniciar_joc():
    global vides, joc_estat, t0, t_actual, puntuacio, monedes
    vides = 3
    joc_estat = "JUGANT"
    t0 = time.time()
    t_actual = 0
    puntuacio = 0
    monedes = []
    granota['x'] = 400
    granota['y'] = 550
    cotxe1['x'] = 50
    cotxe2['x'] = 800
    cotxe3['x'] = 150
    cotxe4['x'] = 600
    cotxe5['x'] = 300
    cotxe6['x'] = 0
    if musica_disponible and 'fons' in sons:
        pygame.mixer.stop()
        sons['fons'].play(-1)

def xoc_granota_cotxe(granota, cotxe):
    return (granota['x'] < cotxe['x'] + cotxe['amp'] and
            granota['x'] + granota['amp'] > cotxe['x'] and
            granota['y'] < cotxe['y'] + cotxe['al'] and
            granota['y'] + granota['al'] > cotxe['y'])

def xoc_granota_moneda(granota, moneda):
    return (granota['x'] < moneda['x'] + moneda['mida'] and
            granota['x'] + granota['amp'] > moneda['x'] and
            granota['y'] < moneda['y'] + moneda['mida'] and
            granota['y'] + granota['al'] > moneda['y'])

def dibuixa_moneda(m):
    # Dibuixar moneda com cercle groc amb brillo
    x, y = m['x'], m['y']
    mida = m['mida']
    f.create_oval(x, y, x + mida, y + mida, fill="gold", outline="orange", width=2)
    # Brillo
    f.create_oval(x + 3, y + 3, x + mida - 5, y + mida - 5, fill="yellow", outline="")

def dibuixa_cotxe(c):
    if 'visible' in c and not c['visible']:
        return

    x, y = c['x'], c['y']
    amp, al = c['amp'], c['al']
    color = c['color']
    tipus = c.get('tipus', 'normal')

    if tipus == 'camio':
        # Dibuixar camio gran
        f.create_rectangle(x, y + 5, x + amp, y + al - 2, fill=color, outline="black", width=3)
        f.create_rectangle(x + 5, y, x + amp - 5, y + 8, fill=color, outline="black", width=2)

        # Finestres cabina
        f.create_rectangle(x + 10, y + 1, x + 20, y + 7, fill="lightblue", outline="navy", width=1)
        f.create_rectangle(x + 25, y + 1, x + 35, y + 7, fill="lightblue", outline="navy", width=1)

        # Rodes (4 rodes - 2 davant, 2 darrere)
        f.create_oval(x + 5, y + al - 2, x + 13, y + al + 4, fill="black", outline="gray")
        f.create_oval(x + amp - 13, y + al - 2, x + amp - 5, y + al + 4, fill="black", outline="gray")
        f.create_oval(x + amp - 25, y + al - 2, x + amp - 17, y + al + 4, fill="black", outline="gray")

    elif tipus == 'moto':
        # Dibuixar moto petita
        f.create_rectangle(x + 3, y + 5, x + amp - 3, y + al - 2, fill=color, outline="black", width=1)
        f.create_oval(x + 2, y + 2, x + amp - 2, y + 8, fill=color, outline="black", width=1)

        # Rodes (2 petites)
        f.create_oval(x + 2, y + al - 2, x + 7, y + al + 2, fill="black", outline="gray", width=1)
        f.create_oval(x + amp - 7, y + al - 2, x + amp - 2, y + al + 2, fill="black", outline="gray", width=1)

    else:
        # Dibuixar cotxe normal
        f.create_rectangle(x, y + 8, x + amp, y + al - 2, fill=color, outline="black", width=2)

        cabin_width = amp * 0.6
        cabin_x_start = x + (amp - cabin_width) // 2 if c['v'] > 0 else x + amp - cabin_width
        f.create_rectangle(cabin_x_start, y, cabin_x_start + cabin_width, y + 10, fill=color, outline="black", width=1)

        window_width = cabin_width * 0.35
        window_spacing = 5

        if c['v'] > 0:
            f.create_rectangle(cabin_x_start + 2, y + 1, cabin_x_start + window_width, y + 9, fill="lightblue", outline="navy", width=1)
            f.create_rectangle(cabin_x_start + window_width + window_spacing, y + 1, cabin_x_start + 2*window_width + window_spacing, y + 9, fill="lightblue", outline="navy", width=1)
        else:
            f.create_rectangle(x + amp - window_width - window_spacing - 2, y + 1, x + amp - window_spacing - 2, y + 9, fill="lightblue", outline="navy", width=1)
            f.create_rectangle(x + amp - 2*window_width - window_spacing - 2, y + 1, x + amp - window_width - window_spacing - 2, y + 9, fill="lightblue", outline="navy", width=1)

        roda_radi = 2
        f.create_oval(x + 4, y + al - 3, x + 4 + roda_radi * 2, y + al + 1, fill="black", outline="gray")
        f.create_oval(x + amp - 8, y + al - 3, x + amp - 4, y + al + 1, fill="black", outline="gray")

        if c['v'] > 0:
            f.create_line(x + amp - 2, y + 8, x + amp - 2, y + al - 2, fill="darkgray", width=2)
        else:
            f.create_line(x + 2, y + 8, x + 2, y + al - 2, fill="darkgray", width=2)

def dibuixa_granota(c):
    if imatge_granota_tk:
        f.create_image(c['x'], c['y'], image=imatge_granota_tk, anchor=NW)
    else:
        x, y = c['x'], c['y']
        amp, al = c['amp'], c['al']

        # Cos principal (oval)
        f.create_oval(x + 5, y + 10, x + amp - 5, y + al - 5, fill="limegreen", outline="darkgreen", width=2)

        # Cap (cercle)
        f.create_oval(x + 8, y, x + amp - 8, y + 15, fill="limegreen", outline="darkgreen", width=2)

        # Ulls
        f.create_oval(x + 12, y + 3, x + 18, y + 9, fill="white", outline="black", width=1)
        f.create_oval(x + 22, y + 3, x + 28, y + 9, fill="white", outline="black", width=1)
        # Pupilles
        f.create_oval(x + 14, y + 4, x + 17, y + 7, fill="black")
        f.create_oval(x + 24, y + 4, x + 27, y + 7, fill="black")

        # Boca
        f.create_arc(x + 10, y + 8, x + 30, y + 14, start=0, extent=180, fill="darkgreen")

        # Potes
        f.create_oval(x, y + 20, x + 8, y + 26, fill="limegreen", outline="darkgreen", width=1)
        f.create_oval(x + amp - 8, y + 20, x + amp, y + 26, fill="limegreen", outline="darkgreen", width=1)

# Cotxes amb zig-zag
cotxe1 = {'x':50,  'y':120, 'amp':45, 'al':25, 'v':8,   'color':'yellow', 'carrils': [120, 180], 'carril': 0, 'canvi_timer': 0, 'tipus': 'normal'}
cotxe2 = {'x':800, 'y':180, 'amp':65, 'al':25, 'v':-10, 'color':'red', 'carrils': [180, 240], 'carril': 0, 'canvi_timer': 0, 'tipus': 'normal'}
cotxe3 = {'x':150, 'y':240, 'amp':45, 'al':25, 'v':12,  'color':'blue', 'carrils': [240, 300], 'carril': 0, 'canvi_timer': 0, 'tipus': 'normal'}
cotxe4 = {'x':600, 'y':300, 'amp':55, 'al':25, 'v':-7,  'color':'orange', 'carrils': [300, 360], 'carril': 0, 'canvi_timer': 0, 'tipus': 'normal'}
cotxe5 = {'x':300, 'y':360, 'amp':50, 'al':25, 'v':14,  'color':'purple', 'carrils': [360, 410], 'carril': 0, 'canvi_timer': 0, 'tipus': 'normal'}
cotxe6 = {'x':0,   'y':420, 'amp':50, 'al':25, 'v':10,  'color':'cyan', 'carrils': [410, 360], 'carril': 0, 'canvi_timer': 0, 'tipus': 'normal'}

# Camions grans
camio1 = {'x':-100, 'y':200, 'amp':90, 'al':30, 'v':6, 'color':'brown', 'carrils': [180, 240], 'carril': 0, 'canvi_timer': 0, 'tipus': 'camio', 'visible': False, 'aparicio_timer': 0}
camio2 = {'x':800, 'y':320, 'amp':90, 'al':30, 'v':-8, 'color':'darkred', 'carrils': [300, 360], 'carril': 0, 'canvi_timer': 0, 'tipus': 'camio', 'visible': False, 'aparicio_timer': 150}

# Motos
moto1 = {'x':400, 'y':280, 'amp':25, 'al':15, 'v':-15, 'color':'red', 'carrils': [270, 300], 'carril': 0, 'canvi_timer': 0, 'tipus': 'moto'}
moto2 = {'x':100, 'y':350, 'amp':25, 'al':15, 'v':13,  'color':'green', 'carrils': [340, 380], 'carril': 0, 'canvi_timer': 0, 'tipus': 'moto'}

cotxes = [cotxe1, cotxe2, cotxe3, cotxe4, cotxe5, cotxe6, camio1, camio2, moto1, moto2]
carrils_y = [110, 170, 230, 290, 350, 410]

# MONEDES
monedes = []
moneda_spawn_timer = 0
puntuacio = 0

# TIMER I ESTATS
t0 = time.time()
joc_estat = "JUGANT"
t_actual = 0

# Iniciar musica de fons
if musica_disponible and 'fons' in sons:
    sons['fons'].play(-1)

while True:
    f.delete("all")

    # Comprovar si reiniciar
    if reiniciar_joc_flag and joc_estat != "JUGANT":
        reiniciar_joc()
        reiniciar_joc_flag = False

    # 1. DIBUIXAR CARRETERA
    f.create_rectangle(0, 100, SCREEN_WIDTH, 450, fill="#333333", outline="")

    # Ratlles blanques entre carrils
    for i in range(len(carrils_y) - 1):
        line_y = carrils_y[i] + 40
        for x in range(0, SCREEN_WIDTH, 40):
            f.create_line(x, line_y, x+20, line_y, fill="white", width=2)

    # 2. LOGICA DEL JOC
    if joc_estat == "JUGANT":
        # Generar monedes aleatòriament
        moneda_spawn_timer += 1
        if moneda_spawn_timer > 80:  # Cada aprox 1.6 segons
            import random
            nova_moneda = {
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(120, 400),
                'mida': 15,
                'timer': 0
            }
            monedes.append(nova_moneda)
            moneda_spawn_timer = 0

        # Actualitzar monedes
        monedes_a_eliminar = []
        for i, m in enumerate(monedes):
            m['timer'] += 1
            if m['timer'] > 300:  # Desapareixen després de 6 segons
                monedes_a_eliminar.append(i)

        for i in reversed(monedes_a_eliminar):
            monedes.pop(i)

        # Moviment granota
        if tecles["up"]: granota['y'] -= granota['v']
        if tecles["down"]: granota['y'] += granota['v']
        if tecles["left"]: granota['x'] -= granota['v']
        if tecles["right"]: granota['x'] += granota['v']

        # Limits pantalla
        granota['x'] = max(0, min(granota['x'], SCREEN_WIDTH - granota['amp']))
        granota['y'] = max(0, min(granota['y'], SCREEN_HEIGHT - granota['al']))

        # Detectar col·lisions amb monedes
        monedes_agafades = []
        for i, m in enumerate(monedes):
            if xoc_granota_moneda(granota, m):
                puntuacio += 10
                monedes_agafades.append(i)

        for i in reversed(monedes_agafades):
            monedes.pop(i)

        # Moviment cotxes amb zig-zag
        for c in cotxes:
            # Logica especial pels camions (aparicio ocasional)
            if c['tipus'] == 'camio':
                c['aparicio_timer'] += 1
                if c['aparicio_timer'] < 200:  # 200 frames = aprox 4 segons visible
                    c['visible'] = True
                elif c['aparicio_timer'] > 600:  # Cada 12 segons
                    c['aparicio_timer'] = 0

            c['x'] += c['v']
            if c['v'] > 0 and c['x'] > SCREEN_WIDTH: c['x'] = -c['amp']
            if c['v'] < 0 and c['x'] + c['amp'] < 0: c['x'] = SCREEN_WIDTH

            # Zig-zag per a tots els cotxes
            c['canvi_timer'] += 1
            tiempo_cambio = 50 + (id(c) % 30)
            if c['canvi_timer'] >= tiempo_cambio:
                c['carril'] = 1 - c['carril']
                c['canvi_timer'] = 0
            target_y = c['carrils'][c['carril']]
            velocitat_carril = 1.5
            if c['y'] < target_y - 0.5:
                c['y'] += velocitat_carril
            elif c['y'] > target_y + 0.5:
                c['y'] -= velocitat_carril
            else:
                c['y'] = target_y

        # Col.lisions
        for c in cotxes:
            if xoc_granota_cotxe(granota, c):
                if musica_disponible and 'xoc' in sons:
                    sons['xoc'].play()
                vides -= 1
                if vides <= 0:
                    joc_estat = "GAME_OVER"
                    print("GAME OVER")
                    if musica_disponible and 'gameover' in sons:
                        pygame.mixer.stop()
                        sons['gameover'].play()
                else:
                    reiniciar()

        # Actualitzar temps
        t_actual = round(time.time() - t0, 1)

        # Comprovar victoria
        if granota['y'] <= 60:
            joc_estat = "GUANYAT"
            if musica_disponible and 'victoria' in sons:
                pygame.mixer.stop()
                sons['victoria'].play()

    # 3. DIBUIXAR
    for c in cotxes: dibuixa_cotxe(c)
    dibuixa_granota(granota)
    for m in monedes: dibuixa_moneda(m)

    # 4. UI
    f.create_text(80, 40, text="VIDES: " + "❤️ " * vides, font=("Arial", 16, "bold"), fill="white", anchor=W)
    f.create_text(SCREEN_WIDTH-120, 40, text="TEMPS: " + str(t_actual) + "s", font=("Arial", 16, "bold"), fill="white", anchor=W)
    f.create_text(SCREEN_WIDTH/2, 40, text="MONEDES: " + str(puntuacio), font=("Arial", 16, "bold"), fill="gold", anchor=W)

    if joc_estat == "GUANYAT":
        f.create_rectangle(150, 180, 650, 420, fill="black", outline="gold", width=4)
        f.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 40, text="HAS GUANYAT!!", font=("Arial", 34, "bold"), fill="lime")
        f.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, text="TEMPS FINAL: " + str(t_actual) + " segons", font=("Arial", 18), fill="white")
        f.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60, text="Prem ESPAI per reiniciar", font=("Arial", 14), fill="yellow")

    elif joc_estat == "GAME_OVER":
        f.create_rectangle(150, 180, 650, 420, fill="black", outline="red", width=4)
        f.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30, text="GAME OVER", font=("Arial", 40, "bold"), fill="red")
        f.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40, text="Prem ESPAI per reiniciar", font=("Arial", 14), fill="yellow")

    f.update()
    time.sleep(0.02)

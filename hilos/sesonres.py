import threading, queue, time, random

LECTURAS = queue.Queue(maxsize=100)
ALERTAS = queue.Queue(maxsize=100)
STOP = threading.Event()

RANGOS = {
    "temp": (18.0, 28.0),
    "hum":  (35.0, 65.0),
    "pres": (2.0, 3.0),
}

def leer_sensor(nombre, periodo_s=0.3, generador=None):
    """Hilo de adquisición: simula sensores."""
    gen = generador or (lambda: {
        "temp": round(random.uniform(15, 31), 2),
        "hum":  round(random.uniform(30, 70), 2),
        "pres": round(random.uniform(1.7, 3.3), 2),
    }[nombre])
    while not STOP.is_set():
        valor = gen()
        ts = time.time()
        try:
            LECTURAS.put_nowait({"sensor": nombre, "valor": valor, "ts": ts})
        except queue.Full:
            # Política: descartar más antiguo para no bloquear
            try: LECTURAS.get_nowait()
            except queue.Empty: pass
            LECTURAS.put_nowait({"sensor": nombre, "valor": valor, "ts": ts})
        time.sleep(periodo_s)

def analizador(n_consecutivas=3):
    """Hilo de análisis con debounce por sensor."""
    consecutivas = {s: 0 for s in RANGOS}
    while not STOP.is_set():
        try:
            dato = LECTURAS.get(timeout=0.5)
        except queue.Empty:
            continue
        s, v = dato["sensor"], dato["valor"]
        low, high = RANGOS[s]
        if v < low or v > high:
            consecutivas[s] += 1
            if consecutivas[s] >= n_consecutivas:
                alerta = f"[ALERTA] {s}={v} fuera de rango ({low}-{high})"
                # publicar alerta
                try: ALERTAS.put_nowait({"msg": alerta, "ts": dato["ts"]})
                except queue.Full: pass
        else:
            consecutivas[s] = 0

def consumidor_alertas():
    """Ejemplo de manejo de alertas (log/print/enviar)."""
    while not STOP.is_set():
        try:
            a = ALERTAS.get(timeout=0.5)
            print(time.strftime("%H:%M:%S"), a["msg"])
        except queue.Empty:
            continue

# Lanzamiento de hilos
hilos = [
    threading.Thread(target=leer_sensor, args=("temp", 0.2)),
    threading.Thread(target=leer_sensor, args=("hum",  0.3)),
    threading.Thread(target=leer_sensor, args=("pres", 0.4)),
    threading.Thread(target=analizador),
    threading.Thread(target=consumidor_alertas),
]
for h in hilos: h.daemon = True; h.start()

# Ejecutar demo 10 s
time.sleep(10)
STOP.set()
for h in hilos: h.join(timeout=1)
import subprocess
import time
import csv
import statistics
from datetime import datetime

# --- CONFIGURACIÓN ---
TARGET_HOST = "8.8.8.8"  # A quién hacemos ping (Google DNS es buena referencia)
NUM_PACKETS = 5          # Cuantos pings por medición
INTERVALO = 10           # Segundos entre cada medición automática
OUTPUT_FILE = "datos_red.csv" # Archivo donde se guardarán los datos

def obtener_metricas():
    # Ejecuta el comando ping del sistema
    # Linux usa '-c', Windows usa '-n'. Asumo Linux por tu servidor.
    comando = ["ping", "-c", str(NUM_PACKETS), TARGET_HOST]
    
    try:
        # Ejecutar ping y capturar salida
        proceso = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        salida = proceso.stdout
        
        # Analizar tiempos (ms) de la respuesta
        tiempos = []
        packet_loss = 0
        
        for linea in salida.split("\n"):
            if "time=" in linea:
                # Extraer el valor de tiempo (ej: time=14.5 ms)
                partes = linea.split("time=")
                tiempo_ms = float(partes[1].split(" ")[0])
                tiempos.append(tiempo_ms)
            if "packet loss" in linea:
                # Extraer porcentaje de pérdida
                # Ej: "0% packet loss"
                partes = linea.split("%")
                packet_loss = float(partes[0].split(" ")[-1])

        if not tiempos:
            return None

        # Cálculos Estadísticos
        latencia_prom = round(statistics.mean(tiempos), 2)
        jitter = round(statistics.stdev(tiempos), 2) if len(tiempos) > 1 else 0.0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return [timestamp, TARGET_HOST, latencia_prom, jitter, packet_loss]

    except Exception as e:
        print(f"Error ejecutando ping: {e}")
        return None

# --- BUCLE PRINCIPAL ---
print(f"[*] Iniciando monitoreo de red hacia {TARGET_HOST}...")
print(f"[*] Guardando en {OUTPUT_FILE}")

# Crear encabezados si el archivo no existe
with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Fecha", "Host", "Latencia_ms", "Jitter_ms", "Packet_Loss_%"])

try:
    while True:
        datos = obtener_metricas()
        if datos:
            print(f"Métrica: {datos}")
            with open(OUTPUT_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(datos)
        else:
            print("Time out o error de red.")
        
        time.sleep(INTERVALO)

except KeyboardInterrupt:
    print("\n[!] Monitoreo detenido por el usuario.")
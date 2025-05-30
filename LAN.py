import socket
import time

PC_IP   = "0.0.0.0"  # Ascolta tutte le interfacce
PC_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((PC_IP, PC_PORT))

def get_module_name(motor_id):
    if motor_id in [10, 12]:
        return "MOD1"
    elif motor_id in [20, 22]:
        return "MOD2"
    else:
        return "UNKNOWN"

with open("smartmotor_data.csv", "a") as f:
    # intestazione CSV
    f.write("timestamp_ms,moduleID,motorID,currentSpeed,targetSpeed,PIDOutput,POutput,IOutput,DOutput\n")
    print("In ascolto su UDP port", PC_PORT)

    while True:
        data, addr = sock.recvfrom(256)
        line = data.decode(errors='ignore').strip()

        try:
            # parsing dei campi separati da virgole
            parts = line.split(",")
            motor_id = int(parts[1])  # s.motorID è il secondo campo
            module_id = get_module_name(motor_id)

            timestamp = int(time.time() * 1000)
            csv_line = f"{timestamp},{module_id},{line}\n"
            f.write(csv_line)
            f.flush()
            print(csv_line, end='')

        except Exception as e:
            print(f"\n[ERRORE PARSING] Linea scartata: {line} ({e})\n")

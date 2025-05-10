import socket

PC_IP   = "0.0.0.0"  # 0.0.0.0 ascolta tutte le interfacce
PC_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((PC_IP, PC_PORT))

with open("smartmotor_data.csv", "a") as f:
    # intestazione (solo la prima volta)
    f.write("timestamp_ms,currentSpeed,targetSpeed,PIDOutput,POutput,IOutput,DOutput\n")
    print("In ascolto su UDP port", PC_PORT)
    while True:
        data, addr = sock.recvfrom(256)  # buffer 256 byte
        line = data.decode(errors='ignore')
        f.write(line)
        f.flush()
        print(line, end='')

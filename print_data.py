import matplotlib.pyplot as plt
import matplotlib.animation as animation

CSV_FILE = "smartmotor_data.csv"
MAX_PLOT_POINTS = 1000  # massimo punti da plottare

def parse_csv():
    try:
        with open(CSV_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return [[] for _ in range(7)]

    if len(lines) <= 1:
        return [[] for _ in range(7)]

    lines = lines[1:]  # rimuovi intestazione

    cols = [[] for _ in range(7)]  # 7 colonne
    for line in lines:
        try:
            values = list(map(float, line.strip().split(",")))
            for i in range(7):
                cols[i].append(values[i])
        except:
            continue

    return cols

def animate(i):
    data = parse_csv()
    if not data[0]:
        return

    ax1.clear()
    ax2.clear()

    step = max(1, len(data[0]) // MAX_PLOT_POINTS)
    t = data[0][::step]

    # Primo grafico: Current Speed vs Target Speed
    ax1.plot(t, data[1][::step], label="Current Speed")
    ax1.plot(t, data[2][::step], label="Target Speed")
    ax1.set_ylabel("Speed")
    ax1.legend()
    ax1.grid(True)

    # Secondo grafico: PID, P, I, D Output
    ax2.plot(t, data[3][::step], label="PID Output")
    ax2.plot(t, data[4][::step], label="P Output")
    ax2.plot(t, data[5][::step], label="I Output")
    ax2.plot(t, data[6][::step], label="D Output")
    ax2.set_xlabel("Time [ms]")
    ax2.set_ylabel("Output")
    ax2.legend()
    ax2.grid(True)

    fig.suptitle("SmartMotor - Real-time Monitoring")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
plt.tight_layout()
ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()

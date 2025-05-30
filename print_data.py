import matplotlib.pyplot as plt
import matplotlib.animation as animation

CSV_FILE = "smartmotor_data.csv"
MAX_PLOT_POINTS = 1000  # massimo punti da plottare

def parse_csv():
    try:
        with open(CSV_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return [[] for _ in range(4)]

    if len(lines) <= 1:
        return [[] for _ in range(4)]

    lines = lines[1:]  # salta intestazione

    # Dati per 4 motori: [time], [current], [target]
    motor_data = {
        0: [[], [], []],  # MOD1 M1
        1: [[], [], []],  # MOD1 M2
        3: [[], [], []],  # MOD2 M1
        4: [[], [], []],  # MOD2 M2
    }

    for line in lines:
        try:
            parts = line.strip().split(",")
            timestamp_ms = int(parts[0])
            motor_id = int(parts[2])
            current_speed = float(parts[3])
            target_speed = float(parts[4])
            if motor_id in motor_data:
                motor_data[motor_id][0].append(timestamp_ms)
                motor_data[motor_id][1].append(current_speed)
                motor_data[motor_id][2].append(target_speed)
        except:
            continue

    return motor_data

def animate(i):
    data = parse_csv()

    for ax in axes:
        ax.clear()

    motor_labels = {
        0: "MOD1 - Motor 1",
        1: "MOD1 - Motor 2",
        3: "MOD2 - Motor 1",
        4: "MOD2 - Motor 2"
    }

    for idx, motor_id in enumerate([0, 1, 3, 4]):
        if motor_id not in data:
            continue
        t, current, target = data[motor_id]
        if not t:
            continue
        step = max(1, len(t) // MAX_PLOT_POINTS)
        t = t[::step]
        current = current[::step]
        target = target[::step]
        axes[idx].plot(t, current, label="Current Speed")
        axes[idx].plot(t, target, label="Target Speed")
        axes[idx].set_ylabel("Speed")
        axes[idx].legend()
        axes[idx].grid(True)
        axes[idx].set_title(motor_labels[motor_id])

    axes[-1].set_xlabel("Time [ms]")

# 4 grafici in colonna
fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
plt.tight_layout()
ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()

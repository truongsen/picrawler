from robot_hat import ADC
import time
from collections import deque

battery = ADC('A4')

# Lưu 10 lần đo gần nhất
voltage_history = deque(maxlen=10)


def read_voltage():
    adc_value = battery.read()

    # Robot HAT battery voltage calculation
    voltage = adc_value / 4095 * 3.3 * 3

    return voltage


def voltage_to_percent(voltage):
    # Approximate percentage for a 2S Li-ion battery pack
    points = [
        (8.40, 100),
        (8.35, 95),
        (8.30, 90),
        (8.20, 80),
        (8.10, 70),
        (8.00, 60),
        (7.90, 50),
        (7.80, 40),
        (7.70, 30),
        (7.60, 20),
        (7.40, 10),
        (7.20, 5),
    ]

    if voltage >= 8.40:
        return 100

    if voltage <= 7.20:
        return 0

    # Linear interpolation
    for i in range(len(points) - 1):
        v1, p1 = points[i]
        v2, p2 = points[i + 1]

        if v2 <= voltage <= v1:
            percent = p2 + (voltage - v2) / (v1 - v2) * (p1 - p2)
            return round(percent)

    return 0


def get_status(percent):
    if percent >= 60:
        return "GOOD"
    elif percent >= 30:
        return "NORMAL"
    elif percent >= 15:
        return "LOW"
    else:
        return "CRITICAL"


print("Battery monitor started")
print("Press Ctrl+C to stop")
print("--------------------------------")

try:
    while True:
        voltage = read_voltage()

        # Add current measurement
        voltage_history.append(voltage)

        # Average voltage
        average_voltage = sum(voltage_history) / len(voltage_history)

        percent = voltage_to_percent(average_voltage)
        status = get_status(percent)

        print(
            f"Battery: {average_voltage:.2f} V | "
            f"Level: {percent}% | "
            f"Status: {status}"
        )

        time.sleep(2)

except KeyboardInterrupt:
    print("\nBattery monitor stopped")
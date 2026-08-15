from robot_hat import ADC
import time

battery = ADC('A4')


def voltage_to_percent(voltage):
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

    for i in range(len(points) - 1):
        v1, p1 = points[i]
        v2, p2 = points[i + 1]

        if v2 <= voltage <= v1:
            # Nội suy giữa hai điểm
            percent = p2 + (voltage - v2) / (v1 - v2) * (p1 - p2)
            return round(percent)

    return 0


while True:
    adc_value = battery.read()

    voltage = adc_value / 4095 * 3.3 * 3
    percent = voltage_to_percent(voltage)

    print(f"🔋 Battery: {voltage:.2f} V | 📊 Level: {percent}%")

    time.sleep(2)
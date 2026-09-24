import random
import time
import pandas as pd

print("⛏️ Mine Subsidence AI Simulation")
print("100 Virtual Sensors")
print("Writing live sensor data to sensor_data.csv")
print()

while True:

    sensor_data = []

    for sensor_id in range(1, 101):

        # Normal sensor readings
        tilt = random.uniform(0.1, 0.5)
        displacement = random.uniform(1.0, 3.0)
        vibration = random.uniform(0.05, 0.2)

        # Developing subsidence zone
        if sensor_id in [46, 47, 48, 56, 57, 58, 66, 67, 68]:

            tilt += random.uniform(0.8, 1.5)
            displacement += random.uniform(5.0, 9.0)
            vibration += random.uniform(0.2, 0.5)

        # Warning zone around subsidence
        elif sensor_id in [
            35, 36, 37,
            45, 49,
            55, 59,
            65, 69,
            75, 76, 77
        ]:

            tilt += random.uniform(0.3, 0.8)
            displacement += random.uniform(2.0, 5.0)
            vibration += random.uniform(0.1, 0.3)

        # Automatic risk classification
        if tilt > 1.2 or displacement > 8:
            status = "Critical"

        elif tilt > 0.7 or displacement > 5:
            status = "Warning"

        else:
            status = "Normal"

        sensor_data.append({
            "Sensor": f"S{sensor_id:03d}",
            "Tilt": round(tilt, 2),
            "Displacement": round(displacement, 2),
            "Vibration": round(vibration, 2),
            "Status": status
        })

    # Save current sensor readings
    df = pd.DataFrame(sensor_data)
    df.to_csv("sensor_data.csv", index=False)

    print(
        f"Updated 100 sensors | "
        f"Critical: {(df['Status'] == 'Critical').sum()} | "
        f"Warning: {(df['Status'] == 'Warning').sum()}"
    )

    time.sleep(2)
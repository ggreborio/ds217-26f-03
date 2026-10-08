"""Assignment 03: summarize a telemetry ward's systolic readings.

Run from the assignment directory with the project environment active:

    python3 analysis.py
"""

import numpy as np


def load_readings(filename):
    """Return (patient_ids, monitors, hour_columns, readings) from the supplied CSV.

    readings is a 2D array of integers: one row per patient, one column per
    monitored hour, in the order the header lists them.
    """
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    header = lines[0].strip().split(",")
    rows = [line.strip().split(",") for line in lines[1:] if line.strip()]

    patient_ids = np.array([row[0] for row in rows])
    monitors = np.array([row[1] for row in rows])
    hour_columns = np.array(header[2:])
    readings = np.array([row[2:] for row in rows]).astype(int)
    return patient_ids, monitors, hour_columns, readings


def main():
    patient_ids, monitors, hour_columns, readings = load_readings("data/bp_readings.csv")
    print(f"Loaded {readings.shape[0]} patients x {readings.shape[1]} hours")

    # TODO: answer each question in the README's summary table with NumPy.
    patients = readings.shape[0]
    how_many_readings = readings.size
    mean_sbp = readings.mean()
    sd_sbp = readings.std()
    min_sbp = readings.min()
    max_sbp = readings.max()

    patient_means = readings.mean(axis=1)

    stage2_patients = np.sum(patient_means >= 140)
    highest_patient = patient_ids[np.argmax(patient_means)]
    highest_patient_mean = patient_means[np.argmax(patient_means)]
    peak_hour_column = hour_columns[np.argmax(readings.mean(axis=0))]
    peak_hour_mean = np.max(readings.mean(axis=0))

    #for high_monitor
    monitor_names = sorted(set(monitors))
    monitor_average = []
    for m in sorted(set(monitors)):
        group = patient_means[monitors == m]
        monitor_average.append(group.mean())
    monitor_average = np.array(monitor_average)
    high_monitor = monitor_names[np.argmax(monitor_average)]

    #for monitor_offset
    bool_high_monitor = monitors == high_monitor
    means_above = patient_means[bool_high_monitor]
    means_below = patient_means[~bool_high_monitor]
    monitor_offset = means_above.mean() - means_below.mean()
    stage2_other_monitors = np.sum((means_below >= 140))


    # TODO: write one "key: value" line per answer to output/vitals_summary.txt.
    with open("output/vitals_summary.txt", "w", encoding="utf-8") as file:
        file.write(f"patients: {patients}\n")
        file.write(f"readings: {how_many_readings}\n")
        file.write(f"mean_sbp: {mean_sbp}\n")
        file.write(f"sd_sbp: {sd_sbp}\n")
        file.write(f"min_sbp: {min_sbp}\n")
        file.write(f"max_sbp: {max_sbp}\n")
        file.write(f"stage2_patients: {stage2_patients}\n")
        file.write(f"highest_patient: {highest_patient}\n")
        file.write(f"highest_patient_mean: {highest_patient_mean}\n")
        file.write(f"peak_hour_column: {peak_hour_column}\n")
        file.write(f"peak_hour_mean: {peak_hour_mean}\n")
        file.write(f"high_monitor: {high_monitor}\n")
        file.write(f"monitor_offset: {monitor_offset}\n")
        file.write(f"stage2_other_monitors: {stage2_other_monitors}\n")

if __name__ == "__main__":
    main()

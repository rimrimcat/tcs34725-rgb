import csv
import os
import time
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import serial
from matplotlib.patches import Rectangle


INTEG_TIME = 0.3  # seconds

n_points = 10
val1 = np.linspace(0, 255, n_points).tolist()
val2 = np.linspace(0, 0, n_points).tolist()


## Crayola colors
# df = pd.read_csv("data/crayola_colors.csv", header=0)
# COLORS = [[int(df["r"][i]), int(df["g"][i]), int(df["b"][i])] for i in range(len(df))]

## All?
# _vals = range(0, 256, 50)
# COLORS = [(r, g, b) for r in _vals for g in _vals for b in _vals]

# Only few
COLORS = (
    list(zip(val2, val2, val1))
    + list(zip(val2, val1, val2))
    + list(zip(val1, val2, val2))
    + [(255, 255, 255)]
)


class Recorder:
    def __init__(
        self,
        filename="test.csv",
        dir="data",
        print_header=False,
        baud_rate=9600,
        port="COM3",
        timeout=1,
    ) -> None:
        self.ser = serial.Serial(port=port, baudrate=baud_rate, timeout=timeout)
        print(f"Connected to Arduino on {port}")
        time.sleep(2)

        if not os.path.exists(dir + "/"):
            os.mkdir(dir)
        self.filename = dir + "/" + filename

        self.print_header = print_header

    def close(self):
        self.ser.close()

    def record(
        self,
        record_start=5 * INTEG_TIME * 1.1,
        record_stop=15 * INTEG_TIME * 1.1,
        extra_data=[],
        once_only=False,
    ):
        # Print headers only if empty file
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                csv_len = len(file.readlines())
        else:
            csv_len = 0

        if self.print_header and (csv_len <= 0):
            printed_headers = False
        else:
            printed_headers = True

        with open(self.filename, "+a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)

            start_time = time.time()
            print(f"Logging data to {self.filename}...")

            try:
                while True:
                    if self.ser.in_waiting:
                        # Read line from Arduino
                        try:
                            line = self.ser.readline().decode("utf-8").strip()
                        except UnicodeDecodeError:
                            print("Error on raw input:", self.ser.readline())
                            raise

                        if line and "," in line:  # Append if CSV row
                            # Wait for header

                            values = line.split(",")

                            if not printed_headers:
                                try:
                                    float(values[0])
                                    # If header not printed yet, wait for actual header
                                    print("Waiting for header...")
                                    continue
                                except:
                                    # Header printed
                                    printed_headers = True
                                    start_time = time.time()
                                    csvwriter.writerow(values)
                                    continue

                            if (time.time() - start_time) >= record_start:
                                all_data = values + extra_data
                                csvwriter.writerow(all_data)
                                print(
                                    f"Written line: {",".join([str(x) for x in all_data])}"
                                )
                                if once_only:
                                    return
                            else:
                                print("Waiting for record start...")

                    # Check if duration has elapsed
                    if (time.time() - start_time) >= record_stop:
                        break

            except KeyboardInterrupt:
                print("\nData collection stopped by user")

    def compare(
        self,
        record_start=5 * INTEG_TIME * 1.1,
        record_stop=15 * INTEG_TIME * 1.1,
        expected_data=[],
        once_only=False,
    ):
        start_time = time.time()

        try:
            while True:
                if self.ser.in_waiting:
                    # Read line from Arduino
                    try:
                        line = self.ser.readline().decode("utf-8").strip()
                    except UnicodeDecodeError:
                        print("Error on raw input:", self.ser.readline())
                        raise

                    if line and "," in line:  # Append if CSV row
                        if (time.time() - start_time) >= record_start:
                            values = line.split(",")
                            values = np.array([float(x) for x in values])
                            dist = np.sqrt(np.sum((values - expected_data) ** 2))

                            print("Detected:", values)
                            print("Expected:", expected_data)
                            print("Distance:", dist)
                            if once_only:
                                return
                        else:
                            pass

                    # Check if duration has elapsed
                    if (time.time() - start_time) >= record_stop:
                        break

        except KeyboardInterrupt:
            print("\nData collection stopped by user")


def display_color(color):
    """
    Display or update a color in a matplotlib figure.
    If no figure exists, creates one. If a figure exists, updates its color.

    Args:
        color: RGB tuple normalized to 0-1, e.g. (1,0,0) for red
    """

    # Normalize colors if any > 1
    color = np.array(color)
    if any(color > 1):
        color = color / 255

    # Check if there's an existing figure
    if not plt.get_fignums():
        # Create new figure and make it full screen
        plt.figure(figsize=(16, 9), frameon=False, layout="tight")
        manager = plt.get_current_fig_manager()
        try:
            # Try using Qt backend's fullscreen
            manager.window.showMaximized()
        except:
            try:
                # Try using Tk backend's fullscreen
                manager.resize(*manager.window.maxsize())
            except:
                # If neither works, just make it as large as possible
                manager.full_screen_toggle()

    # Clear the current plot
    plt.clf()

    # Create a colored rectangle that fills the entire plot
    ax = plt.gca()
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=color))

    # Remove axes and margins
    ax.set_axis_off()
    plt.margins(0, 0)
    plt.autoscale(tight=True)

    # Display the plot
    plt.draw()
    plt.pause(0.1)  # Small pause to ensure display updates


if __name__ == "__main__":
    display_color((0, 0, 0))
    input(f"Press enter to start {len(COLORS)} measurements.")
    rec = Recorder()

    for color in COLORS:
        print("Current color:", color)
        display_color(color)

        # rec.record(
        #     record_start=5 * INTEG_TIME * 1.1,
        #     record_stop=10 * INTEG_TIME * 1.1,
        #     extra_data=list(color),
        #     once_only=True,
        # )

        rec.compare(
            record_start=5 * INTEG_TIME * 1.1,
            record_stop=10 * INTEG_TIME * 1.1,
            expected_data=np.array(color),
            once_only=True,
        )

"""Step 5 - Objective 2. A car pulls up, presses the button, and the light changes for it."""

from time import sleep

from gpiozero import LED, Button

from lights import AMBER, GREEN, RED, all_off, apply_state, hold_green
from pins import BUTTON, MAIN_AMBER, MAIN_GREEN, MAIN_RED

MINIMUM_GREEN_SECONDS = 3.0
MAXIMUM_GREEN_SECONDS = 15.0
AMBER_SECONDS = 2.0
RED_SECONDS = 5.0

MAX_CYCLES = 200


def run_one_cycle(lights, button):
    """Hold green until a car asks or the timer runs out, then amber, then red."""
    if lights is None or len(lights) != 3:
        raise ValueError("run_one_cycle() needs exactly (red, amber, green)")
    if button is None:
        raise ValueError("run_one_cycle() needs a Button object")

    apply_state(lights, GREEN)
    car_waiting = hold_green(button, MINIMUM_GREEN_SECONDS, MAXIMUM_GREEN_SECONDS)

    apply_state(lights, AMBER)
    sleep(AMBER_SECONDS)

    apply_state(lights, RED)
    sleep(RED_SECONDS)

    return car_waiting


def run(lights, button, max_cycles):
    """Repeat the cycle up to max_cycles times. Returns how many were cut short by a car."""
    if lights is None or len(lights) != 3:
        raise ValueError("run() needs exactly (red, amber, green)")
    if max_cycles < 1:
        raise ValueError("max_cycles must be at least 1")

    requests = 0
    for cycle in range(max_cycles):
        if run_one_cycle(lights, button):
            requests += 1
            print("Cycle " + str(cycle + 1) + ": a car cut the green short.")
        else:
            print("Cycle " + str(cycle + 1) + ": green ran the full time.")
    return requests


def main():
    """Objective 2: bounce_time hands the debouncing from step 4 to the library."""
    lights = (LED(MAIN_RED), LED(MAIN_AMBER), LED(MAIN_GREEN))
    button = Button(BUTTON, pull_up=True, bounce_time=0.05)
    try:
        run(lights, button, MAX_CYCLES)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        all_off(lights)


if __name__ == "__main__":
    main()

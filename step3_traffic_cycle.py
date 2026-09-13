"""Step 3 - Objective 1. One traffic light cycling green, amber, red on a timer."""

from time import sleep

from gpiozero import LED

from lights import AMBER, GREEN, RED, all_off, apply_state
from pins import MAIN_AMBER, MAIN_GREEN, MAIN_RED

GREEN_SECONDS = 6.0
AMBER_SECONDS = 2.0
RED_SECONDS = 6.0

# Named ceiling so a forgotten script on the bench stops on its own instead of running all night.
MAX_CYCLES = 200


def run_one_cycle(lights):
    """Green, amber, red, once. Returns the seconds the cycle took."""
    if lights is None or len(lights) != 3:
        raise ValueError("run_one_cycle() needs exactly (red, amber, green)")
    if GREEN_SECONDS <= 0 or AMBER_SECONDS <= 0 or RED_SECONDS <= 0:
        raise ValueError("every phase must last longer than zero seconds")

    apply_state(lights, GREEN)
    sleep(GREEN_SECONDS)

    apply_state(lights, AMBER)
    sleep(AMBER_SECONDS)

    apply_state(lights, RED)
    sleep(RED_SECONDS)

    return GREEN_SECONDS + AMBER_SECONDS + RED_SECONDS


def run(lights, max_cycles):
    """Repeat the cycle up to max_cycles times. Returns how many ran."""
    if lights is None or len(lights) != 3:
        raise ValueError("run() needs exactly (red, amber, green)")
    if max_cycles < 1:
        raise ValueError("max_cycles must be at least 1")

    for cycle in range(max_cycles):
        seconds = run_one_cycle(lights)
        print("Cycle " + str(cycle + 1) + " of " + str(max_cycles) + " took " + str(seconds) + "s")
    return max_cycles


def main():
    """Objective 1: the three LEDs cycle in the order a real light uses."""
    lights = (LED(MAIN_RED), LED(MAIN_AMBER), LED(MAIN_GREEN))
    try:
        run(lights, MAX_CYCLES)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        all_off(lights)


if __name__ == "__main__":
    main()

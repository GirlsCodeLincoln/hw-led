"""Objective 3 - a full intersection: two traffic lights, a cross-traffic button, and a safety interlock.

Reference solution. Try to build it yourself from step5_button_request.py before reading this.
"""

from time import sleep

from gpiozero import LED, Button

from lights import AMBER, GREEN, OFF, RED, all_off, apply_state, hold_green, is_safe
from pins import BUTTON, CROSS_AMBER, CROSS_GREEN, CROSS_RED, MAIN_AMBER, MAIN_GREEN, MAIN_RED

MINIMUM_GREEN_SECONDS = 4.0
MAXIMUM_GREEN_SECONDS = 20.0
CROSS_GREEN_SECONDS = 8.0
AMBER_SECONDS = 3.0

# Both directions red between phases so anyone still in the intersection gets out.
ALL_RED_SECONDS = 2.0

MAX_CYCLES = 200
BOUNCE_SECONDS = 0.05


def set_intersection(main_lights, cross_lights, main_state, cross_state):
    """Drive both lights at once, refusing any combination that would let two directions go.

    Returns the pair of states that were shown.
    """
    if main_lights is None or len(main_lights) != 3:
        raise ValueError("set_intersection() needs exactly (red, amber, green) for main")
    if cross_lights is None or len(cross_lights) != 3:
        raise ValueError("set_intersection() needs exactly (red, amber, green) for cross")
    if not is_safe(main_state, cross_state):
        raise ValueError("Unsafe combination refused: main=" + main_state + " cross=" + cross_state)

    apply_state(main_lights, main_state)
    apply_state(cross_lights, cross_state)
    return (main_state, cross_state)


def serve_main_street(main_lights, cross_lights, button):
    """Green on the main street until a car reaches the cross street, then hand the intersection over."""
    if button is None:
        raise ValueError("serve_main_street() needs a Button object")
    if MINIMUM_GREEN_SECONDS > MAXIMUM_GREEN_SECONDS:
        raise ValueError("MINIMUM_GREEN_SECONDS cannot exceed MAXIMUM_GREEN_SECONDS")

    set_intersection(main_lights, cross_lights, GREEN, RED)
    car_waiting = hold_green(button, MINIMUM_GREEN_SECONDS, MAXIMUM_GREEN_SECONDS)

    set_intersection(main_lights, cross_lights, AMBER, RED)
    sleep(AMBER_SECONDS)

    set_intersection(main_lights, cross_lights, RED, RED)
    sleep(ALL_RED_SECONDS)

    return car_waiting


def serve_cross_street(main_lights, cross_lights):
    """Green on the cross street for a fixed time, then hand the intersection back. Returns seconds used."""
    if main_lights is None or cross_lights is None:
        raise ValueError("serve_cross_street() needs both sets of lights")
    if CROSS_GREEN_SECONDS <= 0 or AMBER_SECONDS <= 0:
        raise ValueError("cross green and amber must both last longer than zero seconds")

    set_intersection(main_lights, cross_lights, RED, GREEN)
    sleep(CROSS_GREEN_SECONDS)

    set_intersection(main_lights, cross_lights, RED, AMBER)
    sleep(AMBER_SECONDS)

    set_intersection(main_lights, cross_lights, RED, RED)
    sleep(ALL_RED_SECONDS)

    return CROSS_GREEN_SECONDS + AMBER_SECONDS + ALL_RED_SECONDS


def run(main_lights, cross_lights, button, max_cycles):
    """Run the intersection up to max_cycles times. Returns how many cars triggered an early change."""
    if button is None:
        raise ValueError("run() needs a Button object")
    if max_cycles < 1:
        raise ValueError("max_cycles must be at least 1")

    requests = 0
    for cycle in range(max_cycles):
        if serve_main_street(main_lights, cross_lights, button):
            requests += 1
            print("Cycle " + str(cycle + 1) + ": car waiting, main green cut short.")
        else:
            print("Cycle " + str(cycle + 1) + ": no car, main green ran the full time.")
        serve_cross_street(main_lights, cross_lights)
    return requests


def main():
    """Wire up both lights and the cross-street button, then run the intersection."""
    main_lights = (LED(MAIN_RED), LED(MAIN_AMBER), LED(MAIN_GREEN))
    cross_lights = (LED(CROSS_RED), LED(CROSS_AMBER), LED(CROSS_GREEN))
    button = Button(BUTTON, pull_up=True, bounce_time=BOUNCE_SECONDS)

    try:
        set_intersection(main_lights, cross_lights, OFF, OFF)
        run(main_lights, cross_lights, button, MAX_CYCLES)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        all_off(main_lights)
        all_off(cross_lights)


if __name__ == "__main__":
    main()

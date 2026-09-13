"""Shared traffic light helpers. Import only - nothing here runs on its own."""

from time import sleep

RED = "red"
AMBER = "amber"
GREEN = "green"
OFF = "off"

STATES = (RED, AMBER, GREEN, OFF)

# Amber counts as "go" on purpose: a car already in the box is still crossing.
GO_STATES = (GREEN, AMBER)


def set_led(led, turn_on):
    """Switch one LED on or off. Returns the state it was set to."""
    # Exempt from Rule 4's second check: only apply_state() calls this, and it validates first.
    if led is None:
        raise ValueError("set_led() needs an LED object")

    if turn_on:
        led.on()
    else:
        led.off()
    return turn_on


def apply_state(lights, state):
    """Show one state on a (red, amber, green) trio of LEDs. Returns the state shown."""
    if lights is None or len(lights) != 3:
        raise ValueError("apply_state() needs exactly (red, amber, green)")
    if state not in STATES:
        raise ValueError("Unknown state: " + str(state))

    red, amber, green = lights
    set_led(red, state == RED)
    set_led(amber, state == AMBER)
    set_led(green, state == GREEN)
    return state


def all_off(lights):
    """Darken a trio of LEDs. Returns how many were switched."""
    if lights is None or len(lights) != 3:
        raise ValueError("all_off() needs exactly (red, amber, green)")
    if not isinstance(lights, tuple):
        raise ValueError("all_off() expects a tuple of LEDs")

    apply_state(lights, OFF)
    return len(lights)


def is_safe(main_state, cross_state):
    """False when both directions are permissive at once - the condition a real signal must never reach."""
    if main_state not in STATES:
        raise ValueError("Unknown main state: " + str(main_state))
    if cross_state not in STATES:
        raise ValueError("Unknown cross state: " + str(cross_state))

    main_go = main_state in GO_STATES
    cross_go = cross_state in GO_STATES
    return not (main_go and cross_go)


def hold_green(button, minimum_seconds, maximum_seconds):
    """Hold a green light. Ends early once a car is waiting, but never before the minimum green.

    Returns True when a car cut the green short, False when it ran the full time.
    """
    if button is None:
        raise ValueError("hold_green() needs a Button object")
    if minimum_seconds <= 0 or maximum_seconds < minimum_seconds:
        raise ValueError("need 0 < minimum_seconds <= maximum_seconds")

    # Minimum green is a safety rule, not a style choice: cars already moving need time to clear.
    sleep(minimum_seconds)
    extra_seconds = maximum_seconds - minimum_seconds
    if extra_seconds <= 0:
        return False
    return bool(button.wait_for_press(timeout=extra_seconds))

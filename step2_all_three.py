"""Step 2 - sweep all three LEDs so every wire is proven before any real logic is written."""

from time import sleep

from gpiozero import LED

from lights import AMBER, GREEN, RED, all_off, apply_state
from pins import MAIN_AMBER, MAIN_GREEN, MAIN_RED

SWEEP_COUNT = 4
STEP_SECONDS = 0.4


def sweep(lights, times, step_seconds):
    """Show red, then amber, then green, `times` times over. Returns times."""
    if lights is None or len(lights) != 3:
        raise ValueError("sweep() needs exactly (red, amber, green)")
    if times < 1 or step_seconds <= 0:
        raise ValueError("times and step_seconds must be positive")

    for _ in range(times):
        for state in (RED, AMBER, GREEN):
            apply_state(lights, state)
            sleep(step_seconds)
    all_off(lights)
    return times


def main():
    """A colour that never lights means a dead LED, a backwards LED, or a loose jumper."""
    lights = (LED(MAIN_RED), LED(MAIN_AMBER), LED(MAIN_GREEN))
    try:
        sweep(lights, SWEEP_COUNT, STEP_SECONDS)
        print("Saw red, then amber, then green? Wiring is good. Move on to step 3.")
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        all_off(lights)


if __name__ == "__main__":
    main()

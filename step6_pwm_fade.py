"""Bonus - PWM from the slides. Same pin, same LED, but brightness instead of on/off."""

from time import sleep

from gpiozero import PWMLED

from pins import MAIN_AMBER

FADE_STEPS = 50
STEP_SECONDS = 0.02
FADE_COUNT = 6

# Night mode on a real signal: the amber blinks instead of the light cycling.
NIGHT_BRIGHTNESS = 0.15
NIGHT_BLINKS = 10
BLINK_SECONDS = 0.5


def fade(led, steps, step_seconds):
    """Ramp an LED up from off to full and back down. Returns the number of steps used."""
    if led is None:
        raise ValueError("fade() needs a PWMLED object")
    if steps < 2 or step_seconds <= 0:
        raise ValueError("steps must be at least 2 and step_seconds must be positive")

    for step in range(steps):
        led.value = step / (steps - 1)
        sleep(step_seconds)
    for step in range(steps):
        led.value = 1.0 - (step / (steps - 1))
        sleep(step_seconds)
    led.value = 0.0
    return steps * 2


def night_mode(led, blinks, brightness):
    """Blink the amber at reduced brightness. Returns the number of blinks done."""
    if led is None:
        raise ValueError("night_mode() needs a PWMLED object")
    if blinks < 1 or not 0.0 < brightness <= 1.0:
        raise ValueError("blinks must be positive and brightness must be between 0 and 1")

    for _ in range(blinks):
        led.value = brightness
        sleep(BLINK_SECONDS)
        led.value = 0.0
        sleep(BLINK_SECONDS)
    return blinks


def main():
    """Duty cycle is the whole trick: the LED is still only ever fully on or fully off."""
    led = PWMLED(MAIN_AMBER)
    try:
        for _ in range(FADE_COUNT):
            fade(led, FADE_STEPS, STEP_SECONDS)
        night_mode(led, NIGHT_BLINKS, NIGHT_BRIGHTNESS)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        led.value = 0.0


if __name__ == "__main__":
    main()

"""Step 1 - prove one LED and one GPIO pin work. See README.md."""

from time import sleep

from gpiozero import LED

from pins import MAIN_RED

BLINK_COUNT = 10
ON_SECONDS = 0.5
OFF_SECONDS = 0.5


def blink(led, times, on_seconds, off_seconds):
    """Blink one LED. Returns the number of blinks actually done."""
    if led is None:
        raise ValueError("blink() needs an LED object")
    if times < 1 or on_seconds <= 0 or off_seconds <= 0:
        raise ValueError("times, on_seconds and off_seconds must all be positive")

    for _ in range(times):
        led.on()
        sleep(on_seconds)
        led.off()
        sleep(off_seconds)
    return times


def main():
    """Blink the main red LED, then leave the pin off."""
    led = LED(MAIN_RED)
    try:
        done = blink(led, BLINK_COUNT, ON_SECONDS, OFF_SECONDS)
        print("Blinked " + str(done) + " times on GPIO " + str(MAIN_RED))
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        led.off()


if __name__ == "__main__":
    main()

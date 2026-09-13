"""Step 4 - read the button, and see bouncing with your own eyes before you fix it."""

from time import monotonic, sleep

from gpiozero import Button

from pins import BUTTON

WINDOW_SECONDS = 10.0
POLL_SECONDS = 0.001
DEBOUNCE_SECONDS = 0.05
NO_DEBOUNCE = 0.0


def count_presses(button, window_seconds, debounce_seconds):
    """Count press edges for a fixed window. Pass debounce_seconds=0 to count every raw edge."""
    if button is None:
        raise ValueError("count_presses() needs a Button object")
    if window_seconds <= 0 or debounce_seconds < 0:
        raise ValueError("window_seconds must be positive and debounce_seconds cannot be negative")

    steps = int(window_seconds / POLL_SECONDS)
    presses = 0
    was_pressed = button.is_pressed
    last_press_at = 0.0

    for _ in range(steps):
        sleep(POLL_SECONDS)
        now_pressed = button.is_pressed
        started_pressing = now_pressed and not was_pressed
        was_pressed = now_pressed
        if not started_pressing:
            continue
        now = monotonic()
        if now - last_press_at < debounce_seconds:
            continue
        last_press_at = now
        presses += 1

    return presses


def main():
    """Press the button exactly five times per round, then compare the two counts."""
    button = Button(BUTTON, pull_up=True, bounce_time=None)

    print("Round 1 - no debounce. Press the button 5 times in the next 10 seconds.")
    raw = count_presses(button, WINDOW_SECONDS, NO_DEBOUNCE)
    print("Counted " + str(raw) + " presses.")

    print("Round 2 - with debounce. Press the button 5 times again.")
    clean = count_presses(button, WINDOW_SECONDS, DEBOUNCE_SECONDS)
    print("Counted " + str(clean) + " presses.")

    print("Round 1 usually overcounts. That extra count is the switch contact bouncing.")


if __name__ == "__main__":
    main()

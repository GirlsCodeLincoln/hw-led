# Hardware 1-1: Traffic Light Controller

Girls Code Lincoln, Hardware track 1 (Embedded Systems), Lesson 1.

You are building a working traffic signal on a Raspberry Pi: LEDs on GPIO pins, a button that a
"car" presses, and logic that must never let two directions go at once. Slides for this lesson are
`Hardware 1-1_ Intro to Microcontrollers.pdf`.

---

## Parts

| Part | Quantity | Notes |
|---|---|---|
| Raspberry Pi (3, 4 or 5) with Raspberry Pi OS | 1 | Set up and booted to the desktop |
| Breadboard | 1 | Half-size is plenty |
| Red / amber / green LED | 2 of each | 6 total for the full intersection |
| 330 Ω resistor | 6 | One per LED, never skip it |
| Momentary push button | 1 | Any 4-pin tactile switch |
| Jumper wires (male-to-female) | ~14 | Pi header to breadboard |
| Multimeter | 1 per table | For the troubleshooting section |

## Wiring

Each LED: **GPIO pin → 330 Ω resistor → LED long leg (anode). LED short leg (cathode) → ground.**
The button goes from GPIO 26 to ground; the Pi's internal pull-up resistor handles the rest, so no
extra resistor is needed there.

| Signal | GPIO (BCM) | Physical pin |
|---|---|---|
| Main red | 17 | 11 |
| Main amber | 27 | 13 |
| Main green | 22 | 15 |
| Cross red | 5 | 29 |
| Cross amber | 6 | 31 |
| Cross green | 13 | 33 |
| Button | 26 | 37 |
| Ground | GND | 6, 9, 39 |

All seven numbers live in `pins.py` and nowhere else. If you wire a pin differently, change it there
and every script follows.

## Run it

```bash
cd hw-led
python3 step1_blink.py
```

`gpiozero` ships with Raspberry Pi OS. If yours is missing it, `pip3 install -r requirements.txt`.
Press `Ctrl+C` to stop any script; they all turn the LEDs off on the way out.

---

## Today's objectives

From the slides, in order:

1. **Cycle a light.** Green, amber, red in the correct order. Timing is your call.
2. **Add a button.** A car pulls up and asks for the light to change. Handle button bounce.
3. **Add cross traffic.** A second trio of LEDs that switches with the first and never creates an
   unsafe condition.

## The ladder

Work down this list. Each file runs on its own and builds on the one above it.

| File | Teaches | Objective |
|---|---|---|
| `step1_blink.py` | One pin, one LED, on and off | Wiring check |
| `step2_all_three.py` | All three LEDs, one state at a time | Wiring check |
| `step3_traffic_cycle.py` | Timed phases in a bounded loop | 1 |
| `step4_button_test.py` | Reading an input, and seeing bounce | 2 |
| `step5_button_request.py` | Button changes the light | 2 |
| `main.py` | Two lights plus a safety interlock | 3 |
| `step6_pwm_fade.py` | PWM brightness and night mode | Bonus |
| `pins.py`, `lights.py` | Shared pin map and light helpers | Imported by the rest |

`main.py` is the reference solution. Try objective 3 yourself from `step5_button_request.py` before
you open it.

---

## Lesson pieces

### 1 — A pin is a voltage, not a light

An output pin sets voltage; an input pin reads it. Above 2.3 V is `True`, below 1 V is `False`, and
in between is where bugs live. `led.on()` is just "put 3.3 V on this pin", and the LED is what makes
that visible.

Mini-task: change `MAIN_RED` in `pins.py` to another pin, move the jumper, run `step1_blink.py`.

Real-world tie: the same read-a-voltage step sits under thermostats, smoke detectors, fuel gauges,
and every limit switch on a factory line.

### 2 — State, not commands

`lights.py` names four states: `RED`, `AMBER`, `GREEN`, `OFF`. `apply_state()` sets all three LEDs
from one state, so it is impossible to leave two colours lit by forgetting a line.

Mini-task: add a `FLASHING_RED` state for a four-way stop.

Real-world tie: state machines run elevators, vending machines, ATM screens, and the checkout flow
on any website you have used.

### 3 — Timing is the program

`step3_traffic_cycle.py` is phases and delays, nothing more. Change `GREEN_SECONDS` and the whole
intersection feels different. Note `MAX_CYCLES`: no loop in this repo runs forever, so a script
someone forgets on the bench stops on its own.

Mini-task: make the green twice as long as the red, then swap it.

Real-world tie: control loops with a fixed tick are how cruise control, PLCs on an assembly line,
and heart-rate monitors work.

### 4 — Bouncing is real

A push button's metal contacts physically bounce, so one press can register as five. Run
`step4_button_test.py`, press exactly five times per round, and compare the counts. Round 1 counts
every raw edge; round 2 ignores anything within 50 ms of the last press.

`step5_button_request.py` hands the same job to the library with `Button(BUTTON, bounce_time=0.05)`.
Now you know what that argument is actually doing.

Mini-task: lower `DEBOUNCE_SECONDS` to 0.001 and see the bouncing come back.

Real-world tie: debouncing applies to keyboards, elevator call buttons, coin acceptors, and the
retry logic in network code.

### 5 — Minimum green is a safety rule

`hold_green()` waits the minimum green **before** it will look at the button. A car already moving
through the intersection needs that time. Cutting a green short on demand is what real actuated
signals do, and the minimum is why they don't cause crashes.

Mini-task: set `MINIMUM_GREEN_SECONDS = 0.1` and press the button repeatedly. Watch the light become
useless.

Real-world tie: minimum dwell times guard elevator doors, garage doors, press brakes, and railway
crossing gates.

### 6 — The interlock

`is_safe()` returns `False` whenever both directions are green or amber. `set_intersection()` calls
it and raises rather than lighting an unsafe pair. The program crashes instead of causing a wreck.

Amber counts as "go" on purpose: a car already in the box is still crossing. The all-red gap between
phases is there for the same reason.

Mini-task: in `main.py`, call `set_intersection(main_lights, cross_lights, GREEN, GREEN)` and watch
it refuse.

Real-world tie: interlocks stop a microwave running with its door open, a lathe spinning with the
guard up, and two trains entering one section of track.

### 7 — PWM (bonus)

`step6_pwm_fade.py` fades an LED. The pin is still only ever fully on or fully off; it just switches
fast enough that your eye averages it. That ratio is the duty cycle. The slides' motor example is
the same trick at a different scale.

Mini-task: dim every LED to 20 % for a "night mode" version of `main.py`.

Real-world tie: PWM drives motor speed, servo position, LED dimming, and laptop fan control.

---

## Troubleshooting with a multimeter

| Symptom | Check | What to expect |
|---|---|---|
| LED never lights | Continuity mode across the jumper | Beep. No beep means a bad wire |
| LED never lights | LED direction | Long leg toward the resistor and the GPIO pin |
| LED never lights | DC volts, GPIO pin to ground, while the script says "on" | About 3.3 V |
| LED is very dim | Resistor value | 330 Ω, not 3.3 kΩ. Check the colour bands |
| Button does nothing | Continuity across the button, pressed and released | Beep only when pressed |
| Button acts pressed constantly | Which pins of the button you used | Tactile switches connect in pairs; use diagonal corners |

`ImportError` or a pin-factory error on a Pi 5 usually means `lgpio` is missing:
`sudo apt install python3-lgpio`.

## Pick an extension

- **Pedestrian crossing.** A second button and a walk/don't-walk LED that only runs during all-red.
- **Latched request.** Remember a press that happens during the cross-street phase instead of
  dropping it.
- **Left turn arrow.** A fourth LED and a protected-turn phase, without breaking `is_safe()`.
- **Rush hour mode.** Longer main-street greens between 4 and 6 pm using `datetime`.
- **Emergency vehicle preempt.** Hold everything red, flash the main red, then recover safely.
- **Fault detection.** Refuse to start if any state would leave all three LEDs dark.

## Learning goals checklist

By the end you should be able to:

- Explain the difference between a microcontroller and a single-board computer
- Wire an LED with the correct resistor and polarity, and a button with a pull-up
- Set and read a GPIO pin from Python
- Describe a system as named states with timed transitions
- Explain what switch bounce is and two ways to handle it
- Write a guard that refuses an unsafe combination instead of trusting the caller
- Explain how PWM fakes an analog output
- Find a broken connection with a multimeter

## Suggested three-hour block

| Time | What |
|---|---|
| 0:00 – 0:35 | Slides: embedded systems, microcontroller vs computer, GPIO, PWM |
| 0:35 – 0:55 | Breadboard the main light, multimeter check, `step1` and `step2` |
| 0:55 – 1:25 | Objective 1: `step3` |
| 1:25 – 1:35 | Break |
| 1:35 – 2:05 | Objective 2: `step4` and `step5` |
| 2:05 – 2:50 | Objective 3: build it, `main.py` as reference |
| 2:50 – 3:00 | Demo each table's intersection |

# nomad-color-picker
A color picker widget for the Work Louder Nomad v1. Capture any color from your screen, display it on the keyboard's IPS screen, copy it , and modify it directly with the knobs.

## Requirements

### Hardware
Work Louder Nomad v1

### Firmware & Software
- firmware_v0.9.0-sdk.1_merged.bin
- input 0.15.0-sdk.1

### Python
- Python 3.x
- pyautogui library
- Pillow library


### Install py dependencies:
pip install pyautogui Pillow

## Features
- Color capture
- Full-screen color swatch 
- Clipboard copy
- Saturation and brightness control with knob
- Screensaver gradient animation (after ~10 seconds of inactivity a gradient animation create with the selected color will start)

## Controls
- FpToggle / color picker mode on/off (dot indicator appears) 
- BTN 1 (top-left) / Copy HEX color to clipboard
- BTN 2 (top-right) / Capture color under cursor
- OPERATOR 1 (left knob) / Adjust Saturation (0–200, step 5)
- OPERATOR 2 (right knob) / Adjust Brightness/Luminosity (10–200, step 5)

! In this widget, the fp input is an on/off toggle be aware to not hold fp when using the color picker

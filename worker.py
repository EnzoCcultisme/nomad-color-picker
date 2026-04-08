import js

register_notify("wlsdk.capture")
register_notify("wlsdk.copy_hex")

log("Color Picker is running")

# ENTER ABSOLUTE PATH TO grab_color.py
GRAB_PATH = r"\Work Louder SDK Widget\color-picker-sdk-widget-git-1.0\grab_color.py"

def do_capture():
    result = exec_process(f"python \"{GRAB_PATH}\"")
    if not result:
        log("Error : grab_color.py return nothing")
        return
    parts = result.strip().split(",")
    if len(parts) != 3:
        log(f"Wrong format : {result}")
        return
    r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
    hex_val = f"#{r:02X}{g:02X}{b:02X}"
    h, s, l = rgb_to_hsl(r, g, b)
    data = {"hex": hex_val, "r": r, "g": g, "b": b,
            "h": h, "s": s, "l": l}
    log(f"Color captured : {hex_val}")
    send_rpc("wlsdk.color_result", data)

def do_copy(hex_val):
    safe = hex_val.replace("#", "")
    exec_process(f'powershell -command "Set-Clipboard -Value \'#{safe}\'"')
    log(f"Copy on clipboard : #{safe}")

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx = max(r, g, b)
    mn = min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        h = s = 0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:   h = (g - b) / d + (6 if g < b else 0)
        elif mx == g: h = (b - r) / d + 2
        else:         h = (r - g) / d + 4
        h /= 6
    return round(h*360), round(s*100), round(l*100)

def handle_notify(method, params):
    if method == "wlsdk.capture":
        do_capture()
    elif method == "wlsdk.copy_hex":
        do_copy(params)
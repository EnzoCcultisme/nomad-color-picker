import js
register_notify("color.capture")
register_notify("color.copy_hex")
last_hex = "#000000"
GRAB_PATH = r"C:\Users\ENTER ABSOLUTE PATH TO grab_color.py"
def to_hex(n):
    x="0123456789ABCDEF"
    return x[n//16]+x[n%16]
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
    data = {"hex": hex_val, "r": r, "g": g, "b": b, "h": h, "s": s, "l": l}
    global last_hex
    last_hex = hex_val
    log(f"Color captured : {hex_val}")
    send_rpc("color.data", data)
def do_copy(params):
    parts=str(params).split(",")
    if len(parts)==3:
        r=int(parts[0]);g=int(parts[1]);b=int(parts[2])
        safe=to_hex(r)+to_hex(g)+to_hex(b)
    else:
        safe=last_hex.replace("#","")
    exec_process(f'powershell -command "Set-Clipboard -Value \'#{safe}\'"')
    log("Copied: #"+safe)
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
    if method == "color.capture":
        do_capture()
    elif method == "color.copy_hex":
        do_copy(str(params))

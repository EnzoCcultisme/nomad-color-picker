import pyautogui
from PIL import ImageGrab

x, y = pyautogui.position()
img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
r, g, b = img.getpixel((0, 0))
print(f"{r},{g},{b}", end="")

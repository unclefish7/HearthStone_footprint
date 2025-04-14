import pyautogui
import time

print("请将鼠标移动到目标位置（3秒后开始显示坐标）")
time.sleep(3)
while True:
    x, y = pyautogui.position()
    print(f"当前鼠标坐标: ({x}, {y})", end="\r")
    time.sleep(0.1)

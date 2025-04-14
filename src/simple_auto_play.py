import cv2
import numpy as np
import pyautogui
import time
import random
import os

# 获取脚本所在路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# 获取屏幕截图
def get_image(source=None, region=None):
    if source:
        return cv2.imread(source)
    screenshot = pyautogui.screenshot(region=region)
    return np.array(screenshot)

# 平滑模拟鼠标移动 + 抖动 + 速度扰动
def smooth_move_to(x, y, duration=None, steps=1):
    duration = duration if duration is not None else random.uniform(0.1, 0.2)
    steps = steps if steps is not None else random.randint(18, 28)
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        t = i / steps
        curr_x = int(start_x + (x - start_x) * t + random.randint(-2, 2))
        curr_y = int(start_y + (y - start_y) * t + random.randint(-2, 2))
        pyautogui.moveTo(curr_x, curr_y)
        time.sleep(duration / steps)
    pyautogui.moveTo(x, y)

# 慢速游走模拟（空闲状态）
def idle_mouse_wiggle():
    screen_w, screen_h = pyautogui.size()
    center_x = screen_w // 2 + random.randint(-100, 100)
    center_y = screen_h // 2 + random.randint(-100, 100)
    duration = random.uniform(0.3, 0.6)
    steps = random.randint(8, 12)
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        t = i / steps
        x = int(start_x + (center_x - start_x) * t + random.randint(-2, 2))
        y = int(start_y + (center_y - start_y) * t + random.randint(-2, 2))
        pyautogui.moveTo(x, y)
        time.sleep(duration / steps)
    pyautogui.moveTo(center_x, center_y)

# 点击指定坐标
def click(x, y):
    smooth_move_to(x, y)
    pyautogui.click()
    time.sleep(0.5)

# 主循环逻辑
def run_loop():

    # 坐标配置
    start_button = (1870, 1177)
    confirm_button = (1291, 1135)
    card_positions = [
        (1100, 1321),
        (1225, 1321),
        (1350, 1321)
    ]
    middle_pos = (602, 829)
    skill_pos = (1519, 1095)
    end_turn_pos = (2062, 659)
    click_anywhere = (974, 177)
    own_minion_positions = [
        (1130, 784),
        (1400, 784),
        (1250, 784)
    ]
    enemy_face = (1287, 277)

    while True:
        screenshot = get_image()
        img_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        def has_template(filename, threshold=0.85):
            try:
                path = os.path.join(ASSETS_DIR, filename)
                template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)
                return len(loc[0]) > 0
            except:
                return False

        if has_template("start_button.png"):
            print("准备界面：点击开始")
            click(*start_button)

        elif has_template("confirm_button.png"):
            print("开始界面：点击确定")
            click(*confirm_button)

        elif has_template("end_turn_button.png"):
            print("游戏中：打3张牌 + 技能 + 攻击 + 结束回合")
            for pos in card_positions:
                click(*pos)
                click(*middle_pos)
            click(*skill_pos)
            for attacker in own_minion_positions:
                click(*attacker)
                click(*enemy_face)
            click(*end_turn_pos)

        elif has_template("victory.png") or has_template("defeat.png"):
            print("游戏结束界面：点击任意位置返回")
            for _ in range(2):
                click(*click_anywhere)
                time.sleep(2)

        else:
            print("等待匹配...鼠标游走中")
            idle_mouse_wiggle()
            time.sleep(0.5)

if __name__ == "__main__":
    run_loop()

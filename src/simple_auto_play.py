import cv2
import numpy as np
import pyautogui
import time
import random

# 获取屏幕截图
def get_image(source=None, region=None):
    if source:
        return cv2.imread(source)
    screenshot = pyautogui.screenshot(region=region)
    return np.array(screenshot)

# 平滑模拟鼠标移动 + 抖动 + 速度扰动
def smooth_move_to(x, y, duration=None, steps=None):
    duration = duration if duration is not None else random.uniform(0.3, 0.6)
    steps = steps if steps is not None else random.randint(18, 28)
    start_x, start_y = pyautogui.position()
    for i in range(steps):
        t = i / steps
        curr_x = int(start_x + (x - start_x) * t + random.randint(-2, 2))
        curr_y = int(start_y + (y - start_y) * t + random.randint(-2, 2))
        pyautogui.moveTo(curr_x, curr_y)
        time.sleep(duration / steps)
    pyautogui.moveTo(x, y)

# 点击指定坐标
def click(x, y):
    smooth_move_to(x, y)
    pyautogui.click()
    time.sleep(0.5)

# 主循环逻辑
def run_loop():
    screen_w, screen_h = pyautogui.size()

    # 坐标配置
    start_button = (screen_w // 2, screen_h // 2 + 200)
    confirm_button = (screen_w // 2, screen_h // 2 + 250)
    card_pos = (screen_w // 2 - 300, screen_h - 150)
    skill_pos = (screen_w // 2 + 250, screen_h - 150)
    end_turn_pos = (screen_w - 180, screen_h // 2)
    click_anywhere = (screen_w // 2, screen_h // 2)

    while True:
        screenshot = get_image()
        img_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # 状态识别简化为图像中是否包含特定模板（需提前准备模板图）
        def has_template(path, threshold=0.85):
            try:
                template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)
                return len(loc[0]) > 0
            except:
                return False

        if has_template("assets/start_button.png"):
            print("准备界面：点击开始")
            click(*start_button)

        elif has_template("assets/confirm_button.png"):
            print("开始界面：点击确定")
            click(*confirm_button)

        elif has_template("assets/end_turn_button.png"):
            print("游戏中：出牌 + 技能 + 结束回合")
            click(*card_pos)
            click(*skill_pos)
            click(*end_turn_pos)

        elif has_template("assets/victory.png") or has_template("assets/defeat.png"):
            print("游戏结束界面：点击任意位置返回")
            for _ in range(5):
                click(*click_anywhere)
                time.sleep(1)

        else:
            print("等待匹配中...")
            time.sleep(2)

if __name__ == "__main__":
    run_loop()

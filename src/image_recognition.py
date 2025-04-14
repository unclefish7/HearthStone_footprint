import cv2
import numpy as np
import pyautogui
import time

# 获取屏幕截图或加载测试图像
def get_image(source=None, region=None):
    if source:
        return cv2.imread(source)
    screenshot = pyautogui.screenshot(region=region)
    return np.array(screenshot)

# 模板匹配函数
def match_template(image, template_path, threshold=0.85):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(res >= threshold)
    return list(zip(*locations[::-1]))

# 绘制检测框
def draw_detection_boxes(image, positions, template_path):
    template = cv2.imread(template_path)
    h, w = template.shape[:2]
    for pos in positions:
        cv2.rectangle(image, pos, (pos[0] + w, pos[1] + h), (0, 255, 0), 2)
    cv2.imshow("Detected", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 识别函数

def detect_own_turn(image):
    screen_w, screen_h = pyautogui.size()
    region = (screen_w // 2, 0, screen_w // 2, screen_h)
    if image is None:
        image = get_image(region=region)
    else:
        image = image[:, screen_w // 2:]
    return match_template(image, "assets/own_turn_indicator.png")

def detect_end_turn(image):
    screen_w, screen_h = pyautogui.size()
    region = (screen_w // 2, 0, screen_w // 2, screen_h)
    if image is None:
        image = get_image(region=region)
    else:
        image = image[:, screen_w // 2:]
    return match_template(image, "assets/end_turn_button.png")

def detect_own_cards(image):
    screen_w, screen_h = pyautogui.size()
    region = (0, screen_h // 2, screen_w, screen_h // 2)
    if image is None:
        image = get_image(region=region)
    else:
        image = image[screen_h // 2:, :]
    return match_template(image, "assets/green_card_border.png")

def detect_own_minions(image):
    screen_w, screen_h = pyautogui.size()
    region = (0, screen_h // 2, screen_w, screen_h // 2)
    if image is None:
        image = get_image(region=region)
    else:
        image = image[screen_h // 2:, :]
    return match_template(image, "assets/green_border.png")

def detect_skill(image):
    screen_w, screen_h = pyautogui.size()
    region = (0, screen_h // 2, screen_w, screen_h // 2)
    if image is None:
        image = get_image(region=region)
    else:
        image = image[screen_h // 2:, :]
    return match_template(image, "assets/green_skill_border.png")

def detect_enemy_minions(image):
    screen_w, screen_h = pyautogui.size()
    region = (0, 0, screen_w, screen_h // 2)
    if image is None:
        image = get_image(region=region)
    else:
        image = image[:screen_h // 2, :]
    return match_template(image, "assets/taunt_border.png")

def detect_enemy_hero(image):
    screen_w, screen_h = pyautogui.size()
    region = (0, 0, screen_w, screen_h // 2)
    if image is None:
        image = get_image(region=region)
    else:
        image = image[:screen_h // 2, :]
    return match_template(image, "assets/enemy_hero.png")

# 主测试函数
def main(test_image_path=None):
    screen = get_image(source=test_image_path)

    own_turn = detect_own_turn(screen.copy())
    if own_turn:
        print("It's your turn!")
        draw_detection_boxes(screen.copy(), own_turn, "assets/own_turn_indicator.png")

    end_turn = detect_end_turn(screen.copy())
    if end_turn:
        print("End turn button detected.")
        draw_detection_boxes(screen.copy(), end_turn, "assets/end_turn_button.png")

    own_cards = detect_own_cards(screen.copy())
    if own_cards:
        print(f"Detected {len(own_cards)} playable card(s).")
        draw_detection_boxes(screen.copy(), own_cards, "assets/green_card_border.png")

    own_minions = detect_own_minions(screen.copy())
    if own_minions:
        print(f"Detected {len(own_minions)} own minion(s) that can attack.")
        draw_detection_boxes(screen.copy(), own_minions, "assets/green_border.png")

    skills = detect_skill(screen.copy())
    if skills:
        print(f"Detected {len(skills)} usable skill(s).")
        draw_detection_boxes(screen.copy(), skills, "assets/green_skill_border.png")

    enemy_minions = detect_enemy_minions(screen.copy())
    if enemy_minions:
        print(f"Detected {len(enemy_minions)} enemy minion(s) with taunt.")
        draw_detection_boxes(screen.copy(), enemy_minions, "assets/taunt_border.png")

    enemy_hero = detect_enemy_hero(screen.copy())
    if enemy_hero:
        print(f"Detected enemy hero.")
        draw_detection_boxes(screen.copy(), enemy_hero, "assets/enemy_hero.png")

if __name__ == "__main__":
    # 示例：main("test_screenshot.png") 或 main() 截图运行
    main()
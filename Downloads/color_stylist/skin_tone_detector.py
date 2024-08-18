import cv2
import numpy as np

def detect_skin_tone(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(hsv_image, lower_skin, upper_skin)
    skin = cv2.bitwise_and(image, image, mask=skin_mask)
    total_color = np.sum(skin, axis=(0, 1))
    num_skin_pixels = np.count_nonzero(skin_mask)
    if num_skin_pixels > 0:
        average_color = total_color / num_skin_pixels
    else:
        return None
    b, g, r = average_color
    if r > 200 and g > 200 and b > 200:
        return "Light"
    elif r > 150 and g > 150 and b > 150:
        return "Medium"
    else:
        return "Dark"

def recommend_colors(skin_tone):
    recommendations = {
        "Light": ["Navy", "Burgundy", "Forest Green", "Deep Purple"],
        "Medium": ["Coral", "Olive Green", "Teal", "Dusty Rose"],
        "Dark": ["Gold", "Emerald", "Royal Blue", "Bright Orange"]
    }
    return recommendations.get(skin_tone, [])
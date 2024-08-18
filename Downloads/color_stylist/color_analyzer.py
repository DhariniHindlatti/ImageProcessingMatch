import cv2
import numpy as np
from collections import Counter

def detect_colors(image, num_colors=10):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image.reshape(-1, 3)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, labels, centers = cv2.kmeans(pixels.astype(np.float32), num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    color_counts = Counter(labels.flatten())
    colors = centers.astype(int)
    total_pixels = labels.size
    color_percentages = [(color_counts[i] / total_pixels * 100, tuple(color)) for i, color in enumerate(colors)]
    color_percentages.sort(reverse=True)
    return color_percentages

def classify_color(rgb):
    r, g, b = rgb
    if r > 200 and g > 200 and b > 200:
        return "White"
    elif r < 50 and g < 50 and b < 50:
        return "Black"
    elif r > max(g, b):
        return "Red"
    elif g > max(r, b):
        return "Green"
    elif b > max(r, g):
        return "Blue"
    elif r > 200 and g > 200 and b < 100:
        return "Yellow"
    else:
        return "Other"

def analyze_wardrobe(tops_image, bottoms_image):
    tops_colors = detect_colors(tops_image)
    bottoms_colors = detect_colors(bottoms_image)
    classified_tops = [classify_color(color) for _, color in tops_colors]
    classified_bottoms = [classify_color(color) for _, color in bottoms_colors]
    return classified_tops, classified_bottoms
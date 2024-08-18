import os
import uuid
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from color_analyzer import analyze_wardrobe
from color_matcher import match_colors
from skin_tone_detector import detect_skin_tone, recommend_colors
from database import Session, UserWardrobe, UserSkinTone

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())
        session = Session()

        tops_file = request.files['tops']
        bottoms_file = request.files['bottoms']
        selfie_file = request.files['selfie']

        if tops_file and bottoms_file and selfie_file:
            tops_filename = os.path.join(UPLOAD_FOLDER, f"{user_id}_tops.jpg")
            bottoms_filename = os.path.join(UPLOAD_FOLDER, f"{user_id}_bottoms.jpg")
            selfie_filename = os.path.join(UPLOAD_FOLDER, f"{user_id}_selfie.jpg")

            tops_file.save(tops_filename)
            bottoms_file.save(bottoms_filename)
            selfie_file.save(selfie_filename)

            tops_image = cv2.imread(tops_filename)
            bottoms_image = cv2.imread(bottoms_filename)
            selfie_image = cv2.imread(selfie_filename)

            tops_colors, bottoms_colors = analyze_wardrobe(tops_image, bottoms_image)
            matches = match_colors(tops_colors, bottoms_colors)

            skin_tone = detect_skin_tone(selfie_image)
            color_recommendations = recommend_colors(skin_tone)

            for color in tops_colors:
                session.add(UserWardrobe(user_id=user_id, item_type='top', color=color, percentage=0))
            for color in bottoms_colors:
                session.add(UserWardrobe(user_id=user_id, item_type='bottom', color=color, percentage=0))

            session.add(UserSkinTone(user_id=user_id, skin_tone=skin_tone))

            session.commit()

            return jsonify({
                'matches': matches,
                'skin_tone': skin_tone,
                'recommendations': color_recommendations
            })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
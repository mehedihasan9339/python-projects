import os
import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from PIL import Image
import io

app = Flask(__name__)
FINGERPRINT_FOLDER = 'wwwroot/Fingers'  # Folder containing PNG images


def read_image_from_base64(base64_string):
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data)).convert("L")
        return np.array(image)
    except Exception as e:
        print("Error decoding image:", e)
        return None


def match_images(img1, img2):
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return 0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    try:
        matches = bf.match(des1, des2)
    except cv2.error:
        return 0

    matches = sorted(matches, key=lambda x: x.distance)
    score = sum([1 - (m.distance / 256) for m in matches]) / len(matches)
    return round(score * 100, 2)  # Return as percentage


@app.route('/api/match', methods=['POST'])
def match_fingerprint():
    data = request.json
    base64_img = data.get("base64Image")
    if not base64_img:
        return jsonify({"error": "Missing base64Image"}), 400

    input_img = read_image_from_base64(base64_img)
    if input_img is None:
        return jsonify({"error": "Invalid base64"}), 400

    best_match = None
    best_score = 0

    for file in os.listdir(FINGERPRINT_FOLDER):
        if file.lower().endswith('.png'):
            file_path = os.path.join(FINGERPRINT_FOLDER, file)
            db_img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if db_img is None:
                continue
            score = match_images(input_img, db_img)
            print(f"{file} => {score}%")
            if score > best_score:
                best_score = score
                best_match = file

    if best_score >= 60:  # Adjust threshold as needed
        return jsonify({
            "fileName": best_match,
            "matchPercent": best_score
        })
    else:
        return jsonify({
            "fileName": None,
            "matchPercent": 0
        })


if __name__ == '__main__':
    app.run(debug=True)

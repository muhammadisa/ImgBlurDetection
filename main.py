# import the necessary packages
from flask import Flask, json, request
import os
import cv2

app = Flask(__name__)


def variance_of_laplacian(img):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(img, cv2.CV_64F).var()


def image_blur_detection(path):
    img = cv2.imread(path)
    gray_crl = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray_crl)

    threshold = 1000

    if fm > threshold:
        return {
            "blur_level": fm,
            "categorized": "CLEAR",
        }
    elif fm < threshold:
        return {
            "blur_level": fm,
            "categorized": "BLURRY",
        }


@app.route('/blurry/detection', methods=['POST'])
def welcome():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    else:
        response = app.response_class(
            response=json.dumps({"file": "required"}),
            status=400,
            mimetype='application/json'
        )
        return response

    image_res = image_blur_detection(uploaded_file.filename)

    if os.path.exists(uploaded_file.filename):
        os.remove(uploaded_file.filename)

    response = app.response_class(
        response=json.dumps(image_res),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1828)

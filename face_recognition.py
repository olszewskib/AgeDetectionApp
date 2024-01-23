import cv2 as cv
import numpy as np
from keras.models import load_model

classifier_path = (
    "venv/lib/python3.11/site-packages/cv2/data/haarcascade_frontalface_default.xml"
)

best_model = load_model("resources/model.h5")


def detect_faces(image):
    face_cascade = cv.CascadeClassifier(classifier_path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    if len(faces) > 0:
        for face in faces:
            x, y, w, h = face

            face_rectangle = image[y : y + h, x : x + w]

            # Preprocess the face image
            preprocessed_face = preprocess_face_image(face_rectangle)

            # Make predictions using the model
            predicted_age = best_model.predict(
                np.expand_dims(preprocessed_face, axis=0)
            )  # Add batch dimension
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(
                image,
                str(predicted_age),
                (x, y + h + 20),
                cv.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )
    else:
        preprocessed_face = preprocess_face_image(image)

        # Make predictions using the model
        predicted_age = best_model.predict(
            np.expand_dims(preprocessed_face, axis=0)
        )  # Add batch dimension
        print(predicted_age, preprocessed_face.shape)

    return image


def preprocess_face_image(face_img):
    # Convert the image to grayscale
    gray = cv.cvtColor(face_img, cv.COLOR_RGB2GRAY)

    # Apply Canny edge detection to find edges
    edges = cv.Canny(gray, 100, 200)

    # Perform dilation to thicken the edges
    kernel = np.ones((3, 3), np.uint8)
    thick_edges = cv.dilate(edges, kernel, iterations=2)
    img_combined = cv.addWeighted(
        face_img, 0.7, cv.cvtColor(thick_edges, cv.COLOR_GRAY2RGB), 0.3, 0
    )
    img_combined = cv.resize(img_combined, (200, 200))
    img_combined = img_combined.astype(np.float32) / 255.0

    return img_combined

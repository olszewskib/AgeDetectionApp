import cv2 as cv

classifier_path = 'venv/lib/python3.11/site-packages/cv2/data/haarcascade_frontalface_default.xml'

def detect_faces(image):
    face_cascade = cv.CascadeClassifier(classifier_path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

def choose_data_source():
    while True:
        choice = input("Wybierz źródło danych (k - kamera, o - obraz, f - film, q - wyjście): ")
        if choice == 'k':
            # Źródło danych: kamera
            cap = cv.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_with_faces = detect_faces(frame)
                cv.imshow('Face Detection', frame_with_faces)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv.destroyAllWindows()
        elif choice == 'o':
            # Źródło danych: obraz
            image_path = input("Podaj ścieżkę do obrazu: ")
            image = cv.imread(image_path)
            if image is not None:
                image_with_faces = detect_faces(image)
                cv.namedWindow('Face Detection', cv.WINDOW_NORMAL)
                cv.imshow('Face Detection', image_with_faces)
                cv.waitKey(0)
                cv.destroyAllWindows()
            else:
                print("Nie można odczytać obrazu.")
        elif choice == 'f':
            # Źródło danych: film
            video_path = input("Podaj ścieżkę do filmu: ")
            cap = cv.VideoCapture(video_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_with_faces = detect_faces(frame)
                cv.namedWindow('Face Detection', cv.WINDOW_NORMAL)  # Ustalenie rozmiaru okna
                cv.imshow('Face Detection', frame_with_faces)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv.destroyAllWindows()
        elif choice == 'q':
            break
        else:
            print("Nieprawidłowy wybór. Wybierz 'k', 'o', 'f' lub 'q'.")

if __name__ == "__main__":
    choose_data_source()
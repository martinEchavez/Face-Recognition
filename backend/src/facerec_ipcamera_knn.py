import cv2
import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG'}

def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    X = []
    y = []

    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


def predict(X_frame, knn_clf=None, model_path=None, distance_threshold=0.5):
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    X_face_locations = face_recognition.face_locations(X_frame)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test image
    faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("desconocido", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


def show_prediction_labels_on_image(frame, predictions):
    pil_image = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # enlarge the predictions for the full sized image.
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0))

        # There's a bug in Pillow where it blows up with non-UTF-8 text
        # when using the default bitmap font
        name = name.encode("UTF-8")
        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 255, 0), outline=(0, 255, 0))
        draw.text((left + 2, bottom - text_height - 2), name, fill=(0, 0, 0, 255))
    # Remove the drawing library from memory as per the Pillow docs.
    del draw
    # Save image in open-cv format to be able to show it.

    opencvimage = np.array(pil_image)
    return opencvimage

def show_date(frame, text):
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    parrafo = text + time
    fuente = cv2.FONT_HERSHEY_TRIPLEX #Se agrega una fuetes
    imagen = np.zeros(shape=(500, 500, 3), dtype=np.int16)
    cv2.rectangle(frame, (0,0), (210, 10), color=(0,0,0), thickness=10)
    cv2.putText(frame, parrafo, org=(5,10), fontFace=fuente, fontScale=0.4, color=(0,255,0), thickness=1, lineType=cv2.LINE_8)
    return time

if __name__ == "__main__":
    print("Training KNN classifier...")
    #ruta= os.path.isdir("knn_examples/train")
    #print(ruta)
    #trainnet = os.path.exists('trained_knn_model.clf')
    #if trainnet:
    #    print("Training complete!")
    #else:
    #classifier = train("knn_examples/train", model_save_path="trained_knn_model.clf", n_neighbors=2)
    # process one frame in every 30 frames for speed
    #process_this_frame = 29
    print('Setting cameras up...')

    cap_0 = cv2.VideoCapture(0)
    cap_1 = cv2.VideoCapture(1)

    w_0 = int(cap_0.get(cv2.CAP_PROP_FRAME_WIDTH))
    h_0 = int(cap_0.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    w_1 = int(cap_1.get(cv2.CAP_PROP_FRAME_WIDTH))
    h_1 = int(cap_1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    code = cv2.VideoWriter_fourcc(*'XVID')
    record_0 = cv2.VideoWriter('Video_0.mp4', code, 20.0, (w_0,h_0))
    record_1 = cv2.VideoWriter('Video_1.mp4', code, 20.0, (w_1,h_1))
    while True:
        ret_0, frame_0 = cap_0.read()
        ret_1, frame_1 = cap_1.read()
        if ret_0:
            # Different resizing options can be chosen based on desired program runtime.
            # Image resizing for more stable streaming
            frame_0 = cv2.flip(frame_0, 1)
            show_date(frame_0, 'Entrada ')
            img_0 = cv2.resize(frame_0, (0, 0), fx=0.5, fy=0.5)
            #process_this_frame = process_this_frame + 1
            #if process_this_frame % 30 == 0:
            predictions_0 = predict(img_0, model_path="trained_knn_model.clf")
            frame_0 = show_prediction_labels_on_image(frame_0, predictions_0)
            record_0.write(frame_0)
            cv2.imshow('camera_0', frame_0)
        if ret_1:
            # Different resizing options can be chosen based on desired program runtime.
            # Image resizing for more stable streaming
            frame_1 = cv2.flip(frame_1, 1)
            show_date(frame_1, 'Salida ')
            img_1 = cv2.resize(frame_1, (0, 0), fx=0.5, fy=0.5)
            #process_this_frame = process_this_frame + 1
            #if process_this_frame % 30 == 0:
            predictions_1 = predict(img_1, model_path="trained_knn_model.clf")
            frame_1 = show_prediction_labels_on_image(frame_1, predictions_1)
            record_1.write(frame_1)
            cv2.imshow('camera_1', frame_1)
        if ord('q') == cv2.waitKey(10):
            cap_0.release()
            cap_1.release()
            record_0.release()
            record_1.release()
            cv2.destroyAllWindows()
            exit(0)
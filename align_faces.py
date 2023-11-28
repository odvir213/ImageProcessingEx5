from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--root_dir", required=True, help="path to root directories of input images")
ap.add_argument("-d", "--des_dir", required=True, help="path to destination directories of output images")
ap.add_argument("-p", "--pred_dir", required=True, help="path to pre-trained shape predictor model")
args = vars(ap.parse_args())

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["pred_dir"])
fa = FaceAligner(predictor, desiredFaceWidth=128)

root_dir = args["root_dir"]
des_dir = args["des_dir"].split("/")[-1]

if not os.path.exists(des_dir):
    os.mkdir(des_dir)

input_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(root_dir)) for f in fn]

# loop over the face detections
for input_file in input_files:
    try:
        print(input_file)
        image = cv2.imread(input_file)
        image = imutils.resize(image, width=800)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        des_path = os.path.join('..', des_dir, *input_file.split("/")[2:-1])

        # Ensure the output directory exists
        os.makedirs(des_path, exist_ok=True)

        file_name, file_extension = os.path.splitext(input_file.split("/")[-1])
        out_file = os.path.join(des_path, f"{file_name}(0){file_extension}")

        # show the original input image and detect faces in the grayscale image
        rects = detector(gray, 2)
        for rect in rects:
            try:
                (x, y, w, h) = rect_to_bb(rect)
                faceOrig = imutils.resize(image[y:y + h, x:x + w], width=128)
                faceAligned = fa.align(image, gray, rect)

                # display the output images
                cv2.imwrite(out_file, faceAligned)
                cv2.waitKey(0)
                print(out_file)
            except Exception as e:
                print("CANNOT SAVE")
                continue
    except Exception as e:
        pass

import cv2
import numpy as np

class PictCompare():

    def pc(images):
        if len(images)>=2:
            W = 1000
            original = cv2.imread(images[-2])
            second = cv2.imread(images[-1])

            height, width, dept = original.shape
            imgScale = W/width
            newX, newY = original.shape[1]*imgScale, original.shape[0]*imgScale
            dupX, dupY = second.shape[1]*imgScale, second.shape[0]*imgScale
            newimg = cv2.resize(original, (int(newX), int(newY)))
            secimg = cv2.resize(second, (int(newX), int(newY)))
            greyori = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            greysec = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)

            if original.shape == second.shape:
                print ("The images have the same size and channels")
                difference = cv2.subtract(greyori, greysec)
                cv2.imshow("Diff", difference)

            sift = cv2.xfeatures2d.SIFT_create()
            kp_1, desc_1 = sift.detectAndCompute(greyori, None)
            kp_2, desc_2 = sift.detectAndCompute(greysec, None)

            print("Keypoing for ori image: " + str(len(kp_1)))
            print("Keypoing for dup image: " + str(len(kp_2)))

            index_params = dict(algorithm = 0, trees = 5)
            search_params = dict()
            flann = cv2.FlannBasedMatcher(index_params, search_params)

            matches = flann.knnMatch(desc_1, desc_2, k=2)
            print(len(matches))

            good_points = []
            for m, n in matches:
                if m.distance < 0.6*n.distance:
                    good_points.append(m)

            number_keypoints = 0
            if len(kp_1) <= len(kp_2):
                number_keypoints = len(kp_1)
            else:
                number_keypoints = len(kp_2)

            print("Good matches: ", len(good_points))

            print("how good is the match: ", len(good_points) * 100 / number_keypoints, "%")
            if len(good_points) * 100 / number_keypoints < 100:
                changed_img.append(images[-1])

            print (len(changed_img)/len(images))
            print ("maszyna jest włączona: ", len(images)*30/60/60, " godziny")
            print("maszyna pracowała w tym czasie: ", len(changed_img)*30/60/60, " godziny")
            result = cv2.drawMatches(greyori, kp_1, greysec, kp_2, good_points, None)

            cv2.imshow("result", result)

            cv2.imshow("Original", cv2.resize(original, None, fx=0.2, fy=0.2))
            cv2.imshow("Compared", cv2.resize(second, None, fx=0.2, fy=0.2))

            cv2.waitKey(0)
            cv2.destroyAllWindows()
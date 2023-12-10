import cv2

# 헤드라인
def line_landmark(landmarks_dict, image_width, image_height):
    left_ear_x = landmarks_dict["left_ear"][0] * image_width
    left_ear_y = landmarks_dict["left_ear"][1] * image_height

    right_ear_x = landmarks_dict["right_ear"][0] * image_width
    right_ear_y = landmarks_dict["right_ear"][1] * image_height

    head_center_x = int((left_ear_x + right_ear_x) / 2)
    head_center_y = int((left_ear_y + right_ear_y) / 2)

    radius = int((left_ear_x - right_ear_x) / 2)
    radius = max(radius, 20)

    left_ankle_x = landmarks_dict["left_ankle"][0] * image_width
    left_ankle_y = landmarks_dict["left_ankle"][1] * image_height

    right_ankle_x = landmarks_dict["right_ankle"][0] * image_width
    right_ankle_y = landmarks_dict["right_ankle"][1] * image_height

    ankle_center_x = int((left_ankle_x + right_ankle_x) / 2)  # 기준선  x좌표값
    ankle_center_y = int((left_ankle_y + right_ankle_y) / 2)

    right_shoulder_x = landmarks_dict["right_shoulder"][0] * image_width
    right_shoulder_y = landmarks_dict["right_shoulder"][1] * image_height


    #right_eye_inner_x = landmarks_dict["right_eye_inner"][0] *image_width
    #right_eye_inner_y = landmarks_dict["right_eye_inner"][1] * image_height

    # 반환값으로 변수들을 반환
    return head_center_x,head_center_y,ankle_center_x,ankle_center_y,radius,right_shoulder_y,left_ear_x


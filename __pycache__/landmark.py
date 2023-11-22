import mediapipe as mp

def get_landmark(mp_pose,landmark):
    mp_pose=mp.solutions.pose
    nose=[landmark[mp_pose.PoseLandmark.NOSE.value].x,
          landmark[mp_pose.PoseLandmark.NOSE.value].y]#0번
    left_eye_inner=[landmark[mp_pose.PoseLandmark.LEFT_EYE_INNER].x,
                    landmark[mp_pose.PoseLandmark.LEFT_EYE_INNER].y]#1번
    left_eye = [landmark[mp_pose.PoseLandmark.LEFT_EYE].x,
                      landmark[mp_pose.PoseLandmark.LEFT_EYE].y]#2번
    left_eye_outer = [landmark[mp_pose.PoseLandmark.LEFT_EYE_OUTER].x,
                      landmark[mp_pose.PoseLandmark.LEFT_EYE_OUTER].y]#3번
    right_eye_inner = [landmark[mp_pose.PoseLandmark.RIGHT_EYE_INNER].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_EYE_INNER].y]#4번
    right_eye = [landmark[mp_pose.PoseLandmark.RIGHT_EYE].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_EYE].y]#5번
    right_eye_outer = [landmark[mp_pose.PoseLandmark.RIGHT_EYE_OUTER].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_EYE_OUTER].y]#6번
    left_ear = [landmark[mp_pose.PoseLandmark.LEFT_EAR].x,
                      landmark[mp_pose.PoseLandmark.LEFT_EAR].y]#7번
    right_ear = [landmark[mp_pose.PoseLandmark.RIGHT_EAR].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_EAR].y]#8번
    mouth_left = [landmark[mp_pose.PoseLandmark.MOUTH_LEFT].x,
                      landmark[mp_pose.PoseLandmark.MOUTH_LEFT].y]#9번
    mouth_right = [landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].x,
                      landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].y]#10번
    left_shoulder = [landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                      landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y]#11번
    right_shoulder = [landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                     landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]  # 11번
    left_elbow = [landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x,
                      landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y]#13번
    right_elbow = [landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y]#14번
    left_wrist = [landmark[mp_pose.PoseLandmark.LEFT_WRIST].x,
                      landmark[mp_pose.PoseLandmark.LEFT_WRIST].y]#15번
    right_wrist = [landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y]#16번
    left_pinky = [landmark[mp_pose.PoseLandmark.LEFT_PINKY].x,
                      landmark[mp_pose.PoseLandmark.LEFT_PINKY].y]#17번
    right_pinky = [landmark[mp_pose.PoseLandmark.RIGHT_PINKY].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_PINKY].y]#18번
    left_index = [landmark[mp_pose.PoseLandmark.LEFT_INDEX].x,
                      landmark[mp_pose.PoseLandmark.LEFT_INDEX].y]#19번
    right_index = [landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y]#20번
    left_thumb = [landmark[mp_pose.PoseLandmark.LEFT_THUMB].x,
                      landmark[mp_pose.PoseLandmark.LEFT_THUMB].y]#21번
    right_thumb = [landmark[mp_pose.PoseLandmark.RIGHT_THUMB].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_THUMB].y]#22번
    left_hip = [landmark[mp_pose.PoseLandmark.LEFT_HIP].x,
                      landmark[mp_pose.PoseLandmark.LEFT_HIP].y]#23번
    right_hip = [landmark[mp_pose.PoseLandmark.RIGHT_HIP].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_HIP].y]#24번
    left_knee = [landmark[mp_pose.PoseLandmark.LEFT_KNEE].x,
                      landmark[mp_pose.PoseLandmark.LEFT_KNEE].y]#25번
    right_knee = [landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_KNEE].y]#26번
    left_ankle = [landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x,
                      landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y]#27번
    right_ankle = [landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y]#28번
    left_heel= [landmark[mp_pose.PoseLandmark.LEFT_HEEL].x,
                      landmark[mp_pose.PoseLandmark.LEFT_HEEL].y]#29번
    right_heel = [landmark[mp_pose.PoseLandmark.RIGHT_HEEL].x,
                      landmark[mp_pose.PoseLandmark.RIGHT_HEEL].y]#30번
    left_foot_index = [landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x,
                      landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y]#31번
    right_foot_index = [landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x,
                       landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y]#32번

# 변수들을 딕셔너리에 담아서 반환
    landmarks_dict = {
        "nose": nose,
        "left_eye_inner": left_eye_inner,
        "left_eye": left_eye,
        "left_eye_outer": left_eye_outer,
        "right_eye_inner": right_eye_inner,
        "right_eye": right_eye,
        "right_eye_outer": right_eye_outer,
        "left_ear": left_ear,
        "right_ear": right_ear,
        "mouth_left": mouth_left,
        "mouth_right": mouth_right,
        "left_shoulder": left_shoulder,
        "right_shoulder": right_shoulder,
        "left_elbow": left_elbow,
        "right_elbow": right_elbow,
        "left_wrist": left_wrist,
        "right_wrist": right_wrist,
        "left_pinky": left_pinky,
        "right_pinky": right_pinky,
        "left_index": left_index,
        "right_index": right_index,
        "left_thumb": left_thumb,
        "right_thumb": right_thumb,
        "left_hip": left_hip,
        "right_hip": right_hip,
        "left_knee": left_knee,
        "right_knee": right_knee,
        "left_ankle": left_ankle,
        "right_ankle": right_ankle,
        "left_heel": left_heel,
        "right_heel": right_heel,
        "left_foot_index": left_foot_index,
        "right_foot_index": right_foot_index
    }
    return landmarks_dict



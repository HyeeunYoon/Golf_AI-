# 기준 선
# 각도 재는 방법 (일단 하나만)
# 58-84 line

import cv2
import mediapipe as mp
from calculate_angle import calculate_angle
from input_slow import slowmotion
from landmark import get_landmark
from line_landmark import line_landmark
from feedback import *


def pose_drawing(video_path, output_path):
    # mediapipe pose 초기화
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils  # 그래픽 생성
    mp_drawing_styles = mp.solutions.drawing_styles  # 그래픽 스타일
    cap = cv2.VideoCapture(video_path) #동영상 파일 열기
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 총 프레임 개수
    fps = int(cap.get(cv2.CAP_PROP_FPS)) #초당 프레임 수

    frame_size = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # 출력 동영상 파일 설정
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    #피드백 딕셔너리 정의 (None으로 해두면 address 먼저 is_first에서 받았을 때 feedback_dict의 나머지 값들이 None이라서 오류가 뜸 ->그래서 -1로 초기화
    feedback_dict = {'address': -1, 'takeback': -1, 'backswing': -1, 'top': -1, 'impact_eye': -1,
                     'impact_knee': -1, 'impact_foot': -1}
    #피드백 변수 선언 (초기화)
    shoulder_len = 0
    tb_cnt =0
    bs_cnt =0
    total_tb_fr=0
    total_bs_fr=0
    total_ip_fr=0
    red_head = 0

    with (mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=2) as pose):

        # 어드레스 시 첫 프레임을 받아오기 위한 플래기
        is_first = True

        while cap.isOpened():
            # 프레임 읽기
            ret, frame = cap.read()
            if not ret:
                break

            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) #동영상 프레임을 BGER->RGB로 변환
            current_time = (cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0) #프레임 당 현재 시각
            image_height, image_width, _ = frame.shape

            if not results.pose_landmarks:
                continue

            annotated_frame = frame.copy() # 결과 그리기

            mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=4, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=4))

# get_landmark 함수 호출
            landmark = results.pose_landmarks.landmark
            landmarks_dict = get_landmark(mp_pose, landmark)

# 페이스/기준선 라인 첫 지점
            # 페이스 작업을 위한 랜드마크
            head_center_x, head_center_y, ankle_center_x, ankle_center_y, radius,right_shoulder_y,right_eye_inner_y = line_landmark(landmarks_dict, image_width, image_height)

            #첫 프레임
            if is_first:
                first_head_center_x, first_head_center_y, first_ankle_center_x, first_ankle_center_y, first_radius,first_right_shoulder_y,first_right_eye_inner_y \
                 = head_center_x, head_center_y, ankle_center_x, ankle_center_y, int(radius * 2),right_shoulder_y,right_eye_inner_y
                #어드레스 피드백
                feedback_dict['address'],shoulder_len = address_feedback(feedback_dict,landmarks_dict)
                is_first = False
            #첫 프레임 다음부터
            else:
                # 첫 프레임 헤드 생성
                cv2.circle(annotated_frame, center=(first_head_center_x, first_head_center_y),radius=first_radius, color=(0, 255, 255), thickness=2)
                # 기준 선 라인 생성
                cv2.line(annotated_frame, (int(first_ankle_center_x), 0), (first_ankle_center_x, image_height),(198, 219, 218), 2)
                cv2.line(annotated_frame, (0,int(first_right_shoulder_y)), (image_width,int(first_right_shoulder_y)),(198, 219, 218), 2)
                cv2.line(annotated_frame, (0, int(first_right_eye_inner_y)), (image_width, int(first_right_eye_inner_y)),(198, 219, 218), 2)

                color = (0, 255, 0)  # 초록색
                # 머리가 원래 위치보다 많이 벗어난 경우 ->초록에서 빨강
                if head_center_x - radius < first_head_center_x - first_radius or head_center_x + radius > first_head_center_x + first_radius:
                    color = (0, 0, 255)  # 빨간색
                    #impact_eye 피드백에 활용 (어드레스-임팩트 구간 내 헤드라인 빨간색이였던 프레임 개수)
                    if(0 <=current_time<=2):  #Time['address']<=current_time<=Time['impact']
                        red_head = red_head+1
                # 실시간 헤드라인
                cv2.circle(annotated_frame, center=(head_center_x, head_center_y),radius=radius, color=color, thickness=2)
# 페이스/기준선 끝 지점

#feedback 호출
            feedback_dict['takeback'],tb_cnt,total_tb_fr = takeback_feedback(feedback_dict,landmarks_dict,current_time,tb_cnt,total_tb_fr)        #takeback
            feedback_dict['backswing'], bs_cnt, total_bs_fr = takeback_feedback(feedback_dict, landmarks_dict, current_time, bs_cnt,total_bs_fr)  #backswing
            feedback_dict['top'] = top_feedback(feedback_dict, landmarks_dict, current_time, first_right_eye_inner_y,image_height)                #top
            feedback_dict['impact_eye'],total_ip_fr = impact_eye(feedback_dict, current_time, red_head, total_ip_fr)                              #impact_eye
            feedback_dict['impact_knee'] = impact_knee(feedback_dict, landmarks_dict, current_time)                                               #impact_knee
            feedback_dict['impact_foot'] = impact_foot(feedback_dict,landmarks_dict,current_time,shoulder_len)                                    #impact_foot

            # 결과 동영상 파일에 추가
            out.write(annotated_frame)
            # 결과 출력
            cv2.imshow("MediaPipe Pose", annotated_frame)
            if cv2.waitKey(1) == ord('q'):
                break

    # 종료 후 정리
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('feedback_dict', feedback_dict)

if __name__ == "__main__":
    video_path = 'C:\\Users\\hyeeu\\OneDrive\\사진\\카메라 앨범\\pro2.mp4'  # 입력 동영상 파일 경로
    output_path = 'C:\\Users\\hyeeu\\OneDrive\\사진\\카메라 앨범\\output_file4.mp4'  # 출력 동영상 파일 경로
    # 쭈현이꺼
    # video_path = "C:\\Users\\eju20\\OneDrive\\capstone\\practice_3.mp4"  # 입력 동영상 파일 경로
    # output_path = "C:\\Users\\eju20\\OneDrive\\capstone\\output_1.mp4"  # 출력 동영상 파일 경로
    slow_path = slowmotion(video_path)
    pose_drawing(slow_path, output_path)


import cv2
from landmark import get_landmark
from calculate_angle import calculate_angle

#1.address
def address_feedback(feedback_dict,landmarks_dict):
    left_shoulder_x  = landmarks_dict["left_shoulder"][0]
    right_shoulder_x  = landmarks_dict["right_shoulder"][0]
    shoulder_len = left_shoulder_x - right_shoulder_x

    left_foot_index_x = landmarks_dict["left_foot_index"][0]
    right_foot_index_x = landmarks_dict["right_foot_index"][0]
    foot_len = left_foot_index_x - right_foot_index_x

    #print("어깨 간격",shoulder_len,"발 간격",foot_len)
    if(foot_len >= shoulder_len):
        if(foot_len>= (shoulder_len+0.2)):
            feedback_dict = {"address": 0}
        else:
            feedback_dict = {"address" : 1}
    elif(foot_len < shoulder_len):
        feedback_dict = {"address": -1}

    return feedback_dict['address'],shoulder_len




#2.takeback
def takeback_feedback(feedback_dict,landmarks_dict,current_time,tb_cnt,total_tb_fr): #!!!!!!!!!!!!!!!!!!!!!time dic 만들어지면 인자에 추가
    if (0 <= current_time <= 1.5): #Time['address'] <= current_time < Time['back']
        total_tb_fr = total_tb_fr + 1
        left_arm_angle = calculate_angle(landmarks_dict['left_shoulder'], landmarks_dict['left_elbow'],landmarks_dict['left_wrist'])
        # 사잇각이 170도를 넘으면
        if left_arm_angle < 170:
            tb_cnt = tb_cnt + 1
    # 170도 넘은게 구간 내의 (총프레임/2)보다 많으면 (==반 이상이 잘못된 자세일 경우)
        if(current_time == 1.5): #current_time == Time['back']
            if (tb_cnt > (total_tb_fr / 2)):
                feedback_dict['takeback'] = 0  # 피드백 필요한 경우
            else:
                feedback_dict['takeback'] = 1  # 피드백 필요없는 경우
    return feedback_dict['takeback'],tb_cnt,total_tb_fr





#3.backswing
def backswing_feedback(feedback_dict,landmarks_dict,current_time,bs_cnt,total_bs_fr):
    if (1.5 <= current_time <= 3): #Time['back'] <= current_time < Time['back_top']
        total_bs_fr = total_bs_fr+ 1
        left_arm_angle = calculate_angle(landmarks_dict['left_shoulder'], landmarks_dict['left_elbow'],landmarks_dict['left_wrist'])
        # 사잇각이 160도를 넘으면
        if left_arm_angle < 160:
            # count 1 증가 (1프레임 당 1씩 증가임)
            bs_cnt = bs_cnt + 1
    # 160도 넘은게 구간 내의 (총프레임/2)보다 많으면 (==반 이상이 잘못된 자세일 경우)
    if(current_time == 3):  #current_time == Time['back_top']
        if (bs_cnt > (total_bs_fr / 2)):
            feedback_dict['backswing'] = 0  # 피드백 필요한 경우
        else:
            feedback_dict['backswing'] = 1  # 피드백 필요없는 경우

    return feedback_dict['backswing'], bs_cnt, total_bs_fr





#4.top_feedback
def top_feedback(feedback_dict,landmarks_dict,current_time,first_right_eye_inner_y,image_height):
    if(current_time==1.8): #current_time == Time['back_top']
        if(first_right_eye_inner_y >= landmarks_dict['left_thumb'][1]*image_height):
            feedback_dict['top'] = 1
        else:
            feedback_dict['top'] = 0
    return feedback_dict['top']





#5, impact - eye
def impact_eye(feedback_dict,current_time,red_head,total_ip_fr):
    if (0<= current_time <= 2):# Time['address'] <= current_time < Time['impact']
        total_ip_fr = total_ip_fr + 1
        if(current_time == 2): #current_time == Time['impact']
            if(red_head > (total_ip_fr/2)):
                feedback_dict['impact_eye'] = 0
            else:
                feedback_dict['impact_eye'] = 1
    return feedback_dict['impact_eye'],total_ip_fr





#6, impact - 발 간격
def impact_knee(feedback_dict,landmarks_dict,current_time):
    if(current_time == 2.2): #Time['impact']
        knee_len = (landmarks_dict['left_knee'][0])-(landmarks_dict['right_knee'][0])
        if(knee_len > 0.2): ###############time되면 전문가 테스트해보고 다시 오차값 결정해야함
            feedback_dict['impact_knee'] = 0
        else:
            feedback_dict['impact_knee'] = 1
    return feedback_dict['impact_knee']




#7, impact - 발 간격
def impact_foot(feedback_dict,landmarks_dict,current_time,shoulder_len):

    left_foot_index_x = landmarks_dict["left_foot_index"][0]
    right_foot_index_x = landmarks_dict["right_foot_index"][0]
    foot_len = left_foot_index_x - right_foot_index_x

    # print("어깨 간격",shoulder_len,"발 간격",foot_len)
    if(current_time == 3): #current_time == Time['impact']
        if(foot_len >= shoulder_len):
            if(foot_len>= (shoulder_len+0.2)):
                feedback_dict = {"impact_foot": 0}
            else:
                feedback_dict = {"impact_foot": 1}
        elif(foot_len < shoulder_len):
            feedback_dict = {"impact_foot": -1}

    return feedback_dict['impact_foot']






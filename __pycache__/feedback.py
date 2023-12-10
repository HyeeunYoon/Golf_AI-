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

    if(foot_len >= shoulder_len):
        if(foot_len>= (shoulder_len+0.2)):
            feedback_dict = {"address": 0}
        else:
            feedback_dict = {"address" : 1}
    elif(foot_len < shoulder_len):
        feedback_dict = {"address": -1}
    print('address :',feedback_dict['address'])
    return feedback_dict['address'],shoulder_len




#2.takeback
def takeback_feedback(feedback_dict, landmarks_dict, current_time, tb_cnt, total_tb_fr, Time, tb_tmp,tb_angle): #!!!!!!!!!!!!!!!!!!!!!time dic 만들어지면 인자에 추가
    left_arm_angle = calculate_angle(landmarks_dict['left_shoulder'], landmarks_dict['left_elbow'],landmarks_dict['left_wrist'])
    #팔 각도 170보다 낮은 경우 cnt 세는 코드
    if (Time['address'] <= current_time  and Time['address']!=-1 and tb_tmp==0): #어드레스를 지났을 때
        total_tb_fr = total_tb_fr + 1
        # 사잇각이 170도를 못 넘으면
        if left_arm_angle < 165:
            tb_cnt = tb_cnt + 1
            tb_angle.append(left_arm_angle)
            if((current_time > Time['back']) and Time['back']!= -1):#알고보니 테이크백 지난 경우일 때
                total_tb_fr = total_tb_fr -1
                tb_cnt = tb_cnt - 1
                tb_angle.pop()

    if(current_time >= Time['back'] and tb_tmp==0 and Time['back'] != -1):
        tb_tmp = tb_tmp + 1
        if (tb_cnt > (total_tb_fr / 2)):
            feedback_dict['takeback'] = sum(tb_angle)/tb_cnt  # 피드백 필요한 경우 ->각도 평균값
        else:
            feedback_dict['takeback'] = 1  # 피드백 필요없는 경우
        print('takeback :',feedback_dict['takeback'])

    return feedback_dict['takeback'],tb_cnt,total_tb_fr,tb_tmp,tb_angle





#3.backswing
##########################문제 ) 너무 구간이 짧아서 못 들어오는건지,확인 (68번재 줄 print가 출력 안 됨)
def backswing_feedback(feedback_dict, landmarks_dict, current_time, bs_cnt, total_bs_fr, Time, bs_tmp,bs_angle):
    left_arm_angle = calculate_angle(landmarks_dict['left_shoulder'], landmarks_dict['left_elbow'],landmarks_dict['left_wrist'])
    if (Time['back'] <= current_time and Time['back']!=-1):
        total_bs_fr = total_bs_fr + 1
        # 사잇각이 160도를 못 넘으면
        if left_arm_angle < 155:
            bs_cnt = bs_cnt + 1
            bs_angle.append(left_arm_angle)
            if((current_time >= Time['back_top']) and Time['back_top']!= -1):#알고보니 백탑 지난 경우일 때
                total_tb_fr = total_bs_fr -1
                bs_cnt = bs_cnt - 1
                bs_angle.pop()


    # 160도 넘은게 구간 내의 (총 프레임/2)보다 많으면 (==반 이상이 잘못된 자세일 경우)
    if(current_time >= Time['back_top'] and bs_tmp ==0 and Time['back_top']!= -1) :
        bs_tmp = bs_tmp + 1
        if (bs_cnt > (total_bs_fr / 2)):
            feedback_dict['backswing'] = sum(bs_angle)/bs_cnt  # 피드백 필요한 경우
        else:
            feedback_dict['backswing'] = 1  # 피드백 필요없는 경우
        print('backswing :',feedback_dict['backswing'])

    return feedback_dict['backswing'], bs_cnt, total_bs_fr,bs_tmp,bs_angle





#4.top_feedback
def top_feedback(feedback_dict,landmarks_dict,current_time,first_head_center_y,image_height,Time,top2_tmp,first_head_center_x,first_left_ear_x):
    if(current_time > Time['back_top'] and top2_tmp ==0 and Time['back_top']!=-1):
        top2_tmp = top2_tmp + 1
        right_wrist = (landmarks_dict['right_wrist'][1] * image_height)
        first_radius = (abs(int(first_head_center_x - first_left_ear_x)))
        if((first_head_center_y - first_radius > right_wrist)):
            feedback_dict['top'] = 1
        else:
            feedback_dict['top'] = 0
        print('top :',feedback_dict['top'])
    return feedback_dict['top'],top2_tmp




#5, impact - eye
def impact_eye(feedback_dict,current_time,red_head,total_ip_fr,Time,impact_eye_tmp):
    if (Time['address'] <= current_time and Time['address']!=-1 and impact_eye_tmp ==0 ):
        total_ip_fr = total_ip_fr + 1
        if(current_time >= Time['impact'] and Time['impact']!=-1 and impact_eye_tmp==0 ):
            if(red_head > (total_ip_fr/2)):
                feedback_dict['impact_eye'] = 0
            else:
                feedback_dict['impact_eye'] = 1
            impact_eye_tmp = impact_eye_tmp + 1

            print('impact_eye :',feedback_dict['impact_eye'])
    return feedback_dict['impact_eye'],total_ip_fr,impact_eye_tmp





#6, impact - 발 간격
def impact_knee(feedback_dict, landmarks_dict, current_time,Time,impact_knee_tmp,shoulder_len):
    left_knee_index_x = landmarks_dict["left_knee"][0]
    right_knee_index_x = landmarks_dict["right_knee"][0]
    knee_len = left_knee_index_x - right_knee_index_x

    if (current_time >= Time['impact'] and Time['impact'] != -1 and impact_knee_tmp == 0):
        if (knee_len > shoulder_len + 0.3):
            feedback_dict = {"impact_knee": 0}#너무 넓은 경우
        elif (knee_len < shoulder_len):
            feedback_dict = {"impact_knee": 1}#적당한 경우
        impact_knee_tmp = impact_knee_tmp + 1
        print('impact_knee :',feedback_dict['impact_knee'])

    return feedback_dict['impact_knee'], impact_knee_tmp





#7, impact - 발 간격
def impact_foot(feedback_dict,landmarks_dict,current_time,shoulder_len,Time,impact_foot_tmp):

    left_foot_index_x = landmarks_dict["left_foot_index"][0]
    right_foot_index_x = landmarks_dict["right_foot_index"][0]
    foot_len = left_foot_index_x - right_foot_index_x

    if(current_time >= Time['impact'] and Time['impact']!= -1 and impact_foot_tmp ==0 ):
        if(foot_len >= shoulder_len):
            if(foot_len>= (shoulder_len+0.2)):
                feedback_dict = {"impact_foot": 0}
            else:
                feedback_dict = {"impact_foot": 1}
        elif(foot_len < shoulder_len):
            feedback_dict = {"impact_foot": -1}
        impact_foot_tmp = impact_foot_tmp + 1
        print('impact_foot :',feedback_dict['impact_foot'])

    return feedback_dict['impact_foot'],impact_foot_tmp















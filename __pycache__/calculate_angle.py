import numpy as np
def calculate_angle(a, b, c):
    # 각 값을 받아 넘파이 배열로 변형
    a = np.array(a)  # 첫 번째
    b = np.array(b)  # 두 번째
    c = np.array(c)  # 세 번째

    # 라디안을 계산하고 실제 각도로 변경한다.
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    # 180도가 넘으면 360에서 뺀 값을 계산한다.
    if angle > 180.0:
        angle = 360 - angle

    # 각도를 리턴한다.
    return angle
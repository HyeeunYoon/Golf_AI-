import cv2

def slowmotion(input_path) :
    # 비디오 파일을 읽어옵니다.
    #input_path = "C:\\Users\\hyeeu\\OneDrive\\사진\\카메라 앨범\\pro2.mp4"
    cap = cv2.VideoCapture(input_path)

    # 비디오의 속성을 가져옵니다.
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #duration = frame_count / fps

    # 슬로우 모션으로 만들기 위해 딜레이를 조절합니다.
    slow_motion_factor = 0.5  # 슬로우 모션 비율
    delay = int(1000 / (fps * slow_motion_factor))  # 밀리세컨드 단위의 딜레이

    # 비디오 출력을 위한 VideoWriter 객체를 생성합니다.
    output_path = ("C:\\Users\\hyeeu\\OneDrive\\사진\\카메라 앨범\\slow_video2.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

    # 비디오의 프레임을 읽어옵니다.
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 현재 프레임을 출력 비디오에 추가합니다.
        out.write(frame)

        # 딜레이를 추가하여 슬로우 모션을 구현합니다.
        for _ in range(int(1/slow_motion_factor) - 1):
            out.write(frame)

        # 딜레이를 추가하여 슬로우 모션을 구현합니다.
        cv2.imshow('Slow Motion Video', frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    # 사용한 자원을 해제합니다.
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return output_path
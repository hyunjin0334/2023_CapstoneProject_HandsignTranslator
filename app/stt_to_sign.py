import sys
import cv2
import os
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextBrowser, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QRect


## STT GUI
class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.video_file = None
        self.cap = None

        self.recognizer = sr.Recognizer()

        self.init_ui()


    def init_ui(self):
        # 전체 레이아웃(메인 페이지)
        main_layout = QVBoxLayout()
        
        # 텍스트 레이블(텍스트 출력 창)
        self.audio_label = QTextBrowser(self)
        self.audio_label.setFixedSize(1001, 61)
        self.audio_label.move(520, 200)

        # 스타일 시트를 사용(텍스트 폰트,크기)
        self.audio_label.setStyleSheet("border: 0;font-size: 30px;")
        self.audio_label.setPlainText("음성 인식을 시작합니다")
        
        # 글자 크기 설정
        font = self.audio_label.currentFont()
        font.setPointSize(50) 
        self.audio_label.setFont(font)

        # 폰트 설정
        font = self.audio_label.currentFont()
        font.setFamily("맑은 고딕")  
        self.audio_label.setFont(font)

        # 볼드체 설정
        font = self.audio_label.currentFont()
        font.setBold(True)  
        self.audio_label.setFont(sfont)

        main_layout.addWidget(self.audio_label)
       
       
        # 영상 출력을 위한 QLabel
        self.label = QLabel(self)
        main_layout.addWidget(self.label)      


        # 버튼 레이아웃
        button_layout = QHBoxLayout()

        # Start Recognition 버튼
        self.start_recognition_button = QPushButton("Start Recognition", self)
        self.start_recognition_button.setFixedSize(301, 101)
        self.start_recognition_button.move(5, 15)
        font = self.start_recognition_button.font()
        font.setFamily("Arial")
        font.setPointSize(20)  
        self.start_recognition_button.setFont(font)
        self.start_recognition_button.setStyleSheet("border: 1px solid black;")
        button_layout.addWidget(self.start_recognition_button)
        self.start_recognition_button.clicked.connect(self.start_recognition)

        # Play Video 버튼
        self.play_video_button = QPushButton("Play Video", self)
        self.play_video_button.setFixedSize(301, 101)
        self.play_video_button.move(10, 15)
        font = self.play_video_button.font()
        font.setFamily("Arial")
        font.setPointSize(20)   
        self.play_video_button.setFont(font)
        self.play_video_button.setStyleSheet("border: 1px solid black;")
        button_layout.addWidget(self.play_video_button)
        self.play_video_button.clicked.connect(self.play_video)

        # Reset 버튼
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFixedSize(301, 101)
        font = self.reset_button.font()
        font.setFamily("Arial")
        font.setPointSize(20)  
        self.reset_button.setFont(font)
        self.reset_button.setStyleSheet("border: 1px solid black;")
        button_layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.reset_video)


        main_layout.addLayout(button_layout)


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.setLayout(main_layout)



## STT 기능 부분
    # 음성인식
    def start_recognition(self):
        self.audio_label.setText("음성 인식 중입니다...")
        QApplication.processEvents()
        
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language="ko-KR")
            self.audio_label.setPlainText("음성 입력: " + text)
            self.video_file = self.get_video_file(text)
        except sr.UnknownValueError:
            self.audio_label.setPlainText("음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            self.audio_label.setPlainText("Google API에 접근할 수 없습니다. 오류: {0}".format(e))

    
    # 동영상 로드
    def get_video_file(self, text):
        # 동영상 폴더 경로
        video_folder = "assets/sign_videos"

        video_file = None
        # 텍스트에 따라 영상 선택 로직
        if "화나" in text:
            video_file = os.path.join(video_folder, "화나다(angry).mp4")
        elif "아름" in text:
            video_file = os.path.join(video_folder, "아름답다(beautiful).mp4")
        elif "믿" in text:
            video_file = os.path.join(video_folder, "믿다(believe).mp4")
        elif "바쁘" and "바빠" in text : 
            video_file = os.path.join(video_folder, "바쁘다(busy).mp4")
        elif "춥" in text : 
            video_file = os.path.join(video_folder, "춥다(cold).mp4")
        elif "시원" in text : 
            video_file = os.path.join(video_folder, "시원하다(cool).mp4")
        elif "미치" and "미친" and "미쳐" in text : 
            video_file = os.path.join(video_folder, "미치다(crazy).mp4")
        elif "귀엽" and "귀여" in text : 
            video_file = os.path.join(video_folder, "귀엽다(cute).mp4")
        elif "나누" and "나눠" in text : 
            video_file = os.path.join(video_folder, "나누다(divide).mp4")
        elif "친" in text : 
            video_file = os.path.join(video_folder, "친하다(familiar).mp4")
        elif "괜" in text : 
            video_file = os.path.join(video_folder, "괜찮다(fine).mp4")
        elif "배부" and "배불러" in text : 
            video_file = os.path.join(video_folder, "배부르다(full).mp4")
        elif "주" in text : 
            video_file = os.path.join(video_folder, "주다(give).mp4")
        elif "가" in text : 
            video_file = os.path.join(video_folder, "가다(go).mp4")
        elif "안녕" in text : 
            video_file = os.path.join(video_folder, "안녕하세요(hello).mp4")
        elif "돕" in text : 
            video_file = os.path.join(video_folder, "돕다(help).mp4")
        elif "때" in text : 
            video_file = os.path.join(video_folder, "때리다(hit).mp4")
        elif "덥" and "더워" in text : 
            video_file = os.path.join(video_folder, "덥다(hot).mp4")
        elif "안" in text : 
            video_file = os.path.join(video_folder, "안다(hug).mp4")
        elif "배고" in text : 
            video_file = os.path.join(video_folder, "배고프다(hungry).mp4")
        elif "상상" in text : 
            video_file = os.path.join(video_folder, "상상하다(imagine).mp4")
        elif "눕" and "누워" in text : 
            video_file = os.path.join(video_folder, "눕다(lie).mp4")
        elif "좋" in text : 
            video_file = os.path.join(video_folder, "좋다(like).mp4")
        elif "예쁘" and "예뻐" in text : 
            video_file = os.path.join(video_folder, "예쁘다(pretty).mp4")
        elif "받" in text : 
            video_file = os.path.join(video_folder, "받다(receive).mp4")
        elif "반성" in text : 
            video_file = os.path.join(video_folder, "반성하다(regret).mp4")
        elif "존경" in text : 
            video_file = os.path.join(video_folder, "존경하다(respect).mp4")
        elif "맞" in text : 
            video_file = os.path.join(video_folder, "맞다(right).mp4")
        elif "달" in text : 
            video_file = os.path.join(video_folder, "달리다(run).mp4")
        elif "무섭" and "무서워" in text : 
            video_file = os.path.join(video_folder, "무섭다(scary).mp4")
        elif "아프" and "아파" in text : 
            video_file = os.path.join(video_folder, "아프다(sick).mp4")
        elif "졸" in text : 
            video_file = os.path.join(video_folder, "졸리다(sleepy).mp4")
        elif "미안" and "죄송" in text : 
            video_file = os.path.join(video_folder, "죄송합니다(sorry).mp4")
        elif "고맙" and "감사" in text : 
            video_file = os.path.join(video_folder, "감사합니다(thankyou).mp4")
        elif "귀찮" in text : 
            video_file = os.path.join(video_folder, "귀찮다(tiresome).mp4")
        elif "보" in text : 
            video_file = os.path.join(video_folder, "보이다(visible).mp4")
        elif "걷" in text : 
            video_file = os.path.join(video_folder, "걷다(walk).mp4")
        elif "틀" in text : 
            video_file = os.path.join(video_folder, "틀리다(wrong).mp4")
        if video_file is None:
            error_message = "해당하는 영상이 존재하지 않습니다."
            self.audio_label.setPlainText(error_message)
            return None

        return video_file


    # 동영상 출력 설정
    def play_video(self):
        if self.video_file is not None:
            try:
                if self.cap is not None:
                    self.cap.release()

                self.cap = cv2.VideoCapture(self.video_file)

                new_width = 640
                new_height = 480
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

                self.timer.start(30)
            except Exception as e:
                print("영상 재생 중 오류 발생: {0}".format(e))

    # 동영상 송출 화면
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            new_width = 1100
            new_height = 700
            frame = cv2.resize(frame, (new_width, new_height))

            h, w, ch = frame.shape
            x = (self.label.width() - w) // 2  # 가로 중앙 정렬
            y = (self.label.height() - h) // 2  # 세로 중앙 정렬
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap)
            self.label.setAlignment(Qt.AlignCenter)

    # reset
    def reset_video(self):
        if self.cap is not None:
            self.cap.release()
        self.audio_label.setPlainText("음성 인식을 시작합니다.")
        self.video_file = None
        self.label.clear()

    # 종료
    def quit_program(self):
        if self.cap is not None:
            self.cap.release()
        self.close()

# Main window 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    video_player = VideoPlayer()
    main_window.setCentralWidget(video_player)
    main_window.setGeometry(100, 100, 1300, 900)
    main_window.setStyleSheet("background-color: white;")
    main_window.setWindowTitle("STT")
    main_window.show()
    sys.exit(app.exec_())

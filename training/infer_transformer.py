import cv2
import numpy as np
import os
import time
import mediapipe as mp
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, MultiHeadAttention, Add, LayerNormalization, GlobalAveragePooling1D
from tensorflow.keras.activations import gelu
import tensorflow as tf
from PIL import ImageFont, ImageDraw, Image

# 한국어 설정
font = ImageFont.truetype('fonts/gulim.ttc', 25)
img = np.full((200, 300, 3), (255, 255, 255), np.uint8)
img = Image.fromarray(img)
draw = ImageDraw.Draw(img)

mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils 

# MediaPipe Code
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False                 
    results = model.process(image)                
    image.flags.writeable = True                
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION) # Draw face connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS) # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw right hand connections


def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                             )
   
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                             )
   
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             )
   
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             )
   
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


# Action & Action mapping
actions = np.array(['angry', 'beautiful', 'believe', 'busy', 'cold',
                    'cool', 'crazy', 'cute', 'divide', 'familiar',
                    'fine', 'full', 'give', 'go', 'hello',
                    'help', 'hit', 'hot', 'hug', 'hungry',
                    'imagine', 'lie', 'like', 'pretty', 'receive',
                    'regret', 'respect', 'right', 'run', 'scary',
                    'sick', 'sleepy', 'sorry', 'thankyou', 'tiresome',
                    'visible', 'walk', 'wrong'])
                    
action_mapping = {'angry': '화나다', 'beautiful': '아름답다', 'believe': '믿다', 'busy': '바쁘다', 'cold': '춥다',
                  'cool': '시원하다', 'crazy': '미치다', 'cute': '귀엽다', 'divide': '나누다', 'familiar': '친하다',
                  'fine': '괜찮다', 'full': '배부르다', 'give': '주다', 'go': '가다', 'hello': '안녕하세요',
                  'help': '돕다', 'hit': '때리다', 'hot': '덥다', 'hug': '안다', 'hungry': '배고프다',
                  'imagine': '상상하다', 'lie': '눕다', 'like': '좋다', 'pretty': '예쁘다', 'receive': '반성하다',
                  'regret': '받다', 'respect': '존경하다', 'right': '맞다', 'run': '달리다', 'scary': '무섭다',
                  'sick': '아프다', 'sleepy': '졸리다', 'sorry': '죄송합니다','thankyou': '감사합니다', 'tiresome': '귀찮다',
                  'visible':'보이다', 'walk': '걷다', 'wrong': '틀리다'}
                


# 한국어로 바꿔주는 Code
def translate_action(action):
    korean_action = action_mapping.get(action, '      ')  # 딕셔너리에서 해당 Action을 찾거나 '_______'을 반환
    return korean_action


# Transformer Code
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, MultiHeadAttention, Add, LayerNormalization, GlobalAveragePooling1D
from tensorflow.keras.activations import gelu
import tensorflow as tf

def positional_encoding(sequence_length, d_model):
    pos = np.arange(sequence_length)[:, np.newaxis]
    i = np.arange(d_model)[np.newaxis, :]
    angle_rates = 1 / np.power(10000, (2 * (i // 2)) / np.float32(d_model))
    angle_rads = pos * angle_rates
    sines = np.sin(angle_rads[:, 0::2])
    cosines = np.cos(angle_rads[:, 1::2])
    pos_encoding = np.concatenate([sines, cosines], axis=-1)
    return pos_encoding

def transformer_model(sequence_length, d_model, num_heads, dense_units, num_classes):
    inputs = Input(shape=(sequence_length, d_model))
    pos_encoding = Input(shape=(sequence_length, d_model))
    attention = MultiHeadAttention(num_heads=num_heads, key_dim=d_model)
    attention_out = attention(inputs, inputs)
    add1 = Add()([inputs, attention_out])
    norm1 = LayerNormalization(epsilon=1e-6)(add1)
    dense1 = Dense(units=dense_units, activation=gelu)(norm1)
    dense2 = Dense(units=d_model, activation=gelu)(dense1)
    add2 = Add()([norm1, dense2])
    norm2 = LayerNormalization(epsilon=1e-6)(add2)
    output = GlobalAveragePooling1D()(norm2)
    output = Dense(units=num_classes, activation='softmax')(output)
    model = Model(inputs=[inputs, pos_encoding], outputs=output)
    return model

sequence_length = 40
d_model = 1662
num_heads = 4
dense_units = 64

actions.shape[0] # This should be the number of classes

transformer_model = transformer_model(sequence_length, d_model, num_heads, dense_units, actions.shape[0])

transformer_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

transformer_model.load_weights('Transformer.h5')

from scipy import stats

sequence = []
sentence = []
predictions = []
threshold = 0.02


# 버튼 영역 좌표
start_button_coords = (150, 400, 100, 50)
end_button_coords = (350, 400, 100, 50)

is_recording = False
recorded_sequence = []

def is_inside_button(button_coords, x, y) :
    button_x, button_y, button_w, button_h = button_coords
    if button_x <= x <= button_x + button_w and button_y <= y <= button_y + button_h:
        return True
    return False


# 마우스 클릭 이벤트 콜백 함수
def mouse_callback(event, x, y, flags, param) :
    global is_recording, recorded_sequence, prev_recording_state
   
    if event == cv2.EVENT_LBUTTONDOWN :
        if is_inside_button(start_button_coords, x, y):
            is_recording = True
            recorded_sequence = []
        elif is_inside_button(end_button_coords, x, y):
            is_recording = False


# Set up the webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow('OpenCV Feed', cv2.WINDOW_NORMAL) 
cv2.resizeWindow('OpenCV Feed', 1300, 950)


# Set mouse callback function
cv2.namedWindow('OpenCV Feed')
cv2.setMouseCallback('OpenCV Feed', mouse_callback)


# Main loop
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic :
    while cap.isOpened() :
        ret, frame = cap.read()

        # Draw buttons
        cv2.rectangle(frame, start_button_coords[:2], (start_button_coords[0] + start_button_coords[2], start_button_coords[1] + start_button_coords[3]), (0, 255, 0), -1)
        cv2.putText(frame, "Start", (start_button_coords[0] + 30, start_button_coords[1] + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        cv2.rectangle(frame, end_button_coords[:2], (end_button_coords[0] + end_button_coords[2], end_button_coords[1] + end_button_coords[3]), (0, 0, 255), -1)
        cv2.putText(frame, "End", (end_button_coords[0] + 25, end_button_coords[1] + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
       
        if is_recording :
            image, results = mediapipe_detection(frame, holistic)

            keypoints = extract_keypoints(results)
            recorded_sequence.append(keypoints)
            recorded_sequence = recorded_sequence[-sequence_length:]

        if len(recorded_sequence) == sequence_length :
            X_test_pe = positional_encoding(sequence_length, d_model)
            res = transformer_model.predict([np.expand_dims(recorded_sequence, axis=0), np.expand_dims(X_test_pe, axis=0)])[0]
            action = actions[np.argmax(res)]

            # Action 결과값(한국어)
            korean_action = translate_action(action)
            text = f"Action : {korean_action}"
            text_size = draw.textsize(text, font=font)
            text_x = 10
            text_y = 10
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(frame_pil)
            draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))
            frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
        else:
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(frame_pil)
            frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

        
        # Display the frame
        cv2.imshow('OpenCV Feed', frame)
        

        # Exit loop if 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q') :
            break

       
# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
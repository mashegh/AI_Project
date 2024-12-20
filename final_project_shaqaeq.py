
import cv2
import speech_recognition as sr
import pyttsx3
import random
import datetime

# مقداردهی اولیه
r = sr.Recognizer()
engine = pyttsx3.init()

# تابع اعلام زمان
def tellmethetime():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%H:%M:%S')}"

# بررسی اینکه مقدار قابل فراخوانی است
def isitafunction(value):
    return callable(value)

# دیکشنری دستورات
commands = {
    'hello': ['hi', 'hello', 'wanna be friends', 'what’s good?'],
    'bye': ['where are you going?', 'stay here, bud!', 'goodbye'],
    'who': ['who are you?', 'I’m an AI assistant!'],
    'time': tellmethetime
}

name = 'test'

# تابع یادگیری دستورات جدید
def learn(inp):
    SpeakText(f"I don't know '{inp}'. Please teach me.")
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            response = r.recognize_google(audio).lower()
            print('Did you say:', response)
            response = response.replace('say', '').strip()
            commands[inp] = [response]
            print('Updated commands:', commands)
    except sr.RequestError:
        print('Error with the request.')
    except sr.UnknownValueError:
        print('I did not hear you. Maybe something is in my ear or maybe you have a problem.')

# پردازش ورودی متن
def textprocess(inp):
    for key, value in commands.items():
        if key in inp:
            if isitafunction(value):
                return value()  # اگر مقدار تابع باشد، آن را اجرا می‌کند
            else:
                return random.choice(value)  # انتخاب تصادفی از لیست پاسخ‌ها
    learn(inp)  # اگر دستور ناشناخته باشد، آن را یاد می‌گیرد

# تبدیل متن به گفتار
def SpeakText(command):
    engine.say(command)
    engine.runAndWait()

# تشخیص چهره و چشم با دوربین
seen = False
camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('face.xml')
eye_cascade = cv2.CascadeClassifier('eye.xml')

while True:
    cam, frame = camera.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=4)

        gray_face = gray_frame[y:y + h, x:x + w]
        color_face = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(gray_face, 1.3, 5)

        for (a, b, c, d) in eyes:
            cv2.rectangle(color_face, (a, b), (a + c, b + d), (0, 255, 0), thickness=4)
            SpeakText("Hi Ryan!")

    cv2.imshow("Window", frame)

    # کلید خروج
    if cv2.waitKey(1) & 0xFF == ord("e"):
        break

    # شناسایی ورودی صوتی
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)
            output = r.recognize_google(audio).lower()
            print("You said:", output)

            if name in output or seen:
                response = textprocess(output.replace(name, '').strip())
                SpeakText(response)
    except sr.UnknownValueError:
        print("I didn't catch that. Could you repeat?")
    except sr.RequestError:
        print("There was an error with the speech recognition service.")

# آزادسازی منابع
camera.release()
cv2.destroyAllWindows()

# مسیحا جان:
# ممنون از شما برای بررسی این پروژه. امیدوارم از آن لذت برده باشید و به یادگیری و تجربه شما افزوده باشد!

from tkinter.constants import COMMAND
from PIL import Image, ImageTk
import tkinter as tk
import cv2
from keras.models import model_from_json
import operator
from string import ascii_uppercase
import pyttsx3


class Application:
    def __init__(self):

        # Setup GUI
        self.root = tk.Tk()
        self.root.title("Indian Sign Language Recognition")
        self.root.config(background="#000")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)

        # Graphics window
        # imageFrame = tk.Frame(self.root, width=600, height=500)
        # imageFrame.grid(row=0, column=0, padx=0, pady=0)

        self.directory = 'model/'

        # self.panel = tk.Label(imageFrame)
        # self.panel.grid(row=0, column=0)
        self.vs = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.vs.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.current_image = None
        self.current_image2 = None

        self.json_file = open(self.directory+"model_uv.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights(self.directory+"model_uv.h5")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        for i in ascii_uppercase:
            self.ct[i] = 0
        print("Loaded model from disk")

        def talk():
            engine = pyttsx3.init()
            engine.say(self.str)
            engine.runAndWait()

        def clearWord():
            self.word = ""

        def clearSentence():
            self.str = ""

        # self.panel = tk.Label(self.root)
        # self.panel.place(width=640, height=640)
        # self.panel.grid(row=0, column=0, padx=(200, 10), pady=(10, 0))
        self.root.geometry("900x1100")
        self.panel = tk.Label(self.root)
        self.panel.place(x=135, y=10, width=640, height=640)
        self.panel2 = tk.Label(self.root)  # initialize image panel
        self.panel2.place(x=460, y=95, width=310, height=310)  # white box

        self.panel3 = tk.Label(self.root)  # Current SYmbol
        self.panel3.place(x=420, y=560)

        self.T1 = tk.Label(self.root)
        self.T1.place(x=300, y=560)
        self.T1.config(text="Character :", font=("Raleway", 10, "bold"))

        self.panel4 = tk.Label(self.root)  # Word
        self.panel4.place(x=420, y=600)

        self.T2 = tk.Label(self.root)
        self.T2.place(x=300, y=600)
        self.T2.config(text="Word :", font=("Raleway", 10, "bold"))

        self.panel5 = tk.Label(self.root)  # Sentence
        self.panel5.place(x=420, y=640)

        self.T3 = tk.Label(self.root)
        self.T3.place(x=300, y=640)
        self.T3.config(text="Sentence :", font=("Raleway", 10, "bold"))

        my_button = tk.Button(self.root, text="speak", command=talk)
        my_button.place(x=620, y=640)

        clear_button = tk.Button(self.root, text="Clear", command=clearWord)
        clear_button.place(x=720, y=600)

        clear_button1 = tk.Button(
            self.root, text="Clear", command=clearSentence)
        clear_button1.place(x=720, y=640)

        self.str = ""
        self.word = ""
        self.current_symbol = "Empty"
        self.photo = "Empty"
        self.video_loop()

    def video_loop(self):
        ok, frame = self.vs.read()
        if ok:
            cv2image = cv2.flip(frame, 1)
            x1 = int(0.5*frame.shape[1])
            y1 = 10
            x2 = frame.shape[1]-10
            y2 = int(0.5*frame.shape[1])
            cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255, 0, 0), 1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
            cv2image = cv2image[y1:y2, x1:x2]
            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 2)
            th3 = cv2.adaptiveThreshold(
                blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            ret, res = cv2.threshold(
                th3, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            self.predict(res)
            self.current_image2 = Image.fromarray(res)
            imgtk = ImageTk.PhotoImage(image=self.current_image2)
            self.panel2.imgtk = imgtk
            self.panel2.config(image=imgtk)
            self.panel3.config(text=self.current_symbol, font=("Raleway", 10))
            self.panel4.config(text=self.word, font=("Raleway", 10))
            self.panel5.config(text=self.str, font=("Raleway", 10))

        self.root.after(10, self.video_loop)

    def predict(self, test_image):
        test_image = cv2.resize(test_image, (128, 128))
        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))
        prediction = {}
        prediction['blank'] = result[0][0]
        inde = 0
        ascii_uppercase = ['U', 'V']
        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1
        # LAYER 1
        prediction = sorted(prediction.items(),
                            key=operator.itemgetter(1), reverse=True)
        self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'blank'):
            for i in ascii_uppercase:
                self.ct[i] = 0
        self.ct[self.current_symbol] += 1
        if(self.ct[self.current_symbol] > 45):
            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue
                tmp = self.ct[self.current_symbol] - self.ct[i]
                if tmp < 0:
                    tmp *= -1
                if tmp <= 20:
                    self.ct['blank'] = 0
                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return
            self.ct['blank'] = 0
            for i in ascii_uppercase:
                self.ct[i] = 0
            if self.current_symbol == 'blank':
                if self.blank_flag == 0:
                    self.blank_flag = 1
                    if len(self.str) > 0:
                        self.str += " "
                    self.str += self.word
                    self.word = ""
            else:
                if(len(self.str) > 16):
                    self.str = ""
                self.blank_flag = 0
                self.word += self.current_symbol

    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

    def destructor1(self):
        print("Closing Application...")
        self.root1.destroy()


print("Starting Application...")
pba = Application()
pba.root.mainloop()

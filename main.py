# online voting system using face_recognition
import cv2
import numpy as np
import face_recognition
import os
# kivy framework for app development
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
# pandas to work with csv file
import pandas as pd


# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()
        popFun2()
        popFun3()
        popFun4()

# classes to build GUI for a popup window
class P(FloatLayout):
    pass


class P1(FloatLayout):
    pass


class P2(FloatLayout):
    pass


class P3(FloatLayout):
    pass


# function that displays the content
def popFun():
    show = P()
    window = Popup(title="popup", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()


def popFun2():
    show = P1()
    window = Popup(title="popup", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()


def popFun3():
    show = P2()
    window = Popup(title="popup", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()


def popFun4():
    show = P3()
    window = Popup(title="popup", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()


# class for Home page of the app adn navigate to desired window
class homeWindow(Screen):

    def display(self):
        sm.current = 'login'

    def display1(self):
        sm.current = 'voter'


# class to allow admin to login
class adminloginWindow(Screen):
    username = ObjectProperty(None)
    pwd = ObjectProperty(None)

    # function to check username and password of the admin
    def validate1(self):
        if self.username.text != "Microsoft" or self.pwd.text != "2022":
            popFun()
        else:
            sm.current = 'signup'


# class to accept sign up info from the admin of the voter to be able to vote
class signupWindow(Screen):
    # fetching input from text_input field in gui
    name2 = ObjectProperty(None)
    voting = ObjectProperty(None)
    username = ObjectProperty(None)
    age = ObjectProperty(None)
    city = ObjectProperty(None)
    state = ObjectProperty(None)

    # function to add the voter and save its image for face verification using opencv
    def signupbtn(self):
        users = pd.read_csv('voter_info.csv')
        a = int(self.age.text)
        # creating a DataFrame of the info
        if self.name2.text != "":
            # checking whether the admin gives correct details of the voter
            if self.username.text not in users['username'].unique() and a > 18 and self.voting.text not in users['Voting_id'].unique():
                # if email does not exist already then append to the csv file
                # change current screen to log in the user now
                user = pd.DataFrame([[self.name2.text, self.voting.text, self.username.text, self.age.text,
                                      self.city.text, self.state.text]],
                                    columns=['Name', 'Voting_id', 'username', 'age', 'city', 'state'])
                user.to_csv('voter_info.csv', mode='a', header=False, index=False)
                name14 = self.username.text
                self.name2.text = ""
                self.voting.text = ""
                self.username.text = ""
                self.age.text = ""
                self.city.text = ""
                self.state.text = ""
                self.ids.over.text = f'look towards the camera and kindly wait'
                # setting the path of the folder where images are stored
                path = 'images'
                # real time face capture for face verification while voting
                # capturing image from webcam
                cap = cv2.VideoCapture(0)
                i = 0
                b = 1
                while b == 1:
                    b = 0
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # storing image to folder
                    cv2.imwrite(os.path.join(path, name14 + ".jpg"), frame)
                    i += 1
                cap.release()
                cv2.destroyAllWindows()
                sm.current = 'useradded'
            else:
                if a < 18:
                    popFun2()
                else:
                    popFun3()
        else:
            # if values are empty or invalid show pop up
            popFun()


# class for logging in as voter and casting vote
class voterloginWindow(Screen):
    name5 = ObjectProperty(None)
    v_id = ObjectProperty(None)
    # function to verify voter has registered or not
    def validate1(self):
        if self.name5.text not in users['username'].unique():
            popFun()
        else:
            # getting voting id of the person who is trying to login
            str1 = users.loc[users['username'] == self.name5.text]
            x = str1.iat[0, 1]
            if self.name5.text not in users['username'].unique() or x not in users['Voting_id'].unique():
                # invalid username or voting id
                popFun()
            else:
                # if person enter respective voting id allow login
                if x == self.v_id.text:
                    voters = pd.read_csv('voted_candidates.csv')
                    # if not voted once
                    if self.name5.text not in voters['username'].unique():
                        path = 'images'
                        images = []
                        # creating list to store person name of respective images
                        personName = []
                        # giving path to access images from folder
                        myList = os.listdir(path)
                        # to check images in the list and append to images list
                        for cu_img in myList:
                            current_Img = cv2.imread(f'{path}/{cu_img}')
                            images.append(current_Img)
                            # extract the person name for the current image
                            personName.append(os.path.splitext(cu_img)[0])

                        # after marking the face embeddings storing it to compare
                        def faceEncodings(images):
                            # list to store unique faces
                            encodeList = []
                            for img in images:
                                # images are in bgr format so to convert bgr to rgb
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                # applying encoding after converting the images on image matrix
                                encode = face_recognition.face_encodings(img)[0]
                                # appending encoding to the list
                                encodeList.append(encode)
                            return encodeList
                        # after encoding the faces
                        encodeListKnown = faceEncodings(images)
                        # take the image of the voter
                        cap = cv2.VideoCapture(0)
                        a = True
                        while a:
                            # frame the image form the webcam
                            ret, frame = cap.read()
                            faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
                            # image is in bgr convert it to rgb
                            faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)
                            # ending the loop once detected
                            a = False
                            # making object of the functions
                            faceCurrentFrame = face_recognition.face_locations(faces)
                            encodesCurrentFrame = face_recognition.face_encodings(faces, faceCurrentFrame)
                            # matching and taking the image
                            for encodeFace, faceLoc in zip(encodesCurrentFrame, faceCurrentFrame):
                                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                                # checking if image has been correctly verified to the index
                                matchIndex = np.argmin(faceDis)
                                if matches[matchIndex]:
                                    name = personName[matchIndex]
                                    # if does not match show to the same user then show warning
                                    if name not in users['username'].unique() or name != self.name5.text:
                                        popFun()
                                    else:
                                        # adding user to voted csv so that he can not vote again
                                        voters = pd.DataFrame([[self.name5.text]],
                                                              columns=['username'])
                                        voters.to_csv('voted_candidates.csv', mode='a', header=False, index=False)
                                        # switching the current screen to display validation result
                                        sm.current = 'logdata'
                                        # reset TextInput widget
                                        self.name5.text = ""
                                        self.v_id.text = ""
                                    # showing frame around the face for user
                                    y1, x2, y2, x1 = faceLoc
                                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255), 2)
                                # camera frame access to detect face
                                cv2.imshow("Camera", frame)
                                if cv2.waitKey(100) == 13:
                                    break

                            cap.release()
                            cv2.destroyAllWindows()
                    else:
                        # pop warning
                        popFun4()
                else:
                    popFun()


# class to display validation result
class logDataWindow(Screen):
    def final(self):
        sm.current = 'final'

# class to display user added result
class useraddedWindow(Screen):
    pass

# class to show final voted result
class finalWindow(Screen):
    def final1(self):
        sm.current = 'home'


# class for managing screens
class windowManager(ScreenManager):
    pass


# kv file
kv = Builder.load_file('bg.kv')
# to change windows
sm = windowManager()

# reading all the data stored
users = pd.read_csv('voter_info.csv')
# adding screens
sm.add_widget(homeWindow(name='home'))
sm.add_widget(adminloginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(voterloginWindow(name='voter'))
sm.add_widget(finalWindow(name='final'))
sm.add_widget(useraddedWindow(name='useradded'))


# class that builds gui
class loginMain(App):
    def build(self):
        return sm


# driver function to run the app
if __name__ == "__main__":
    loginMain().run()

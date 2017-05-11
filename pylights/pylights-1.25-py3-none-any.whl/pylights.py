import pyphue # Manages phillips hue lights
import time # Manages timing of notes
import librosa # Manages detection of onsets and onset strength
import pickle # Manages saving/loading of data
import os # Manages directories
import random # Manages random color generation
from pygame import mixer # Plays mp3 files

class PyLights:
    def __init__(self, philipsBridge):
        self.bridge = philipsBridge
        self.primaryLights = []
        self.secondaryLights = []


    def run(self):
        colorTheme = random.randint(0, 65535)
        lastBigBeat = 0
        secondaryOn = 0
        primaryBrightness = 255
        primaryOff = False

        for item in self.primaryLights:
            if item[1]:
                self.bridge.setHue(item[0], colorTheme + random.randint(-5000, 5000))
                self.bridge.setSaturation(item[0], 255)
            self.bridge.turnOn(item[0])
            self.bridge.setBrightness(item[0],255)

        for item in self.secondaryLights:
            if item[1]:
                self.bridge.setHue(item[0], colorTheme + random.randint(-5000, 5000))
                self.bridge.setSaturation(item[0], 255)
            self.bridge.turnOn(item[0])
            self.bridge.setBrightness(item[0], 255)

        starttime = time.time()

        mixer.init()
        mixer.music.load(os.path.join(self.songPath, "%s" % self.fileName))
        mixer.music.play()

        tick = 0
        for i in range(0, len(self.beat_times)):
            colorTheme = random.randint(0, 65535)

            if (primaryOff):
                for item in self.primaryLights:
                    self.bridge.turnOn(item[0])
                primaryOff = False
            tick = (tick + 1) % 2

            if (tick == 1):
                primaryBrightness = 255 - int(275 - (100 / (self.o_env[i] + 0.01)))
            else:
                primaryBrightness = int(275 - (100 / (self.o_env[i] + 0.01)))

            if (primaryBrightness < 125):
                primaryBrightness -= 50
            else:
                primaryBrightness += 50

            primaryBrightness = min(primaryBrightness, 255);
            primaryBrightness = max(primaryBrightness, 0);

            if primaryBrightness == 255:  # On power notes it should reach 255, and we want to light up all secondary lights on power notes
                secondaryOn = abs(self.beat_times[i] - lastBigBeat)
                if (secondaryOn > 1):
                    lastBigBeat = self.beat_times[i]
                    for item in self.secondaryLights:
                        if item[1]:
                            self.bridge.setHue(item[0], colorTheme + random.randint(-5000, 5000))
                        self.bridge.turnOn(item[0])
                        self.bridge.setBrightness(item[0], int(50 * secondaryOn))

                for item in self.primaryLights:
                    if item[1]:
                        self.bridge.setHue(item[0], colorTheme + random.randint(-5000, 5000))
                    self.bridge.setBrightness(item[0], primaryBrightness)

            elif primaryBrightness > 10:
                for item in self.primaryLights:
                    if item[1]:
                        self.bridge.setHue(item[0], colorTheme + random.randint(-5000, 5000))
                    self.bridge.setBrightness(item[0], primaryBrightness)
            else:
                secondaryOn = abs(self.beat_times[i] - lastBigBeat)
                if (secondaryOn > 1):
                    lastBigBeat = self.beat_times[i]
                    for item in self.secondaryLights:
                        if item[1]:
                            self.bridge.setHue(item[0], colorTheme + random.randint(-5000, 5000))
                        self.bridge.turnOn(item[0])
                        self.bridge.setBrightness(item[0], int(50 * secondaryOn))
                for item in self.primaryLights:
                    if item[1]:
                        self.bridge.setHue(item[0], colorTheme + random.randint(-5000, 5000))
                    self.bridge.setBrightness(item[0], primaryBrightness)
                    self.bridge.turnOff(item[0])
                primaryOff = True

            for item in self.secondaryLights:
                self.bridge.turnOff(item[0])

            if (i < len(self.beat_times) - 1):
                time.sleep(max(self.beat_times[i + 1] - (time.time() - starttime), 0))

    def loadLight(self, lightId, primary=True, color=False):
        if (primary):
            if [lightId, color] not in self.primaryLights:
                self.primaryLights.append([lightId, color]) #Append light id to the primary light list, include color support info
        else:
            if [lightId, color] not in self.secondaryLights:
                self.secondaryLights.append([lightId, color]) #Append light id to the primary light list, include color support info

    def loadAudio(self, fileName, songPath=None, dataPath=None, saveAndLoad=True): # Allows you to select an audio file, chose what path to look for the audio file, what path to save compiled data, and if to save compiled data
        if songPath == None:
            songPath = os.path.join(os.getcwd() + "/Songs/")

        if dataPath == None:
            dataPath = os.path.join(os.getcwd() + "/SongData/")

        self.songPath = songPath
        self.dataPath = dataPath
        self.fileName = fileName

        if not os.path.exists(songPath):
            os.makedirs(songPath)

        if not os.path.exists(dataPath):
            os.makedirs(dataPath)

        if (saveAndLoad):
            if (os.path.isfile(os.path.join(dataPath, "%s.txt" % fileName))):
                self.beat_times = []
                self.o_env = []
                with open(os.path.join(dataPath, "%s.txt" % fileName), 'rb') as file:
                    readSongData = pickle.load(file)

                for item in readSongData:
                    self.beat_times.append(item[0])
                    self.o_env.append(item[1])
            else:
                try:
                    y, sr = librosa.load(os.path.join(songPath, "%s" % fileName))
                    self.o_env = librosa.onset.onset_strength(y=y, sr=sr)
                    self.beat_times = librosa.frames_to_time(librosa.onset.onset_detect(y=y, sr=sr), sr=sr)

                    writeSongData = []
                    for pos, item in enumerate(self.beat_times):
                        writeSongData.append([item, self.o_env[pos]])

                    with open(os.path.join(dataPath, "%s.txt" % fileName), 'wb') as file:
                        pickle.dump(writeSongData, file)
                except Exception as e:
                    print(e)
                    exit()
        else:
            try:
                y, sr = librosa.load(os.path.join(songPath, "%s" % fileName))
                self.o_env = librosa.onset.onset_strength(y=y, sr=sr)
                self.beat_times = librosa.frames_to_time(librosa.onset.onset_detect(y=y, sr=sr), sr=sr)

            except Exception as e:
                print(e)
                exit()

# EXAMPLE CODE

# setIp = "192.168.1.1" # Change this to the IP of your philips hue bridge
# userId = "tLWZE6rPwKQbnYm-S6Gx9u5FVT8oJd9r5YYArxPL" # Change this to your user ID attained from your philips hue bridge, this way you do not have to constantly authorize
# myHue = pyphue.PyPHue(ip = setIp, user = userId, AppName = 'PyPhue', DeviceName = 'Desktop:YourUserName', wizard = False) # Use the PyPhue module to connect to your bridge

# pylights = PyLights(myHue)
# pylights.loadLight(lightId = '3', primary=True, color=True)
# pylights.loadLight(lightId = '2', primary=False, color=False)
# pylights.loadLight(lightId = '1', primary=False, color=False)
# pylights.loadAudio(fileName = "CurtainsDown.mp3", songPath = os.path.abspath("CustomSongPath"), dataPath = os.path.abspath("CustomDataPath"), saveAndLoad=True)
# pylights.run()
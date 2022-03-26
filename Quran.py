import speech_recognition as sr
import os
import csv

COLORS = {
    'red': '\u001b[31m',
    'green': '\u001b[32m'
}
RIGHT = 'صح'
WRONG = 'خطا'
REPEAT = 'اعدها من جديد'

BASE_DIR = f'{os.getcwd()}/quran/chapters/'

mapping = {
    0: f'al_fatiha/al_fatiha'
}

class QuranSpeechRecognition:
    def __init__(self, chapter=0, soura_index=0):
        self.chapter = chapter
        self.soura_index = soura_index
        self.recognizer = sr.Recognizer()
        # self.recognizer.pause_threshold = 1
        # self.recognizer.phrase_threshold = 1
        self.recognizer.non_speaking_duration = 0.1

        self.mic = sr.Microphone(device_index=14, sample_rate=48000)
        self.file = None
        self.file_csv = None
        self.aya = ''
        self.human_aya = ''
        self.quranic_writing = ''

    def __enter__(self):
        self.file = open(BASE_DIR + mapping[self.soura_index])
        self.file_csv = csv.reader(self.file)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def __iter__(self):
        return self

    def __next__(self):
        aya = next(self.file_csv)
        self.aya = aya[0].strip()
        self.quranic_writing = aya[1].strip()

    def listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            self.human_aya = self.recognizer.recognize_google(audio,
                                                              language='ar-TN')

    def verify(self):
        if self.human_aya != self.aya:
            print(f'{COLORS["red"]}{WRONG}: {self.human_aya}{COLORS["red"]}')
            print(
                f'{COLORS["green"]}{RIGHT}: {self.quranic_writing}{COLORS["green"]}')
            return False
        return True


quran = QuranSpeechRecognition()
with quran as q:
    while True:
        try:
            next(quran)
            quran.listen()
            while quran.verify() == False:
                print('>>>', REPEAT)
                quran.listen()
            print(f'{COLORS["green"]}{quran.quranic_writing}{COLORS["green"]}')
        except StopIteration:
            break

import sys
import os
import random
import time
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer
import pygame

class TransparentGif(QLabel):
    def __init__(self, gif_filename):
        super().__init__()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(script_dir, gif_filename)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)
        self.movie.start()

        self.movie.jumpToFrame(0)
        pixmap = self.movie.currentPixmap()
        print("GIF size:", pixmap.size())

        if pixmap.isNull():
            self.resize(200, 200)
        else:
            self.resize(pixmap.size())

        self.show()

        self.normal_speed = self.movie.speed()

        self.timer = QTimer()
        self.timer.timeout.connect(self.accelerate_gif)
        self.start_random_timer()

        self.drag_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def start_random_timer(self):
        interval = random.randint(0, 10000)  
        self.timer.start(interval)

    def accelerate_gif(self):
        self.movie.setSpeed(300)  

        accel_duration = random.randint(1000, 7000)
        QTimer.singleShot(accel_duration, self.reset_speed)
        self.timer.stop()

    def reset_speed(self):
        self.movie.setSpeed(self.normal_speed)
        self.start_random_timer()

def play_music(music_filename):
    pygame.mixer.init()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    music_path = os.path.join(script_dir, music_filename)

    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

if __name__ == "__main__":
    random.seed(time.time())

    app = QApplication(sys.argv)

    gifs = [
        # "tennaDancing/Tenna1.gif",
        "tennaDancing/Tenna2.gif"
    ]
    musics = [
        "tennaDancing/songsDir/TvTime.wav",
        "tennaDancing/songsDir/TvWorld.wav",
        "tennaDancing/songsDir/BurningEyes.wav"
    ]

    chosen_gif = random.choice(gifs)
    chosen_music = random.choice(musics)

    print(f"Chosen GIF: {chosen_gif}")
    print(f"Chosen music: {chosen_music}")

    play_music(chosen_music)
    gif_window = TransparentGif(chosen_gif)

    sys.exit(app.exec_())
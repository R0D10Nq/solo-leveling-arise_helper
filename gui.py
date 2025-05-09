import sys
from PyQt5.QtWidgets import QApplication
from models import Profile, Character, Artifact
from storage import load_profile, save_profile, load_characters, save_characters, load_artifacts, save_artifacts
from analytics import generate_analytics
from gui_impl import MainWindow

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

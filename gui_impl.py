from PyQt5.QtCore import QBuffer, QIODevice
import sys
sys.modules['PyQt5.QtCore.QBuffer'] = QBuffer
sys.modules['PyQt5.QtCore.QIODevice'] = QIODevice
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QTabWidget
from PyQt5.QtGui import QImage
from PIL import Image, ImageOps
from storage import load_profile, save_profile, load_characters, save_characters, load_artifacts, save_artifacts
from analytics import generate_analytics
from dialogs import ProfileDialog, CharacterDialog, ArtifactDialog
from ocr_import import ocr_image_to_text, parse_character_stats, parse_artifact

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Solo Leveling Helper (Python)')
        self.resize(800, 500)
        self.profile = load_profile()
        self.characters = load_characters()
        self.artifacts = load_artifacts()
        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        # --- Вкладка 1: Профиль и персонажи ---
        tab1 = QWidget()
        layout = QVBoxLayout(tab1)
        self.profile_label = QLabel(self.profile_str())
        btn_profile = QPushButton('Редактировать профиль')
        btn_profile.clicked.connect(self.edit_profile)
        layout.addWidget(self.profile_label)
        layout.addWidget(btn_profile)
        layout.addWidget(QLabel('Персонажи:'))
        self.char_list = QListWidget()
        self.update_char_list()
        layout.addWidget(self.char_list)
        btns = QHBoxLayout()
        btn_add = QPushButton('Добавить')
        btn_edit = QPushButton('Изменить')
        btn_del = QPushButton('Удалить')
        btn_add.clicked.connect(self.add_char)
        btn_edit.clicked.connect(self.edit_char)
        btn_del.clicked.connect(self.del_char)
        btns.addWidget(btn_add)
        btns.addWidget(btn_edit)
        btns.addWidget(btn_del)
        layout.addLayout(btns)
        self.tabs.addTab(tab1, 'Профиль и персонажи')
        # --- Вкладка 2: Артефакты ---
        tab2 = QWidget()
        layout2 = QVBoxLayout(tab2)
        layout2.addWidget(QLabel('Артефакты/Оружие:'))
        self.art_list = QListWidget()
        self.update_art_list()
        layout2.addWidget(self.art_list)
        abtns = QHBoxLayout()
        abtn_add = QPushButton('Добавить')
        abtn_edit = QPushButton('Изменить')
        abtn_del = QPushButton('Удалить')
        abtn_add.clicked.connect(self.add_art)
        abtn_edit.clicked.connect(self.edit_art)
        abtn_del.clicked.connect(self.del_art)
        abtns.addWidget(abtn_add)
        abtns.addWidget(abtn_edit)
        abtns.addWidget(abtn_del)
        layout2.addLayout(abtns)
        self.tabs.addTab(tab2, 'Артефакты')
        # --- Вкладка 3: Аналитика ---
        tab3 = QWidget()
        layout3 = QVBoxLayout(tab3)
        self.analytics_text = QTextEdit()
        self.analytics_text.setReadOnly(True)
        btn_refresh = QPushButton('Обновить аналитику')
        btn_refresh.clicked.connect(self.update_analytics)
        layout3.addWidget(self.analytics_text)
        layout3.addWidget(btn_refresh)
        self.tabs.addTab(tab3, 'Аналитика')
        self.update_analytics()

        # --- Вкладка 4: Импорт по скрину ---
        tab4 = QWidget()
        layout4 = QVBoxLayout(tab4)
        self.ocr_btn = QPushButton('Загрузить скриншот')
        self.ocr_btn.clicked.connect(self.ocr_import)
        self.ocr_clip_btn = QPushButton('Вставить из буфера')
        self.ocr_clip_btn.clicked.connect(self.ocr_import_clipboard)
        self.ocr_text = QTextEdit()
        self.ocr_text.setReadOnly(False)
        self.ocr_result_btn = QPushButton('Импортировать в профиль')
        self.ocr_result_btn.clicked.connect(self.ocr_apply)
        btns4 = QHBoxLayout()
        btns4.addWidget(self.ocr_btn)
        btns4.addWidget(self.ocr_clip_btn)
        layout4.addLayout(btns4)
        layout4.addWidget(QLabel('Распознанный текст:'))
        layout4.addWidget(self.ocr_text)
        layout4.addWidget(self.ocr_result_btn)
        self.tabs.addTab(tab4, 'Импорт по скрину')

    def ocr_import(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Выбери скриншот', '', 'Images (*.png *.jpg *.jpeg)')
        if fname:
            text = ocr_image_to_text(fname)
            self.ocr_text.setText(text)

    def ocr_apply(self):
        from PyQt5.QtWidgets import QMessageBox
        text = self.ocr_text.toPlainText()
        stats = parse_character_stats(text)
        artifact = parse_artifact(text)
        # Импортируем как нового персонажа и артефакт
        imported = False
        if stats:
            char = {'name': 'Импорт', 'class': '', 'rank': '', **stats}
            self.characters.append(char)
            save_characters(self.characters)
            self.update_char_list()
            imported = True
        if artifact and artifact['name']:
            self.artifacts.append(artifact)
            save_artifacts(self.artifacts)
            self.update_art_list()
            imported = True
        self.update_analytics()
        if not imported:
            QMessageBox.warning(self, 'Импорт не удался', 'Не удалось распознать характеристики или артефакт. Проверь текст или попробуй другой скрин.')

    def ocr_import_clipboard(self):
        # Получаем изображение из буфера обмена и улучшаем для OCR
        from PyQt5.QtWidgets import QApplication
        import pytesseract
        app = QApplication.instance() or QApplication([])
        clipboard = app.clipboard()
        mime = clipboard.mimeData()
        if mime.hasImage():
            qt_img = clipboard.image()
            # Конвертация QImage -> PIL.Image через буфер
            qt_img = qt_img.convertToFormat(QImage.Format_RGBA8888)
            width, height = qt_img.width(), qt_img.height()
            buffer = qt_img.bits().asstring(qt_img.byteCount())
            pil_img = Image.frombytes("RGBA", (width, height), buffer, "raw", "RGBA")
            # Преобразуем для OCR
            pil_img = pil_img.convert('L')  # grayscale
            pil_img = ImageOps.autocontrast(pil_img)
            pil_img = pil_img.point(lambda x: 0 if x < 128 else 255, '1')  # threshold
            text = pytesseract.image_to_string(pil_img, lang='rus+eng')
            self.ocr_text.setText(text)
        else:
            self.ocr_text.setText('В буфере нет изображения!')
    def profile_str(self):
        return f"Профиль: {self.profile.get('name','')} | Уровень: {self.profile.get('level','')} | ID: {self.profile.get('id','')}"
    def edit_profile(self):
        dlg = ProfileDialog(self.profile, self)
        if dlg.exec_():
            self.profile = dlg.get_data()
            save_profile(self.profile)
            self.profile_label.setText(self.profile_str())
    def update_char_list(self):
        self.char_list.clear()
        for c in self.characters:
            item = QListWidgetItem(
                f"{c.get('name', '')} ({c.get('class', '')}, {c.get('rank', '')}) | "
                f"HP:{c.get('hp', '-')} ATK:{c.get('atk', '-')} DEF:{c.get('def', '-')} CRIT:{c.get('crit', '-')}"
            )
            self.char_list.addItem(item)
    def add_char(self):
        dlg = CharacterDialog(parent=self)
        if dlg.exec_():
            self.characters.append(dlg.get_data())
            save_characters(self.characters)
            self.update_char_list()
    def edit_char(self):
        row = self.char_list.currentRow()
        if row >= 0:
            dlg = CharacterDialog(self.characters[row], self)
            if dlg.exec_():
                self.characters[row] = dlg.get_data()
                save_characters(self.characters)
                self.update_char_list()
    def del_char(self):
        row = self.char_list.currentRow()
        if row >= 0:
            del self.characters[row]
            save_characters(self.characters)
            self.update_char_list()
    def update_art_list(self):
        self.art_list.clear()
        for a in self.artifacts:
            item = QListWidgetItem(f"{a['name']} ({a['type']}) | бонусы: {', '.join([f'{k.upper()}:{v}' for k,v in a['bonus'].items()])}")
            self.art_list.addItem(item)
    def add_art(self):
        dlg = ArtifactDialog(parent=self)
        if dlg.exec_():
            self.artifacts.append(dlg.get_data())
            save_artifacts(self.artifacts)
            self.update_art_list()
    def edit_art(self):
        row = self.art_list.currentRow()
        if row >= 0:
            dlg = ArtifactDialog(self.artifacts[row], self)
            if dlg.exec_():
                self.artifacts[row] = dlg.get_data()
                save_artifacts(self.artifacts)
                self.update_art_list()
    def del_art(self):
        row = self.art_list.currentRow()
        if row >= 0:
            del self.artifacts[row]
            save_artifacts(self.artifacts)
            self.update_art_list()
    def update_analytics(self):
        analytics = generate_analytics(self.profile, self.characters, self.artifacts)
        self.analytics_text.setText(analytics)

from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class ProfileDialog(QDialog):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Профиль игрока')
        self.layout = QFormLayout(self)
        self.name = QLineEdit(profile.get('name', ''))
        self.level = QLineEdit(str(profile.get('level', '')))
        self.id = QLineEdit(profile.get('id', ''))
        self.layout.addRow('Имя:', self.name)
        self.layout.addRow('Уровень:', self.level)
        self.layout.addRow('ID:', self.id)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)
    def get_data(self):
        return {
            'name': self.name.text(),
            'level': int(self.level.text()) if self.level.text().isdigit() else 0,
            'id': self.id.text()
        }

class CharacterDialog(QDialog):
    def __init__(self, char=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Персонаж')
        self.layout = QFormLayout(self)
        self.name = QLineEdit(char.get('name', '') if char else '')
        self.char_class = QLineEdit(char.get('class', '') if char else '')
        self.rank = QLineEdit(char.get('rank', '') if char else '')
        self.hp = QLineEdit(str(char.get('hp', '')) if char else '')
        self.atk = QLineEdit(str(char.get('atk', '')) if char else '')
        self.def_ = QLineEdit(str(char.get('def', '')) if char else '')
        self.crit = QLineEdit(str(char.get('crit', '')) if char else '')
        self.layout.addRow('Имя:', self.name)
        self.layout.addRow('Класс:', self.char_class)
        self.layout.addRow('Ранг:', self.rank)
        self.layout.addRow('HP:', self.hp)
        self.layout.addRow('ATK:', self.atk)
        self.layout.addRow('DEF:', self.def_)
        self.layout.addRow('CRIT:', self.crit)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)
    def get_data(self):
        return {
            'name': self.name.text(),
            'class': self.char_class.text(),
            'rank': self.rank.text(),
            'hp': int(self.hp.text()) if self.hp.text().isdigit() else 0,
            'atk': int(self.atk.text()) if self.atk.text().isdigit() else 0,
            'def': int(self.def_.text()) if self.def_.text().isdigit() else 0,
            'crit': int(self.crit.text()) if self.crit.text().isdigit() else 0
        }

class ArtifactDialog(QDialog):
    def __init__(self, art=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Артефакт/Оружие')
        self.layout = QFormLayout(self)
        self.name = QLineEdit(art.get('name', '') if art else '')
        self.type = QLineEdit(art.get('type', '') if art else '')
        self.bonus = QLineEdit(','.join([f"{k}+{v}" for k,v in art.get('bonus', {}).items()]) if art else '')
        self.layout.addRow('Название:', self.name)
        self.layout.addRow('Тип:', self.type)
        self.layout.addRow('Бонус (пример: atk+500,crit+5):', self.bonus)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)
    def get_data(self):
        bonus_dict = {}
        for part in self.bonus.text().split(','):
            if '+' in part:
                k, v = part.strip().split('+')
                bonus_dict[k] = int(v)
        return {
            'name': self.name.text(),
            'type': self.type.text(),
            'bonus': bonus_dict
        }

import pytesseract
from PIL import Image
import re

def ocr_image_to_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='eng+rus')
    return text

def parse_character_stats(text):
    import re
    stats = {}
    # Гибкие паттерны для русского и английского, с учётом OCR-опечаток
    hp = re.search(r'(Зд[аa]ров[ьb][еe]|HP|НР|НР)[ :\-=]*([0-9]{3,})', text, re.IGNORECASE)
    atk = re.search(r'(Атака|Atk|АТК|ATK)[ :\-=]*([0-9]{3,})', text, re.IGNORECASE)
    defense = re.search(r'(Защита|Def|DEF)[ :\-=]*([0-9]{3,})', text, re.IGNORECASE)
    crit = re.search(r'(Крит|Crit|CRIT)[ :\-=]*([0-9]{1,3})', text, re.IGNORECASE)
    if hp: stats['hp'] = int(hp.group(2))
    if atk: stats['atk'] = int(atk.group(2))
    if defense: stats['def'] = int(defense.group(2))
    if crit: stats['crit'] = int(crit.group(2))
    print(f'[DEBUG] Распознано характеристик: {stats}')
    return stats

def parse_artifact(text):
    # Пример: ищет строки вида "Artifact: Sword of Power, Type: Weapon, Bonus: ATK+500"
    name = re.search(r'Artifact[:\s]+([\w\s]+)', text, re.IGNORECASE)
    type_ = re.search(r'Type[:\s]+([\w\s]+)', text, re.IGNORECASE)
    bonus = re.findall(r'(ATK|HP|DEF|CRIT)\+([0-9]+)', text, re.IGNORECASE)
    bonus_dict = {k.lower(): int(v) for k, v in bonus}
    return {
        'name': name.group(1).strip() if name else '',
        'type': type_.group(1).strip() if type_ else '',
        'bonus': bonus_dict
    }

# Можно добавить парсеры для других сущностей (навыки, ядра и т.д.)

import json
import os
from models import Profile, Character, Artifact

PROFILE_FILE = 'profile.json'
CHARACTERS_FILE = 'characters_data.json'
ARTIFACTS_FILE = 'artifacts_data.json'

def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_profile():
    return load_json(PROFILE_FILE, {})

def save_profile(profile):
    save_json(PROFILE_FILE, profile)

def load_characters():
    return load_json(CHARACTERS_FILE, [])

def save_characters(characters):
    save_json(CHARACTERS_FILE, characters)

def load_artifacts():
    return load_json(ARTIFACTS_FILE, [])

def save_artifacts(artifacts):
    save_json(ARTIFACTS_FILE, artifacts)

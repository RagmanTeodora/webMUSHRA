import yaml

# -----------------------------
# SETTINGS (edit these!)
# -----------------------------

# Test metadata
TESTNAME = "My TTS Listening Test"
TESTID = "my_tts_test"

# Base audio path (adjust if needed)
BASE_PATH = "configs/resources/audio/RT_swara"

# List of utterance IDs you want as pages
utterance_ids = [
    "bas_rnd2_456",
    "bas_rnd2_479",
    "bas_rnd2_468",
    "bas_rnd2_494",
    "bas_rnd2_488",
    "bas_rnd2_469",
    "bas_rnd2_462",
    "bas_rnd2_457",
    "bas_rnd2_490",
    "bas_rnd2_483"
]

# Define the TTS systems and their subfolders
systems = {
    "FASTPITCH": "FASTPITCH",
    "Grad-TTS": "Grad-TTS",
    "Matcha-TTS": "Matcha-TTS",
    "VITS": "VITS"
}

# -----------------------------
# GENERATE PAGES
# -----------------------------

pages = []

for i, utt in enumerate(utterance_ids, start=1):
    page = {
        "type": "mushra",
        "id": f"page{i}",
        "name": f"MUSHRA page{i}",
        "content": "In this test, please rate the quality of each sample compared to the reference.",
        "showWaveform": True,
        "enableLooping": False,
        "reference": f"{BASE_PATH}/originals/bas/{utt}.wav",
        "stimuli": {
            sys_name: f"{BASE_PATH}/{folder}/bas/10/{utt}_gen.wav"
            if sys_name in ["FASTPITCH", "VITS"] else f"{BASE_PATH}/{folder}/bas/10/{utt}.wav"
            for sys_name, folder in systems.items()
        },
        "createAnchor35": False,
        "createAnchor70": False
    }
    pages.append(page)

# -----------------------------
# FINAL CONFIG STRUCTURE
# -----------------------------

config = {
    "testname": TESTNAME,
    "testId": TESTID,
    "bufferSize": 2048,
    "stopOnErrors": True,
    "showButtonPreviousPage": True,
    "remoteService": "service/write.php",
    "pages": [
        {
            "type": "generic",
            "id": "first_page",
            "name": "Welcome",
            "content": "Welcome to the listening test! Please follow the instructions and rate the samples."
        },
        *pages,
        {
            "type": "finish",
            "name": "Thank you",
            "content": "Thank you for attending!",
            "showResults": True,
            "writeResults": True,
            "questionnaire": [
                {"type": "text", "label": "eMail", "name": "email"},
                {"type": "number", "label": "Age", "name": "age", "min": 0, "max": 100, "default": 30},
                {"type": "likert", "name": "gender", "label": "Gender", "response": [
                    {"value": "female", "label": "Female"},
                    {"value": "male", "label": "Male"},
                    {"value": "other", "label": "Other"},
                ]}
            ]
        }
    ]
}

# -----------------------------
# WRITE YAML FILE
# -----------------------------

with open("swara_pages.yaml", "w") as f:
    yaml.dump(config, f, sort_keys=False)

print("swara_pages.yaml generated with", len(utterance_ids), "MUSHRA pages!")
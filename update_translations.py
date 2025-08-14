# update_translations.py
import os
import json
from extract_ui_strings import find_ui_files, extract_strings_from_ui
from extract_py_strings import find_py_files, extract_strings_from_py

if __name__ == '__main__':
    ui_directory = 'ui'
    py_directory = 'src/main/python/plotlyst/view/'
    json_file_path = 'src/main/resources/i18n/zh_CN.json'

    # Extract strings
    ui_strings = set()
    ui_files = find_ui_files(ui_directory)
    for file in ui_files:
        ui_strings.update(extract_strings_from_ui(file))

    py_strings = set()
    py_files = find_py_files(py_directory)
    for file in py_files:
        py_strings.update(extract_strings_from_py(file))

    all_strings = sorted(list(ui_strings.union(py_strings)))

    # Load existing translations
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
    else:
        translations = {}

    # Add new strings
    new_strings_added = 0
    for s in all_strings:
        if s not in translations:
            translations[s] = ""  # Add with empty translation
            new_strings_added += 1

    # Save updated translations
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=4, sort_keys=True)

    print(f"Translation file updated. Added {new_strings_added} new strings.")

# pseudo_translate.py
import json

def pseudo_translate(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for key, value in data.items():
        if not value:
            data[key] = f"[zh]{key}"

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

    print("Pseudo-translated all empty strings.")

if __name__ == '__main__':
    json_file_path = 'src/main/resources/i18n/zh_CN.json'
    pseudo_translate(json_file_path)

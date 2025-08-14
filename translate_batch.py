# translate_batch.py
import json

def translate_batch(input_file, output_file, batch_size=30):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    untranslated_keys = [k for k, v in data.items() if not v]

    batch_keys = untranslated_keys[:batch_size]

    # In a real scenario, this is where you'd call a translation API.
    # For this simulation, I will manually provide translations for a few.
    translations_batch = {
        "Add new marker (or double-click on the map)": "添加新标记（或在地图上双击）",
        "Add new note": "添加新笔记",
        "Add new objective": "添加新目标",
        "Add new page": "添加新页面",
        "Add new question": "添加新问题",
        "Add new relation": "添加新关系",
        "Add new scene": "添加新场景",
        "Add new scene or chapter": "添加新场景或章节",
        "Add new story": "添加新故事",
        "Add new story structure": "添加新故事结构",
        "Add new storyline": "添加新故事情节",
        "Add new task": "添加新任务",
        "Add new text": "添加新文本",
        "Add new tool": "添加新工具",
        "Add scene": "添加场景",
        "Add section": "添加段落",
        "Add structure": "添加结构",
        "Add subtask": "添加子任务",
        "Add topics": "添加主题",
        "Added | Removed": "已添加 | 已移除",
        "Advanced settings": "高级设置",
        "Age": "年龄",
        "All": "全部",
        "All (": "全部（",
        "All Writers (": "所有作者（",
        "All writers": "所有作者",
        "Allow synchronization from Scrivener, so every new change will be reflected in Plotlyst.": "允许从Scrivener同步，以便每个新更改都将反映在Plotlyst中。",
        "Alternate History": "架空历史",
        "Amusement": "娱乐",
    }

    # Create a dictionary of translations for the current batch
    batch_to_translate = {key: translations_batch.get(key, "") for key in batch_keys if key in translations_batch}

    # Update the main data object
    for key, value in batch_to_translate.items():
        if key in data:
            data[key] = value

    # Write the full data back
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

    print(f"Translated a batch of {len(batch_to_translate)} strings and updated the file.")


if __name__ == '__main__':
    json_file_path = 'src/main/resources/i18n/zh_CN.json'
    translate_batch(json_file_path, json_file_path)

import os
import re
import xml.etree.ElementTree as ET

def find_ui_files(directory):
    """Find all .ui files in a directory."""
    ui_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.ui'):
                ui_files.append(os.path.join(root, file))
    return ui_files

def is_likely_translatable(s):
    """
    Heuristics to determine if a string is likely user-facing text.
    """
    if not s or not s.strip():
        return False
    # Filter out short, non-alphabetic strings
    if len(s.strip()) < 3 and not s.strip().isalpha():
        return False
    # Filter out identifiers (camelCase, snake_case)
    if re.match(r'^[a-z]+([A-Z][a-z0-9]*)+$', s):
        return False
    if re.match(r'^[a-z_]+$', s):
        return False
    # Filter out CSS, HTML, color codes, etc.
    if any(c in s for c in ['{', '}', '<', '>', '#', ':', ';', 'px', 'border', 'color', 'background-color']):
        return False
    # Filter out things that look like icon names
    if re.match(r'^[a-z0-9]+\.[a-z0-9]+', s):
        return False
    return True

def extract_strings_from_ui(file_path):
    """Extract translatable strings from a .ui file."""
    strings = set()
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        properties_to_check = ['windowTitle', 'text', 'toolTip', 'placeholderText', 'title']

        for prop_name in properties_to_check:
            # For properties like <property name="text"><string>Hello</string></property>
            for prop in root.findall(f".//property[@name='{prop_name}']/string"):
                if is_likely_translatable(prop.text):
                    strings.add(prop.text.strip())

            # For attributes like <widget title="Hello">
            for widget in root.findall(f".//widget[@{prop_name}]"):
                 text = widget.get(prop_name)
                 if is_likely_translatable(text):
                     strings.add(text.strip())

        # For menu actions specifically
        for action in root.findall('.//action'):
            text = action.get('text')
            if is_likely_translatable(text):
                strings.add(text.strip())

    except ET.ParseError:
        print(f"Warning: Could not parse {file_path}")
    return strings

if __name__ == '__main__':
    ui_directory = 'ui'
    all_strings = set()
    ui_files = find_ui_files(ui_directory)
    for file in ui_files:
        all_strings.update(extract_strings_from_ui(file))

    sorted_strings = sorted(list(all_strings))

    print("Found translatable strings:")
    for s in sorted_strings:
        print(s)

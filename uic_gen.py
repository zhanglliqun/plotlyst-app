import os
import subprocess

def compile_dir(ui_dir, out_dir, recursive=False):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for root, _, files in os.walk(ui_dir):
        for file in files:
            if file.endswith('.ui'):
                ui_path = os.path.join(root, file)
                py_path = os.path.join(out_dir, os.path.splitext(file)[0] + '_ui.py')

                # Ensure the __init__.py file exists in the target directory
                init_path = os.path.join(os.path.dirname(py_path), "__init__.py")
                if not os.path.exists(init_path):
                    with open(init_path, 'w') as f:
                        pass

                command = ['pyuic6', '-o', py_path, ui_path]
                print(f"Compiling {ui_path} to {py_path}")
                subprocess.run(command, check=True)

        if not recursive:
            break

if __name__ == '__main__':
    compile_dir('ui', 'src/main/python/plotlyst/view/generated', recursive=True)

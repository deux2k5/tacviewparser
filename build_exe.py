import PyInstaller.__main__
import os

def build_exe():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tacview_app_path = os.path.join(script_dir, 'tacview_app.py')
    image_path = os.path.join(script_dir, 'objectIcons')

    PyInstaller.__main__.run([
        'tacview_app.py',
        '--onefile',
        '--windowed',
        '--add-data', f'{image_path};objectIcons',
        '--name', 'TacviewApp',
        '--icon', os.path.join(image_path, 'icon.ico'),  # Make sure you have an icon file
    ])

if __name__ == '__main__':
    build_exe()

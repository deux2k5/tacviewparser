import PyInstaller.__main__
import os

def build_exe():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tacview_app_path = os.path.join(script_dir, 'tacview_app.py')
    image_path = os.path.join(script_dir, 'objectIcons')
    icon_path = os.path.join(image_path, 'icon.ico')

    # Check if the icon file exists
    if not os.path.exists(icon_path):
        print(f"Warning: Icon file {icon_path} not found. Using default PyInstaller icon.")
        icon_path = None  # PyInstaller will use its default icon

    PyInstaller.__main__.run([
        'tacview_app.py',
        '--onefile',
        '--windowed',
        '--add-data', f'{image_path};objectIcons',
        '--name', 'TacviewApp',
    ] + (['--icon', icon_path] if icon_path else []))

if __name__ == '__main__':
    build_exe()

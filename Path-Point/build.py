import subprocess
import sys
import os

print("=" * 50)
print("Сборка проекта Path-Point в .exe (onefile)")
print("=" * 50)

# Шаг 1: Удаляем конфликтующий пакет pathlib
print("\n[1/2] Проверяем и удаляем конфликтующий пакет pathlib...")
subprocess.run([sys.executable, "-m", "pip", "uninstall", "pathlib", "-y"], 
               capture_output=True)
print("✓ pathlib удален (если был установлен)")

# Шаг 2: Запускаем сборку в режиме onefile
print("\n[2/2] Запускаем PyInstaller (onefile)...")

cmd = [
    sys.executable,
    "-m", "PyInstaller",
    "--noconfirm",
    "--onefile",  # <-- ОДИН файл exe
    "--windowed",
    "--name", "Path-Point",
    "--add-binary", "physics.dll;.",  # Включаем C-DLL
    "--hidden-import", "arcade",
    "--hidden-import", "cv2",
    "--hidden-import", "numpy",
    "--hidden-import", "PIL",
    "--hidden-import", "video_editor",
    "--hidden-import", "app_config",
    "--hidden-import", "logic",
    "--hidden-import", "visualizer",
    "main.py"
]

print(f"\nКоманда: {' '.join(cmd)}\n")

result = subprocess.run(cmd, capture_output=False)

if result.returncode == 0:
    print("\n" + "=" * 50)
    print("✓ Сборка завершена успешно!")
    print(f"✓ Готовый .exe находится в: {os.path.join(os.getcwd(), 'dist', 'Path-Point.exe')}")
    print("=" * 50)
else:
    print("\n" + "=" * 50)
    print("✗ Ошибка при сборке!")
    print("=" * 50)
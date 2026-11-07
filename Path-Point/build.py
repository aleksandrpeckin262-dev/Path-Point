import PyInstaller.__main__
import os
import shutil

# НАХОДИМ КОРЕНЬ ПРОЕКТА
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ЖЕСТКИЙ СНОС ВСЕХ СКРЫТЫХ ПАПОК КЭША И БИЛДОВ
# (Уничтожаем кэш самого Питона и временные папки сборщика)
for root, dirs, files in os.walk(BASE_DIR):
    for d in dirs:
        if d in ['__pycache__', 'build', 'dist', '.pytest_cache']:
            try:
                shutil.rmtree(os.path.join(root, d))
            except Exception:
                pass

# ЖЕСТКИЙ СНОС ФАЙЛА СПЕЦИФИКАЦИИ .spec (Из-за него PyInstaller и берет старье!)
spec_file = os.path.join(BASE_DIR, 'Path_Point.spec')
if os.path.exists(spec_file):
    try:
        os.remove(spec_file)
    except Exception:
        pass

print("🔥 Кэш и старые билды полностью выжжены дотла! Начинаем чистую сборку...")

# Запуск чистейшей сборки с нуля
PyInstaller.__main__.run([
    os.path.join(BASE_DIR, 'main.py'),
    '--name=Path_Point',
    '--onefile',
    '--windowed',
    '--clean',  # Внутренняя очистка PyInstaller
    f'--add-data={os.path.join(BASE_DIR, "physics.dll")}{os.pathsep}.',
])

# Автокопирование свежего конфига в новенькую папку dist
try:
    shutil.copy(os.path.join(BASE_DIR, 'config.json'), os.path.join(BASE_DIR, 'dist', 'config.json'))
    print("\n🚀 БАБАХ! Сборка полностью обновлена. Проверяй свежий Path_Point.exe в dist/")
except Exception as e:
    print(f"\n⚠️ Не удалось скопировать конфиг: {e}")

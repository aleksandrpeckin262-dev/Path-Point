# ГЛАВНЫЙ ИСТОЧНИК СИЛЫ — ИМПОРТИРУЕМ ВСЁ ТУТ
import os
import sys
import builtins

# Насильно пихаем sys и os во все модули программы, чтобы никто не смел их не видеть!
builtins.sys = sys
builtins.os = os

# Вычисляем корень прямо в мэине
if getattr(sys, 'frozen', False):
    builtins._root_dir = os.path.dirname(sys.executable)
else:
    builtins._root_dir = os.path.dirname(os.path.abspath(__file__))

# Только ПОСЛЕ этого запускаем логику
from logic import start_logic
from visualizer import main as run_visualizer

video_flag = 1

# Логика
start_logic(video_flag)

# Отрисовка
run_visualizer()

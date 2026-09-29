from logic import start_logic
from visualizer import main as run_visualizer

# Запускаем логику
start_logic()

# Запускаем отрисовку (блокирует главный поток)
run_visualizer()
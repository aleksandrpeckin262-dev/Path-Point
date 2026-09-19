import random
import time
import app_config
import threading

# Позиции спавна
spawn_positions = [
    (app_config.point_position_0_X, app_config.point_position_0_Y),  # 0
    (app_config.point_position_1_X, app_config.point_position_1_Y),  # 1
    (app_config.point_position_2_X, app_config.point_position_2_Y),  # 2
    (app_config.point_position_3_X, app_config.point_position_3_Y),  # 3
    (app_config.point_position_4_X, app_config.point_position_4_Y),  # 4
    (app_config.point_position_5_X, app_config.point_position_5_Y),  # 5
    (app_config.point_position_6_X, app_config.point_position_6_Y),  # 6
    (app_config.point_position_7_X, app_config.point_position_7_Y)   # 7
]

active_points = [] 

INTERVAL = app_config.tik_rate / 100  # Раз в тик

def spawn_point():
    position = random.randint(0, 7)
               
    position_x = 0
    position_y = 0
    point_rotation = 0
    
    
    if position == 0:
        position_x = app_config.point_position_0_X + random.randint(point_X_random_min, point_X_random_max)
        position_y = point_position_0_Y + random.randint(point_Y_random_min, point_Y_random_max)
        point_rotation = point_rotation_1 + random.randint(point_rotation_min, point_rotation_max)
        print("Стартовая точка")
        print(position)
        print("Позиция X")
        print(position_x)
        print("Позиция Y")
        print(position_y)
        print("Позиция Y")
        print(position_y)
        print("Поворот")
        print(position_y)
    time.sleep(INTERVAL)
        
while True:
    start_time = time.time()  # Засекаем время начала
    
    spawn_point()     # Запускаем вашу функцию с кучей if
    
    execution_time = time.time() - start_time  # Считаем, сколько она шла
    
    # Считаем, сколько осталось спать (чтобы в сумме было 5 секунд)
    sleep_time = max(0, INTERVAL - execution_time) 
    time.sleep(sleep_time)
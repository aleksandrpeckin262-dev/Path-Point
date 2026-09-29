import random
import time
import math
import app_config
import threading
import arcade

screen_width, screen_height = arcade.get_display_size()
if not screen_width or not screen_height:
    screen_width, screen_height = 1920, 1080

screen_size = screen_width + screen_height

spawn_positions = [
    (screen_width * app_config.point_position_0_X / 100, screen_height * app_config.point_position_0_Y / 100),
    (screen_width * app_config.point_position_1_X / 100, screen_height * app_config.point_position_1_Y / 100),
    (screen_width * app_config.point_position_2_X / 100, screen_height * app_config.point_position_2_Y / 100),
    (screen_width * app_config.point_position_3_X / 100, screen_height * app_config.point_position_3_Y / 100),
    (screen_width * app_config.point_position_4_X / 100, screen_height * app_config.point_position_4_Y / 100),
    (screen_width * app_config.point_position_5_X / 100, screen_height * app_config.point_position_5_Y / 100),
    (screen_width * app_config.point_position_6_X / 100, screen_height * app_config.point_position_6_Y / 100),
    (screen_width * app_config.point_position_7_X / 100, screen_height * app_config.point_position_7_Y / 100)
]

base_rotations = [
    app_config.point_rotation_0, app_config.point_rotation_1,
    app_config.point_rotation_2, app_config.point_rotation_3,
    app_config.point_rotation_4, app_config.point_rotation_5,
    app_config.point_rotation_6, app_config.point_rotation_7
]

active_points = [] 
collision_pairs = []

SPAWN_INTERVAL = app_config.tik_rate / 100000
UPDATE_INTERVAL = app_config.tik_rate / 100

points_lock = threading.Lock()

def spawn_point():
    position = random.randint(0, 7)
    base_x, base_y = spawn_positions[position]
    base_rotation = base_rotations[position]
    
    position_x = base_x + random.randint(app_config.point_X_random_min, app_config.point_X_random_max)
    position_y = base_y + random.randint(app_config.point_Y_random_min, app_config.point_Y_random_max)
    point_rotation = base_rotation + random.randint(app_config.point_rotation_min, app_config.point_rotation_max)
    
    point_speed_x = random.randint(app_config.point_speed_random_min, app_config.point_speed_random_max)
    point_speed_y = random.randint(app_config.point_speed_random_min, app_config.point_speed_random_max)
    
    if point_speed_x == 0:
        point_speed_x += 1
    if point_speed_y == 0:
        point_speed_y += 1
    
    with points_lock:
        active_points.append((position_x, position_y, point_rotation, point_speed_x, point_speed_y))
    
def update_position():
    with points_lock:
        for i in range(len(active_points)):
            x, y, rotation, speed_x, speed_y = active_points[i]
            new_x = x + speed_x
            new_y = y + speed_y
            active_points[i] = (new_x, new_y, rotation, speed_x, speed_y)
        
def delete_point():
    with points_lock:
        i = 0
        while i < len(active_points):
            x, y, rotation, speed_x, speed_y = active_points[i]
            
            if x > screen_width or y > screen_height or x < 0 or y < 0:
                active_points.pop(i)
            else:
                i += 1

def detect_collisions():
    global collision_pairs
    
    with points_lock:
        pairs = []
        radius_sq = (screen_size / app_config.point_collision) ** 2
        
        for i in range(len(active_points)):
            for j in range(i + 1, len(active_points)):
                x1, y1 = active_points[i][0], active_points[i][1]
                x2, y2 = active_points[j][0], active_points[j][1]
                
                dist_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
                
                if dist_sq <= radius_sq:
                    pairs.append((active_points[i], active_points[j]))
        
        # НЕ пересоздаём список, а очищаем и заполняем тот же объект
        collision_pairs.clear()
        collision_pairs.extend(pairs)

def spawn_loop():    
    while True:
        with points_lock:
            current_count = len(active_points)
        
        if current_count < app_config.limit_point:
            start_time = time.time()
            spawn_point()
            execution_time = time.time() - start_time
            sleep_time = max(0, SPAWN_INTERVAL - execution_time) 
            time.sleep(sleep_time)
        else:
            time.sleep(0.1)

def move_loop(): 
    while True:
        start_time = time.time()
        update_position()
        sleep_time = max(0, UPDATE_INTERVAL - (time.time() - start_time))
        time.sleep(sleep_time)

def delete_loop():  
    while True:
        start_time = time.time()
        delete_point()
        sleep_time = max(0, UPDATE_INTERVAL - (time.time() - start_time))
        time.sleep(sleep_time)

def collision_loop():
    while True:
        start_time = time.time()
        detect_collisions()
        sleep_time = max(0, UPDATE_INTERVAL - (time.time() - start_time))
        time.sleep(sleep_time)

def start_logic():
    t1 = threading.Thread(target=spawn_loop, daemon=True)
    t2 = threading.Thread(target=move_loop, daemon=True)
    t3 = threading.Thread(target=delete_loop, daemon=True)
    t4 = threading.Thread(target=collision_loop, daemon=True)
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    
    return t1, t2, t3, t4
import random
import time
import math
import app_config
import threading
import arcade
import ctypes
import os
import pyautogui
from datetime import datetime

# --- Шаг 1: Подключение скомпилированной C-библиотеки ---
dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "physics.dll")
try:
    physics = ctypes.CDLL(dll_path)
except Exception as e:
    raise FileNotFoundError(
        f"Не удалось загрузить physics.dll по пути {dll_path}. "
        f"Убедитесь, что вы скомпилировали его в MSYS2 командой: gcc -O3 -shared physics.c -o physics.dll"
    ) from e

# --- Шаг 2: Описание структур данных C для Python ---
class PointC(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("rotation", ctypes.c_double),
        ("speed_x", ctypes.c_double),
        ("speed_y", ctypes.c_double)
    ]

class CollisionPairC(ctypes.Structure):
    _fields_ = [
        ("index1", ctypes.c_int32),
        ("index2", ctypes.c_int32)
    ]


# --- Инициализация геометрии и базовых позиций ---
screen_width, screen_height = arcade.get_display_size()
if not screen_width or not screen_height:
    screen_width, screen_height = 1920, 1080

screen_size = screen_width + screen_height

# Флаг того, что у нас режим записи (1), или режим генерации без записи (0)
video_flag = 1

# Имя папки создаваемое в reate folder
new_folder_name = "video_1"

# ФПС для записи видео
VIDEO_FPS = app_config.video_FPS

# Номер кадра в записи
frame_number = 1

# Базовые позиции (в пикселях, из процентов)
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

# Погрешности позиции для каждой базы (в пикселях, из процентов)
random_x_min = [
    screen_width * app_config.point_X_random_min_0 / 100,
    screen_width * app_config.point_X_random_min_1 / 100,
    screen_width * app_config.point_X_random_min_2 / 100,
    screen_width * app_config.point_X_random_min_3 / 100,
    screen_width * app_config.point_X_random_min_4 / 100,
    screen_width * app_config.point_X_random_min_5 / 100,
    screen_width * app_config.point_X_random_min_6 / 100,
    screen_width * app_config.point_X_random_min_7 / 100,
]

random_x_max = [
    screen_width * app_config.point_X_random_max_0 / 100,
    screen_width * app_config.point_X_random_max_1 / 100,
    screen_width * app_config.point_X_random_max_2 / 100,
    screen_width * app_config.point_X_random_max_3 / 100,
    screen_width * app_config.point_X_random_max_4 / 100,
    screen_width * app_config.point_X_random_max_5 / 100,
    screen_width * app_config.point_X_random_max_6 / 100,
    screen_width * app_config.point_X_random_max_7 / 100,
]

random_y_min = [
    screen_height * app_config.point_Y_random_min_0 / 100,
    screen_height * app_config.point_Y_random_min_1 / 100,
    screen_height * app_config.point_Y_random_min_2 / 100,
    screen_height * app_config.point_Y_random_min_3 / 100,
    screen_height * app_config.point_Y_random_min_4 / 100,
    screen_height * app_config.point_Y_random_min_5 / 100,
    screen_height * app_config.point_Y_random_min_6 / 100,
    screen_height * app_config.point_Y_random_max_7 / 100,
]

random_y_max = [
    screen_height * app_config.point_Y_random_max_0 / 100,
    screen_height * app_config.point_Y_random_max_1 / 100,
    screen_height * app_config.point_Y_random_max_2 / 100,
    screen_height * app_config.point_Y_random_max_3 / 100,
    screen_height * app_config.point_Y_random_max_4 / 100,
    screen_height * app_config.point_Y_random_max_5 / 100,
    screen_height * app_config.point_Y_random_max_6 / 100,
    screen_height * app_config.point_Y_random_max_7 / 100,
]

# Индивидуальные погрешности поворота для каждой базы
rotation_min = [
    app_config.point_rotation_0_min, app_config.point_rotation_1_min,
    app_config.point_rotation_2_min, app_config.point_rotation_3_min,
    app_config.point_rotation_4_min, app_config.point_rotation_5_min,
    app_config.point_rotation_6_min, app_config.point_rotation_7_min,
]

rotation_max = [
    app_config.point_rotation_0_max, app_config.point_rotation_1_max,
    app_config.point_rotation_2_max, app_config.point_rotation_3_max,
    app_config.point_rotation_4_max, app_config.point_rotation_5_max,
    app_config.point_rotation_6_max, app_config.point_rotation_7_max,
]

active_points = [] 
collision_pairs = []

SPAWN_INTERVAL = app_config.spawn_interval
UPDATE_INTERVAL = app_config.tik_rate

points_lock = threading.Lock()
last_move_time = time.time()


def spawn_point():
    position = random.randint(0, 7)
    base_x, base_y = spawn_positions[position]
    base_rotation = base_rotations[position]
    
    position_x = base_x + random.randint(int(random_x_min[position]), int(random_x_max[position]))
    position_y = base_y + random.randint(int(random_y_min[position]), int(random_y_max[position]))
    
    rot_min = rotation_min[position]
    rot_max = rotation_max[position]
    if rot_min > rot_max:
        rot_min, rot_max = rot_max, rot_min
    point_rotation = base_rotation + random.randint(rot_min, rot_max)
    
    speed = random.randint(abs(app_config.point_speed_random_min), abs(app_config.point_speed_random_max))
    point_speed_x = speed * math.cos(math.radians(point_rotation))
    point_speed_y = speed * math.sin(math.radians(point_rotation))
    
    if point_speed_x == 0 and point_speed_y == 0:
        point_speed_x = 1.0
    
    with points_lock:
        active_points.append((position_x, position_y, point_rotation, point_speed_x, point_speed_y))


# --- Измененные функции с гарантированным сохранением ссылок ---

def update_position(dt):
    if not active_points:
        return

    with points_lock:
        count = len(active_points)
        c_array = (PointC * count)()
        
        for i, p in enumerate(active_points):
            c_array[i] = PointC(
                ctypes.c_double(p[0]),
                ctypes.c_double(p[1]),
                ctypes.c_double(p[2]),
                ctypes.c_double(p[3]),
                ctypes.c_double(p[4])
            )
        
        physics.update_position_c(c_array, ctypes.c_int32(count), ctypes.c_double(dt))
        
        # ВАЖНО: Обновляем старый список на месте, не создавая новый объект в памяти!
        for i in range(count):
            p = c_array[i]
            active_points[i] = (float(p.x), float(p.y), float(p.rotation), float(p.speed_x), float(p.speed_y))


def detect_collisions():
    global collision_pairs
    if not active_points:
        return

    with points_lock:
        count = len(active_points)
        c_array = (PointC * count)()
        for i, p in enumerate(active_points):
            c_array[i] = PointC(
                ctypes.c_double(p[0]),
                ctypes.c_double(p[1]),
                ctypes.c_double(p[2]),
                ctypes.c_double(p[3]),
                ctypes.c_double(p[4])
            )
        
        radius_sq = (screen_size / app_config.point_collision) ** 2
        
        max_pairs = 5000
        c_pairs = (CollisionPairC * max_pairs)()
        
        actual_pairs_count = physics.detect_collisions_c(
            c_array, 
            ctypes.c_int32(count), 
            ctypes.c_double(radius_sq), 
            c_pairs,
            ctypes.c_int32(max_pairs)
        )
        
        new_pairs = []
        for i in range(actual_pairs_count):
            idx1 = c_pairs[i].index1
            idx2 = c_pairs[i].index2
            if idx1 < count and idx2 < count:
                new_pairs.append((active_points[idx1], active_points[idx2]))
        
        # Полностью перезаписываем содержимое глобального списка коллизий
        collision_pairs.clear()
        collision_pairs.extend(new_pairs)


def delete_point():
    with points_lock:
        i = 0
        margin = 10  
        while i < len(active_points):
            x, y, rotation, speed_x, speed_y = active_points[i]
            if x > screen_width + margin or y > screen_height + margin or x < -margin or y < -margin:
                active_points.pop(i)
            else:
                i += 1
                
def create_folder(video_flag, new_folder_name):
    if video_flag == 1:
        # Собираем путь к нужной папке (например, ./video/video_1)
        path = os.path.join(".", "video", new_folder_name)
    
        # Проверяем, существует ли папка, и создаем ее
        if not os.path.exists(path):
          os.mkdir(path)
          print(f"Папка успешно создана: {path}")
        else:
          print("Такая папка уже есть!")
    else:
        print("Флаг 0!")
        
def make_scrinshot(video_FPS, video_flag, frame_number, path):
    if video_flag == 1:
        # Скриншот
        screenshot = pyautogui.screenshot()
        # Создание имени для кадра
        screenshot_name = f"frame_{frame_number}.png"
        # Увеличиваем счетчик кадров
        frame_number += 1
        # Создание полного пути для сохранения
        screenshot_path = os.path.join(path, screenshot_name)
        # Сохранение скриншота
        screenshot.save(screenshot_path)
        print(f"Скриншот успешно сохранен в: {screenshot_path}")
    else:
        print("Флаг 0!")
        

# --- Фоновые циклы и потоки ---

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
            time.sleep(0.01)


def move_loop(): 
    global last_move_time
    while True:
        current_time = time.time()
        dt = current_time - last_move_time
        last_move_time = current_time
        
        start_time = time.time()
        update_position(dt) 
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
        
def video_record_loop():
        global frame_number
        # Рассчитываем задержку между кадрами на основе твоего VIDEO_FPS
        frame_delay = 1.0 / VIDEO_FPS
        path = os.path.join(".", "video", new_folder_name)
        
        # Сколько нужно снять кадров
        max_frames = app_config.max_frames
    
         # Сначала один раз создаем папку
        create_folder(video_flag, new_folder_name)

        while video_flag == 1 and frame_number <= max_frames:
            start_time = time.time()
    
            # Делаем скриншот через твою функцию
            make_scrinshot(VIDEO_FPS, video_flag, frame_number, path)
            frame_number += 1  # Увеличиваем счетчик кадра для следующей итерации

            # Выдерживаем точный FPS записи
            execution_time = time.time() - start_time
            sleep_time = max(0, frame_delay - execution_time)
            time.sleep(sleep_time)
        
def start_logic(video_flag):
    t1 = threading.Thread(target=spawn_loop, daemon=True)
    t2 = threading.Thread(target=move_loop, daemon=True)
    t3 = threading.Thread(target=delete_loop, daemon=True)
    t4 = threading.Thread(target=collision_loop, daemon=True)
    
    t_video = threading.Thread(target=video_record_loop, daemon=True)
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    
    if video_flag == 1:
        t_video.start()
    else:
        pass
    
    return t1, t2, t3, t4
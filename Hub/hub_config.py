# Настройки главного окна
APP_TITLE = "Path-Point-v2"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
APPEARANCE_MODE = "Dark"
COLOR_THEME = "dark-blue"
GENERATIONS_FOLDER = "generations"

# Настройки анимации многоугольников
POLYGON_SIDES = 8                  # Количество углов (6 - шестиугольник, 8 - восьмиугольник)
POLYGON_RADII = [80, 150, 220]     # Радиусы трёх колец в пикселях
POLYGON_LINE_WIDTH = 16            # Толщина линий многоугольников
POLYGON_ROTATION_SPEED = 0.6       # Скорость вращения (градусов за кадр)
ANIMATION_FRAME_DELAY_MS = 30      # Задержка между кадрами (~33 FPS)

# Настройки анимации заголовка (печатная машинка)
WELCOME_TEXT = "Welcome to Hub"
TYPING_CURSOR = "_"
TYPING_SPEED_MS = 70               # Скорость появления одной буквы в миллисекундах

# Шрифты (семейство, размер, стиль)
FONT_TITLE_MAIN = ("Arial", 50, "bold")
FONT_TITLE_SELECT = ("Arial", 36, "bold")
FONT_SUBTITLE = ("Arial", 14)
FONT_STATUS = ("Arial", 13, "bold")
FONT_BUTTON_MAIN = ("Arial", 16, "bold")
FONT_BUTTON_SECONDARY = ("Arial", 16)
FONT_BUTTON_BACK = ("Arial", 15)
FONT_MODULE_CARD = ("Arial", 18, "bold")
FONT_EMPTY_MSG = ("Arial", 15)

# Цветовая палитра (HEX)
COLOR_ACCENT_BG = "#1F2833"        # Цвет многоугольников и карточек модулей
COLOR_ACCENT_HOVER = "#2C3A4A"     # Цвет карточки модуля при наведении
COLOR_BTN_SECONDARY = "#2B303A"    # Цвет второстепенных кнопок (Exit, Back)
COLOR_BTN_SEC_HOVER = "#3B4252"    # Цвет второстепенных кнопок при наведении
COLOR_CONTAINER_BG = "#16191F"     # Фон списка генераторов

COLOR_TEXT_PRIMARY = "#8F96A3"     # Заголовок Select Generator
COLOR_TEXT_MUTED = "#5A5F69"       # Заголовок Welcome и подзаголовки
COLOR_TEXT_EMPTY = "#6C7380"       # Текст при пустой папке generations
COLOR_STATUS_INFO = "#4DA8DA"      # Информационный статус
COLOR_STATUS_SUCCESS = "#98C379"   # Успешный запуск .exe
COLOR_STATUS_ERROR = "#E06C75"     # Ошибка запуска

# Размеры и координаты элементов интерфейса
WELCOME_TITLE_Y = 80
WELCOME_BUTTONS_Y = 220
MAIN_BTN_WIDTH = 220
MAIN_BTN_HEIGHT = 44
BACK_BTN_WIDTH = 160
BACK_BTN_HEIGHT = 38
MODULES_BOX_WIDTH = 550
MODULES_BOX_HEIGHT = 360
MODULE_CARD_HEIGHT = 55

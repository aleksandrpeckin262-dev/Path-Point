import os
import sys
import math
import subprocess
import customtkinter as ctk
import hub_config as cfg

# Установка темы оформления
ctk.set_appearance_mode(cfg.APPEARANCE_MODE)
ctk.set_default_color_theme(cfg.COLOR_THEME)


def get_base_dir() -> str:
    """Возвращает путь к папке, где лежит hub.py или скомпилированный hub.exe."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки главного окна
        self.title(cfg.APP_TITLE)
        self.geometry(f"{cfg.WINDOW_WIDTH}x{cfg.WINDOW_HEIGHT}")
        self.resizable(False, False)

        # Путь к папке generations
        self.generations_dir = os.path.join(get_base_dir(), cfg.GENERATIONS_FOLDER)
        os.makedirs(self.generations_dir, exist_ok=True)

        # Состояние анимаций и холста
        self.canvas = None
        self.angle = 0.0
        self.is_animating = False
        self.typing_job = None

        # Контэйнеры для экранов
        self.welcome_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.select_frame = ctk.CTkFrame(self, fg_color="transparent")

        # Инициализируем наполнение экранов
        self.setup_welcome_screen()
        self.setup_select_screen()

        # Показываем стартовый экран
        self.show_welcome_screen()

    def draw_decorations(self, parent_frame):
        """Создаёт холст для вращающихся многоугольников."""
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTk"]["fg_color"])

        self.canvas = ctk.CTkCanvas(
            parent_frame,
            width=cfg.WINDOW_WIDTH,
            height=cfg.WINDOW_HEIGHT,
            bg=bg_color,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.place(x=0, y=0)

    def animate_polygons(self):
        """Отрисовка и вращение многоугольников в нижних углах."""
        if not self.is_animating or self.canvas is None:
            return

        self.canvas.delete("poly")
        self.angle = (self.angle + cfg.POLYGON_ROTATION_SPEED) % 360

        for idx, r in enumerate(cfg.POLYGON_RADII):
            direction = -1 if idx == 1 else 1
            rad_offset = math.radians(self.angle * direction)

            pts_left = []
            pts_right = []

            for i in range(cfg.POLYGON_SIDES):
                a = rad_offset + (2 * math.pi * i / cfg.POLYGON_SIDES)
                pts_left.extend([
                    0 + math.cos(a) * r,
                    cfg.WINDOW_HEIGHT + math.sin(a) * r,
                ])
                pts_right.extend([
                    cfg.WINDOW_WIDTH + math.cos(-a) * r,
                    cfg.WINDOW_HEIGHT + math.sin(-a) * r,
                ])

            self.canvas.create_polygon(
                pts_left,
                fill="",
                outline=cfg.COLOR_ACCENT_BG,
                width=cfg.POLYGON_LINE_WIDTH,
                tags="poly",
            )
            self.canvas.create_polygon(
                pts_right,
                fill="",
                outline=cfg.COLOR_ACCENT_BG,
                width=cfg.POLYGON_LINE_WIDTH,
                tags="poly",
            )

        self.after(cfg.ANIMATION_FRAME_DELAY_MS, self.animate_polygons)

    def animate_welcome_text(self, index: int = 0):
        """Эффект печатной машинки для главного заголовка."""
        full_text = cfg.WELCOME_TEXT

        if index <= len(full_text):
            cursor = cfg.TYPING_CURSOR if index < len(full_text) else ""
            self.welcome_label.configure(text=full_text[:index] + cursor)
            self.typing_job = self.after(cfg.TYPING_SPEED_MS, self.animate_welcome_text, index + 1)
        else:
            self.typing_job = None

    def setup_welcome_screen(self):
        """Наполнение стартового экрана."""
        self.draw_decorations(self.welcome_frame)

        self.welcome_label = ctk.CTkLabel(
            self.welcome_frame,
            text="",
            font=cfg.FONT_TITLE_MAIN,
            text_color=cfg.COLOR_TEXT_MUTED,
        )
        self.welcome_label.place(relx=0.5, y=cfg.WELCOME_TITLE_Y, anchor="center")

        buttons_box = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        buttons_box.place(relx=0.5, y=cfg.WELCOME_BUTTONS_Y, anchor="center")

        btn_generate = ctk.CTkButton(
            buttons_box,
            text="Start generation",
            width=cfg.MAIN_BTN_WIDTH,
            height=cfg.MAIN_BTN_HEIGHT,
            font=cfg.FONT_BUTTON_MAIN,
            command=self.show_select_screen,
        )
        btn_generate.pack(pady=8)

        btn_exit = ctk.CTkButton(
            buttons_box,
            text="Exit",
            width=cfg.MAIN_BTN_WIDTH,
            height=cfg.MAIN_BTN_HEIGHT,
            font=cfg.FONT_BUTTON_SECONDARY,
            fg_color=cfg.COLOR_BTN_SECONDARY,
            hover_color=cfg.COLOR_BTN_SEC_HOVER,
            command=self.destroy,
        )
        btn_exit.pack(pady=8)

    def setup_select_screen(self):
        """Экран выбора генератора со строгим центрированием."""
        container = ctk.CTkFrame(self.select_frame, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            container,
            text="Select Generator",
            font=cfg.FONT_TITLE_SELECT,
            text_color=cfg.COLOR_TEXT_PRIMARY,
        )
        title.pack(pady=(0, 8))

        subtitle = ctk.CTkLabel(
            container,
            text=f"Choose an effect module from /{cfg.GENERATIONS_FOLDER} folder",
            font=cfg.FONT_SUBTITLE,
            text_color=cfg.COLOR_TEXT_MUTED,
        )
        subtitle.pack(pady=(0, 15))

        self.status_label = ctk.CTkLabel(
            container,
            text="",
            font=cfg.FONT_STATUS,
            text_color=cfg.COLOR_STATUS_INFO,
        )
        self.status_label.pack(pady=(0, 10))

        self.modules_container = ctk.CTkScrollableFrame(
            container,
            width=cfg.MODULES_BOX_WIDTH,
            height=cfg.MODULES_BOX_HEIGHT,
            fg_color=cfg.COLOR_CONTAINER_BG,
            corner_radius=12,
        )
        self.modules_container.pack(pady=5)

        btn_back = ctk.CTkButton(
            container,
            text="← Back",
            width=cfg.BACK_BTN_WIDTH,
            height=cfg.BACK_BTN_HEIGHT,
            font=cfg.FONT_BUTTON_BACK,
            fg_color=cfg.COLOR_BTN_SECONDARY,
            hover_color=cfg.COLOR_BTN_SEC_HOVER,
            command=self.show_welcome_screen,
        )
        btn_back.pack(pady=(15, 0))

    def refresh_modules_list(self):
        """Сканирует папку generations и создаёт кнопки для каждой подпапки."""
        self.status_label.configure(text="")
        for widget in self.modules_container.winfo_children():
            widget.destroy()

        folders = [
            f for f in os.listdir(self.generations_dir)
            if os.path.isdir(os.path.join(self.generations_dir, f))
        ]

        if not folders:
            empty_label = ctk.CTkLabel(
                self.modules_container,
                text=f"Папка '{cfg.GENERATIONS_FOLDER}' пуста.\nСоздайте внутри неё папку (например, 'Plexus') и положите туда .exe файл.",
                font=cfg.FONT_EMPTY_MSG,
                text_color=cfg.COLOR_TEXT_EMPTY,
                justify="center",
            )
            empty_label.pack(pady=130, padx=20)
            return

        for folder_name in sorted(folders):
            btn = ctk.CTkButton(
                self.modules_container,
                text=f"⚡  {folder_name}",
                height=cfg.MODULE_CARD_HEIGHT,
                font=cfg.FONT_MODULE_CARD,
                anchor="w",
                fg_color=cfg.COLOR_ACCENT_BG,
                hover_color=cfg.COLOR_ACCENT_HOVER,
                command=lambda name=folder_name: self.launch_generator(name),
            )
            btn.pack(fill="x", padx=15, pady=8)

    def find_executable(self, module_path: str, module_name: str) -> str | None:
        """Ищет подходящий .exe файл внутри папки генератора."""
        exe_files = [
            f for f in os.listdir(module_path)
            if f.lower().endswith(".exe") and os.path.isfile(os.path.join(module_path, f))
        ]

        if not exe_files:
            return None

        for f in exe_files:
            if os.path.splitext(f)[0].lower() == module_name.lower():
                return os.path.join(module_path, f)

        for priority_name in ("main.exe", "app.exe"):
            for f in exe_files:
                if f.lower() == priority_name:
                    return os.path.join(module_path, f)

        for f in exe_files:
            if "ffmpeg" not in f.lower():
                return os.path.join(module_path, f)

        return os.path.join(module_path, exe_files[0])

    def launch_generator(self, module_name: str):
        """Находит и запускает .exe файл выбранного генератора."""
        module_path = os.path.join(self.generations_dir, module_name)
        exe_path = self.find_executable(module_path, module_name)

        if not exe_path:
            self.status_label.configure(
                text=f"Ошибка: в папке '{module_name}' не найден .exe файл!",
                text_color=cfg.COLOR_STATUS_ERROR,
            )
            return

        try:
            subprocess.Popen([exe_path], cwd=module_path)
            self.status_label.configure(
                text=f"Запущен: {os.path.basename(exe_path)}",
                text_color=cfg.COLOR_STATUS_SUCCESS,
            )
        except Exception as e:
            self.status_label.configure(
                text=f"Не удалось запустить {module_name}: {e}",
                text_color=cfg.COLOR_STATUS_ERROR,
            )
            
    def show_welcome_screen(self):
        """Показать главный экран и перезапустить анимации."""
        self.select_frame.place_forget()
        self.welcome_frame.place(x=0, y=0, relwidth=1, relheight=1)

        if not self.is_animating:
            self.is_animating = True
            self.animate_polygons()

        if self.typing_job is not None:
            self.after_cancel(self.typing_job)
        self.animate_welcome_text(0)

    def show_select_screen(self):
        """Скрыть главный экран и показать выбор генератора."""
        self.is_animating = False
        self.welcome_frame.place_forget()
        self.refresh_modules_list()
        self.select_frame.place(x=0, y=0, relwidth=1, relheight=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()

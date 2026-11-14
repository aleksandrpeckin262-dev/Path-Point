import os
import sys
import subprocess
import tkinter as tk
import customtkinter as ctk

# Установка темы оформления
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


def get_base_dir() -> str:
    """Возвращает путь к папке, где лежит hub.py или скомпилированный hub.exe."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки главного окна
        self.title("Path-Point-v2")
        self.geometry("900x700")
        self.resizable(False, False)

        # Путь к папке generations рядом с hub.exe
        self.generations_dir = os.path.join(get_base_dir(), "generations")
        os.makedirs(self.generations_dir, exist_ok=True)

        # Создаём контейнеры для экранов
        self.welcome_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.select_frame = ctk.CTkFrame(self, fg_color="transparent")

        # Инициализируем наполнение экранов
        self.setup_welcome_screen()
        self.setup_select_screen()

        # Показываем стартовый экран
        self.show_welcome_screen()

    def draw_decorations(self, parent_frame):
        """Отрисовка абсолютно гладких и симметричных дуг без наложения рамок."""
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTk"]["fg_color"])

        canvas = tk.Canvas(
            parent_frame,
            width=900,
            height=700,
            bg=bg_color,
            highlightthickness=0,
            bd=0,
        )
        canvas.place(x=0, y=0)

        radii = [80, 150, 220]

        for r in radii:
            # Левый нижний угол
            canvas.create_oval(
                0 - r, 700 - r, 0 + r, 700 + r,
                outline="#1F2833",
                width=16,
            )
            # Правый нижний угол
            canvas.create_oval(
                900 - r, 700 - r, 900 + r, 700 + r,
                outline="#1F2833",
                width=16,
            )

    def setup_welcome_screen(self):
        """Наполнение стартового экрана."""
        self.draw_decorations(self.welcome_frame)

        label = ctk.CTkLabel(
            self.welcome_frame,
            text="Welcome to Hub",
            font=("Arial", 50, "bold"),
            text_color="#5A5F69",
        )
        label.place(relx=0.5, y=80, anchor="center")

        buttons_box = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        buttons_box.place(relx=0.5, y=220, anchor="center")

        btn_generate = ctk.CTkButton(
            buttons_box,
            text="Start generation",
            width=220,
            height=44,
            font=("Arial", 16, "bold"),
            command=self.show_select_screen,
        )
        btn_generate.pack(pady=8)

        btn_exit = ctk.CTkButton(
            buttons_box,
            text="Exit",
            width=220,
            height=44,
            font=("Arial", 16),
            fg_color="#2B303A",
            hover_color="#3B4252",
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
            font=("Arial", 36, "bold"),
            text_color="#8F96A3",
        )
        title.pack(pady=(0, 8))

        subtitle = ctk.CTkLabel(
            container,
            text="Choose an effect module from /generations folder",
            font=("Arial", 14),
            text_color="#5A5F69",
        )
        subtitle.pack(pady=(0, 15))

        # Статусная строка для уведомлений (запущено / ошибка)
        self.status_label = ctk.CTkLabel(
            container,
            text="",
            font=("Arial", 13, "bold"),
            text_color="#4DA8DA",
        )
        self.status_label.pack(pady=(0, 10))

        # Скроллируемая область для карточек генераторов
        self.modules_container = ctk.CTkScrollableFrame(
            container,
            width=550,
            height=360,
            fg_color="#16191F",
            corner_radius=12,
        )
        self.modules_container.pack(pady=5)

        # Кнопка возврата назад
        btn_back = ctk.CTkButton(
            container,
            text="← Back",
            width=160,
            height=38,
            font=("Arial", 15),
            fg_color="#2B303A",
            hover_color="#3B4252",
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
                text="Папка 'generations' пуста.\nСоздайте внутри неё папку (например, 'Plexus') и положите туда .exe файл.",
                font=("Arial", 15),
                text_color="#6C7380",
                justify="center",
            )
            empty_label.pack(pady=130, padx=20)
            return

        for folder_name in sorted(folders):
            btn = ctk.CTkButton(
                self.modules_container,
                text=f"⚡  {folder_name}",
                height=55,
                font=("Arial", 18, "bold"),
                anchor="w",
                fg_color="#1F2833",
                hover_color="#2C3A4A",
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

        # Приоритет 1: файл совпадает с именем папки (например, Plexus.exe)
        for f in exe_files:
            if os.path.splitext(f)[0].lower() == module_name.lower():
                return os.path.join(module_path, f)

        # Приоритет 2: файл называется main.exe или app.exe
        for priority_name in ("main.exe", "app.exe"):
            for f in exe_files:
                if f.lower() == priority_name:
                    return os.path.join(module_path, f)

        # Иначе возвращаем первый найденный .exe (игнорируя ffmpeg.exe, если он там лежит)
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
                text_color="#E06C75",
            )
            return

        try:
            # Запускаем независимый процесс в его родной рабочей директории (cwd)
            subprocess.Popen([exe_path], cwd=module_path)
            self.status_label.configure(
                text=f"Запущен: {os.path.basename(exe_path)}",
                text_color="#98C379",
            )
        except Exception as e:
            self.status_label.configure(
                text=f"Не удалось запустить {module_name}: {e}",
                text_color="#E06C75",
            )

    def show_welcome_screen(self):
        """Показать главный экран."""
        self.select_frame.place_forget()
        self.welcome_frame.place(x=0, y=0, relwidth=1, relheight=1)

    def show_select_screen(self):
        """Скрыть главный экран и показать выбор генератора."""
        self.welcome_frame.place_forget()
        self.refresh_modules_list()
        self.select_frame.place(x=0, y=0, relwidth=1, relheight=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
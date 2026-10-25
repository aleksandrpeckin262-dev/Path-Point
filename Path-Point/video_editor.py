import cv2
import os
import app_config

fps = app_config.video_FPS
max_frame = app_config.max_frames

image_folder = "images"

frame_number = 1

video_name = "video_1.mp4"

def create_video_from_images(image_folder: str, output_path: str, fps) -> bool:
    """
    Склеивает изображения из папки в один видеофайл.
    
    :param image_folder: Путь к папке с фотографиями.
    :param output_path: Путь для сохранения готового видео (например, 'res.mp4').
    :param fps: Количество кадров в секунду.
    :return: True, если видео успешно создано, иначе False.
    """
    # Поддерживаемые форматы
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    # Получаем и сортируем список картинок
    images = [img for img in os.listdir(image_folder) if img.lower().endswith(valid_extensions)]
    images.sort()

    if not images:
        print(f"Ошибка: В папке {image_folder} не найдено подходящих изображений.")
        return False

    # Берем размер первой картинки за эталон
    first_image_path = os.path.join(image_folder, images[0])
    first_frame = cv2.imread(first_image_path)
    
    if first_frame is None:
        print(f"Ошибка: Не удалось прочитать файл {first_image_path}")
        return False
        
    height, width, _ = first_frame.shape

    # Настройка кодека и запись видео
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        
        if frame is None:
            continue  # Пропускаем поврежденные кадры
            
        # Автоматический ресайз под размер эталона, если фото разные
        if frame.shape[1] != width or frame.shape[0] != height:
            frame = cv2.resize(frame, (width, height))
            
        video.write(frame)

    video.release()
    cv2.destroyAllWindows()
    return True

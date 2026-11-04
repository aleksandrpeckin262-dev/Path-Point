import cv2
import os
import app_config

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

    # Пробуем кодек H.264 (avc1) - лучшее качество
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Если avc1 не открылся, пробуем mp4v
    if not video.isOpened():
        print("avc1 не поддерживается, пробую mp4v...")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Если mp4v не открылся, пробуем XVID
    if not video.isOpened():
        print("mp4v не поддерживается, пробую XVID...")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))


    if not video.isOpened():
        print("Критическая ошибка: Не удалось инициализировать VideoWriter")
        return False

    # Устанавливаем максимальное качество
    video.set(cv2.VIDEOWRITER_PROP_QUALITY, 100)
    
    print(f"Собираю видео: {len(images)} кадров, {width}x{height}, {fps} FPS, качество 100%")

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
    print(f"Видео успешно сохранено: {output_path}")
    return True
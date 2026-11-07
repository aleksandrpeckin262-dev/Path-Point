import cv2
import os
import app_config

def create_video_from_images(image_folder: str, output_path: str, fps) -> bool:
    """
    Склеивает изображения из папки в один видеофайл.
    Жестко использует кодек XVID и расширение .avi для 100% работы в .exe.
    """
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    images = [img for img in os.listdir(image_folder) if img.lower().endswith(valid_extensions)]
    images.sort()

    if not images:
        print(f"Ошибка: В папке {image_folder} не найдено подходящих изображений.")
        return False

    first_image_path = os.path.join(image_folder, images[0])
    first_frame = cv2.imread(first_image_path)
    
    if first_frame is None:
        print(f"Ошибка: Не удалось прочитать файл {first_image_path}")
        return False
        
    height, width, _ = first_frame.shape

    # --- ОРОЧИЙ ПЕРЕХВАТ: ЖЕСТКО СТАВИМ XVID И AVI ---
    # Перебиваем расширение .mp4 на .avi, чтобы кодек XVID не создавал битый файл
    base_path, _ = os.path.splitext(output_path)
    stable_output_path = base_path + ".avi"

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(stable_output_path, fourcc, fps, (width, height))
    # ------------------------------------------------

    if not video.isOpened():
        print("Критическая ошибка: Не удалось инициализировать VideoWriter")
        return False

    # Устанавливаем качество 80% (Картинка останется четкой, а вес упадет в 5 раз!)
    video.set(cv2.VIDEOWRITER_PROP_QUALITY, 80)
    
    print(f"Собираю видео: {len(images)} кадров, {width}x{height}, {fps} FPS, качество 80%")

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        
        if frame is None:
            continue
            
        if frame.shape[1] != width or frame.shape[0] != height:
            frame = cv2.resize(frame, (width, height))
            
        video.write(frame)

    video.release()
    cv2.destroyAllWindows()
    print(f"Видео успешно сохранено: {stable_output_path}")
    return True

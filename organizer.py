import os
import sys


CATEGORIES = {
    "Documents": {".txt", ".pdf", ".docx", ".md"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp"},
    "Audio": {".mp3", ".wav", ".flac", ".aac"},
    "Video": {".mp4", ".avi", ".mkv", ".mov"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}


def get_category(filename):
    _, extension = os.path.splitext(filename)
    extension = extension.lower()

    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category

    return "Other"


def get_unique_path(directory, filename):
    name, extension = os.path.splitext(filename)
    target_path = os.path.join(directory, filename)

    if not os.path.exists(target_path):
        return target_path

    counter = 1

    while True:
        new_name = f"{name}_{counter}{extension}"
        target_path = os.path.join(directory, new_name)

        if not os.path.exists(target_path):
            return target_path

        counter += 1


def main():
    if len(sys.argv) > 2:
        print("Ошибка: программа принимает только один аргумент — путь к директории.")
        sys.exit(1)

    if len(sys.argv) == 2:
        target_dir = os.path.abspath(sys.argv[1])
    else:
        target_dir = os.getcwd()

    print(f"Директория: {target_dir}")

    if not os.path.exists(target_dir):
        print("Ошибка: указанная директория не существует.")
        sys.exit(1)

    if not os.path.isdir(target_dir):
        print("Ошибка: указанный путь не является директорией.")
        sys.exit(1)

    script_name = os.path.basename(sys.argv[0])
    ignored_files = {script_name, "organizer.py"}

    try:
        entries = os.listdir(target_dir)
    except OSError as error:
        print(f"Ошибка при чтении директории: {error}")
        sys.exit(1)

    files = []

    for entry in entries:
        full_path = os.path.join(target_dir, entry)

        if not os.path.isfile(full_path):
            continue

        if entry in ignored_files:
            continue

        files.append(entry)

    if not files:
        print("Директория пуста: файлов для обработки нет.")
        sys.exit(0)

    moved = {
        "Documents": 0,
        "Images": 0,
        "Audio": 0,
        "Video": 0,
        "Archives": 0,
        "Other": 0,
    }

    failed = 0
    processed = 0

    for filename in files:
        processed += 1

        category = get_category(filename)
        category_dir = os.path.join(target_dir, category)

        try:
            os.makedirs(category_dir, exist_ok=True)
        except OSError as error:
            print(f"Ошибка создания каталога {category}: {error}")
            failed += 1
            continue

        source_path = os.path.join(target_dir, filename)
        target_path = get_unique_path(category_dir, filename)

        try:
            os.rename(source_path, target_path)

            print(
                f"{filename} -> "
                f"{category}\\{os.path.basename(target_path)}"
            )

            moved[category] += 1

        except OSError as error:
            print(f"Не удалось переместить {filename}: {error}")
            failed += 1

    print()
    print("=== Отчёт ===")
    print(f"Documents: {moved['Documents']}")
    print(f"Images: {moved['Images']}")
    print(f"Audio: {moved['Audio']}")
    print(f"Video: {moved['Video']}")
    print(f"Archives: {moved['Archives']}")
    print(f"Other: {moved['Other']}")
    print(f"Не удалось переместить: {failed}")
    print(f"Всего обработано файлов: {processed}")


if __name__ == "__main__":
    main()

import argparse
import os
from pathlib import Path


def get_extension(file):
    extension = file.suffix.replace(".", "").upper()

    if not extension:
        return "NullExt"

    return extension


def get_unique_path(directory, filename):
    name = Path(filename).stem
    extension = Path(filename).suffix

    target = directory / filename

    if not target.exists():
        return target

    counter = 1

    while True:
        new_name = f"{name}_{counter}{extension}"
        target = directory / new_name

        if not target.exists():
            return target

        counter += 1


def main():
    parser = argparse.ArgumentParser(description="TrashCleaner")

    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Path to directory"
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursive directory scan"
    )

    args = parser.parse_args()

    if args.path:
        target_dir = Path(args.path).resolve()
    else:
        target_dir = Path(os.getcwd()).resolve()

    print(f"Target directory: {target_dir}")
    print(f"Recursive mode: {args.recursive}")

    if not target_dir.exists():
        print("ERR: directory does not exist")
        return 1

    if not target_dir.is_dir():
        print("ERR: path is not a directory")
        return 1

    script_name = Path(__file__).name
    temp_dir = target_dir / f".TrashCleaner_tmp_{os.getpid()}"

    try:
        entries = (
            target_dir.rglob("*")
            if args.recursive
            else target_dir.glob("*")
        )

        all_files = []

        for item in entries:
            if not item.is_file():
                continue

            if item.name == script_name:
                continue

            relative_parts = item.relative_to(target_dir).parts

            # Не даём recursive mode заходить во временные каталоги.
            if (
                relative_parts
                and relative_parts[0].startswith(".TrashCleaner_tmp_")
            ):
                continue

            extension = get_extension(item)
            destination_dir = target_dir / extension

            # Уже отсортированные файлы в корневых каталогах
            # расширений не трогаем при recursive запуске.
            if args.recursive and destination_dir in item.parents:
                continue

            all_files.append(item)

    except OSError as error:
        print(f"ERR scanning directory: {error}")
        return 1

    if not all_files:
        print("No files to process")
        return 0

    print(f"Files found: {len(all_files)}")

    # Сначала переносим всё найденное во временное дерево.
    # После этого исходное дерево больше не меняется во время сортировки.
    staged_files = []
    failed = 0

    for file in all_files:
        relative_path = file.relative_to(target_dir)
        stage_path = temp_dir / relative_path

        try:
            stage_path.parent.mkdir(parents=True, exist_ok=True)
            file.rename(stage_path)
            staged_files.append((stage_path, file.name))

        except OSError as error:
            failed += 1
            print(f"ERR staging {file}: {error}")

    moved = 0
    conflicts = 0

    for stage_path, original_name in staged_files:
        extension = get_extension(stage_path)
        destination_dir = target_dir / extension

        try:
            destination_dir.mkdir(parents=True, exist_ok=True)

            target_path = get_unique_path(
                destination_dir,
                original_name
            )

            if target_path.name != original_name:
                conflicts += 1

            stage_path.rename(target_path)

            print(
                f"move: {original_name} -> "
                f"{extension}/{target_path.name}"
            )

            moved += 1

        except OSError as error:
            failed += 1
            print(f"ERR moving {original_name}: {error}")

    # При полном успехе удаляем пустое временное дерево.
    # При ошибках оставляем его как безопасное место для недоведённых файлов.
    if failed == 0 and temp_dir.exists():
        try:
            for item in sorted(
                temp_dir.rglob("*"),
                key=lambda path: len(path.parts),
                reverse=True
            ):
                if item.is_dir():
                    item.rmdir()

            temp_dir.rmdir()

        except OSError as error:
            print(f"ERR cleaning temp directory: {error}")

    print()
    print("=== Report ===")
    print(f"Found:     {len(all_files)}")
    print(f"Moved:     {moved}")
    print(f"Conflicts: {conflicts}")
    print(f"Failed:    {failed}")

    if failed:
        print(f"Temp files remain in: {temp_dir}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

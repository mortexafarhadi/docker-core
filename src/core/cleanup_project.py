import os
import shutil

from _0_utils.functions.string_function import red_text, green_text, PrintColored


def clean_project(project_path="."):
    # لیست پوشه‌هایی که نباید وارد آن‌ها شویم
    ignored_dirs = {
        "zmedias",
        "zstatic",
        "ztemplates",
        "zzrequirements",
        "_2_locales",
        "_0_deploy",
        "_1_data",
        ".venv",
        ".zzvenv",
        "venv",
        "zzvenv",
        ".git",
        ".vscode",
        ".ai",
        ".idea",
    }
    deleted_cache = 0
    deleted_migration = 0
    for root, dirs, files in os.walk(project_path, topdown=True):
        # 1. فیلتر کردن پوشه‌های نادیده گرفته شده (مانند venv)
        # تغییر dirs در جا (in-place) باعث می‌شود os.walk وارد این پوشه‌ها نشود
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        # 2. حذف پوشه‌های __pycache__ در کل پروژه (بجز مسیرهای نادیده گرفته شده)
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                print(f"[REMOVED CACHE]  {pycache_path}")
                # حذف از لیست dirs تا os.walk سعی نکند وارد آن شود
                dirs.remove("__pycache__")
                deleted_cache += 1
            except Exception as e:
                print(f"[ERROR CACHE]    Could not delete {pycache_path}: {e}")

        # 3. پاکسازی فایل‌های migrations
        if os.path.basename(root) == "migrations":
            print(f"[CLEANING MIGRATIONS] {root}")
            for file in files:
                if file != "__init__.py":
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"  - Deleted: {file}")
                        deleted_migration += 1
                    except Exception as e:
                        print(f"  - Error deleting {file}: {e}")

    pc = PrintColored()
    pc.add_red("\n\nRemoved ")
    pc.add_green(deleted_cache)
    pc.add_red(" Cached Folder")
    pc.print()
    pc = PrintColored()
    pc.add_red("Removed ")
    pc.add_green(deleted_migration)
    pc.add_red(" Migrations File")
    pc.print()


if __name__ == "__main__":
    pc = PrintColored()
    pc.add_blue(
        "Are you sure you want to delete Migrations and Caches in the entire project "
    )
    pc.add_magenta("(except venv)")
    pc.add_blue("? (")
    pc.add_red("y")
    pc.add_blue("/")
    pc.add_yellow("n")
    pc.add_blue("):")
    pc.print()

    confirm = input()
    if confirm.lower() == "y":
        clean_project()
        print(green_text("\nThe Operation Completed Successfully."))
    else:
        print(red_text("\nOperation Canceled."))

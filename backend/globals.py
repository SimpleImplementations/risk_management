import os


DEFAULT_XLSX_PATH = os.path.join("data", "returns.xlsx")
UPLOADED_XLSX_PATH = os.path.join("data", "uploaded.xlsx")


def remove_old_files():
    if os.path.exists(UPLOADED_XLSX_PATH):
        os.remove(UPLOADED_XLSX_PATH)

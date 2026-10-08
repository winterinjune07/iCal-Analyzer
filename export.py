import csv, os, shutil, subprocess, tempfile
from pathlib import Path
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

# Columns C..F (indices 2-5), every row starting at row 1
rows = []
with open(os.environ["OUTPUT_CSV"], newline="", encoding="utf-8-sig") as f:
    for r in csv.reader(f):
        r = r[2:6]
        rows.append(r + [""] * (4 - len(r)))

dest_type = os.environ["DEST_TYPE"].lower()
dest      = os.environ["DEST_SPREADSHEET"]
cell      = os.environ["DEST_CELL"].upper()
sheet     = os.environ.get("DEST_SHEET") or None


def to_val(v):
    if v == "":
        return None
    for cast in (int, float):
        try:
            return cast(v)
        except ValueError:
            pass
    return v


def write_gsheets():
    import gspread
    gc = gspread.service_account(filename=os.environ["GOOGLE_CREDENTIALS"])
    sh = gc.open_by_url(dest) if dest.startswith("http") else gc.open_by_key(dest)
    ws = sh.worksheet(sheet) if sheet else sh.sheet1
    ws.update(rows, cell, value_input_option="USER_ENTERED")


def write_xlsx(path):
    import openpyxl
    wb = openpyxl.load_workbook(path)
    ws = wb[sheet] if sheet else wb.active
    col_letter, row0 = coordinate_from_string(cell)
    col0 = column_index_from_string(col_letter)
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            ws.cell(row=row0 + i, column=col0 + j, value=to_val(v))
    wb.save(path)


def soffice_convert(src, fmt, outdir):
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        raise SystemExit("LibreOffice (soffice) is required for ods mode but was not found")
    subprocess.run([exe, "--headless", "--convert-to", fmt, "--outdir", str(outdir), str(src)],
                   check=True, capture_output=True)
    return Path(outdir) / (Path(src).stem + "." + fmt)


def write_ods(path):
    # No lossless pure-Python ODS writer exists: ods -> xlsx -> edit -> ods via LibreOffice
    with tempfile.TemporaryDirectory() as tmp:
        a, b = Path(tmp, "a"), Path(tmp, "b")
        a.mkdir(); b.mkdir()
        xlsx = soffice_convert(path, "xlsx", a)
        write_xlsx(xlsx)
        ods = soffice_convert(xlsx, "ods", b)
        shutil.copy2(ods, path)


if dest_type == "gsheets":
    write_gsheets()
elif dest_type in ("xlsx", "ods"):
    shutil.copy2(dest, dest + ".bak")   # backup before overwriting
    (write_xlsx if dest_type == "xlsx" else write_ods)(dest)
else:
    raise SystemExit(f"Unknown DEST_TYPE: {os.environ['DEST_TYPE']}")

print(f"Exported {len(rows)} rows to {dest_type} at {cell}")

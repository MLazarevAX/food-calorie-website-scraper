import re, csv
import json
from typing import Iterable


def writefile(file_name: str, page_html: str, file_extension: str, dop_name=''):
    with open(f"data/{dop_name}{file_name}{file_extension}", "w", encoding='utf-8') as file:
        return file.write(page_html)


def sub_items_in_string(string: str, character: str = "_"):
    res = re.sub(r'[^a-zA-Zа-яёА-ЯЁ0-9_]', character, string)
    return re.sub(r'_{2,10}', "_", res)


def write_json(file_full_path, mode, write_info, indent: int = 4,
               ensure_ascii: bool = False, encoding: str = "utf-8-sig"):
    with open(file_full_path, mode, encoding=encoding) as file:
        json.dump(write_info, file, indent=indent, ensure_ascii=ensure_ascii)


def read_json(file_full_path: str):
    with open(file_full_path, encoding="utf-8-sig") as file:
        a = json.load(file)
    return a


def write_to_csv(file_full_path, ittereble: Iterable,
                 mode: str = "w", encoding: str = "utf-8-sig"):
    with open(file_full_path, mode, encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(ittereble)


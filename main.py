from tkinter import *
from tkinter import ttk, scrolledtext
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter import messagebox
import psutil
from os import remove
import json
import xml.etree.ElementTree as ET
import os
import zipfile

root = Tk()

root.title("Практика 2. Сидоров М.М, БСБО-02-20")
root.resizable(False, False)

WIDTH, HEIGHT = 900, 700

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (WIDTH / 2)
y = (screen_height / 2) - (HEIGHT / 2)

root.geometry(F"{WIDTH}x{HEIGHT}+{int(x)}+{int(y) - 40}")

tab_panel = ttk.Notebook(root, padding=5)

tab1 = Frame(tab_panel)
tab2 = Frame(tab_panel)
tab3 = Frame(tab_panel)
tab4 = Frame(tab_panel)
tab5 = Frame(tab_panel)

tab_panel.add(tab1, text="Информация о дисках")
tab_panel.add(tab2, text="Работа с файлами")
tab_panel.add(tab3, text="Работа с JSON")
tab_panel.add(tab4, text="Работа с XML")
tab_panel.add(tab5, text="Работа с ZIP")

tab_panel.pack(expand=True, fill=BOTH)

info_view = scrolledtext.ScrolledText(tab1, font="Times", height=33, width=107, padx=3, pady=1)
info_view.place(x=3, y=10)


def show_drive_info():
    def write(text: str) -> None:
        info_view["state"] = "normal"
        info_view.delete(1.0, END)
        info_view.insert(1.0, text)

    def get_drive_info(drive):
        drive_info = {}
        drive_info["Название"] = drive.device
        drive_info["Тип"] = drive.fstype

        if psutil.disk_usage(drive.mountpoint).total:
            drive_info["Объём диска"] = psutil.disk_usage(drive.mountpoint).total
            drive_info["Свободное пространство"] = psutil.disk_usage(drive.mountpoint).free
            drive_info["Метка"] = drive.mountpoint
        return drive_info

    drives = psutil.disk_partitions()
    drive_str = ""
    for drive in drives:
        drive_info = get_drive_info(drive)
        drive_str += f"\n\nНазвание: {drive_info['Название']}\nТип: {drive_info['Тип']}"

        if "Объём диска" in drive_info:
            drive_str += f'\nОбъём диска: {drive_info["Объём диска"]}\nСвободное пространство: {drive_info["Свободное пространство"]}\nМетка: {drive_info["Метка"]}'

    write(drive_str.strip())
    info_view["state"] = "disabled"


btn_color = "#CBCBCB"
btn_text_color = fg = "#000000"
btn_font = "Arial 13 bold"

refresh_btn = Button(tab1, text="Обновить данные", width=25, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                     command=show_drive_info, bd=0, )
refresh_btn.place(x=333, y=308)

text_view = scrolledtext.ScrolledText(tab2, padx=5, pady=3, font="Times 11", height=32, width=120, state="disabled")
text_view.place(x=3, y=28)

current_file = ""

label = Label(tab2, font="Times 11", text="Файл не выбран")
label.place(x=0, y=3)


def open_file():
    global current_file
    file = askopenfilename(title="Открытие файла", filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
    if file == "": return
    text_view["state"] = "normal"
    save_text_btn["state"] = "normal"
    current_file = file
    label["text"] = os.path.basename(file)
    text_view.delete(1.0, END)
    with open(file, "r", encoding="utf-8") as f:
        text_view.insert(1.0, f.read())


def save_file():
    if current_file == "": return
    text_file = text_view.get(1.0, END).rstrip()
    with open(current_file, "w", encoding="utf-8") as f:
        f.write(text_file)


def delete_text():
    file = askopenfilename(title="Удаление файла", filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
    if file == "": return

    choice = messagebox.askyesno("Удаление",
                                 f"Вы действительно хотите удалить файл {os.path.basename(file)}? Отменить данное действие будет невозможно.")
    if not choice: return

    if file == current_file:
        label["text"] += " (удалён)"
        save_text_btn["state"] = "disabled"
        text_view["state"] = "disabled"
    remove(file)


def create_file():
    path = asksaveasfilename(title="Создание файла", filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
                             defaultextension=".txt")
    if path == "": return
    with open(path, "w", encoding="utf-8"): pass


save_text_btn = Button(tab2, text="Сохранить изменения", width=20, height=2, bg=btn_color, font=btn_font,
                       fg=btn_text_color, command=save_file, bd=0, state="disabled")
create_text_btn = Button(tab2, text="Создать файл", width=15, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                         command=create_file, bd=0)
open_text_btn = Button(tab2, text="Открыть файл", width=15, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                       command=open_file, bd=0)
delete_text_btn = Button(tab2, text="Удалить файл", width=15, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                         command=delete_text, bd=0)

save_text_btn.place(x=3, y=616)
create_text_btn.place(x=358, y=616)
open_text_btn.place(x=532, y=616)
delete_text_btn.place(x=706, y=616)

fio_lbl = Label(tab3, text="ФИО", font="Times 11")
number_lbl = Label(tab3, text="Номер телефона", font="Times 11")
address_lbl = Label(tab3, text="Адрес", font="Times 11")

fio_lbl.place(x=0, y=3)
number_lbl.place(x=300, y=3)
address_lbl.place(x=460, y=3)

fio_entr = Entry(tab3, font="Times 11", bd=2)
number_entr = Entry(tab3, font="Times 11", bd=2)
address_entr = Entry(tab3, font="Times 11", bd=2)

fio_entr.place(x=4, y=25, width=285)
number_entr.place(x=300, y=25, width=150)
address_entr.place(x=460, y=25, width=285)

json_view = scrolledtext.ScrolledText(tab3, padx=5, pady=3, font="Calibri 11", height=35, width=120, state="disabled")
json_view.place(x=3, y=130)

json_list = []


def get_formatted_data(data_list: list) -> str:
    result = ""
    for d in data_list:
        result += f"\nФИО: {d['name']}\nТелефон: {d['number']}\nАдрес: {d['address']}\n"
    return result.strip()


def add_json():
    global json_list
    json_view["state"] = "normal"
    json_view.delete(1.0, END)
    fio, number, address = fio_entr.get(), number_entr.get(), address_entr.get()

    if fio.strip() == "": fio = "None"
    if number.strip() == "": number = "None"
    if address.strip() == "": address = "None"

    json_list.append({"name": fio, "number": number, "address": address})
    json_view.insert(1.0, get_formatted_data(json_list))

    save_json_btn["state"] = "normal"
    json_view["state"] = "disabled"


def read_json():
    global json_list
    file = askopenfilename(title="Открытие файла", filetypes=[("Файлы JSON", "*.json"), ("Все файлы", "*.*")])
    if file == "": return
    result = ""
    with open(file, "r", encoding="utf-8") as f:
        json_data = json.loads(f.read())

    json_list = json_data["people"]
    for person in json_data["people"]:
        result += f"\nФИО: {person['name']}\nТелефон: {person['number']}\nАдрес: {person['address']}\n"

    json_view["state"] = "normal"
    json_view.delete(1.0, END)
    json_view.insert(1.0, result.strip())
    save_json_btn["state"] = "normal"
    json_view["state"] = "disabled"


def save_json():
    path = asksaveasfilename(title="Сохранение файла", filetypes=[("Файлы JSON", "*.json"), ("Все файлы", "*.*")],
                             defaultextension=".json")
    if path == "": return
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"people": json_list}, f, indent=3, ensure_ascii=False)


def delete_file():
    file = askopenfilename(title="Удаление файла", filetypes=[("Все файлы", "*.*")])
    if file == "": return

    choice = messagebox.askyesno("Удаление",
                                 f"Вы действительно хотите удалить файл {os.path.basename(file)}? Отменить данное действие будет невозможно.")
    if not choice: return

    remove(file)


add_json_btn = Button(tab3, text="Добавить запись", width=20, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                      command=add_json, bd=0)
read_json_btn = Button(tab3, text="Прочитать файл", width=20, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                       command=read_json, bd=0)
save_json_btn = Button(tab3, text="Сохранить файл", width=20, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                       command=save_json, bd=0, state="disabled")
delete_json_btn = Button(tab3, text="Удалить файл", width=20, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                         command=delete_file, bd=0)

add_json_btn.place(x=4, y=55)
read_json_btn.place(x=300, y=55)
save_json_btn.place(x=505, y=55)
delete_json_btn.place(x=700, y=55)

fio_lbl_2 = Label(tab4, text="ФИО", font="Calibri 11")
number_lbl_2 = Label(tab4, text="Номер телефона", font="Calibri 11")
address_lbl_2 = Label(tab4, text="Адрес", font="Calibri 11")

fio_lbl_2.place(x=0, y=3)
number_lbl_2.place(x=300, y=3)
address_lbl_2.place(x=460, y=3)

fio_entr_2 = Entry(tab4, font="Calibri 11", bd=2)
number_entr_2 = Entry(tab4, font="Calibri 11", bd=2)
address_entr_2 = Entry(tab4, font="Calibri 11", bd=2)

fio_entr_2.place(x=4, y=25, width=285)
number_entr_2.place(x=300, y=25, width=150)
address_entr_2.place(x=460, y=25, width=285)

xml_view = scrolledtext.ScrolledText(tab4, padx=5, pady=3, font="Consolas 11", height=26, width=107, state="disabled")
xml_view.place(x=3, y=130)

people_data = []


def add_xml():
    fio, number, address = fio_entr_2.get(), number_entr_2.get(), address_entr_2.get()

    if fio.strip() == "": fio = "None"
    if number.strip() == "": number = "None"
    if address.strip() == "": address = "None"

    people_data.append({"name": fio, "number": number, "address": address})

    xml_view["state"] = "normal"
    xml_view.insert(END, f"ФИО: {fio}\nТелефон: {number}\nАдрес: {address}\n\n")
    save_xml_btn["state"] = "normal"
    xml_view["state"] = "disabled"


def read_xml():
    file = askopenfilename(title="Открытие файла", filetypes=[("Файлы XML", "*.xml"), ("Все файлы", "*.*")])
    if file == "": return

    tree = ET.parse(file).getroot()

    xml_view["state"] = "normal"

    xml_view.delete(1.0, END)
    people_data.clear()
    for child in tree:
        xml_view.insert(END, f"ФИО: {child[0].text}\nТелефон: {child[1].text}\nАдрес: {child[2].text}\n\n")
        people_data.append({"name": child[0].text, "number": child[1].text, "address": child[2].text})

    xml_view["state"] = "disabled"


def save_xml():
    path = asksaveasfilename(title="Сохранение файла", filetypes=[("Файлы XML", "*.xml"), ("Все файлы", "*.*")],
                             defaultextension=".xml")
    if path == "": return

    xml_doc = ET.Element("people")

    for pers in people_data:
        person = ET.SubElement(xml_doc, "person")
        ET.SubElement(person, "name").text = pers['name']
        ET.SubElement(person, "number").text = pers['number']
        ET.SubElement(person, "address").text = pers['address']

    tree = ET.ElementTree(xml_doc)
    ET.indent(tree, space="\t")
    tree.write(path, encoding="UTF-8", xml_declaration=True)


add_xml_btn = Button(tab4, text="Добавить запись", width=20, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                     command=add_xml,
                     bd=0)
read_xml_btn = Button(tab4, text="Прочитать файл", width=20, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                      command=read_xml,
                      bd=0)
save_xml_btn = Button(tab4, text="Сохранить файл", width=20, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                      command=save_xml,
                      bd=0, state="disabled")
delete_xml_btn = Button(tab4, text="Удалить файл", width=20, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                        command=delete_file, bd=0)

add_xml_btn.place(x=4, y=55)
read_xml_btn.place(x=300, y=55)
save_xml_btn.place(x=505, y=55)
delete_xml_btn.place(x=700, y=55)

zip_view = scrolledtext.ScrolledText(tab5, padx=5, pady=3, font="Times 11", height=33, width=119, state="disabled")
zip_view.place(x=3, y=10)

is_open = False
current_zip = None
added_files = []


def save_zip():
    global added_files
    path = asksaveasfilename(title="Сохранение архива", filetypes=[("Файлы ZIP", "*.zip"), ("Все файлы", "*.*")],
                             defaultextension=".zip")
    if path == "": return

    with zipfile.ZipFile(path, 'w') as zip_file:

        for file_path in added_files:
            file_name = os.path.basename(file_path)
            zip_file.write(file_path, file_name)


def add_zip():
    global added_files
    global is_open
    path = askopenfilename(title="Открытие файла", filetypes=[("Все файлы", "*.*")])
    if path == "": return

    file_name = os.path.basename(path)

    zip_view["state"] = "normal"

    if is_open:
        zip_view.delete(1.0, END)
        is_open = False

    zip_view.insert(END, f"Файл: {file_name}\nРазмер: {os.path.getsize(path) // 8} байт\n\n")
    added_files.append(path)

    extract_zip_btn["state"] = "disabled"
    save_zip_btn["state"] = "normal"
    zip_view["state"] = "disabled"


def extract_zip():
    path = askdirectory(title="Выбор каталога для разархивирования")
    if path == "": return

    with zipfile.ZipFile(current_zip, 'r') as zip_file:
        zip_file.extractall(path)


def open_zip():
    global is_open
    global added_files
    global current_zip
    path = askopenfilename(title="Открытие архива", filetypes=[("Файлы ZIP", "*.zip"), ("Все файлы", "*.*")],
                           defaultextension=".zip")
    if path == "": return

    current_zip = path
    is_open = True
    added_files.clear()

    zip_file = zipfile.ZipFile(path)
    file_count = len(zip_file.namelist())
    archive_size = os.path.getsize(path)

    info_string = "Архив: {}\n".format(os.path.basename(path))
    info_string += "Файлов в архиве: {}\n".format(file_count)
    info_string += "Размер архива: {} байт\n".format(archive_size)
    info_string += "-" * 107

    for file_info in zip_file.infolist():
        info_string += "\nФайл: {}\n".format(file_info.filename)
        info_string += "Размер: {} байт\n".format(file_info.file_size)

    zip_view["state"] = "normal"
    zip_view.delete(1.0, END)
    zip_view.insert(1.0, info_string)
    extract_zip_btn["state"] = "normal"
    save_zip_btn["state"] = "disabled"
    zip_view["state"] = "disabled"


save_zip_btn = Button(tab5, text="Сохранить архив", width=20, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                      command=save_zip, bd=0, state="disabled")
add_zip_btn = Button(tab5, text="Добавить файл\n в архив", width=16, height=2, bg=btn_color, font=btn_font,
                     fg=btn_text_color, command=add_zip, bd=0)
open_zip_btn = Button(tab5, text="Открыть архив", width=19, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                      command=open_zip, bd=0)
delete_zip_btn = Button(tab5, text="Удалить архив", width=19, height=2, bg=btn_color, font=btn_font, fg=btn_text_color,
                        command=delete_file, bd=0)
extract_zip_btn = Button(tab5, text="Разархивировать", width=19, height=2, bg=btn_color, font=btn_font,
                         fg=btn_text_color, command=extract_zip, bd=0, state="disabled")

save_zip_btn.place(x=3, y=616)
add_zip_btn.place(x=222, y=616)
open_zip_btn.place(x=386, y=616)
extract_zip_btn.place(x=550, y=616)
delete_zip_btn.place(x=714, y=616)

if __name__ == "__main__":
    os.system("cls")
    show_drive_info()
    root.mainloop()
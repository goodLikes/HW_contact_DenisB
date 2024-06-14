import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

# Функция для чтения контактов из файла
def read_contacts_from_file(filename):
    contacts = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    contacts.append({"name": parts[0], "surname": parts[1], "phone": parts[2]})
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл {filename} не найден.")
    return contacts

# Функция для записи контактов в файл
def write_contacts_to_file(filename, contacts):
    with open(filename, 'w', encoding='utf-8') as file:
        for contact in contacts:
            file.write(f"{contact['name']},{contact['surname']},{contact['phone']}\n")

# Изначальный список контактов (читаем из файла contacts.txt)
phonebook = read_contacts_from_file("contacts.txt")

# Функция для отображения всех контактов в текстовом поле
def display_contacts():
    text_area.delete(1.0, tk.END)
    for contact in phonebook:
        text_area.insert(tk.END, f"{contact['name']} {contact['surname']}: {contact['phone']}\n")

# Функция для добавления нового контакта
def add_contact(name, surname, phone):
    phonebook.append({"name": name, "surname": surname, "phone": phone})
    display_contacts()
    write_contacts_to_file("contacts.txt", phonebook)  # Сохраняем изменения в файл
    messagebox.showinfo("Информация", f"Контакт {name} {surname} добавлен.")

# Функция для удаления контакта
def delete_contact(name, surname):
    global phonebook
    phonebook = [contact for contact in phonebook if not (contact["name"] == name and contact["surname"] == surname)]
    display_contacts()
    write_contacts_to_file("contacts.txt", phonebook)  # Сохраняем изменения в файл
    messagebox.showinfo("Информация", f"Контакт {name} {surname} удален.")

# Функция для обновления контакта
def update_contact(old_name, old_surname, new_name, new_surname, new_phone):
    for contact in phonebook:
        if contact["name"] == old_name and contact["surname"] == old_surname:
            contact["name"] = new_name
            contact["surname"] = new_surname
            contact["phone"] = new_phone
            display_contacts()
            write_contacts_to_file("contacts.txt", phonebook)  # Сохраняем изменения в файл
            messagebox.showinfo("Информация", f"Контакт {old_name} {old_surname} обновлен.")
            return
    messagebox.showerror("Ошибка", f"Контакт {old_name} {old_surname} не найден.")

# Функция для поиска контактов
def find_contact(name=None, surname=None):
    results = []
    for contact in phonebook:
        if name and contact["name"] == name:
            results.append(contact)
        elif surname and contact["surname"] == surname:
            results.append(contact)
    return results

# Функция для диалога добавления контакта
def add_contact_dialog():
    name = simpledialog.askstring("Введите имя", "Введите имя:")
    surname = simpledialog.askstring("Введите фамилию", "Введите фамилию:")
    phone = simpledialog.askstring("Введите номер телефона", "Введите номер телефона:")
    if name and surname and phone:
        add_contact(name, surname, phone)
    else:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")

# Функция для диалога удаления контакта
def delete_contact_dialog():
    name = simpledialog.askstring("Введите имя", "Введите имя:")
    surname = simpledialog.askstring("Введите фамилию", "Введите фамилию:")
    if name and surname:
        delete_contact(name, surname)
    else:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")

# Функция для диалога обновления контакта
def update_contact_dialog():
    old_name = simpledialog.askstring("Введите текущее имя", "Введите текущее имя:")
    old_surname = simpledialog.askstring("Введите текущую фамилию", "Введите текущую фамилию:")
    new_name = simpledialog.askstring("Введите новое имя", "Введите новое имя:")
    new_surname = simpledialog.askstring("Введите новую фамилию", "Введите новую фамилию:")
    new_phone = simpledialog.askstring("Введите новый номер телефона", "Введите новый номер телефона:")
    if old_name and old_surname and new_name and new_surname and new_phone:
        update_contact(old_name, old_surname, new_name, new_surname, new_phone)
    else:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")

# Функция для диалога поиска контакта
def find_contact_dialog():
    search_name = simpledialog.askstring("Введите имя для поиска", "Введите имя для поиска (оставьте пустым для пропуска):")
    search_surname = simpledialog.askstring("Введите фамилию для поиска", "Введите фамилию для поиска (оставьте пустым для пропуска):")
    results = find_contact(name=search_name or None, surname=search_surname or None)
    if results:
        result_text = "\n".join([f"{contact['name']} {contact['surname']}: {contact['phone']}" for contact in results])
        messagebox.showinfo("Найденные контакты", result_text)
    else:
        messagebox.showinfo("Найденные контакты", "Контакты не найдены.")

#######


# Создание GUI с использованием tkinter
root = tk.Tk()
root.title("1.3 |Телефонный справочник | made Denis B.|")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

text_area = tk.Text(frame, height=15, width=50)
text_area.pack()

display_contacts()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Показать все контакты", command=display_contacts).grid(row=0, column=0, pady=5)
tk.Button(button_frame, text="Добавить контакт", command=add_contact_dialog).grid(row=1, column=0, pady=5)
tk.Button(button_frame, text="Удалить контакт", command=delete_contact_dialog).grid(row=2, column=0, pady=5)
tk.Button(button_frame, text="Изменить контакт", command=update_contact_dialog).grid(row=3, column=0, pady=5)
tk.Button(button_frame, text="Найти контакт", command=find_contact_dialog).grid(row=4, column=0, pady=5)

tk.Button(button_frame, text="Выход", command=root.quit).grid(row=6, column=0, pady=5)

root.mainloop()

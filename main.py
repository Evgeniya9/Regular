from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

def clean_address_book(address_book):

  cleaned_book = []
  seen_entries = set()

  for entry in address_book:
    # Разбиваем запись на поля
    fields = entry.split(',')

    # Обработка ФИО
    name_parts = " ".join(fields[:3]).split(" ")
    if len(name_parts) == 2:
      # Ф + ИО
      fields[0] = name_parts[0]
      fields[1] = name_parts[1]
      fields[2] = ""
    elif len(name_parts) == 3:
      # ФИО
      fields[0] = name_parts[0]
      fields[1] = name_parts[1]
      fields[2] = name_parts[2]

    # Обработка телефона
    phone = fields[5]
    if phone:
      # Приводим телефон к единому формату
      phone = re.sub(r'[^0-9\+ \-\(\)]', '', phone)
      phone = re.sub(r'(\+7) ?(\d{3}) ?(\d{3})-?(\d{2})-?(\d{2})', r'+7(\2)\3-\4-\5', phone)
      # Если есть добавочный номер
      if 'доб.' in phone:
        phone = re.sub(r'(\+7\(\d{3}\)\d{3}-\d{2}-\d{2}) доб\.(\d+)', r'\1 доб.\2', phone)
      fields[5] = phone

    # Объединение дублирующих записей
    key = tuple(fields[:3])  # Используем ФИО для группировки
    if key not in seen_entries:
      cleaned_book.append(fields)
      seen_entries.add(key)

  return cleaned_book

# Пример использования
address_book = [
    "Иванов,Иван Иванович,ООО \"Рога и копыта\",Менеджер,8(903)123-45-67,ivan.ivanov@example.com",
    "Петров,Петр Сергеевич,АО \"Птицефабрика\",Директор,8-916-123-45-67,petr.petrov@example.com",
    "Сидоров,Сидор,АО \"Птицефабрика\",Директор,+79031234567 доб 1234,sid.sid@example.com",
    "Иванов,Иван Иванович,ООО \"Рога и копыта\",Менеджер,+7 916 123 45 67,ivan.ivanov@example.com",  # Дубликат
    "Смирнова,Анна,АО \"Птицефабрика\",Секретарь,+7(999)999-99-99 доб.1111,anna.smirnova@example.com"
]

cleaned_address_book = clean_address_book(address_book)

for entry in cleaned_address_book:
  # TODO 2: сохраните получившиеся данные в другой файл
  # код для записи файла в формате CSV
  with open("phonebook.csv", "w", encoding="utf-8") as f:
      datawriter = csv.writer(f, delimiter=',')
      # Вместо contacts_list подставьте свой список
      datawriter.writerows(contacts_list)
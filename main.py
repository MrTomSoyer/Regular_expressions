import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    #print(contacts_list)


for idx, contact in enumerate(contacts_list):
    if idx == 0:
        continue
    else:
        fio_list = contact[:3]
        fio = ' '.join(fio_list).split()
        for i in range(len(fio)):
            contacts_list[idx][i] = fio[i]


for contact in contacts_list[1:]:
    if not contact[5]:
        continue
    else:
        number = contact[5]
        number_pattern = r'(?:\+7|8)\s*(?:\(?(\d{3})\)?)(?:\s*|-)(\d{3})(?:[\s-]?)(\d{2})(?:[\s-]?)(\d{2})'
        replace_pattern = r'+7(\1)\2-\3-\4'
        contact[5] = re.sub(number_pattern, replace_pattern, number)
        if "доб" in contact[5]:
            number = contact[5]
            add_number_pattern = r'(?:\(?(доб)\.?)\s*(\d+)(?:\)?)'
            replace_pattern = r'\1.\2'
            contact[5] = re.sub(add_number_pattern, replace_pattern, number)


result = []
contacts_dict = {}
for contact in contacts_list[1:]:
    print(contacts_dict)
    key = (contact[0], contact[1])
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        existing = contacts_dict[key]
        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

result.append(contacts_list[0])
result.extend(contacts_dict.values())


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(result)




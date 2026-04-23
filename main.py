import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


for contact in contacts_list:
    fio = " ".join(contact[:3]).split()
    contact[0] = fio[0] if len(fio) > 0 else ""
    contact[1] = fio[1] if len(fio) > 1 else ""
    contact[2] = fio[2] if len(fio) > 2 else ""


for contact in contacts_list[1:]:
    if not contact[5]:
        continue
    number = contact[5]
    main_match = re.search(r'(?:\+7|8)[\s\-()]*((\d[\s\-()]*){10})', number)
    ext_match = re.search(r'доб\.?\s*(\d{4})', number, re.IGNORECASE)
    formatted_number = ''
    if main_match:
        digits = re.sub(r'\D', '', main_match.group(1))
        formatted_number = f'+7({digits[:3]}){digits[3:6]}-{digits[6:8]}-{digits[8:]}'
        if ext_match:
            formatted_number += f' доб.{ext_match.group(1)}'
    contact[5] = formatted_number


result = [contacts_list[0]]

contacts_dict = {}
for contact in contacts_list[1:]:
    key = (contact[0], contact[1])
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        existing = contacts_dict[key]
        if existing[2] and contact[2] and existing[2] != contact[2]:
            new_key = (contact[0], contact[1], contact[2])
            contacts_dict[new_key] = contact
            continue

        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

result.extend(contacts_dict.values())


with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)



import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


for idx, contact in enumerate(contacts_list):
    if idx == 0:
        continue
    else:
        fio_list = contact[:3]
        fio = ' '.join(fio_list).split()
        for i in range(3):
            if i < len(fio):
                contacts_list[idx][i] = fio[i]
            else:
                contacts_list[idx][i] = ''


for contact in contacts_list[1:]:
    if not contact[5]:
        continue
    else:
        number = contact[5]
        number_pattern = (
                        r'(?:\+7|8)[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(\d{1})[\s\-()]*'
                        r'(?:(доб)[\s\-().]*'
                        r'(\d{4})[\s\-().]*)?'
        )

        matches = re.findall(number_pattern, number)
        formated_number = '+7'
        if matches:
            for idx, match in enumerate(matches[0]):
                if not match:
                    break

                if idx in range(10):
                    formated_number +=match
                elif idx == 10:
                    formated_number +=' ' + match
                elif idx == 11:
                    formated_number +='.' + match

        contact[5] = formated_number


result = []
contacts_dict = {}
for contact in contacts_list[1:]:
    key = (contact[0], contact[1])
    #key = (contact[0], contact[1], contact[2])         #Если считать, что есть везде отчества.
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        existing = contacts_dict[key]
        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

result.append(contacts_list[0])
result.extend(contacts_dict.values())


with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)




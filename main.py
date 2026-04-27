import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


#Обработка ФИО
for contact in contacts_list:
    fio = " ".join(contact[:3]).strip().split()
    contact[0] = fio[0] if len(fio) > 0 else ""
    contact[1] = fio[1] if len(fio) > 1 else ""
    contact[2] = " ".join(fio[2:]) if len(fio) > 2 else ""


#Обработка номера телефона
def processing_phone(number):
    cleaned = re.sub(r'[^+\w]', '', number)
    if cleaned.startswith('8'):
        cleaned = '+7' + cleaned[1:]

    ext_match = re.search(r'([a-zA-Za-яА-Я]+)(\d+)', cleaned, re.IGNORECASE)
    if ext_match:
        main_number = cleaned[:ext_match.start()]
        ext_number = ext_match.group(1) + "." +  ext_match.group(2)
        formatted_number = f'{main_number} {ext_number}'
    else:
        formatted_number = cleaned
    return formatted_number


for contact in contacts_list[1:]:
    if not contact[5]:
        continue
    contact[5] = processing_phone(contact[5])


#Объединение дубликатов
result = [contacts_list[0]]

key_contact_dict = {}
for contact in contacts_list[1:]:
    lastname = contact[0].strip()
    firstname = contact[1].strip()
    surname = contact[2].strip()
    phone = contact[5].strip()
    email = contact[6].strip().lower()

    keys = []
    if email:
        keys.append(("email", email))
    if phone:
        keys.append(("phone", phone))
    if lastname and firstname and surname:
        keys.append(("fio_full", lastname, firstname, surname))
    if lastname and firstname:
        keys.append(("fio_partial", lastname, firstname))

    existing = None
    for key in keys:
        if key in key_contact_dict:
            candidate = key_contact_dict[key]

            existing_phone = candidate[5].strip()
            existing_email = candidate[6].strip().lower()

            conflict = False
            if phone and existing_phone and phone != existing_phone:
                conflict = True
            if email and existing_email and email != existing_email:
                conflict = True
            if not conflict:
                existing = candidate
                break

    if existing:
        for i in range(3, len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]
            elif existing[i] and contact[i] and existing[i] != contact[i]:
                existing[i] += "|" + contact[i]
        target = existing
    else:
        target = contact

    if email:
        key_contact_dict[("email", email)] = target
    if phone:
        key_contact_dict[("phone", phone)] = target
    if lastname and firstname and surname:
        key_contact_dict[("fio_full", lastname, firstname, surname)] = target
    if lastname and firstname:
        key_contact_dict[("fio_partial", lastname, firstname)] = target

result.extend(list({id(v): v for v in key_contact_dict.values()}.values()))


with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)



import re
from operator import contains
from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv

with open("phonebook_raw.csv",'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

contact_correct=[]
contact_temp = []
for i in range(1,len(contacts_list)):
    contact_temp.append(','.join(contacts_list[i]).strip())

def find_index(fam, im):
    index = -1
    for i in range(len(contact_correct)):
        if fam.strip().lower() == contact_correct[i][0].strip().lower() and im.strip().lower() == contact_correct[i][1].strip().lower():
            index = i
    return index
def update_record(index,o, org, place, phone, email):
    if contact_correct[index][2] == '':
        contact_correct[index][2] = o
    if contact_correct[index][3] == '':
        contact_correct[index][3] = org
    if contact_correct[index][4] == '':
        contact_correct[index][4] = place
    if contact_correct[index][5] == '':
        contact_correct[index][5] = phone
    if contact_correct[index][6] == '':
        contact_correct[index][6] = email



pattern = r'(^\w+)[\s,](\w+)[\s,](\w*)[\s,]*(\w*),+([^,|^+|^\d|^[a-zA-Z]*]*)'
pattern_phone = r',(\+7|8)\s?\(?(\d{3})\)?-?\s?(\d{3})-?(\d{2})-?(\d{2})'
pattern_add = r'доб.\s*(\d*)'
pattern_email = r',([\w\.]+)@([\w\.]+)\.([\w\.]+)'
for i in contact_temp:
    result = re.search(pattern, i)
    fam, im, ot, org, place = result.group(1), result.group(2), result.group(3), result.group(4), result.group(5)
    index = find_index(fam, im)
    phone = re.search(pattern_phone, i)
    if phone == None:
        p = ''
    else:
        p =  phone.group(1).replace('8','+7',1)+'('+phone.group(2)+')'+phone.group(3)+'-'+phone.group(4)+'-'+phone.group(5)
    phone_add = re.search(pattern_add, i)
    if phone_add!=None :
       p += ' доб.'+phone_add.group(1)

    result = re.search(pattern_email,i)
    if result != None:
        email = result.group(1)+'@'+result.group(2)+'.'+result.group(3)
    else:
        email = ''
    if index == -1:
        contact_correct.append([fam, im, ot, org, place, p, email])
    else:
        update_record(index, ot, org, place, p, email)

pprint(contact_correct)

# 2. Сохраните получившиеся данные в другой файл.
# Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')

    ## Вместо contacts_list подставьте свой список:
    datawriter.writerows(contact_correct)
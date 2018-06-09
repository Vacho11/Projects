import xml.etree.ElementTree as et
import sqlite3
import hashlib

conn = sqlite3.connect('PersonalData.sqlite')
cur = conn.cursor()

Faculties = ['Факультет анализа рисков и экономической безопасности',
            'Менеджмент', 'Международные экономические отношения​',
            'Международный туризм', 'спорт и гостиничный бизнес',
            'Международный финансовый', 'Налоги и налогообложение',
            'Прикладная математика и информационные технологии',
            'Социология и политология', 'Учет и аудит',
            'Финансово-экономический', 'Финансовых рынков Юридически']
Data = []
# Make a frensh SQL table
try:
    cur.executescript('''

    CREATE TABLE Code (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        hash TEXT UNIQUE
        );

    CREATE TABLE Faculty (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        faculty TEXT UNIQUE,
        Code_id INTEGER,
        name TEXT,
        birthday TEXT,
        graduation TEXT
        );
    ''')
except:
    print('Table for Personal Data is already in Use')

def hash_data():
    hash = hashlib.sha1()
    for data in Data:
        data = data.encode('utf-8')
        hash.update(data)
        hash.update(b'\0')
    code = hash.hexdigest
    return code

def get_name():
    name = input("Please enter your Name and Surname: ")
    Data.append(name)
    return name

def get_birthday():
    year = str(input('Enter a year:'))
    month = str(input('Enter a month:'))
    day = str(input('Enter a day:'))
    birthday = year + ' / ' + month + ' / ' + day
    Data.append(birthday)
    return birthday

def get_graduation():
    graduation = str(input('Please enter your year of graduation: '))
    Data.append(graduation)
    return graduation

def get_Faculty():
    print(Faculties)
    faculty = input("Please Select faculty from the following List: ")
    Data.append(faculty)
    return faculty

while True:
    print("Write Command")
    print("N - Add Name and Surname")
    print("B - Add Birthday Date")
    print("G - Graduation Year")
    print("F - Faculty")
    print("E - Exit the programme")
    user_input = input()
    if user_input == 'N':
        name = get_name()
    if user_input == 'B':
        birthday = get_birthday()
    if user_input == 'G':
        graduation = get_graduation()
    if user_input == 'F':
        faculty = get_Faculty()
    if user_input == 'E':
        print(Data)
        code = hash_data()
        print(code)
        print(type(code))
        break
#if name is None or birthday is None or graduation is None or faculty is None:
#    continue
try:
    Name = name
    Birthday = birthday
    Graduation = graduation
    Faculty = faculty
    Hash = str(code)
    Hash = Hash[-11:-1]
except:
    print("Please indicate all necessary Data")

cur.execute('''INSERT INTO Code (hash) VALUES (?) ''', (Hash, ))
cur.execute('SELECT id FROM Code WHERE hash = ? ', (Hash, ))
Code_id = cur.fetchone()[0]

cur.execute('''INSERT INTO Faculty (name, birthday, graduation, faculty, Code_id)
VALUES (?, ?, ?, ?, ?)''', (Name, Birthday, Graduation, Faculty, Code_id))

conn.commit()

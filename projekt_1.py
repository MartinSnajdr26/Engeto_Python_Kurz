"""
projekt_1.py: první projekt do Engeto Online Python Akademie

author: Martin Snajdr
email: martin.snajdr.japan@gmail.com
"""

TEXTS = ['''
Situated about 10 miles west of Kemmerer,
Fossil Butte is a ruggedly impressive
topographic feature that rises sharply
some 1000 feet above Twin Creek Valley
to an elevation of more than 7500 feet
above sea level. The butte is located just
north of US 30N and the Union Pacific Railroad,
which traverse the valley. ''',
'''At the base of Fossil Butte are the bright
red, purple, yellow and gray beds of the Wasatch
Formation. Eroded portions of these horizontal
beds slope gradually upward from the valley floor
and steepen abruptly. Overlying them and extending
to the top of the butte are the much steeper
buff-to-white beds of the Green River Formation,
which are about 300 feet thick.''',
'''The monument contains 8198 acres and protects
a portion of the largest deposit of freshwater fish
fossils in the world. The richest fossil fish deposits
are found in multiple limestone layers, which lie some
100 feet below the top of the butte. The fossils
represent several varieties of perch, as well as
other freshwater genera and herring similar to those
in modern oceans. Other fish such as paddlefish,
garpike and stingray are also present.''']

# Přihlašovací údaje
user_name = input("username: ")
password = input("password: ")

registered_users = {"bob": "123",
                    "ann": "pass123",
                    "mike": "password123",
                    "liz": "pass123"}

# Ověření přihlášení
if user_name in registered_users and registered_users[user_name] == password:
    print(f"""
{'-' * 40}
Welcome to the app, {user_name}.
We have 3 texts to be analyzed.
""")

    # Slovník pro texty
    text_parts = {index: text for index, text in enumerate(TEXTS)}

    # Inicializace výsledků
    results = {}

    # Iterace přes všechny texty
    for index, text in text_parts.items():
        # Inicializace proměnných pro analýzu
        word_count = 0
        capitalized_words = 0  # Slova začínající velkým písmenem
        uppercase_words = 0  # Slova psaná velkými písmeny
        lowercase_words = 0  # Slova psaná malými písmeny
        numeric_count = 0  # Počet čísel
        numeric_sum = 0  # Součet všech čísel

        # Iterace přes slova v aktuálním textu
        for word in text.split():
            word_count += 1  # Počet slov

            if word.istitle():  # Slovo začíná velkým písmenem
                capitalized_words += 1
            if word.isupper() and word.isalpha():  # Slovo je psáno pouze velkými písmeny
                uppercase_words += 1
            if word.islower():  # Slovo je psáno pouze malými písmeny
                lowercase_words += 1
            if word.isdigit():  # Pokud je slovo číslo
                numeric_count += 1
                numeric_sum += int(word)

        # Uložení výsledků do slovníku
        results[index] = {
            "word_count": word_count,
            "capitalized_words": capitalized_words,
            "uppercase_words": uppercase_words,
            "lowercase_words": lowercase_words,
            "numeric_count": numeric_count,
            "numeric_sum": numeric_sum,
        }

    # Uživatelský výběr textu
    choice = input(f"{'-' * 40}\nEnter a number btw. 1 and 3 to selects: ")

    if choice.isdigit():  # Kontrola, zda je vstup číslo
        choice = int(choice) - 1  # Převod na index
        if 0 <= choice < len(text_parts):  # Kontrola rozsahu
            text = text_parts[choice]

            # Výstup analýzy textu
            selected_results = results[choice]

            print(f"""
{'-' * 40}
There are {selected_results['word_count']} words in the selected text.
There are {selected_results['capitalized_words']} titlecase words.
There are {selected_results['uppercase_words']} uppercase words.
There are {selected_results['lowercase_words']} lowercase words.
There are {selected_results['numeric_count']} numeric strings.
The sum of all the numbers is {selected_results['numeric_sum']}
{'-' * 40}
""")

            # Analýza délek slov
            word_length = {}
            for word in text.split():
                word = word.strip(",.:;")  # Odstranění interpunkce
                length = len(word)
                if length > 0:  # Kontrola, že délka slova je větší než 0
                    if length in word_length:
                        word_length[length] += 1
                    else:
                        word_length[length] = 1

            # Výstup analýzy délek slov
            print("LEN | OCCURRENCES    | NR.")
            print("-" * 40)
            for length, count in sorted(word_length.items()):  # Řazení podle délky slova
                stars = "*" * count
                print(f"{length:>3} | {stars:<15} | {count}")

        else:
            print("Invalid input. You did not select a number between 1 and 3. Terminating the program...")
            exit()
    else:
        print("Invalid input. You did not enter a number. Terminating the program...")
        exit()
else:
    print(f"username: {user_name}\npassword: {password}\nunregistered users: terminating the program...")
    exit()

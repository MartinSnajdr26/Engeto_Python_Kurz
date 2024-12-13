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
garpike and stingray are also present.'''
]

user_name = input("Please Enter your USER_NAME: ")
password = input("Please Enter your PASSWORD: ")

registered_users = {"bob": "123",
                    "ann": "pass123",
                    "mike": "password123",
                    "liz": "pass123"}

text_parts = {index: text for index, text in enumerate(TEXTS)} # prevod textu do dictionary s indexem 

# Slovník pro výsledky analýzy
results = {}

words_lenght = {}

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

        # Slovo začíná velkým písmenem (např. "Word")
        if word.istitle():
            capitalized_words += 1
        
        # Slovo je psáno pouze velkými písmeny (např. "WORD")
        if word.isupper():
            uppercase_words += 1
        
        # Slovo je psáno pouze malými písmeny (např. "word")
        if word.islower():
            lowercase_words += 1
        
        # Pokud je slovo číslo (např. "123")
        if word.isdigit():
            numeric_count += 1
            numeric_sum += int(word)  # Převod na číslo a přičtení k součtu

    # Uložení výsledků do slovníku
    results[index] = {
        "word_count": word_count,
        "capitalized_words": capitalized_words,
        "uppercase_words": uppercase_words,
        "lowercase_words": lowercase_words,
        "numeric_count": numeric_count,
        "numeric_sum": numeric_sum,
    }


for word in text.split():
    words_lenght[word] = len(word)

for index, words_lenght in word.items():
    words_lenght[word] += 1


# Zjištění, jestli uživatel je registrován
if user_name in registered_users and registered_users[user_name] == password:
    print(f"Welcome to the app, {user_name}.\nWe have 3 texts to be analyzed.")
    
    # Uživatelský výběr
    choice = input("Please select 1 of 3 texts for analysis: ")
    
    if choice.isdigit():  # Kontrola, zda je vstup číslo
        choice = int(choice)  # Převod na celé číslo
        if 1 <= choice <= 3:  # Kontrola, zda je číslo v rozsahu
            print(f"You selected text {choice}. Proceeding to analysis...")
            if choice == 1: 
                print(
                    f"There are {results[word_count]} words in the selected text"\n
                    f"There are {results[capitalized_words]} capitalized words"\n
                    f"There are {results[uppercase_words]} uppercase words"\n
                    f"There are {results[lowercase_words]} lowercase words"\n
                    f"There are {results[numeric_count]} numeric strings"\n"
                    f"The sum of all numbers is {reuslts[numeric_sum]}."
                )
                print
            elif choice == 2:
                print(
                    f"There are {results[word_count]} words in the selected text"\n
                    f"There are {results[capitalized_words]} capitalized words"\n
                    f"There are {results[uppercase_words]} uppercase words"\n
                    f"There are {results[lowercase_words]} lowercase words"\n
                    f"There are {results[numeric_count]} numeric strings"\n"
                    f"The sum of all numbers is {reuslts[numeric_sum]}."
                )
            elif choice == 3:
                print(
                    f"There are {results[word_count]} words in the selected text"\n
                    f"There are {results[capitalized_words]} capitalized words"\n
                    f"There are {results[uppercase_words]} uppercase words"\n
                    f"There are {results[lowercase_words]} lowercase words"\n
                    f"There are {results[numeric_count]} numeric strings"\n"
                    f"The sum of all numbers is {reuslts[numeric_sum]}."
                )
        else:
            print("Invalid input. You did not select a number between 1 and 3. Terminating the program...")
            exit()
    else:
        print("Invalid input. You did not enter a number. Terminating the program...")
        exit()
else:
    print(f"username: {user_name}\npassword: {password}\nunregistered users: terminating the program...")
    exit()
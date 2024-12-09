leden = ["Nový rok", "Karina / Vasil", "Radmila / Radomil", "Diana", "Dalimil", "Tři králové", "Vilma", "Čestmír",
    "Vladan / Valtr", "Břetislav", "Bohdana", "Pravoslav", "Edita", "Radovan", "Alice", "Ctirad", "Drahoslav",
    "Vladislav / Vladislava", "Doubravka", "Ilona / Sebastián", "Běla", "Slavomír / Slavomíra", "Zdeněk", "Milena",
    "Miloš", "Zora", "Ingrid", "Otýlie", "Zdislava", "Robin / Erna", "Marika",]

unor = ["Nový rok", "Karina / Vasil", "Radmila / Radomil", "Diana", "Dalimil", "Tři králové", "Vilma", "Čestmír",
    "Vladan / Valtr", "Břetislav", "Bohdana", "Pravoslav", "Edita", "Radovan", "Alice", "Ctirad", "Drahoslav",
    "Vladislav / Vladislava", "Doubravka", "Ilona / Sebastián", "Oldřich", "Lenka / Eleonora", "Petr", "Svatopluk",
    "Matěj / Matyáš", "Liliana", "Dorota", "Alexandr", "Lumír", "Horymír"]

leden = set(leden)
unor = set(unor)

print("Svátek jak v lednu, tak v únoru:")
print(leden & unor)

print("\nSvátek v lednu, ale ne v únoru:")
print(leden - unor)

print("\nSvátek v únoru, ale ne v lednu:")
print(unor - leden)

print("\nSvátek jenom v lednu nebo jenom v únoru:")
print(leden ^ unor)

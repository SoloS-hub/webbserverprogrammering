import hashlib

# Läs passwords.csv och skapa dictionary med hash som nyckel

def crack_hash(type, file):
    password_dict = {}
    password_dict_cracked = {}
    password_not_found = {}

    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                username, hash_value = line.split(';')
                password_dict[hash_value] = username
    
    with open(f'break-hash/rainbow_{type}.csv', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                pasword_cracked, hash_value_cracked = line.split(';')
                if hash_value_cracked in password_dict:
                    password_dict_cracked[password_dict[hash_value_cracked]] = pasword_cracked
                else:
                    password_not_found[hash_value] = username
                    
    

    print(f"Läst {len(password_dict)} hashar från passwords.csv")
    print(f"Dictionary skapad med hash som nyckel och användarnamn som värde")
    # print(password_dict)
    print(f"Passwords cracked: {password_dict_cracked}")
    print(f"Passwords not cracked: {password_not_found}")
    return password_dict_cracked

# Man kan nu plocka upp användarnamn med hjälp av hashvärden, t.ex.:
# hash_to_lookup = '5d41402abc4b2a76b9719d911017c592'
# if hash_to_lookup in password_dict:  
#     print(f"Användarnamn för hash {hash_to_lookup} är {password_dict[hash_to_lookup]}")

file = 'break-hash/passwords2.csv'
crack_hash('sha1', file)

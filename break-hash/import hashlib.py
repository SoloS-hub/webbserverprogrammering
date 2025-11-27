import hashlib

hash_value = "047faf021517f69765c98163c82c516baec592f9"

def check_SHA1(string):

    hash_object = hashlib.sha1(string.encode())
    pbHash = hash_object.hexdigest()
    return pbHash

characters = ["", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

number_of_characters_to_test = 4


for i in range(len(characters)):
    for j in range(len(characters)):
        for k in range(len(characters)):
            for l in range(len(characters)):
                test_string = characters[l] + characters[k] + characters[j] + characters[i]
                print(f"Testing string: {test_string}")
                if check_SHA1(test_string) == hash_value:
                    print(f"Found matching string: {test_string}")
                    exit(0)

import re
#
# IBAN_Check.py
# Utility to check the integrity of an IBAN bank account No.
# <strong class="highlight">Python</strong> 2.5.1

# Sample IBAN account numbers.
#-----------------------------
# BE31435411161155
# CH5108686001256515001
# GB35MIDL40253432144670


# Dictionaries - Refer to ISO 7064 <strong class="highlight">mod</strong> 97-10
letter_dic={"A":10, "B":11, "C":12, "D":13, "E":14, "F":15, "G":16, "H":17, "I":18, "J":19, "K":20, "L":21, "M":22,
            "N":23, "O":24, "P":25, "Q":26, "R":27, "S":28, "T":29, "U":30, "V":31, "W":32, "X":33, "Y":34, "Z":35}

# ISO 3166-1 alpha-2 country code
country_dic={"AL":[28,"Albania"],
             "AD":[24,"Andorra"],
             "AT":[20,"Austria"],
             "BE":[16,"Belgium"],
             "BA":[20,"Bosnia"],
             "BG":[22,"Bulgaria"],
             "HR":[21,"Croatia"],
             "CY":[28,"Cyprus"],
             "CZ":[24,"Czech Republic"],
             "DK":[18,"Denmark"],
             "EE":[20,"Estonia"],
             "FO":[18,"Faroe Islands"],
             "FI":[18,"Finland"],
             "FR":[27,"France"],
             "DE":[22,"Germany"],
             "GI":[23,"Gibraltar"],
             "GR":[27,"Greece"],
             "GL":[18,"Greenland"],
             "HU":[28,"Hungary"],
             "IS":[26,"Iceland"],
             "IE":[22,"Ireland"],
             "IL":[23,"Israel"],
             "IT":[27,"Italy"],
             "LV":[21,"Latvia"],
             "LI":[21,"Liechtenstein"],
             "LT":[20,"Lithuania"],
             "LU":[20,"Luxembourg"],
             "MK":[19,"Macedonia"],
             "MT":[31,"Malta"],
             "MU":[30,"Mauritius"],
             "MC":[27,"Monaco"],
             "ME":[22,"Montenegro"],
             "NL":[18,"Netherlands"],
             "NO":[15,"Northern Ireland"],
             "PO":[28,"Poland"],
             "PT":[25,"Portugal"],
             "RO":[24,"Romania"],
             "SM":[27,"San Marino"],
             "SA":[24,"Saudi Arabia"],
             "RS":[22,"Serbia"],
             "SK":[24,"Slovakia"],
             "SI":[19,"Slovenia"],
             "ES":[24,"Spain"],
             "SE":[24,"Sweden"],
             "CH":[21,"Switzerland"],
             "TR":[26,"Turkey"],
             "TN":[24,"Tunisia"],
             "GB":[22,"United Kingdom"]}

def check_mod97(n):
    if int(n) % 97 != 1:
        return False
    else:
        return True

def validate_bban(BBAN):
    p = re.compile('( |/|-)')
    BBAN = p.sub('', BBAN)
    try:
        cc = int(BBAN[-2:])
        code = BBAN[:-2]
        check = int(code) % 97
        check = 97 if check == 0 else check
    except ValueError:
        return False, BBAN

    return check == cc, BBAN

def validate_iban(IBAN):
    p = re.compile('( |/|-)')
    IBAN = p.sub('', IBAN)
    while True:
        length = len(IBAN)
        country = IBAN[:2]
        if country_dic.has_key(country):
            data = country_dic[country]
            length_c = data[0]
            name_c = data[1]
            if length == length_c:
                header = IBAN[:4]                                   # Get the first four characters
                body = IBAN[4:]                                     # And the remaining characters
                IBAN = body+header                                  # Move the first block at the end
                IBAN_ = list(IBAN)                                  # Transform string into a list
                string_=""
                for index in range(len(IBAN_)):                     # Convert letters to integers
                    if letter_dic.has_key(IBAN_[index]):
                        value = letter_dic[IBAN_[index]]
                        IBAN_[index] = value
                for index in range(len(IBAN_)):                     # Transform list into a string
                    string_ = string_ + str(IBAN_[index])
                valid = check_mod97(string_)                              # Check validity
                if not valid:
                    return False, IBAN
                else:
                    trailer = IBAN[len(IBAN)-4:]                    # Get the four last characters
                    body = IBAN[:len(IBAN)-4]                       # And the remaining characters
                    IBAN = trailer+body                             # Move the trailer at the begin
                    break
            else:
                return False, IBAN
        else:
            return False, IBAN

    # Display a formated account No. (Thanks to Griboullis)
    split_IBAN = lambda block,string:[string[f:f+block] for f in range(0,len(string),block)]
    BankAccountNo = split_IBAN(4,IBAN)

    return True, IBAN

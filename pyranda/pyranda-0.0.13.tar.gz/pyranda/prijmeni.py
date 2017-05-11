class Prijmeni:
    """ Třída zapouzdřující chování obyčejného jména.. """
    def __init__(self, nazev, nazev2):
        self.nazev = nazev
        self.nazev2 = nazev2


prijmenis = []

def Init():
    prijmenis.append(Prijmeni("Novák", "Nováková")) 
    prijmenis.append(Prijmeni("Koudelka", "Koudelková")) 
    prijmenis.append(Prijmeni("Procházka", "Procházková")) 

def PrintAll():
    for prijmeni in prijmenis:
        print(prijmeni.nazev)

import lingcorpora

list = ['styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec', 'lipiec', 'sierpień', 'wrzesień', 'październik',
        'listopad', 'grudzień', 'biały', 'różowy', 'czerwony', 'pomarańczowy', 'brązowy', 'żółty', 'szary', 'zielony',
        'błękitny', 'niebieski', 'czarny', 'fioletowy', 'poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek',
        'sobota', 'niedziela']

for word in list:
    lingcorpora.pol_search(query=word, write=True)
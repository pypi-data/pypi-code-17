def _poslat():
    import os
    from colorama import Fore
    print('Если у вас есть какие-нибудь возражения или предложения прочитайте статью 1.')
    a = True
    while a:
        ans = input('Прочитать статью 1? [' + Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET + ',' + Fore.LIGHTRED_EX + ' n'+ Fore.RESET +']').upper()
        if ans == 'Y':
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Статья 1:')
            print('Пожалуйса прочитайте статью 1, если у вас есть возражения или предложения.\n\n')
        else: a = False
    os.system('cls' if os.name == 'nt' else 'clear')
    input(Fore.CYAN+ '\nСпасибо, что полностью со мной согласились!' + Fore.RESET)
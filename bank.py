from BankDB import Linklist
from colorama import Back, Fore
from getpass import getpass

# Initializing Database
db = Linklist()

# Function definitions
def transfer_process(profile:dict):
    while True:
        recipent:str = input("Enter recipent's email: ")
        if db.searchCol({'email': recipent}) != {}:
            while True:
                try:
                    amount:int = int(input('Enter {}amount{} to be transferred: '.format(Fore.BLUE, Fore.RESET)))
                    if amount <= (profile['amount'] - 1000):
                        profile['amount'] -= amount
                        recAmount:int = db.searchCol({'email': recipent})['amount']
                        recAmount += amount
                        db.updateCol({'email': profile['email']}, {'amount': profile['amount']})
                        db.updateCol({'email': recipent}, {'amount': recAmount})
                        print(f'{Fore.GREEN}Transfer process succeeded{Fore.RESET}')
                        break
                    else:
                        print(f'{Fore.RED}Insufficient Inventory{Fore.RESET}')
                except Exception as err:
                    print(f'{Fore.RED}Error: {err}{Fore.RESET}')
            break
        else:
            print(f'Recipent{Fore.RED}Not Found{Fore.RESET}')

def cashIn_process(profile:dict):
    while True:
        try:
            amount:int = int(input('Enter {}amount{} to be saved: '.format(Fore.BLUE, Fore.RESET)))
            profile['amount'] += amount
            db.updateCol({'email': profile['email']}, {'amount': profile['amount']})
            print(f'{Fore.GREEN}Money have been saved in the account{Fore.RESET}')
            break
        except Exception as err:
            print(f'{Fore.RED}Error: {err}{Fore.RESET}')

def withdraw_process(profile:dict):
    print(f'{Fore.YELLOW}Withdraw Process under maintenance{Fore.RESET}')

def show_profile(profile:dict):
    for item in profile:
        print(f'{item:<20s}: {Fore.BLUE}{profile[item]}{Fore.RESET}')

def delete_process(profile:dict):
    password:str = getpass('Enter {}password{} to delete your account: '.format(Fore.BLUE, Fore.RESET))
    confirm:str = input(f'{Fore.RED}Are you sure [{Fore.BLUE}Yes{Fore.RED}]{Fore.RESET}: ')
    if (password == profile['password']) and (confirm.lower() == 'yes'):
        db.deleteCol({'email': profile['email']})

# Start of Main Program
if __name__ == "__main__":
    try:
        print(Back.BLACK,Fore.MAGENTA,"***\tE_BANKING SERVICE\t***",Fore.RESET)
        while True:
            option:str = input(f'How may I help [ {Fore.BLUE}Register{Fore.RESET}, {Fore.BLUE}Login{Fore.RESET} or {Fore.BLUE}Exit{Fore.RESET} ]: ')
            if option.lower() == 'register':
                profile:dict = {}
                while True:
                    rEmail:str = input('{:<30s}: '.format(f'Enter {Fore.BLUE}email{Fore.RESET}'))
                    profile['email'] = rEmail
                    if db.searchCol(profile) == {}:
                        for freq in range(3):
                            rPass:str = getpass('{:30s}: '.format(f'Enter {Fore.BLUE}password{Fore.RESET}'))
                            rePass:str = getpass('{:30s}: '.format(f'Comfirm {Fore.BLUE}password{Fore.RESET}'))
                            if rPass == rePass:
                                profile['password'] = rPass
                                rName:str = input('{:30s}: '.format(f'Enter {Fore.BLUE}username{Fore.RESET}'))
                                profile['name'] = rName
                                rPhone:str = input('{:30s}: '.format(f'Enter {Fore.BLUE}phone no:{Fore.RESET}'))
                                profile['phone'] = rPhone
                                while True:
                                    try:
                                        rAmount:int = int(input('{:30s}: '.format(f'Enter {Fore.BLUE}amount{Fore.RESET}')))
                                        profile['amount'] = rAmount
                                        break
                                    except Exception as err:
                                        print(Fore.RED, "Error: ", err, Fore.RESET)
                                db.insertCol(profile)
                                print(Fore.GREEN, 'Registration succeeded', Fore.RESET)
                                break
                            else:
                                print(f'{Fore.RED}Passwords are not matched!{Fore.RESET}')
                        break          
                    else:
                        print(f'{Fore.RED}Email Already Existed!{Fore.RESET}')
                        if input(f'RollBack[ {Fore.BLUE}yes{Fore.RESET} ]?: ').lower() == 'yes':
                            break
            elif option.lower() == 'login':
                profile:dict = {}
                while True:
                    rEmail:str = input('{:<30s}: '.format(f'Enter {Fore.BLUE}email{Fore.RESET}'))
                    profile = db.searchCol({'email': rEmail}) 
                    if profile != {}:
                        for freq in range(3):
                            rPass:str = getpass('{:30s}: '.format(f'Enter {Fore.BLUE}password{Fore.RESET}'))
                            if rPass == profile['password']:
                                print(f'{Fore.GREEN}***\tWelcome {profile["name"]}\t***{Fore.RESET}')
                                while True:
                                    option:str = input("{}, {}, {}, {}, {} or {}".format(f'{Fore.BLUE}Transfer{Fore.RESET}',
                                                                                    f'{Fore.BLUE}CashIn{Fore.RESET}',
                                                                                    f'{Fore.BLUE}Withdraw{Fore.RESET}',
                                                                                    f'{Fore.BLUE}Delete{Fore.RESET}',
                                                                                    f'{Fore.BLUE}show{Fore.RESET}',
                                                                                    f'{Fore.BLUE}Exit{Fore.RESET}: '))
                                    profile = db.searchCol({'email': rEmail})
                                    if option.lower() == 'transfer':
                                        transfer_process(profile)
                                    elif option.lower() == 'withdraw':
                                        withdraw_process(profile)
                                    elif option.lower() == 'cashin':
                                        cashIn_process(profile)
                                    elif option.lower() == 'delete':
                                        delete_process(profile)
                                    elif option.lower() == 'show':
                                        show_profile(profile)
                                    elif option.lower() == 'exit':
                                        break
                                break
                            else:
                                print(Fore.RED,"Wrong Credential!",Fore.RESET)
                        break
                    else:
                        print(f'{Fore.RED}User Not Found!{Fore.RESET}')
                        if input(f'RollBack[ {Fore.BLUE}yes{Fore.RESET} ]?: ').lower() == 'yes':
                            break
            elif option.lower() == 'exit':
                db.terminate()
                print(Fore.MAGENTA, '\n...Pleasure to serve you...\n', Fore.RESET, Back.RESET)
                break
            else:
                print(f'{Fore.RED}Wrong Input!{Fore.RESET}')
    except KeyboardInterrupt:
        db.terminate()
        print(Fore.MAGENTA, '\n...Pleasure to serve you...\n', Fore.RESET, Back.RESET)

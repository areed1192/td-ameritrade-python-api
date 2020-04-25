from td.client import TDClient
from td.AccountsManager import AccountsManager
import Extensions.file_utils as file_utils
import json
import os

Accounts = AccountsManager("***client_id****", '***redirect_uri***')

Accounts.add_account('name of an account', '### account ###', '***credentials_path***')
Accounts.add_account('2', '### account ###', '***credentials_path***')
#...

Accounts.login() #logs in all accounts

Accounts.print_account_worths() #prints liquidation values of all accounts -- just handy, arguably moved/removed

#save:
file_utils.save_json('../Accounts.json', Accounts.to_dict()) 

Accounts.logout()


#load:
accounts_dict = file_utils.load_json('../Accounts.json')
if len(accounts_dict) == 0:
    print('Found no accounts logged in!')
    pass
Accounts = AccountsManager.from_dict(accounts_dict)

Accounts.login()

Accounts.print_account_worths()



TDSession = Accounts['My IRA']

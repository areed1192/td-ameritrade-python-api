from td.client import TDClient
from td.AccountsManager import AccountsManager

#-----------set up accounts programatically-------------------------

Accounts = AccountsManager("***client_id****", '***redirect_uri***')

Accounts.add_account('My IRA', '### account ###', '***credentials_path***')
Accounts.add_account('Dads IRA', '### account ###', '***credentials_path***')
#...

Accounts.login() #logs in all accounts

#prints liquidation values of all accounts -- just handy, arguably could be moved|removed
Accounts.print_account_worths() 

#Save by any user chosen means (with possible helpers to be included in td.utils):
Accounts.to_dict()

Accounts.logout()

#-----------------------------Load from anything-----------------------
accounts_dict = #pull from something, eg with json.load

#initialize once source is known good:
Accounts = AccountsManager.from_dict(accounts_dict)

#repeat:
Accounts.login()

Accounts.print_account_worths()



current_session = Accounts['My IRA']

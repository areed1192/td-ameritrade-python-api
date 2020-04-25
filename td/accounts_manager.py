from __future__ import annotations

import os
from td.client import TDClient

class AccountsManager():
    accounts = {}
    
    def __init__(self, client_id: str, redirect_uri: str) -> None:
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self._should_be_logged_in = False

    @classmethod
    def from_dict(cls, d: dict) -> AccountsManager:
        am = cls(d['client_id'], d['redirect_uri'])
        for account in d['accounts'].items():
            am.add_account(account[0], account[1]['account_number'], account[1]['credentials_path'])
        return am

    def to_dict(self) -> dict:
        return {
            'client_id':self.client_id,
            'redirect_uri':self.redirect_uri,
            'accounts':{a[0]:{b[0]:b[1] for b in a[1].items() if b[0] != 'client'} for a in self.accounts.items()}
        }

    def print_account_worths(self) -> None:
        for account in self.accounts.items():
            client = account[1].get('client')
            if client is not None:
                accInfo = client.get_accounts(fields = ['orders','positions'])
                if accInfo is None or 'error' in accInfo:
                    print('Error, get_accounts returned: ',print(json.dumps(accInfo,sort_keys=True, indent=4)))
                else:
                    for acc in [acc['securitiesAccount'] for acc in accInfo]:
                        if acc['accountId'] == account[1]['account_number']:
                            print(str.format('{} (#{}) Liquidation Value = {}',account[0],acc['accountId'], acc['currentBalances']['liquidationValue']))
        
    def add_account(self, key: str, accountNumber: str, accountPath: str=None) -> None:
        self.accounts[key] = {'account_number':accountNumber, 'credentials_path':accountPath, 'client':None}

        if self._should_be_logged_in:
            self.login_single(key=key, should_relogin=False)
    
    def login(self, should_relogin: bool=True) -> None:
        if should_relogin or not self._should_be_logged_in:
            for acc in self.accounts.keys():
                self.login_single(acc, should_relogin=self._should_be_logged_in)
        self._should_be_logged_in = True
    
    def login_single(self, key: str, should_relogin: bool=True) -> None:
        account = self.accounts.get(key)
        if account is None:
            raise KeyError("The passed key is not registered with this AccountManager; Please add_account(...) first!")
        client = account['client']
        
        if should_relogin and client is not None:
            client.logout()
        
        print('Logging in: ',key)
        
        client = TDClient(
            account_number = account['account_number'],
            client_id = self.client_id, redirect_uri = self.redirect_uri,
            credentials_path = account['credentials_path'])
        client.login()
        account['client'] = client
        client.client_key = key
        
    def logout(self) -> None:
        for account in self.accounts.values():
            client = account['client']
            if client is not None:
                client.logout()
                account['client'] = None

        self._should_be_logged_in = False

    def __getitem__(self, key: str) -> TDClient:
        return self.accounts[key]['client']

if __name__ == "__main__":
    pass
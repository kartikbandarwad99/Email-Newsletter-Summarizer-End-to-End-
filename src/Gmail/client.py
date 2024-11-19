import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class GmailClient:
    def __init__(self,config):
        self.config = config
        self.creds = self.get_creds()

    def get_creds(self):
        creds_file = self.config['gmail']['credentials']['credentials_file']
        token_file = self.config['gmail']['credentials']['token_file']
        SCOPES = self.config['gmail']['credentials']['scopes']
        
        # Authentication flow
        flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
        
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            if not creds.valid:
                print('Creds not valid. Refreshing token....')
                try:
                    creds.refresh(Request())
                    print(f'Creds refreshed. Creds now valid: {creds.valid}')
                    with open(token_file, "w") as token:
                        token.write(creds.to_json())
                except Exception as e:
                    print(f'Failed to refresh credentials: {e}')
                    creds = flow.run_local_server(port=0)
                    with open(token_file, "w") as token:
                        token.write(creds.to_json())
        else:
            creds = flow.run_local_server(port=0)
            print('No token.json')
            with open(token_file, "w") as token:
                token.write(creds.to_json())
        return creds
    def get_credentials(self):
        return self.creds

# config = load_config()
# client = GmailClient(config)
# client.get_credentials()
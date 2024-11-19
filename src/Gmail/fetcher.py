# fetcher.py
from googleapiclient.discovery import build
import base64
from datetime import datetime

class EmailFetcher:
    def __init__(self, gmail_client,config):
        self.service = build("gmail", "v1", credentials=gmail_client.creds)
        self.config = config

    def get_newsletter_mails(self, start_date=None, end_date=None, label=None):
        query = ''
        
        if not label:
            label = self.config['gmail']['fetch']['default_label']
        if label:
            query += f'label:{label} '
        
        print(f'From: {start_date} To: {end_date}')
        query += f'after:{start_date} before:{end_date} '
        
        response = self.service.users().messages().list(
            userId='me',
            q=query.strip(),
            maxResults=self.config['gmail']['fetch']['max_emails']
        ).execute()
        
        emails = []
        
        for message in response.get('messages', []):
            msg_id = message['id']
            print(f"Processing email ID: {msg_id}")
            
            msg = self.service.users().messages().get(userId='me', id=msg_id).execute()
            print(msg_id)
            try:
                # Determine if 'parts' is present and if it has more than one part
                if 'parts' in msg['payload'] and len(msg['payload']['parts']) >= 1:
                    if len(msg['payload']['parts']) == 2 and msg['payload']['parts'][1].get('mimeType') == 'text/html':
                        email_data = {'mimeType': 'html'}
                        body = msg['payload']['parts'][1]['body']['data']
                    else:
                        email_data = {'mimeType': 'text'}
                        body = msg['payload']['parts'][0]['body']['data']
                else:
                    email_data = {'mimeType': 'text'}
                    body = msg['payload']['body']['data']
                    
                body_decoded = base64.urlsafe_b64decode(body).decode(
                    self.config['gmail']['fetch']['processing']['decode_encoding']
                )
                
            except (KeyError, IndexError) as e:
                print(f"Error getting body for message {msg_id}: {e}")
                continue
            
            email_data.update({
                'id': msg['id'],
                'snippet': msg.get('snippet', 'No snippet available'),
                'subject': next((header['value'] for header in msg['payload']['headers'] 
                            if header['name'] == 'Subject'), 'No Subject'),
                'from': next((header['value'] for header in msg['payload']['headers'] 
                            if header['name'] == 'From'), 'Unknown Sender'),
                'body': body_decoded,
                'date': next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date')
            })
            
            emails.append(email_data)
        
        return emails

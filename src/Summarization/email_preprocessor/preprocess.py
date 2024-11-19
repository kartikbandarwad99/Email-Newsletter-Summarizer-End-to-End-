import re
from bs4 import BeautifulSoup
import unicodedata
import requests
import base64

class Preprocess:
    def __init__(self, mail):
        self.mail = mail.copy()

    def remove_links(self):
        print("Removing links...")
        url_pattern = r'https?://[^\s]+'
        links = re.findall(url_pattern, self.mail['body'])
        cleaned_text = re.sub(url_pattern, '', self.mail['body'])
        cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
        self.mail['links'] = links
        self.mail['body'] = cleaned_text
        return self.mail

    def parse_html_file(self):
        print("Parsing HTML file...")
        soup = BeautifulSoup(self.mail['body'], 'html.parser')
        self.mail['body'] = soup.get_text()
        return self.mail

    def remove_unwanted_chars(self):
        print("Removing unwanted characters...")

        def remove_control_chars(text):
            return ''.join(char for char in text if unicodedata.category(char)[0] != 'C')

        self.mail['body'] = remove_control_chars(self.mail['body'])
        self.mail['body'] = re.sub(r'\n\s*\n', '\n', self.mail['body'])
        return self.mail

    def decode_urls(self):
        decoded_urls = []
        urls = self.mail['links']
        if 'strictlyvc.com' in self.mail['from'] or 'news.pitchbook.com' in self.mail['from']:
            self.mail['links'] = []
            return self.mail

        for url in urls:
            if "convertkit" in url:
                encoded_part = url.split('/')[-1]
                try:
                    decoded_url = base64.urlsafe_b64decode(encoded_part).decode('utf-8')
                    decoded_urls.append(decoded_url)
                except Exception as e:
                    print(f"Failed to decode URL {url}: {e}")
            else:
                decoded_urls.append(url)
        
        self.mail['links'] = list(set(decoded_urls))
        return self.mail

    def clean(self):
        urls = self.mail['links']
        exclude_keywords = [
            "unsubscribe", "sponsored", "x.com", "twitter.com", "images", "image",
            "imgur", "gif", ".com/ads", "fonts.pitchbook.com", "img.pitchbook.com",
            "/icons?icon", '/images/'
        ]
        filtered_urls = [
            url for url in urls if not any(keyword in url.lower() for keyword in exclude_keywords)
        ]
        self.mail['links'] = list(set(filtered_urls))
        return self.mail


# def remove_unwanted_chars(mail):
#     print("Removing unwanted characters...")
#     cleaned_text = re.sub(r'\n\s*\n', '\n', mail['body'])
#     cleaned_text = cleaned_text.replace('\u2007', '').replace('\xad', '')
#     cleaned_text = re.sub(r'[\u0000-\u001f\u007f-\u009f\u2000-\u200f\u2028-\u202f\u205f-\u206f\u3000-\u303f]', '', cleaned_text)
#     new_mail = mail.copy()
#     new_mail['body'] = cleaned_text
#     return new_mail

# def remove_unwanted_chars(mail):
#     print("Removing unwanted characters...")
#     cleaned_text = mail['body']
#     cleaned_text = re.sub(r'[\u0000-\u001f\u007f-\u009f\u2000-\u200f\u2028-\u202f\u205f-\u206f\u3000-\u303f]', '', cleaned_text)
#     cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
#     cleaned_text = cleaned_text.replace('\u2007', '').replace('\xad', '')
#     new_mail = mail.copy()
#     new_mail['body'] = cleaned_text
#     return new_mail




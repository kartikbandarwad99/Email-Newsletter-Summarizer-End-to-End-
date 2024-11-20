from src.utils.helper import load_config, get_date_range
from src.Gmail import *
from src.Summarization.email_preprocessor import Preprocess
import tiktoken
from src.Summarization.Summarizer.summarizer import NewsletterSummarizer
import os
from src.Notion.client import create_database, add_to_database

config = load_config()

def get_the_mails(config=config):
    # get the credentials
    gmail_client = GmailClient(config)
    # Date range from a week back to today 
    start_date,end_date = get_date_range(config)
    # fetch emails
    fetcher = EmailFetcher(gmail_client,config)
    mails = fetcher.get_newsletter_mails(start_date=start_date,end_date=end_date,label = 'Newsletter')
    print(f'Fetched all the Newsletters from {start_date} to {end_date}')
    return mails


def preprocess_mails(mails):
    processed_mails = []
    for mail in mails:
        preprocess = Preprocess(mail)
        preprocess.remove_links()
        preprocess.parse_html_file()
        preprocess.remove_unwanted_chars()
        preprocess.decode_urls()
        preprocess.clean()
        processed_mails.append(preprocess.mail)
    return processed_mails

if __name__ == '__main__':
    mails = get_the_mails()
    print('Cleaning the mails...')
    cleaned_mails = preprocess_mails(mails)
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')

    google_key = os.getenv('google_api_key')
    summary_generator = NewsletterSummarizer(api_key= google_key)

    # for mail in cleaned_mails[:3]:
    #     print('----------------------------------------------------------------------------------')
    #     print(f'Summary for {mail['id']}: {summary_generator.generate_summary(mail['body'])}')
    #     print('----------------------------------------------------------------------------------')
    #     print()
    cleaned_mails = [
        {**mail, 'summary': summary_generator.generate_summary(mail['body'])} 
        for mail in cleaned_mails
    ]

    page_id = os.getenv('page_id')
    # database_id = os.getenv('Database_id')
    Notion_token = os.getenv('Notion_token')
    headers = {
    "Authorization": "Bearer " + Notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
    }
    start_date,end_date = get_date_range(config)
    title = f'Newsletters from: {start_date} to {end_date}'
    [print(len(mail['summary'])) for mail in cleaned_mails]
    database_id = create_database(page_id=page_id,headers=headers,title = title)
    print(f'database_id: {database_id}')
    print(f'page_id: {page_id}')
    print(f'Notion_token: {Notion_token}')
    add_to_database(headers=headers,database_id=database_id,email_list=cleaned_mails)

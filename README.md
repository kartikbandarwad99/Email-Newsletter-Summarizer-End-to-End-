# Gmail and Notion Automation Project

This project automates the process of fetching emails from Gmail, summarizing their content, and storing the summarized data into Notion databases. The system is designed to streamline workflows, leveraging APIs and summarization techniques.

---

## 📁 Directory Structure

``` 
Gmail_try
├── config
│   └── config.yml                
├── scripts
│   └── main.py                   
├── src
│   ├── Gmail
│   │   ├── __init__.py           
│   │   ├── client.py             
│   │   └── fetcher.py            
│   ├── Notion
│   │   ├── __init__.py           
│   │   ├── client.py            
│   │   └── preprocess.py         
│   ├── Summarization
│   │   ├── Summarizer
│   │   │   └── summarizer.py     
│   │   └── email_preprocessor
│   │       ├── __init__.py       
│   │       └── preprocess.py    
│   └── utils
│       └── helper.py             
├── .gitignore                    
├── requirements.txt              
└── .github
    └── workflows
        └── actions.yml           
```
## 🛠️ Setup Instructions

### Prerequisites

- Python 3.9
- Gmail API and Notion API credentials
- `pip` for installing dependencies

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kartikbandarwad99/Email-Newsletter-Summarizer-End-to-End-
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your configuration:

   - Add the following to `config/config.yml`:

     - **Gmail Credentials**: Path to `credentials.json` and `token.json`, along with Gmail API scopes.
     - **Email Fetch Settings**: Configure the default label (`INBOX`), date range (e.g., emails from the last 7 days), supported MIME types (`text/plain` or `text/html`), maximum number of emails to fetch, and fields to extract (e.g., `id`, `subject`, `from`, `body`).
     - **Logging**: Define logging level (e.g., `INFO`), log format, and log handlers (e.g., file-based logs with rotation and console logs).
     - **Error Handling**: Specify maximum retries, retry delay, and notification settings for failures.

## 🚀 How to Run

#### Configure Secrets
- Set up `credentials.json`, `token.json`, google api key and Notion API credentials as GitHub Secrets for secure access.
- For larger files like `credentials.json` and `token.json`, encode them as base64 strings and decode them dynamically during execution. Refer to the `.github/workflows/actions.yml` file for the encoding and decoding process.
- **Note**: Encoding smaller secrets like `google_api_key`, `Notion_token`, and `page_id` didn't work for me
- 
#### Run the Script
- Execute the following command to run the script:

    ```bash
    python -m scripts.main
    ```

## 📂 Modules and Key Features

1. **Gmail Module**
   - `client.py`: Sets up Gmail API authentication.
   - `fetcher.py`: Fetches emails based on user-defined criteria.
   - 
2. **Notion Module**
   - `client.py`: Handles interactions with Notion databases, including adding data to existing databases, creating new databases, and deleting databases.

3. **Summarization Module**
   - `Summarizer/summarizer.py`: Summarizes the email content using google's gemini model.
   - `email_preprocessor/preprocess.py`: Cleans and tokenizes email content.

4. **Utilities**
   - `helper.py`: Contains helper functions shared across modules.
  
## ⚙️ GitHub Actions

The workflow defined in `.github/workflows/actions.yml` performs the following:

- **Scheduled Runs**: Executes automatically every 7 days.
- **Code Quality**: Ensures the integrity of the codebase and automation pipeline.

## 🛡️ Security Notes

- Add `credentials.json`, `token.json`, and other sensitive files to `.gitignore` to prevent them from being committed to version control.
- Store secrets securely using environment variables or CI/CD platforms (e.g., GitHub Actions Secrets).

## 💬 Feedback

If you have any thoughts, suggestions, or run into issues, feel free to:

- Reach out to me directly at [kbandarwad@gmail.com].

Your input is greatly appreciated and helps me make this project even better. Thank you! 😊

## 📜 License

This project is licensed under the [MIT License](LICENSE).




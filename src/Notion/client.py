import requests 
from datetime import datetime
DATABASE_SCHEMA = {
    "From": {
        "title": {}
    },
    "Subject": {
        "rich_text": {}
    },
    "Summary": {
        "rich_text": {}
    },
    "Links": {
        "rich_text": {}
    },
    "Date": {
        "date": {}
    }
}

def create_database(headers, page_id, title="Email Database"):
    database_data = {
        "parent": {
            "type": "page_id",
            "page_id": page_id
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": title
                }
            }
        ],
        "properties": DATABASE_SCHEMA  # Use the global schema
    }

    url = "https://api.notion.com/v1/databases"
    response = requests.post(url, headers=headers, json=database_data)
    
    if response.status_code == 200:
        print("Database created successfully!")
        print("Database ID:", response.json()["id"])
        return response.json()["id"]
    else:
        print("Error creating database:", response.status_code)
        print(response.json())
        return None

def split_text_into_chunks(text, chunk_size=2000):
    """Splits text into chunks of specified size."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def add_to_database(headers, database_id, email_list):
    url = "https://api.notion.com/v1/pages"

    for email_data in email_list:
        # Prepare the properties for the email
        summary_i = email_data.get("summary", "")
        content_chunks = split_text_into_chunks(email_data.get("summary", ""), 2000)

        properties = {
            "From": {
                "title": [{ "type": "text", "text": {"content": email_data.get("from", "")} }]
            },
            "Subject": {
                "rich_text": [{ "type": "text", "text": {"content": email_data.get("subject", "")} }]
            },
            "Summary": {
                "rich_text": [{"type": "text", "text": {"content": chunk}} for chunk in content_chunks]
            },
            "Links": {
                "rich_text": [
                    {"type": "text", "text": {"content": f"Link {i + 1}\n", "link": {"url": url}}}
                    for i, url in enumerate(email_data.get("links", []))
                ]
            },
            "Date": {
                "date": {"start": datetime.strptime(email_data.get("date", "").replace(" (UTC)", ""), "%a, %d %b %Y %H:%M:%S %z").date().strftime('%Y-%m-%d')}
            }
        }

        data = {
            "parent": { "type": "database_id", "database_id": database_id },
            "properties": properties
        }

        # Post to Notion API
        response = requests.post(url, headers=headers, json=data)

        # Log the result
        if response.status_code == 200:
            print(f"Successfully added email: {email_data.get('subject', 'No Subject')}")
        else:
            print(f"Failed to add email: {email_data.get('subject', 'No Subject')} (Status Code: {response.status_code})")
            print(response.json())

# def create_database(data,headers):
#     url = "https://api.notion.com/v1/databases"
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         print("Database created successfully!")
#         print("Database ID:", response.json()["id"])
#     else:
#         print("Error:", response.status_code)
#         print(response.json())

def delete_database(database_id,headers):
    url = f"https://api.notion.com/v1/blocks/{database_id}"
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print("Database successfully deleted!")
    else:
        print("Error:", response.status_code)
        print(response.json())
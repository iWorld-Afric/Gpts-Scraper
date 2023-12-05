
import requests
import json
import openai
import csv
import os
import time
import logging
from config.settings import OPENAI_API_KEY

# Set up logging
log_file = os.path.join('logs', 'scraper_errors.log')
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize the OpenAI client with the API key directly
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Function to add a delay between API calls to prevent rate limiting
def rate_limit_delay():
    time.sleep(1)  # Delay for 1 second

def process_raw_data(url, raw_text):
    # Construct the payload for the POST request
    prompt = (
        f"URL: {url}\n\n"
        "Here is some raw text:\n"
        f"{raw_text}\n\n"
        "I need you to analyze and classify this information into the following categories:\n"
        "- Name: (The name or title)\n"
        "- Description: (A brief description of what it is about)\n"
        "- Instructions: (Instructions or usage information)\n"
        "- Additional Info: (Any other relevant information)\n"
        "Please provide the classified information under these categories."
    )

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    # Headers for the POST request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    try:
        # Make the POST request to the OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        # Assuming the response's content is in JSON format
        response_json = response.json()
        return response_json['choices'][0]['message']['content'].strip()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    return None  # Return None if there was an error

def parse_processed_data(processed_data):
    # Parse the processed_data string to extract name, description, instructions, and additional info
    # Example format: "Name: XYZ\nDescription: ABC\nInstructions: 123\nAdditional Info: None"
    data_parts = processed_data.split('\n')
    data = {'name': '', 'description': '', 'instructions': '', 'additional_info': ''}
    
    for part in data_parts:
        if part.startswith('Name:'):
            data['name'] = part[len('Name:'):].strip()
        elif part.startswith('Description:'):
            data['description'] = part[len('Description:'):].strip()
        elif part.startswith('Instructions:'):
            data['instructions'] = part[len('Instructions:'):].strip()
        elif part.startswith('Additional Info:'):
            data['additional_info'] = part[len('Additional Info:'):].strip()

    return data

def process_and_save_data(url, raw_text):
    processed_text = process_raw_data(url, raw_text)
    if processed_text:
        data = parse_processed_data(processed_text)
        if data:
            # Check if the CSV file exists, create if not
            csv_file = 'outputs/scraped_data.csv'
            file_exists = os.path.isfile(csv_file)

            with open(csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Write headers if the file is new
                if not file_exists:
                    writer.writerow(['Name', 'Description', 'Instructions', 'Additional Information'])
                # Write the data
                writer.writerow([data['name'], data['description'], data['instructions'], data['additional_info']])
        else:
            logging.error(f"Unable to parse processed data: {processed_text}")
    else:
        logging.error(f"No processed text returned for URL: {url}")

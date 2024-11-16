# Tyson Discord Bot

A Twitter bot that generates humorous and philosophical X posts in the style of Mike Tyson, focusing on topics related to Jake Paul and boxing. The bot utilizes the Groq API for generating responses and sends them to a specified Discord webhook.

## Features

- Generates dynamic topics and contexts with an 80% focus on Jake Paul.
- Creates engaging prompts for Mike Tyson's character.
- Sends concise and entertaining posts to a X
- Utilizes environment variables for API keys and webhook URLs.

## Requirements

- Python 3.7+
- `requests` library
- `dotenv` library
- `groq` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/miketysonai/miketysonai.git
   cd miketysonai
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Update the X & Groq variables to be your API keys

## Usage

Run the bot using:
```bash
python webhook.py
```


The bot will start generating tweets and sending them on your X account.


## License

This project is licensed under the MIT License.

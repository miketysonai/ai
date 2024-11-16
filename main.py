import os
import time
import random
import logging
from datetime import datetime
from typing import Optional, Tuple
from groq import Groq
import tweepy

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API credentials
TWITTER_CONSUMER_KEY = "your_consumer_key_here"
TWITTER_CONSUMER_SECRET = "your_consumer_secret_here"
TWITTER_ACCESS_TOKEN = "your_access_token_here"
TWITTER_ACCESS_TOKEN_SECRET = "your_access_token_secret_here"
TWITTER_BEARER_TOKEN = "your_bearer_token_here"
GROQ_API_KEY = "your_groq_api_here"

# Topics that Mike might tweet about
TOPICS = [
    "boxing",
    "life lessons",
    "training",
    "motivation",
    "success",
    "challenges",
    "philosophy",
    "pigeons",
    "Jake Paul fight",
    "fight preparation",
    "upcoming match",
    "fight predictions",
    "training camp",
    "fight promotion"
]

# Define OTHER_TOPICS dictionary
OTHER_TOPICS = {
    "philosophical": [
        "the meaning of life",
        "the nature of success",
        "overcoming adversity"
    ],
    "boxing": [
        "the importance of training",
        "the psychology of a fight",
        "strategies for victory"
    ],
    "personal": [
        "life lessons learned",
        "mentoring young fighters",
        "the role of discipline"
    ]
}

class TysonBot:
    def __init__(self):
        # Initialize Twitter client with bearer token
        self.twitter = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            wait_on_rate_limit=True  # Automatically handles rate limiting
        )
        
        # Initialize Groq client
        self.groq = Groq(api_key=GROQ_API_KEY)

    def generate_prompt(self) -> str:
        """Generate a random prompt for Mike to respond to"""
        topic, context = self.generate_topic_and_context()
        
        prompts = [
            f"Hey Mike, {context}, share your thoughts about {topic}. Keep it engaging and insightful.",
            f"While {context}, give your perspective on {topic}. Make it thought-provoking.",
            f"During {context}, reflect on {topic}. Share your wisdom.",
            f"{context} - what insights do you have about {topic}?"
        ]
        return random.choice(prompts)

    def generate_topic_and_context(self) -> Tuple[str, str]:
        """Generate a topic and context with 80% chance of Jake Paul focus"""
        if random.random() < 0.8:  # 80% chance of Jake Paul topic
            topic = random.choice(TOPICS)
            contexts = [
                "while hitting the heavy bag",
                "during media face-off",
                "at the press conference",
                "watching his YouTube videos",
                "during weigh-in",
                "in the locker room",
                "during fight prep",
                "while shadow boxing",
                "during interview",
                "at fight promotion"
            ]
        else:
            category = random.choice(list(OTHER_TOPICS.keys()))
            topic = random.choice(OTHER_TOPICS[category])
            contexts = {
                "philosophical": [
                    "during morning meditation",
                    "while feeding pigeons",
                    "reflecting in solitude"
                ],
                "boxing": [
                    "during training",
                    "between rounds",
                    "watching old fights"
                ],
                "personal": [
                    "thinking about the past",
                    "talking to young fighters",
                    "visiting the gym"
                ]
            }[category]
        
        return topic, random.choice(contexts)

    def get_tyson_response(self, prompt: str) -> Optional[str]:
        """Get a response using Groq"""
        system_prompt = """You are Mike Tyson on the day of your fight with Jake Paul. 
        Respond in your distinctive speaking style and personality. Keep responses under 280 characters. 
        Use your characteristic speech patterns ('th' instead of 's' sounds) and perspective.
        Be intense, confident, and philosophical. Reference the upcoming fight with Jake Paul occasionally.
        You're excited but focused, ready to show that experience beats youth.
        
        Example responses:
        "Thlike the great philothopherth thaid - everyone hath a plan until they get punched in the mouth. Jake'th about to learn thith truthth tonight. #TysonPaul"
        
        "My pigeonth are more focused than Jake Paul right now. When that bell ringth, experience will devour youth. Bathic physics. #IronMike"
        """
        
        try:
            response = self.groq.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
                temperature=0.9,  # Add some randomness to responses
                max_tokens=100    # Keep responses concise
            )
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating Groq response: {e}")
            return None

    def clean_response(self, response: Optional[str]) -> Optional[str]:
        """Clean and format the response to fit Twitter's requirements"""
        if not response:
            return None
        
        # Trim to Twitter's max length
        cleaned = response[:279]
        
        # Remove quotes if they exist
        cleaned = cleaned.strip('"')
        
        # Add fight-related hashtags if they're not already present
        hashtags = " #TysonPaul #IronMike #Boxing"
        if not any(tag.lower() in cleaned.lower() for tag in ["#tysonpaul", "#ironmike", "#boxing"]):
            if len(cleaned) + len(hashtags) <= 279:
                cleaned += hashtags
                
        return cleaned

    def post_tweet(self, text: str) -> bool:
        """Post a tweet using Twitter API v2"""
        try:
            response = self.twitter.create_tweet(text=text)
            logger.info(f"Tweet posted successfully: {text}")
            return True
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False

    def run_bot(self):
        """Main loop to run the bot"""
        while True:
            try:
                # Generate and post tweet
                prompt = self.generate_prompt()
                response = self.get_tyson_response(prompt)
                cleaned_response = self.clean_response(response)
                
                if cleaned_response:
                    success = self.post_tweet(cleaned_response)
                    if success:
                        logger.info("Successfully posted tweet using Groq")
                    
                # Wait 10 minutes
                logger.info("Waiting 10 minutes until next tweet...")
                time.sleep(600)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(60)  # Wait a minute before retrying if there's an error

if __name__ == "__main__":
    logger.info("Starting Mike Tyson Twitter Bot...")
    bot = TysonBot()
    bot.run_bot()
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

import os

load_dotenv(find_dotenv(), override=False)

@dataclass
class BotConfig:
    bot_token: str = os.getenv("BOT_TOKEN")


@dataclass
class OpenAIConfig:
    model_name: str = 'gpt-4o-mini'
    api_key: str = os.getenv("OPENAI_API_KEY")
    chat_history_tokens: int = 1000
    recursion_limit: int = 10
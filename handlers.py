from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from utils import clean_markdown_text
from langchain_core.messages import HumanMessage


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот для веб-поиска. Задайте мне вопрос, и я помогу найти информацию в Интернете.")


@router.message(F.text)
async def handle_message(message: Message, bot: Bot):
    agent = bot.agent
    user_id = message.from_user.id
    user_context = f"User id :{user_id}, Username :{message.from_user.username}, User first name :{message.from_user.first_name}, User last name :{message.from_user.last_name}, User language code :{message.from_user.language_code}"

    process_msg = await message.answer("🤔 Секундочку, ищу информацию для вас...")
    config = {
        "configurable": {
            "thread_id": user_id, 
            "user": user_context,
        }
        }
    
    messages = [HumanMessage(content=message.text)]

    response = await agent.ainvoke(
        {"messages": messages},
        config=config
    )

    last_message = response["messages"][-1]

    result = clean_markdown_text(last_message.content)

    await message.answer(result)

    await bot.delete_message(message.chat.id, process_msg.message_id)

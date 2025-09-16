import re

def clean_markdown_text(text: str) -> str:

    try:
        cleaned = text
        
        # Убираем жирный текст **bold** -> bold
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)
        # Убираем курсив *italic* -> italic  
        cleaned = re.sub(r'\*(.*?)\*', r'\1', cleaned)
        # Убираем подчеркивания __underline__ -> underline
        cleaned = re.sub(r'__(.*?)__', r'\1', cleaned)
        # Убираем заголовки ## header -> header
        cleaned = re.sub(r'#{1,6}\s*', '', cleaned)
        # Убираем лишние пробелы и переносы
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)  # Множественные переносы
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)       # Множественные пробелы
        
        return cleaned.strip()
        
    except Exception as e:
        print(f"[Markdown Cleaner] ❌ Error cleaning markdown: {e}")
        return text

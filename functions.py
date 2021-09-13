from typing import Any





async def parse_and_recognize_command(text: str) -> Any:
    if text and text[0] == '!':
        message = text[1:].split()
        if message[0] in COMMANDS:

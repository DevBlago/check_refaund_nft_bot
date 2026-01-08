from aiogram.types import BotCommand
from typing import List

from src.lexicon import MainMenu

def get_main_menu_commands() -> List[BotCommand]:
    menu_commands = {
        "/start": MainMenu.start,
    }
    
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in menu_commands.items()
    ]
    return main_menu_commands
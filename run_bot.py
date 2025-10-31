#!/usr/bin/env python3
"""
Запуск Telegram-бота для Print3DUz
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == '__main__':
    # Import and run the bot
    from bot.main import main
    main()
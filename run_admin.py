#!/usr/bin/env python3
"""
Запуск админ-панели для Print3DUz
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == '__main__':
    # Import and run the Flask app
    from admin.app import app
    app.run(debug=True, host='0.0.0.0', port=5000)
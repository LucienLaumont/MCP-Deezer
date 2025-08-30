#!/usr/bin/env python3
"""
Entry point script to run the Deezer MCP server.
This script can be used directly from Claude Desktop configuration.
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the server
from mcp_deezer.server import main

if __name__ == "__main__":
    # Configure logging for debugging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('deezer_mcp_server.log'),
            logging.StreamHandler()
        ]
    )
    
    # Run the server
    asyncio.run(main())
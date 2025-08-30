#!/usr/bin/env python3
"""
Automatic installation script for MCP Deezer.
Automatically configures Claude Desktop to use the MCP Deezer server.
"""

import json
import os
import platform
import sys
from pathlib import Path
import shutil

def get_claude_config_path():
    """Returns the path to the Claude Desktop MCP configuration file."""
    system = platform.system()
    
    if system == "Windows":
        return Path(os.getenv("APPDATA")) / "Claude" / "claude_desktop_config.json"
    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Linux":
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    else:
        raise Exception(f"Unsupported operating system: {system}")

def check_python_version():
    """Verifies that Python 3.8+ is installed."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        raise Exception(f"Python 3.8+ required. Current version: {version.major}.{version.minor}")
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")

def install_dependencies():
    """Installs Python dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Dependencies installed successfully")
        else:
            print(f"❌ Error installing dependencies:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False
    
    return True

def backup_config(config_path):
    """Backs up the existing configuration file."""
    if config_path.exists():
        backup_path = config_path.with_suffix('.json.backup')
        shutil.copy2(config_path, backup_path)
        print(f"✓ Configuration backed up: {backup_path}")

def update_claude_config():
    """Updates the Claude Desktop configuration."""
    config_path = get_claude_config_path()
    project_root = Path(__file__).parent.absolute()
    
    # Create configuration directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Backup existing configuration
    backup_config(config_path)
    
    # Load existing configuration or create new one
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("⚠️ Corrupted configuration file, creating new one")
            config = {}
    else:
        config = {}
    
    # Add MCP configuration
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Path to launch script and Python virtual environment
    run_script_path = project_root / "run_server.py"
    
    # Configuration for Windows vs Unix
    if platform.system() == "Windows":
        script_path_str = str(run_script_path).replace("/", "\\")
        python_path = str(project_root / ".venv" / "Scripts" / "python.exe").replace("/", "\\")
    else:
        script_path_str = str(run_script_path)
        python_path = str(project_root / ".venv" / "bin" / "python")
    
    config["mcpServers"]["deezer-api"] = {
        "command": python_path,
        "args": [script_path_str],
        "env": {
            "DEEZER_BASE_URL": "https://api.deezer.com"
        }
    }
    
    # Write new configuration
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Claude Desktop configuration updated: {config_path}")
    return True

def test_installation():
    """Basic installation test."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test server import
        sys.path.insert(0, str(Path(__file__).parent))
        import mcp_deezer.server
        print("✓ MCP server imported successfully")
        
        # Test client imports
        from mcp_deezer.functions.deezer_client.track import TrackNameClient
        from mcp_deezer.functions.deezer_client.artist import ArtistNameClient
        print("✓ Deezer clients imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main installation function."""
    print("🎵 MCP Deezer Installation for Claude Desktop")
    print("=" * 50)
    
    try:
        # Preliminary checks
        check_python_version()
        
        # Install dependencies
        if not install_dependencies():
            sys.exit(1)
        
        # Configure Claude Desktop
        print(f"\n⚙️ Configuring Claude Desktop...")
        if not update_claude_config():
            sys.exit(1)
        
        # Test installation
        if not test_installation():
            sys.exit(1)
        
        print("\n🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Restart Claude Desktop completely")
        print("2. Test with a query like: 'Find information about Daft Punk'")
        print("3. If issues occur, check logs in 'deezer_mcp_server.log'")
        
    except Exception as e:
        print(f"\n❌ Installation error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Claude Desktop is closed")
        print("2. Try running as administrator if necessary")
        print("3. Check permissions on the Claude folder")
        sys.exit(1)

if __name__ == "__main__":
    main()
# 🎵 MCP Deezer API Server

A professional MCP (Model Context Protocol) server that enables Claude Desktop to access the Deezer API for searching tracks, artists, albums, and playlists with comprehensive music data retrieval.

## 🚀 Features

- **🎵 Track Search** - Search by name or artist with detailed metadata
- **🎤 Artist Search** - Comprehensive artist information with statistics
- **💿 Album Search** - Full album details with track count and release dates
- **🎼 Playlist Search** - Public and private playlists with advanced filtering

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Claude Desktop** application installed and configured
- Active internet connection for Deezer API access

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/MCP-Deezer.git
cd MCP-Deezer
```

### 2. Set Up Virtual Environment and Install Dependencies

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Claude Desktop Configuration

#### **Windows:**

1. Locate your Claude Desktop MCP configuration file:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add this configuration to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "deezer-api": {
      "command": "CHEMIN_COMPLET_VERS_VOTRE_PROJET\\MCP-Deezer\\.venv\\Scripts\\python.exe",
      "args": [
        "ABSOLUTE_PATH_TO_YOUR_PROJECT\\MCP-Deezer\\run_server.py"
      ],
      "env": {
        "DEEZER_BASE_URL": "https://api.deezer.com"
      }
    }
  }
}
```

**⚠️ Important:** 
- Replace `ABSOLUTE_PATH_TO_YOUR_PROJECT` with the actual path to your project folder
- Use the Python executable from the virtual environment (`.venv\Scripts\python.exe`)

#### **macOS/Linux:**

The MCP configuration file is typically located at:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Use forward slashes (`/`) for paths and `.venv/bin/python` for the Python executable.

### 4. Restart Claude Desktop

Close Claude Desktop completely and restart the application.

## 🎯 Usage

Once configured, you can use these commands in Claude Desktop:

### Example Queries:

```
Find information about the artist Daft Punk
```

```
Search for the track "Blinding Lights" by The Weeknd
```

```
Find the album "Random Access Memories"
```

```
Search for popular playlists with "Rock"
```

```
Give me 5 tracks by Ed Sheeran
```

## 🔧 Installation Testing

To verify everything works correctly, you can test the server manually:

```bash
python test_deezer_clients.py
```

This script tests all clients with popular Deezer content.

## 🛠️ Available MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_track` | Search for a track | `track_name`, `limit` (optional) |
| `search_track_by_artist` | Search track by artist | `track_name`, `artist_name` |
| `search_artist` | Search for an artist | `artist_name`, `limit` (optional) |
| `search_album` | Search for an album | `album_name`, `limit` (optional) |
| `search_playlist` | Search for playlists | `playlist_name`, `limit`, `public_only` |

## 📁 Project Structure

```
MCP-Deezer/
├── mcp_deezer/
│   ├── functions/
│   │   └── deezer_client/
│   │       ├── base.py          # Base HTTP client
│   │       ├── track.py         # Track search client
│   │       ├── artist.py        # Artist search client  
│   │       ├── album.py         # Album search client
│   │       └── playlist.py      # Playlist search client
│   ├── server.py                # Main MCP server
│   └── types.py                 # Pydantic type definitions
├── run_server.py                # Server entry point
├── test_deezer_clients.py       # Client testing suite
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🐛 Troubleshooting

### Server Won't Start
1. Verify Python is installed: `python --version`
2. Check dependencies are installed: `pip install -r requirements.txt`
3. Ensure you're using the virtual environment Python executable
4. Check logs for error messages

### Claude Desktop Can't See the Server
1. Verify the path in `claude_desktop_config.json`
2. Ensure Claude Desktop has been completely restarted
3. Verify `claude_desktop_config.json` is valid JSON
4. Check **Developer > Local MCP Servers** to verify configuration

### API Errors
- The Deezer API is public and requires no authentication key
- Verify your internet connection
- Some content may be unavailable based on your region

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Lucien Laumont**  
📧 [laumontlucien@gmail.com](mailto:laumontlucien@gmail.com)

## 🙏 Acknowledgments

- [Deezer](https://www.deezer.com/) for providing their public API
- [Anthropic](https://www.anthropic.com/) for Claude and the MCP protocol
- The Python community for excellent libraries and tools

---

**Built with ❤️ for the Claude Desktop community**
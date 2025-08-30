#!/usr/bin/env python3
"""
Script d'installation automatique pour MCP Deezer.
Configure automatiquement Claude Desktop pour utiliser le serveur MCP Deezer.
"""

import json
import os
import platform
import sys
from pathlib import Path
import shutil

def get_claude_config_path():
    """Retourne le chemin vers le fichier de configuration Claude Desktop."""
    system = platform.system()
    
    if system == "Windows":
        return Path(os.getenv("APPDATA")) / "Claude" / "config.json"
    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "config.json"
    elif system == "Linux":
        return Path.home() / ".config" / "Claude" / "config.json"
    else:
        raise Exception(f"Système d'exploitation non supporté: {system}")

def check_python_version():
    """Vérifie que Python 3.8+ est installé."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        raise Exception(f"Python 3.8+ requis. Version actuelle: {version.major}.{version.minor}")
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} détecté")

def install_dependencies():
    """Installe les dépendances Python."""
    print("\n📦 Installation des dépendances...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Dépendances installées avec succès")
        else:
            print(f"❌ Erreur lors de l'installation des dépendances:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False
    
    return True

def backup_config(config_path):
    """Sauvegarde le fichier de configuration existant."""
    if config_path.exists():
        backup_path = config_path.with_suffix('.json.backup')
        shutil.copy2(config_path, backup_path)
        print(f"✓ Configuration sauvegardée: {backup_path}")

def update_claude_config():
    """Met à jour la configuration Claude Desktop."""
    config_path = get_claude_config_path()
    project_root = Path(__file__).parent.absolute()
    
    # Créer le dossier de configuration s'il n'existe pas
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder la configuration existante
    backup_config(config_path)
    
    # Charger la configuration existante ou créer une nouvelle
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("⚠️ Fichier de configuration corrompu, création d'un nouveau")
            config = {}
    else:
        config = {}
    
    # Ajouter la configuration MCP
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Chemin vers le script de lancement
    run_script_path = project_root / "run_server.py"
    
    # Configuration pour Windows vs Unix
    if platform.system() == "Windows":
        script_path_str = str(run_script_path).replace("/", "\\")
    else:
        script_path_str = str(run_script_path)
    
    config["mcpServers"]["deezer-api"] = {
        "command": "python",
        "args": [script_path_str],
        "env": {
            "DEEZER_BASE_URL": "https://api.deezer.com"
        }
    }
    
    # Écrire la nouvelle configuration
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Configuration Claude Desktop mise à jour: {config_path}")
    return True

def test_installation():
    """Test basique de l'installation."""
    print("\n🧪 Test de l'installation...")
    
    try:
        # Test d'import du serveur
        sys.path.insert(0, str(Path(__file__).parent))
        import mcp_deezer.server
        print("✓ Serveur MCP importé avec succès")
        
        # Test d'import des clients
        from mcp_deezer.functions.deezer_client.track import TrackNameClient
        from mcp_deezer.functions.deezer_client.artist import ArtistNameClient
        print("✓ Clients Deezer importés avec succès")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale d'installation."""
    print("🎵 Installation MCP Deezer pour Claude Desktop")
    print("=" * 50)
    
    try:
        # Vérifications préliminaires
        check_python_version()
        
        # Installation des dépendances
        if not install_dependencies():
            sys.exit(1)
        
        # Configuration de Claude Desktop
        print(f"\n⚙️ Configuration de Claude Desktop...")
        if not update_claude_config():
            sys.exit(1)
        
        # Test de l'installation
        if not test_installation():
            sys.exit(1)
        
        print("\n🎉 Installation terminée avec succès !")
        print("\n📋 Prochaines étapes :")
        print("1. Redémarrez Claude Desktop complètement")
        print("2. Testez avec une requête comme : 'Trouve-moi des infos sur Daft Punk'")
        print("3. En cas de problème, consultez les logs dans 'deezer_mcp_server.log'")
        
    except Exception as e:
        print(f"\n❌ Erreur d'installation: {e}")
        print("\n🔧 Dépannage :")
        print("1. Vérifiez que Claude Desktop est fermé")
        print("2. Réessayez en tant qu'administrateur si nécessaire")
        print("3. Vérifiez les permissions sur le dossier Claude")
        sys.exit(1)

if __name__ == "__main__":
    main()
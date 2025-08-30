# 🎵 MCP Deezer API Server

Un serveur MCP (Model Context Protocol) qui permet à Claude Desktop d'accéder à l'API Deezer pour rechercher des titres, artistes, albums et playlists.

## 🚀 Fonctionnalités

- **🎵 Recherche de titres** - Par nom ou par artiste
- **🎤 Recherche d'artistes** - Informations détaillées et statistiques
- **💿 Recherche d'albums** - Avec nombre de pistes et date de sortie
- **🎼 Recherche de playlists** - Publiques et privées avec filtres

## 📋 Prérequis

- **Python 3.8+** installé sur votre système
- **Claude Desktop** installé et fonctionnel
- Connexion internet pour accéder à l'API Deezer

## 🛠️ Installation

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/MCP-Deezer.git
cd MCP-Deezer
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration de Claude Desktop

#### **Windows :**

1. Localisez votre fichier de configuration Claude Desktop :
   ```
   %APPDATA%\Claude\config.json
   ```

2. Ajoutez cette configuration à votre fichier `config.json` :

```json
{
  "mcpServers": {
    "deezer-api": {
      "command": "python",
      "args": [
        "CHEMIN_COMPLET_VERS_VOTRE_PROJET\\MCP-Deezer\\run_server.py"
      ],
      "env": {
        "DEEZER_BASE_URL": "https://api.deezer.com"
      }
    }
  }
}
```

**⚠️ Important :** Remplacez `CHEMIN_COMPLET_VERS_VOTRE_PROJET` par le chemin réel vers votre dossier.

#### **macOS/Linux :**

Le fichier de configuration se trouve généralement dans :
```
~/Library/Application Support/Claude/config.json
```

Utilisez des barres obliques normales (`/`) dans les chemins.

### 4. Redémarrer Claude Desktop

Fermez complètement Claude Desktop et relancez-le.

## 🎯 Utilisation

Une fois configuré, vous pouvez utiliser ces commandes dans Claude Desktop :

### Exemples de requêtes :

```
Trouve-moi des informations sur l'artiste Daft Punk
```

```
Cherche le titre "Blinding Lights" par The Weeknd
```

```
Trouve l'album "Random Access Memories"
```

```
Cherche des playlists populaires avec "Rock"
```

```
Donne-moi 5 titres de Ed Sheeran
```

## 🔧 Test de l'installation

Pour vérifier que tout fonctionne, vous pouvez tester le serveur manuellement :

```bash
python test_deezer_clients.py
```

Ce script teste tous les clients avec du contenu populaire de Deezer.

## 🛠️ Outils MCP disponibles

| Outil | Description | Paramètres |
|-------|-------------|------------|
| `search_track` | Chercher un titre | `track_name`, `limit` (optionnel) |
| `search_track_by_artist` | Chercher un titre par artiste | `track_name`, `artist_name` |
| `search_artist` | Chercher un artiste | `artist_name`, `limit` (optionnel) |
| `search_album` | Chercher un album | `album_name`, `limit` (optionnel) |
| `search_playlist` | Chercher une playlist | `playlist_name`, `limit`, `public_only` |

## 📁 Structure du projet

```
MCP-Deezer/
├── mcp_deezer/
│   ├── functions/
│   │   └── deezer_client/
│   │       ├── base.py          # Client de base
│   │       ├── track.py         # Client pour les titres
│   │       ├── artist.py        # Client pour les artistes  
│   │       ├── album.py         # Client pour les albums
│   │       └── playlist.py      # Client pour les playlists
│   ├── server.py                # Serveur MCP principal
│   └── types.py                 # Types Pydantic
├── run_server.py                # Script de lancement
├── test_deezer_clients.py       # Tests des clients
├── requirements.txt             # Dépendances Python
└── README.md                    # Ce fichier
```

## 🐛 Dépannage

### Le serveur ne démarre pas
1. Vérifiez que Python est installé : `python --version`
2. Vérifiez les dépendances : `pip install -r requirements.txt`
3. Vérifiez les logs dans `deezer_mcp_server.log`

### Claude Desktop ne voit pas le serveur
1. Vérifiez le chemin dans `config.json`
2. Assurez-vous d'avoir redémarré Claude Desktop
3. Vérifiez que le fichier `config.json` est valide (JSON bien formé)

### Erreurs d'API
- L'API Deezer est publique et ne nécessite pas de clé
- Vérifiez votre connexion internet
- Certains contenus peuvent être indisponibles selon votre région

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commit vos changements
4. Push vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour les détails.

## 🙏 Remerciements

- [Deezer](https://www.deezer.com/) pour leur API publique
- [Anthropic](https://www.anthropic.com/) pour Claude et le protocole MCP
- La communauté Python pour les excellentes bibliothèques utilisées

---

**Made with ❤️ for the Claude Desktop community**
from config import get_settings

def main():
    settings = get_settings()
    print("🎵 API Deezer URL:", settings.deezer_base_url)
    print("🔑 Mistral API Key:", settings.mistral_api_key)

if __name__ == "__main__":
    main()

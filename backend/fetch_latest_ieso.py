import requests
import os


def download_latest_2026():
    # 1. Setup the Pathing (Always relative to this file)
    # This goes to project_root/data/raw/
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # If this script is in 'backend/', use '..' to go up to the project root
    target_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "raw"))
    save_path = os.path.join(target_dir, "PUB_DemandZonal_2026.csv")

    # 2. Safety Check: Make sure the folder exists before saving
    os.makedirs(target_dir, exist_ok=True)

    # 3. Disguise our request so IESO doesn't hang up on us
    url = "https://reports.ieso.ca/public/DemandZonal/PUB_DemandZonal_2026.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Fetching latest 2026 data from IESO...")

    try:
        # Use stream=True to download in chunks
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()

        # 4. The Save Logic: Write the file in small chunks
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        print(f"✅ Successfully updated: {save_path}")

    except requests.exceptions.HTTPError as e:
        print(f"❌ Site responded with an error: {e}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection was aborted. The server might be blocking automated requests.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    download_latest_2026()
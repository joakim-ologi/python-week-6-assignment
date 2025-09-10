import os
import requests
from urllib.parse import urlparse, unquote
import sys

def get_filename_from_url(url):
    """
    Extract filename from URL or generate one if not present.
    """
    path = urlparse(url).path
    filename = os.path.basename(path)
    filename = unquote(filename)  # Decode URL-encoded characters
    if not filename or '.' not in filename:
        # Generate a filename if no valid filename found in URL
        filename = "downloaded_image"
    return filename

def main():
    url = input("Enter the URL of the image: ").strip()
    if not url:
        print("No URL entered. Exiting.")
        return

    folder = "Fetched_Images"
    os.makedirs(folder, exist_ok=True)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Check if the content type is an image
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image'):
            print(f"Error: The URL does not point to an image. Content-Type: {content_type}")
            return

        filename = get_filename_from_url(url)
        # Ensure unique filename in folder
        base, ext = os.path.splitext(filename)
        if not ext or not ext.startswith('.'):
            # Try to guess extension from content-type
            if '/' in content_type:
                ext = '.' + content_type.split('/')[-1].split(';')[0]
            else:
                ext = '.jpg'  # default extension if none
        filename = base + ext

        filepath = os.path.join(folder, filename)
        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(folder, f"{base}_{counter}{ext}")
            counter += 1

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"Image saved to: {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

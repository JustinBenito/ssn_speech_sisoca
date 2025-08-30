import gdown

# Replace with your folder ID (from share link)
url = "https://drive.google.com/drive/folders/1Y7TtMrXAvwT1MLIggGkFt1Egijwmo3Xc?usp=sharing"

gdown.download_folder(url, quiet=False, use_cookies=False)

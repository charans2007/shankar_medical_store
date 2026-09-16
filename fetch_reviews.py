import urllib.request
import ssl
import json
import re

url = "https://www.google.com/search?client=ms-android-oneplus-terr1-rso2&hs=ozIB&sca_esv=6f3ccd550fd6cf18&cs=1&hl=en-IN&output=search&kgmid=/g/11f55jnyh5&q=Shankar+homoeo+stores&shem=epsd1,ltae,rimspwouoe&shndl=30&source=sh/x/loc/act/m1/4&kgs=084631fbe5f3335a&utm_source=epsd1,ltae,rimspwouoe,sh/x/loc/act/m1/4"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-IN,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
)

try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
        html = response.read().decode('utf-8', errors='ignore')
        print(f"Downloaded {len(html)} bytes")
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved page.html")
except Exception as e:
    print("Error:", e)

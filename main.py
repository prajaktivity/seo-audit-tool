from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SEO Audit API 🚀"}

@app.get("/seo-audit")
def seo_audit(url: str, keyword: str = ""):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title = soup.title.string if soup.title else "Missing"

        # Meta Description
        meta = soup.find("meta", attrs={"name": "description"})
        description = meta["content"] if meta else "Missing"

        # H1 Tags
        h1_tags = [h1.text.strip() for h1 in soup.find_all("h1")]

        # Images without ALT
        images = soup.find_all("img")
        missing_alt = sum(1 for img in images if not img.get("alt"))

        # ✅ KEYWORD LOGIC (ADD HERE)
        content = soup.get_text().lower()
        keyword_found = keyword.lower() in content if keyword else "Not checked"

        # SEO Score
        score = 100
        if title == "Missing":
            score -= 20
        if description == "Missing":
            score -= 20
        if len(h1_tags) == 0:
            score -= 20
        if missing_alt > 0:
            score -= 10

        return {
            "success": True,
            "data": {
                "title": title,
                "title_status": "Good" if title != "Missing" else "Missing",
                "meta_description": description,
                "h1_tags": h1_tags,
                "images_without_alt": missing_alt,
                "keyword_found": keyword_found,
                "seo_score": score
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup

router = APIRouter()

@router.get("/recommendations")
def get_recommendations(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        tips = []

        # Title check
        if not soup.title:
            tips.append("Add a proper title tag")

        # Meta description
        meta = soup.find("meta", attrs={"name": "description"})
        if not meta:
            tips.append("Add a meta description")

        # H1 check
        if len(soup.find_all("h1")) == 0:
            tips.append("Use at least one H1 tag")

        # Image ALT check
        images = soup.find_all("img")
        if any(not img.get("alt") for img in images):
            tips.append("Add ALT text to all images")

        # Default message
        if len(tips) == 0:
            tips.append("Your SEO looks good! Minor improvements possible.")

        return {
            "success": True,
            "tips": tips
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
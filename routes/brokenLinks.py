from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup

router = APIRouter()

@router.get("/broken-links")
def check_broken_links(url: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        links = [a.get("href") for a in soup.find_all("a") if a.get("href")]

        broken = []

        for link in links:
            if link.startswith("http"):
                try:
                    res = requests.get(link, timeout=3)
                    if res.status_code >= 400:
                        broken.append(link)
                except:
                    broken.append(link)

        return {
            "success": True,
            "data": {
                "total_links": len(links),
                "broken_links": broken,
                "broken_count": len(broken)
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
from fastapi import APIRouter
import requests
import re
from bs4 import BeautifulSoup


router = APIRouter()

@router.get("/keyword-density")
def keyword_density(url: str, keyword: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    content = re.sub(r'[^a-zA-Z0-9\s]', '', soup.get_text().lower())
    words = content.split()

    total_words = len(words)
    keyword_count = words.count(keyword.lower())

    density = round((keyword_count / total_words) * 100, 2)

    return {
        "keyword": keyword,
        "density": density
    }
from fastapi import FastAPI
from routes import seo, keyword
from routes import recommendations

app = FastAPI()

app.include_router(seo.router)
app.include_router(keyword.router)
app.include_router(recommendations.router)


@app.get("/")
def home():
    return {"message": "SEO Audit API 🚀"}
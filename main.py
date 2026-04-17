from fastapi import FastAPI
from routes import seo, keyword
from routes import recommendations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(seo.router)
app.include_router(keyword.router)
app.include_router(recommendations.router)


@app.get("/")
def home():
    return {"message": "SEO Audit API 🚀"}
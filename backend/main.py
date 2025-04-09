from fastapi import FastAPI
from routes.Newsroute import router as news_router

app = FastAPI()

# Inclusion du router pour les routes /news
app.include_router(news_router)

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur FastAPI avec Fedora!"}
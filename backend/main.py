from fastapi import FastAPI 

app = FastAPI()  # Crée une instance de l'application FastAPI

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur FastAPI avec Fedora!"}

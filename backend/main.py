from fastapi import FastAPI,HTTPException
from database import Database  # Assurez-vous que le fichier database.py est dans le même répertoire

app = FastAPI()  # Crée une instance de l'application FastAPI
database=Database()

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur FastAPI avec Fedora!"}


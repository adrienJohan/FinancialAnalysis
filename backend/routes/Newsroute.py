from fastapi import APIRouter, HTTPException
from database import Database  # Import de ta classe Database
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/news",
    tags=["news"],
    responses={404: {"description": "Not found"}},
)

class NewsCreate(BaseModel):
    ticker: str
    timestamp: datetime
    title: str
    description: str | None = None 
    source: str | None = None      

class NewsItem(NewsCreate):
    news_id: int

@router.get("/", response_model=list[NewsItem])
async def get_all_news():
    db = Database()
    try:
        results = db.query("SELECT news_id, ticker, timestamp, title, description, source FROM News", fetch=True)
        if not results:
            raise HTTPException(status_code=404, detail="Aucune news trouvée")
        news_list = [NewsItem(
            news_id=row[0],
            ticker=row[1],
            timestamp=row[2],
            title=row[3],
            description=row[4],
            source=row[5]
        ) for row in results]
        return news_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur base de données : {str(e)}")
    finally:
        db.close()

@router.post("/", response_model=NewsItem)
async def create_news(news: NewsCreate):
    db = Database()
    try:
        sql = """
            INSERT INTO News (ticker, timestamp, title, description, source)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (news.ticker, news.timestamp, news.title, news.description, news.source)
        db.query(sql, params, fetch=False)
        
        last_id = db.query("SELECT LAST_INSERT_ID()", fetch=True)[0][0]
        
        return NewsItem(
            news_id=last_id,
            ticker=news.ticker,
            timestamp=news.timestamp,
            title=news.title,
            description=news.description,
            source=news.source
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur base de données : {str(e)}")
    finally:
        db.close()

@router.get("/ticker/{ticker}", response_model=list[NewsItem])
async def get_news_by_ticker(ticker: str):
    db = Database()
    try:
        sql = "SELECT news_id, ticker, timestamp, title, description, source FROM News WHERE ticker = %s"
        results = db.query(sql, (ticker,), fetch=True)
        if not results:
            raise HTTPException(status_code=404, detail=f"Aucune news trouvée pour le ticker {ticker}")
        news_list = [NewsItem(
            news_id=row[0],
            ticker=row[1],
            timestamp=row[2],
            title=row[3],
            description=row[4],
            source=row[5]
        ) for row in results]
        return news_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur base de données : {str(e)}")
    finally:
        db.close()
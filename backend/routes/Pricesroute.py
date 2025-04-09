from fastapi import APIRouter, HTTPException

router=APIRouter(
    prefix="/prices",
    tags=["prices"],
    responses={404: {"description": "Not found"}},
)


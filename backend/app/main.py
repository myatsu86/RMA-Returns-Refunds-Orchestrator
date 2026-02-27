from fastapi import FastAPI
from app.routers import health, products, rma

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "OK"} 


app.include_router(products.router)
app.include_router(rma.router)

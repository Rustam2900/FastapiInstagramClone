from fastapi import FastAPI
from FastapiInstagramClone.app.router.user import router as user_router
from FastapiInstagramClone.app.router.auth import router as auth_router
app = FastAPI(title="Instagram")


@app.get('/')
async def root():
    return {"Hello Word"}


app.include_router(user_router)
app.include_router(auth_router)

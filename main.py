from fastapi import FastAPI

from wecom import routes

app = FastAPI()
app.include_router(routes.router)

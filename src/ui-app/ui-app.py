# this app uses FastAPI to ensure OpenAPI and JSON compliant interfaces
# https://fastapi.tiangolo.com
# default port is 3200

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="ui-app",
    description="User Interface Application refresh to FastAPI",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    This application provides the UI for the Decision Support
    System (DSS).
    
    Go to '/docs' or '/redocs' to see the API documentation.
    """
    return templates.TemplateResponse("leaflet-map-ui.html", {"request": request})


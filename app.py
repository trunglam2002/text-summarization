from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, Response
from text_summarizer.pipeline.prediction import PredictionPipeline
import uvicorn
import os

app = FastAPI()

# Mount the static directory to serve CSS files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/predict")
async def predict_route(request: Request):
    try:
        body = await request.json()
        text = body['text']
        obj = PredictionPipeline()
        summary = obj.predict(text)
        return Response(content=summary, media_type="text/plain")
    except Exception as e:
        raise e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

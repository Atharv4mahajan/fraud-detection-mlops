from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import shutil
import os

from src.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")

pipeline = PredictionPipeline()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):

    upload_path = f"temp_{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_csv(upload_path)

    results = []

    for _, row in df.iterrows():
        prediction = pipeline.predict(row.to_dict())
        results.append(prediction["fraud_prediction"])

    df["fraud_prediction"] = results

    output_file = "prediction_output.csv"
    df.to_csv(output_file, index=False)

    os.remove(upload_path)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": "Prediction Completed!",
            "rows": len(df),
            "fraud_count": sum(results)
        }
    )
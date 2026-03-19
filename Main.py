from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io

app = FastAPI(title="Skin Lesion Prototype")

# Serve the files inside /static at URLs like /static/styles.css
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    allowed_types = {"image/jpeg", "image/png", "image/webp"}

    if file.content_type not in allowed_types:
        return JSONResponse(
            status_code=400,
            content={"error": "Please upload a JPG, PNG, or WEBP image."},
        )

    data = await file.read()

    try:
        image = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Could not read that image file."},
        )

    # Fake result for Step 1 only
    result = {
        "top_class": "nv",
        "confidence": 0.82,
        "classes": {
            "akiec": 0.03,
            "bcc": 0.02,
            "bkl": 0.07,
            "df": 0.01,
            "mel": 0.04,
            "nv": 0.82,
            "vasc": 0.01,
        },
        "image_size": {
            "width": image.width,
            "height": image.height,
        },
        "note": "Prototype only. Not a diagnosis."
    }

    return result
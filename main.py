from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests, os, uuid, json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, name="index")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def post_index(request: Request, text: str = Form(...), language: str = Form(...)):
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + language
    constructed_url = endpoint + path + target_language_parameter

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{"text": text}]
    #Make the call using POST
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    #Retrieve the JSON response
    translator_response = translator_request.json()
    #Retrive the translation
    translated_text = translator_response[0]['translations'][0]['text']

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "translated_text": translated_text,
            "original_text" : text,
            "target_language": language
        }
    )
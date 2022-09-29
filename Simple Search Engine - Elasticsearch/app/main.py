from fastapi import FastAPI, Request
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch({
        "scheme": "http",
        "host": "localhost",
        "port": 9200
    }
)

if not es.ping():
    raise ValueError("Connection failed")
else:
    print("Successfully connected to Elasticsearch")

index_name = "flickrphotos"

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

@app.get('/search/{search}')
def index(search: str):
    json = {
        "query": {
            "query_string": {
                "query": search
            }
        }
    }
    res = es.search(index=index_name, body=json)
    if res["hits"]["total"]["value"] > 0:
        records = []
        for i in res["hits"]["hits"]:
            records.append(i)
        return records
    else:
        return {}

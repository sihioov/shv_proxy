from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
END_POINT_PATH = '/shv-proxy'

app = FastAPI()

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
clientApi = '';
isSetAPI = False;

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get(END_POINT_PATH+"/setapi")
async def set_api(apiurl: str):
    clientApiUrl = apiurl;
    global isSetAPI;
    isSetAPI = True;
    print('SetAPI : '+clientApiUrl);


@app.get(END_POINT_PATH+"/{url1}/{url2}")
def get_resource(url1: str, url2: str):
    if isSetAPI:
        print(url1);
    else:
        return;
    
    print(url2);
    

@app.post(END_POINT_PATH+"/{url1}/{url2}")
async def post_resource(request: Request, url1: str, url2: str):
    global isSetAPI;
    if isSetAPI:
        print('test')
        print(request.headers);
        print('..............................')
        raw_body = await request.json();
        print(raw_body)
        print(url1);
    #requests.post(clientApi+'/'+{url1}+'/'+{url2});
        
            

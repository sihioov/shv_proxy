from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
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
clientApiURL = '';
isSetAPI = False;

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get(END_POINT_PATH+"/setapi")
async def set_api(apiurl: str):
    global clientApi;
    global clientApiURL;
    clientApiURL = apiurl;
    global isSetAPI;
    isSetAPI = True;
    print('SetAPI : '+clientApiURL);


@app.get(END_POINT_PATH+"/{url1}/{url2}")
def get_resource(url1: str, url2: str):
    if isSetAPI:
        print(url1);
    else:
        return;
    
    print(url2);
    
@app.post(END_POINT_PATH+"/{url1}/{url2}")
async def post_resource(request: Request, url1: str, url2: str):
    global isSetAPI, clientApiURL
    if isSetAPI:
        targetApiURL = f"{clientApiURL}/{url1}/{url2}"
        
        data = await request.json()  # 한 번만 호출
        print(data)
        #headers = dict(request.headers)
        #headers.pop("host", None)  # 필요에 따라 헤더 수정
        
        #print(request.headers)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(targetApiURL, json=data)#, headers=headers)
                print(response.json())  # 타겟 서버의 응답 반환
                return response.json();
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
            return {"error": "Request failed"}

    else:
        return {"error": "API is not set or target URL is not defined"}

            

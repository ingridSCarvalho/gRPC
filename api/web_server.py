from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import grpc
import dictionary_pb2
import dictionary_pb2_grpc
from typing import List

app = FastAPI(title="Dicionário API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


channel = grpc.insecure_channel('localhost:50051')
stub = dictionary_pb2_grpc.DictionaryServiceStub(channel)


class WordRequest(BaseModel):
    word: str

class WordResponse(BaseModel):
    count: int

class WordCount(BaseModel):
    word: str
    count: int

@app.post("/add-word", response_model=WordResponse)
async def add_word(request: WordRequest):
    try:
       
        grpc_request = dictionary_pb2.WordRequest(word=request.word)
        response = stub.AddWord(grpc_request)
        return {"count": response.count}
    except grpc.RpcError as e:
        raise HTTPException(status_code=400, detail=str(e.details()))

@app.get("/dictionary", response_model=List[WordCount])
async def get_dictionary():
    try:
        request = dictionary_pb2.EmptyRequest()
        response = stub.PrintDictionary(request)
        return [
            {"word": word.word, "count": word.count}
            for word in response.words
        ]
    except grpc.RpcError as e:
        raise HTTPException(status_code=400, detail=str(e.details()))


@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

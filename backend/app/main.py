import os
from enum import Enum

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv('LINGVANEX_API_KEY')


class Lang(Enum):
    RU = 'ru_RU'
    KG = 'ky_KG'
    UZ = 'uz_UZ'
    TJ = 'tg_TJ'


class IOSchema(BaseModel):
    content: str
    lang_to: Lang
    lang_from: Lang

    class Config:
        use_enum_values = True


def __raise(mess: str) -> None:
    logger.error(mess)
    raise HTTPException(status_code=500, detail=mess)


@app.post('/api', response_model=IOSchema)
async def translate(intake: IOSchema) -> IOSchema:
    url = 'https://api-b2b.backenster.com/b1/api/v3/translate'
    h = {
        'Authorization': API_KEY,
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    j = {
        'translateMode': 'html',
        'platform': 'api',
        'data': intake.content,
        'from': intake.lang_from,
        'to': intake.lang_to
    }

    try:
        sess = httpx.AsyncClient()
        resp = await sess.post(url, headers=h, json=j)
    except (httpx.ConnectError, httpx.ConnectTimeout):
        __raise('Cannot connect to translation server.')
    else:
        if resp.status_code != 200:
            __raise(f'Http code from lingvanex: {resp.status_code}.')

        j = resp.json()
        err = j['err']

        if err is not None:
            __raise(f'Error code from lingvanex: {err}.')

        return IOSchema(
            lang_from=intake.lang_from,
            lang_to=intake.lang_to,
            content=j['result']
        )


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

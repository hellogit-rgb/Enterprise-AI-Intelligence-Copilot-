from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import router

app = FastAPI(title='Enterprise AI Intelligence Copilot AI Service')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router, prefix='/ai')


@app.get('/ai/health')
def health():
    return {
        'status': 'ok',
        'service': 'ai-service',
        'capabilities': ['agent', 'retrieve', 'rerank', 'verify', 'evaluate']
    }

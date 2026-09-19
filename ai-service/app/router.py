from typing import List, Dict, Any

from fastapi import APIRouter

from app.confidence import ConfidenceEngine
from app.ingestion import DocumentIngestionPipeline, build_sample_documents
from app.query_rewrite import QueryRewriter
from app.retrieval import HybridRetriever
from app.tools import DocumentSearchTool, SQLQueryTool
from app.verification import EvidenceVerifier

router = APIRouter()

sample_documents = build_sample_documents()
injected_chunks = DocumentIngestionPipeline(sample_documents).build_chunks()
retrieval_documents = [chunk.to_retrieval_dict() for chunk in injected_chunks]
retriever = HybridRetriever(retrieval_documents)
document_tool = DocumentSearchTool(retriever)
sql_tool = SQLQueryTool()
confidence_engine = ConfidenceEngine()


@router.post('/agent')
def agent_route(payload: dict):
    query = payload.get('query', '')
    lowered = query.lower()
    is_structured = 'revenue' in lowered or 'highest' in lowered or ('customer' in lowered and 'payment' not in lowered)
    tool = 'SQLQueryTool' if is_structured else 'DocumentSearchTool'
    intent = 'structured business data' if is_structured else 'contract information'

    hits = document_tool.execute(QueryRewriter.rewrite(query), top_k=5) if tool == 'DocumentSearchTool' else []
    confidence = confidence_engine.score(query, hits, tool)

    return {
        'intent': intent,
        'tool': tool,
        'confidence': confidence['score'],
        'needs_review': confidence['needs_review'],
        'query': query
    }


@router.post('/retrieve')
def retrieve(payload: dict):
    query = payload.get('query', '')
    rewritten = QueryRewriter.rewrite(query)
    hits = document_tool.execute(rewritten, top_k=5)
    confidence = confidence_engine.score(query, hits, 'DocumentSearchTool')
    return {'hits': hits, 'rewritten_query': rewritten, 'confidence': confidence}


@router.post('/sql')
def run_sql(payload: dict):
    q = payload.get('query', '')
    try:
        result = sql_tool.execute(q)
        return {'ok': True, 'result': result}
    except ValueError as exc:
        return {'ok': False, 'error': str(exc)}


@router.post('/verify')
def verify(payload: dict):
    claim = payload.get('claim', '')
    evidence = payload.get('evidence', {})
    return EvidenceVerifier.verify_claim(claim, evidence)

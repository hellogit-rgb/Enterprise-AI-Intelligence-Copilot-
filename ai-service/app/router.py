from typing import List, Dict, Any
from uuid import uuid4

from fastapi import APIRouter

from app.answering import GroundedAnswerGenerator
from app.access_control import can_access_document
from app.confidence import ConfidenceEngine
from app.document_store import DocumentStore
from app.evaluation import EvaluationEngine, load_sample_dataset
from app.ingestion import DocumentIngestionPipeline, build_sample_documents, document_from_file, ingest_documents
from app.query_rewrite import QueryRewriter
from app.retrieval import HybridRetriever
from app.tools import DocumentSearchTool, SQLQueryTool
from app.verification import EvidenceVerifier

router = APIRouter()

sample_documents = build_sample_documents()
document_store = DocumentStore()
stored_documents = document_store.list_documents()
all_documents = [*sample_documents, *stored_documents]
injected_chunks = DocumentIngestionPipeline(all_documents).build_chunks()
retrieval_documents = [chunk.to_retrieval_dict() for chunk in injected_chunks]
retriever = HybridRetriever(retrieval_documents)
document_tool = DocumentSearchTool(retriever)
sql_tool = SQLQueryTool()
confidence_engine = ConfidenceEngine()
answer_generator = GroundedAnswerGenerator()


@router.post('/ingest')
def ingest(payload: dict):
    global retriever, document_tool, retrieval_documents, stored_documents

    documents = payload.get('documents', [])
    if not documents:
        return {'ok': False, 'message': 'No documents provided', 'chunks': []}

    document_store.upsert(documents)
    stored_documents = document_store.list_documents()
    all_documents = [*sample_documents, *stored_documents]
    retrieval_documents = ingest_documents(all_documents)
    retriever = HybridRetriever(retrieval_documents)
    document_tool = DocumentSearchTool(retriever)
    chunks = ingest_documents(documents)
    return {'ok': True, 'count': len(chunks), 'chunks': chunks}


@router.post('/ingest-file')
def ingest_file(payload: dict):
    name = payload.get('name', '')
    content_base64 = payload.get('content_base64', '')
    section = payload.get('section', 'Uploaded Document')
    if not name or not content_base64:
        return {'ok': False, 'message': 'File name and content are required.', 'chunks': []}

    try:
        document = document_from_file(name, content_base64, section)
    except ValueError as exc:
        return {'ok': False, 'message': str(exc), 'chunks': []}

    document['id'] = f'upload_{uuid4().hex}'
    document['allowed_roles'] = payload.get('allowed_roles', [])
    return ingest({'documents': [document]})


@router.get('/documents')
def list_documents():
    return {'documents': document_store.list_documents()}


@router.delete('/documents/{document_id}')
def delete_document(document_id: str):
    global retriever, document_tool, retrieval_documents, stored_documents

    deleted = document_store.delete(document_id)
    if not deleted:
        return {'ok': False, 'message': 'Document not found'}

    stored_documents = document_store.list_documents()
    all_documents = [*sample_documents, *stored_documents]
    retrieval_documents = ingest_documents(all_documents)
    retriever = HybridRetriever(retrieval_documents)
    document_tool = DocumentSearchTool(retriever)
    return {'ok': True, 'document_id': document_id}


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
    role = payload.get('role', 'user')
    rewritten = QueryRewriter.rewrite(query)
    hits = [hit for hit in document_tool.execute(rewritten, top_k=5) if can_access_document(hit, role)]
    confidence = confidence_engine.score(query, hits, 'DocumentSearchTool')
    return {'hits': hits, 'rewritten_query': rewritten, 'confidence': confidence}


@router.post('/answer')
def answer(payload: dict):
    query = payload.get('query', '')
    role = payload.get('role', 'user')
    rewritten = QueryRewriter.rewrite(query)
    hits = [hit for hit in document_tool.execute(rewritten, top_k=5) if can_access_document(hit, role)]
    confidence = confidence_engine.score(query, hits, 'DocumentSearchTool')
    grounded = answer_generator.generate(query, hits)
    return {
        **grounded,
        'confidence': confidence['score'],
        'needs_review': grounded['needs_review'] or confidence['needs_review'],
        'query': query,
        'rewritten_query': rewritten,
    }


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


@router.get('/evaluate')
def evaluate():
    dataset = load_sample_dataset()
    report = EvaluationEngine(dataset).run()
    return {
        'summary': {
            'total_questions': report['total_questions'],
            'accuracy': report['accuracy']
        },
        'results': report['results']
    }

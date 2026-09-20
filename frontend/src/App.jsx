import { useEffect, useState } from 'react'
import './styles/global.css'

const defaultMetrics = [
  { label: 'Documents', value: '126' },
  { label: 'Queries', value: '842' },
  { label: 'Verified', value: '94%' },
  { label: 'Avg Latency', value: '2.8 sec' },
  { label: 'Review Needed', value: '31' }
]

const sampleQuestions = [
  'What were Q2 revenues for Customer A?',
  'Compare Customer A payment terms with policy.',
  'Which customers have overdue payments?'
]

function encodeBase64(buffer) {
  const bytes = new Uint8Array(buffer)
  let binary = ''
  for (let offset = 0; offset < bytes.length; offset += 0x8000) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + 0x8000))
  }
  return btoa(binary)
}

function App() {
  const [metrics, setMetrics] = useState(defaultMetrics)
  const [evaluation, setEvaluation] = useState({ total_questions: 3, accuracy: 100 })
  const [question, setQuestion] = useState('What were Q2 revenues for Customer A?')
  const [documentName, setDocumentName] = useState('')
  const [documentText, setDocumentText] = useState('')
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadState, setUploadState] = useState('')
  const [response, setResponse] = useState({
    answer: 'Customer A generated ₹42.8 lakh in Q2. The result was validated against the sales database and the financial report.',
    sources: [
      { title: 'Financial Report', page: 31, section: 'Revenue Overview' },
      { title: 'Sales Database', page: 1, section: 'Q2 Revenue' }
    ],
    confidence: 96,
    verification: 'passed',
    needsReview: false,
    toolUsed: 'SQLQueryTool'
  })

  useEffect(() => {
    fetch('http://localhost:4000/api/dashboard')
      .then((res) => res.json())
      .then((data) => {
        if (data?.metrics) {
          setMetrics([
            { label: 'Documents', value: String(data.metrics.documents) },
            { label: 'Queries', value: String(data.metrics.queries) },
            { label: 'Verified', value: String(data.metrics.verified) },
            { label: 'Avg Latency', value: String(data.metrics.avgLatency) },
            { label: 'Review Needed', value: String(data.metrics.reviewNeeded) }
          ])
        }

        if (data?.evaluation) {
          setEvaluation(data.evaluation)
        }
      })
      .catch(() => {})
  }, [])

  const handleAsk = async () => {
    const result = await fetch('http://localhost:4000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    }).then((res) => res.json())
      .catch(() => ({
        answer: 'The backend is unavailable right now, but the project architecture is ready for live AI routing.',
        sources: [],
        confidence: 0,
        verification: 'pending',
        needsReview: true,
        toolUsed: 'Offline mode'
      }))

    setResponse(result)
  }

  const handleUpload = async (event) => {
    event.preventDefault()
    setUploadState('Uploading...')

    const request = selectedFile
      ? selectedFile.arrayBuffer().then((buffer) => fetch('http://localhost:4000/api/documents/file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: selectedFile.name,
          content_base64: encodeBase64(buffer),
          section: 'Uploaded Document'
        })
      }))
      : fetch('http://localhost:4000/api/documents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: documentName, text: documentText, section: 'Uploaded Document' })
      })

    const result = await request.then((res) => res.json())
      .catch(() => ({ ok: false, error: 'Backend unavailable' }))

    if (result.ok) {
      setUploadState(`Ingested ${result.count} chunk${result.count === 1 ? '' : 's'}`)
      setDocumentName('')
      setDocumentText('')
      setSelectedFile(null)
    } else {
      setUploadState(result.error || 'Upload failed')
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">AI</div>
          <div>
            <strong>Enterprise AI</strong>
            <span>Copilot</span>
          </div>
        </div>

        <nav className="nav">
          <button className="nav-item active">Dashboard</button>
          <button className="nav-item">Documents</button>
          <button className="nav-item">Chat</button>
          <button className="nav-item">Evaluation</button>
          <button className="nav-item">Security</button>
        </nav>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow">Enterprise intelligence</p>
            <h1>Enterprise AI Intelligence Copilot</h1>
          </div>
          <button className="primary-btn">New Query</button>
        </header>

        <section className="metric-grid">
          {metrics.map((m) => (
            <div key={m.label} className="metric-card">
              <span>{m.label}</span>
              <strong>{m.value}</strong>
            </div>
          ))}
        </section>

        <section className="upload-panel">
          <div>
            <p className="eyebrow">Knowledge base</p>
            <h2>Add a text document</h2>
          </div>
          <form className="upload-form" onSubmit={handleUpload}>
            <input
              type="text"
              value={documentName}
              onChange={(event) => setDocumentName(event.target.value)}
              placeholder="Document name"
              required={!selectedFile}
            />
            <input
              type="file"
              accept=".txt,.md,.csv,.json,.pdf"
              onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
            />
            <textarea
              value={documentText}
              onChange={(event) => setDocumentText(event.target.value)}
              placeholder="Paste document content"
              rows="4"
              required={!selectedFile}
            />
            <div className="upload-actions">
              <button className="primary-btn" type="submit">Ingest document</button>
              {uploadState && <span className="upload-status">{uploadState}</span>}
            </div>
          </form>
        </section>

        <section className="chat-panel">
          <div className="chat-header">
            <div>
              <p className="eyebrow">Ask anything about your enterprise data</p>
              <h2>{question}</h2>
            </div>
          </div>

          <div className="prompt-row">
            {sampleQuestions.map((q) => (
              <button key={q} className="chip" onClick={() => setQuestion(q)}>{q}</button>
            ))}
          </div>

          <div className="response-box">
            <div className="answer-block">
              <label>Answer</label>
              <p>{response.answer}</p>
            </div>

            <div className="meta-grid">
              <div>
                <label>Sources</label>
                <ul>
                  {response.sources?.length ? response.sources.map((s, index) => (
                    <li key={`${s.title}-${index}`}>{s.title} - Page {s.page} - {s.section}</li>
                  )) : <li>No citations yet</li>}
                </ul>
              </div>
              <div>
                <label>Confidence</label>
                <strong>{response.confidence}%</strong>
              </div>
              <div>
                <label>Citation Verification</label>
                <strong>{response.verification}</strong>
              </div>
              <div>
                <label>Answer Review</label>
                <strong>{response.needsReview ? 'Required' : 'Clear'}</strong>
              </div>
            </div>

            <div className="meta-grid" style={{ marginTop: '1rem' }}>
              <div>
                <label>Evaluation Accuracy</label>
                <strong>{evaluation.accuracy}%</strong>
              </div>
              <div>
                <label>Questions</label>
                <strong>{evaluation.total_questions}</strong>
              </div>
              <div>
                <label>Review State</label>
                <strong>{evaluation.accuracy >= 90 ? 'Stable' : 'Needs Review'}</strong>
              </div>
            </div>
          </div>

          <div className="input-row">
            <input type="text" value={question} onChange={(e) => setQuestion(e.target.value)} />
            <button className="primary-btn" onClick={handleAsk}>Ask</button>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App

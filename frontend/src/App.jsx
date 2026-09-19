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

function App() {
  const [metrics, setMetrics] = useState(defaultMetrics)
  const [question, setQuestion] = useState('What were Q2 revenues for Customer A?')
  const [response, setResponse] = useState({
    answer: 'Customer A generated ₹42.8 lakh in Q2. The result was validated against the sales database and the financial report.',
    sources: [
      { title: 'Financial Report', page: 31, section: 'Revenue Overview' },
      { title: 'Sales Database', page: 1, section: 'Q2 Revenue' }
    ],
    confidence: 96,
    verification: 'passed',
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
        toolUsed: 'Offline mode'
      }))

    setResponse(result)
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

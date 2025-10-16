import { useState } from 'react'

interface Message {
  id: number
  type: 'user' | 'bot'
  content: string
  timestamp: Date
}

interface EmployeeResult {
  success: boolean
  employee_email?: string
  employee_name?: string
  employee_level?: string
  purchase_limit?: number
  approved_items?: string[]
  department?: string
  designation?: string
  error?: string
}

const styles = {
  container: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column' as const,
    backgroundColor: '#f5f5f5'
  },
  header: {
    backgroundColor: 'white',
    borderBottom: '1px solid #e0e0e0',
    padding: '20px 24px'
  },
  title: {
    fontSize: '24px',
    fontWeight: '600',
    color: '#333',
    margin: 0
  },
  subtitle: {
    fontSize: '14px',
    color: '#666',
    marginTop: '4px'
  },
  messagesContainer: {
    flex: 1,
    overflowY: 'auto' as const,
    padding: '20px 24px'
  },
  messageRow: {
    display: 'flex',
    marginBottom: '16px'
  },
  messageRowUser: {
    justifyContent: 'flex-end'
  },
  messageRowBot: {
    justifyContent: 'flex-start'
  },
  messageBubbleUser: {
    maxWidth: '600px',
    padding: '12px 16px',
    borderRadius: '12px',
    backgroundColor: '#2563eb',
    color: 'white'
  },
  messageBubbleBot: {
    maxWidth: '600px',
    padding: '12px 16px',
    borderRadius: '12px',
    backgroundColor: 'white',
    border: '1px solid #e0e0e0',
    color: '#333'
  },
  messageText: {
    whiteSpace: 'pre-wrap' as const,
    margin: 0,
    lineHeight: '1.5'
  },
  timestamp: {
    fontSize: '11px',
    marginTop: '8px',
    display: 'block'
  },
  timestampUser: {
    color: '#bfdbfe'
  },
  timestampBot: {
    color: '#999'
  },
  loadingDots: {
    display: 'flex',
    gap: '6px'
  },
  dot: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: '#999',
    animation: 'bounce 1.4s infinite ease-in-out both'
  },
  inputContainer: {
    backgroundColor: 'white',
    borderTop: '1px solid #e0e0e0',
    padding: '16px 24px'
  },
  inputForm: {
    display: 'flex',
    gap: '12px'
  },
  input: {
    flex: 1,
    padding: '12px 16px',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    fontSize: '14px',
    outline: 'none'
  },
  button: {
    padding: '12px 24px',
    backgroundColor: '#2563eb',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer'
  },
  buttonDisabled: {
    backgroundColor: '#9ca3af',
    cursor: 'not-allowed'
  }
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'bot',
      content: 'Welcome to Employee Lookup Agent. Please enter an employee email address to get started.',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = {
      id: messages.length + 1,
      type: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('http://localhost:5000/api/lookup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: input })
      })

      const data: EmployeeResult = await response.json()

      const botMessage: Message = {
        id: messages.length + 2,
        type: 'bot',
        content: formatResponse(data),
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: messages.length + 2,
        type: 'bot',
        content: 'Error: Could not connect to the server. Please make sure the backend is running on http://localhost:5000',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const formatResponse = (data: EmployeeResult): string => {
    if (!data.success) {
      return data.error || 'Employee not found'
    }

    return `Employee Found:

Name: ${data.employee_name}
Email: ${data.employee_email}
Level: ${data.employee_level}
Department: ${data.department}
Designation: ${data.designation}

Purchase Limit: $${data.purchase_limit?.toLocaleString()}

Approved Items:
${data.approved_items?.map(item => `- ${item}`).join('\n')}`
  }

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Employee Lookup Agent</h1>
        <p style={styles.subtitle}>Enter employee email to check purchase eligibility</p>
      </header>

      <div style={styles.messagesContainer}>
        {messages.map((message) => (
          <div
            key={message.id}
            style={{
              ...styles.messageRow,
              ...(message.type === 'user' ? styles.messageRowUser : styles.messageRowBot)
            }}
          >
            <div style={message.type === 'user' ? styles.messageBubbleUser : styles.messageBubbleBot}>
              <p style={styles.messageText}>{message.content}</p>
              <span style={{
                ...styles.timestamp,
                ...(message.type === 'user' ? styles.timestampUser : styles.timestampBot)
              }}>
                {message.timestamp.toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
        
        {loading && (
          <div style={{ ...styles.messageRow, ...styles.messageRowBot }}>
            <div style={styles.messageBubbleBot}>
              <div style={styles.loadingDots}>
                <div style={styles.dot}></div>
                <div style={styles.dot}></div>
                <div style={styles.dot}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div style={styles.inputContainer}>
        <form onSubmit={handleSubmit} style={styles.inputForm}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter employee email (e.g., john.doe@abc-company.com)"
            style={styles.input}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            style={{
              ...styles.button,
              ...(loading || !input.trim() ? styles.buttonDisabled : {})
            }}
          >
            {loading ? 'Searching...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default App

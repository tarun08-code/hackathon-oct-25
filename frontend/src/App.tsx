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
    width: '100vw',
    display: 'flex',
    flexDirection: 'column' as const,
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    margin: 0,
    padding: 0,
    overflow: 'hidden'
  },
  header: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    backdropFilter: 'blur(10px)',
    borderBottom: '1px solid rgba(0,0,0,0.1)',
    padding: '24px 32px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
  },
  headerContent: {
    maxWidth: '1200px',
    margin: '0 auto',
    display: 'flex',
    alignItems: 'center',
    gap: '16px'
  },
  logo: {
    fontSize: '28px',
    fontWeight: '700',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    margin: 0
  },
  titleContainer: {
    flex: 1
  },
  title: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#333',
    margin: 0
  },
  subtitle: {
    fontSize: '13px',
    color: '#666',
    marginTop: '4px'
  },
  link: {
    fontSize: '13px',
    color: '#667eea',
    textDecoration: 'none',
    fontWeight: '500'
  },
  messagesContainer: {
    flex: 1,
    overflowY: 'auto' as const,
    padding: '32px 24px',
    width: '100%'
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
    maxWidth: '70%',
    padding: '14px 18px',
    borderRadius: '18px 18px 4px 18px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    boxShadow: '0 2px 8px rgba(102, 126, 234, 0.3)'
  },
  messageBubbleBot: {
    maxWidth: '70%',
    padding: '14px 18px',
    borderRadius: '18px 18px 18px 4px',
    backgroundColor: 'white',
    border: 'none',
    color: '#333',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
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
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    backdropFilter: 'blur(10px)',
    borderTop: '1px solid rgba(0,0,0,0.1)',
    padding: '20px 24px',
    boxShadow: '0 -2px 8px rgba(0,0,0,0.1)'
  },
  inputForm: {
    display: 'flex',
    gap: '12px',
    width: '100%'
  },
  input: {
    flex: 1,
    padding: '14px 18px',
    border: '2px solid #e0e0e0',
    borderRadius: '24px',
    fontSize: '15px',
    outline: 'none',
    transition: 'all 0.2s',
    backgroundColor: 'white'
  },
  inputFocus: {
    borderColor: '#667eea'
  },
  button: {
    padding: '14px 32px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '24px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)'
  },
  buttonHover: {
    transform: 'translateY(-2px)',
    boxShadow: '0 6px 16px rgba(102, 126, 234, 0.5)'
  },
  buttonDisabled: {
    backgroundColor: '#9ca3af',
    cursor: 'not-allowed'
  },
  suggestionsContainer: {
    display: 'flex',
    gap: '8px',
    flexWrap: 'wrap' as const,
    padding: '12px 0',
    justifyContent: 'center'
  },
  suggestionChip: {
    padding: '8px 16px',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    border: '1px solid #e0e0e0',
    borderRadius: '20px',
    fontSize: '13px',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    color: '#667eea',
    fontWeight: '500'
  },
  suggestionChipHover: {
    backgroundColor: '#667eea',
    color: 'white',
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 8px rgba(102, 126, 234, 0.3)'
  }
}


function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'bot',
      content: 'Welcome to PaperShare Employee Lookup Agent. Please enter an employee email address to get started, or try one of the suggestions below!',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  
  // Pre-prepared suggestion questions
  const suggestions = [
    { label: 'What can you do?', query: 'what can you do?' },
    { label: 'Show me an example', query: 'john.doe@abc-company.com' },
    { label: 'Help me get started', query: 'help' },
    { label: 'List all employees', query: 'show me all employees' }
  ]

  const handleSuggestionClick = (query: string) => {
    if (loading) return
    setInput(query)
    // Auto-submit after setting input
    setTimeout(() => {
      const form = document.querySelector('form') as HTMLFormElement
      if (form) form.requestSubmit()
    }, 100)
  }

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

  const formatResponse = (data: any): string => {
    // Handle natural language responses
    if (data.type === 'natural_language' && data.ai_response) {
      return data.ai_response
    }
    
    // Handle not found with AI response
    if (!data.success) {
      return data.error || 'Employee not found'
    }

    // Format successful employee lookup
    return `Employee Found:

Name: ${data.employee_name}
Email: ${data.employee_email}
Level: ${data.employee_level}
Department: ${data.department}
Designation: ${data.designation}

Purchase Limit: $${data.purchase_limit?.toLocaleString()}

Approved Items:
${data.approved_items?.map((item: string) => `- ${item}`).join('\n')}`
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
        
        {/* Suggestion Chips */}
        {!loading && messages.length <= 3 && (
          <div style={styles.suggestionsContainer}>
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion.query)}
                style={styles.suggestionChip}
                onMouseEnter={(e) => {
                  Object.assign(e.currentTarget.style, styles.suggestionChipHover)
                }}
                onMouseLeave={(e) => {
                  Object.assign(e.currentTarget.style, styles.suggestionChip)
                }}
              >
                {suggestion.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default App

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
    color: 'rgba(255, 255, 255, 0.9)',
    margin: 0,
    fontSize: '16px',
    fontWeight: '400'
  },
  userStatus: {
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: '12px',
    marginTop: '8px',
    padding: '4px 12px',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: '12px',
    display: 'inline-block'
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
      content: '� Welcome to PaperShare Smart Assistant! To give you personalized help with employee lookup, budget checking, and equipment recommendations, please enter your employee email address to get started.',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string>('')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [userContext, setUserContext] = useState<any>(null)
  
  // Pre-prepared suggestion questions with smart search
  const suggestions = [
    { label: '👋 What can you do?', query: 'what can you do?' },
    { label: '💻 MacBook options for developers', query: 'show me MacBook options for software engineers' },
    { label: '🚗 Company cars under $40k', query: 'company cars under 40000 budget' },
    { label: '👨‍💼 John Doe eligibility', query: 'john.doe@abc-company.com' },
    { label: '🏢 IT department employees', query: 'show me all IT department employees' },
    { label: '💰 Senior IC budget limits', query: 'what is the budget limit for Senior IC employees' },
    { label: '📱 Best tablets for presentations', query: 'tablets suitable for presentations and meetings' },
    { label: '⚡ Engineering equipment', query: 'best equipment for engineering department' }
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

  // Create session on component mount
  useEffect(() => {
    const initializeSession = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/session/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        })
        const data = await response.json()
        if (data.success) {
          setSessionId(data.session_id)
        }
      } catch (error) {
        console.error('Failed to create session:', error)
      }
    }
    
    initializeSession()
  }, [])

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
        body: JSON.stringify({ 
          email: input,
          session_id: sessionId 
        })
      })

      const data: EmployeeResult = await response.json()

      // Update session ID if provided
      if (data.session_id) {
        setSessionId(data.session_id)
      }

      // Handle authentication success
      if (data.type === 'authentication_success') {
        setIsAuthenticated(true)
        setUserContext({
          name: data.employee_name,
          email: data.employee_email,
          budget: data.user_context?.budget,
          level: data.user_context?.level,
          department: data.user_context?.department
        })
      }

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
    // Handle authentication success
    if (data.type === 'authentication_success' && data.welcome_message) {
      return data.welcome_message
    }
    
    // Handle authentication required
    if (data.requires_auth && data.message) {
      return data.message
    }
    
    // Handle natural language responses with session context
    if (data.type === 'natural_language' && data.ai_response) {
      return data.ai_response
    }
    
    // Handle not found with AI response
    if (!data.success) {
      return data.error || 'Employee not found'
    }

    // Handle successful employee lookup with AI summary (prioritize AI response)
    if (data.success && data.ai_summary) {
      return data.ai_summary
    }

    // Fallback format for successful employee lookup
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
        <div style={styles.headerContent}>
          <h1 style={styles.title}>PaperShare Smart Assistant</h1>
          <p style={styles.subtitle}>
            {isAuthenticated && userContext 
              ? `Welcome ${userContext.name}! Budget: $${userContext.budget?.toLocaleString() || '0'}`
              : 'Enter your employee email to get started'
            }
          </p>
          {isAuthenticated && (
            <div style={styles.userStatus}>
              ✅ Authenticated • {userContext?.level} • {userContext?.department}
            </div>
          )}
        </div>
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

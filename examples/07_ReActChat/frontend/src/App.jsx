import { useState, useRef, useEffect } from 'react'
import {
  Layout, Input, Button, Card, Typography, Space, Tag, Spin, message, Collapse,
} from 'antd'
import {
  SendOutlined, RobotOutlined, UserOutlined, SearchOutlined,
  BulbOutlined, ThunderboltOutlined, EyeOutlined, CheckCircleOutlined,
} from '@ant-design/icons'

const { Header, Content, Footer } = Layout
const { Text, Paragraph } = Typography

const API_BASE = '/api'

function App() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    const question = inputValue.trim()
    if (!question || loading) return
    setMessages((prev) => [...prev, { role: 'user', content: question }])
    setInputValue('')
    setLoading(true)
    const botMsg = { role: 'bot', content: '', steps: [], status: 'thinking' }
    setMessages((prev) => [...prev, botMsg])

    try {
      const resp = await fetch(API_BASE + '/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })
      if (!resp.ok) throw new Error('HTTP ' + resp.status)
      const reader = resp.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n\n')
        buffer = lines.pop()
        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          try {
            const data = JSON.parse(line.slice(6))
            if (data.type === 'done') {
              setMessages((prev) => { const u = [...prev]; u[u.length-1].status = 'done'; return u })
              continue
            }
            setMessages((prev) => {
              const u = [...prev]; const last = u[u.length-1]
              last.steps = [...last.steps, data]
              if (data.type === 'finish') { last.content = data.content; last.status = 'done' }
              return u
            })
          } catch (e) { console.error('SSE parse error', e) }
        }
      }
    } catch (err) {
      message.error('Request failed')
      setMessages((prev) => { const u = [...prev]; u[u.length-1].content = err.message; u[u.length-1].status = 'error'; return u })
    } finally { setLoading(false) }
  }

  const stepConfig = {
    thought: { icon: <BulbOutlined style={{color:'#faad14'}} />, label: 'Thought', color: 'gold' },
    action: { icon: <ThunderboltOutlined style={{color:'#1677ff'}} />, label: 'Action', color: 'blue' },
    observation: { icon: <EyeOutlined style={{color:'#52c41a'}} />, label: 'Observation', color: 'green' },
    finish: { icon: <CheckCircleOutlined style={{color:'#52c41a'}} />, label: 'Finish', color: 'success' },
    error: { icon: <SearchOutlined style={{color:'#ff4d4f'}} />, label: 'Error', color: 'red' },
  }

  const renderStep = (step, i) => {
    const c = stepConfig[step.type] || stepConfig.error
    return (
      <div key={i} className="step-item">
        <Tag icon={c.icon} color={c.color}>Step {step.step} - {c.label}</Tag>
        <Paragraph style={{margin:'4px 0 4px 24px'}}>{step.content}</Paragraph>
      </div>
    )
  }

  const renderMessage = (msg, i) => {
    const isUser = msg.role === 'user'
    return (
      <div key={i} className={'message-row ' + (isUser ? 'user' : 'bot')}>
        {!isUser && <div className="avatar bot-avatar"><RobotOutlined /></div>}
        <div className={'message-bubble ' + (isUser ? 'user-bubble' : 'bot-bubble')}>
          {isUser ? <Text>{msg.content}</Text> : (
            <>
              {msg.steps.length > 0 && (
                <Collapse size="small" defaultActiveKey={msg.status==='done'?[]:['steps']} items={[{
                  key: 'steps',
                  label: <Space><BulbOutlined /><span>Reasoning ({msg.steps.length} steps)</span>{msg.status==='thinking'&&<Spin size="small"/>}</Space>,
                  children: msg.steps.map(renderStep),
                }]} />
              )}
              {msg.content && <Card size="small" className="answer-card"><Text strong>{msg.content}</Text></Card>}
              {msg.status==='thinking'&&!msg.content&&msg.steps.length===0&&<Space><Spin size="small"/><Text type="secondary">Thinking...</Text></Space>}
            </>
          )}
        </div>
        {isUser && <div className="avatar user-avatar"><UserOutlined /></div>}
      </div>
    )
  }

  return (
    <Layout className="app-layout">
      <Header className="app-header">
        <Space><RobotOutlined style={{fontSize:24}}/><Text strong style={{color:'#fff',fontSize:18}}>ReAct Chat</Text><Tag color="blue">Reasoning + Acting</Tag></Space>
      </Header>
      <Content className="app-content">
        <div className="messages-container">
          {messages.length===0&&(
            <div className="welcome"><RobotOutlined style={{fontSize:64,color:'#1677ff'}}/><Text type="secondary" style={{fontSize:16,marginTop:16}}>Hello! I am a ReAct agent. Ask me anything.</Text></div>
          )}
          {messages.map(renderMessage)}
          <div ref={messagesEndRef} />
        </div>
      </Content>
      <Footer className="app-footer">
        <div className="input-area">
          <Input size="large" placeholder="Ask a question..." value={inputValue} onChange={e=>setInputValue(e.target.value)} onPressEnter={handleSend} disabled={loading} prefix={<SearchOutlined style={{color:'#bfbfbf'}}/>} />
          <Button type="primary" size="large" icon={<SendOutlined/>} onClick={handleSend} loading={loading}>Send</Button>
        </div>
      </Footer>
    </Layout>
  )
}

export default App

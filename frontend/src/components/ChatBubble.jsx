export default function ChatBubble({ role, text }) {
  const isUser = role === 'user'

  return (
    <div className={`bubble-row ${isUser ? 'bubble-row-user' : 'bubble-row-bot'}`}>
      <div className={`bubble ${isUser ? 'bubble-user' : 'bubble-bot'}`}>
        <p>{text}</p>
      </div>
    </div>
  )
}

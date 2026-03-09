import { useEffect, useMemo, useRef, useState } from "react";
import { sendChatMessage } from "../api";
import ChatBubble from "./ChatBubble";
import TypingIndicator from "./TypingIndicator";

const starterMessage = {
  role: "assistant",
  text: "Hi, I am your OWASP-aware chatbot. Ask me anything about web security or general topics.",
};

function getSessionId() {
  const key = "chatbot-assignment-session-id";
  let value = localStorage.getItem(key);
  if (!value) {
    value = crypto.randomUUID();
    localStorage.setItem(key, value);
  }
  return value;
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([starterMessage]);
  const [error, setError] = useState("");
  const messagesEndRef = useRef(null);
  const sessionId = useMemo(() => getSessionId(), []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  async function handleSend() {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    const userMessage = { role: "user", text: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setError("");

    try {
      const data = await sendChatMessage({
        session_id: sessionId,
        message: trimmed,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.response,
        },
      ]);
    } catch (err) {
      setError(err.message || "Something went wrong.");
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Sorry, I ran into an error while processing your message.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }

  return (
    <>
      <div className="page-shell">
        <div className="demo-card">
          <h1>Chat Widget Demo</h1>
          <p>
            This page simulates a website with a floating chatbot widget at the
            bottom-right corner.
          </p>
          <p>
            The backend supports Gemini responses, in-memory session history,
            and OWASP CSV retrieval.
          </p>
        </div>
      </div>

      <div className="chatbot-container">
        {isOpen && (
          <section className="chat-window" aria-label="Chatbot widget">
            <header className="chat-header">
              <div>
                <h2>Security Chatbot</h2>
                <p>Gemini + OWASP CSV RAG</p>
              </div>
              <button
                className="icon-button"
                onClick={() => setIsOpen(false)}
                aria-label="Close chat"
              >
                ×
              </button>
            </header>

            <div className="chat-messages">
              {messages.map((message, index) => (
                <ChatBubble
                  key={`${message.role}-${index}`}
                  role={message.role}
                  text={message.text}
                />
              ))}
              {isLoading && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </div>

            {error && <div className="chat-error">{error}</div>}

            <div className="chat-input-area">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about XSS, BOLA, or anything else..."
                rows={2}
              />
              <button
                className="send-button"
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
              >
                Send
              </button>
            </div>
          </section>
        )}

        <button
          className="launcher-button"
          onClick={() => setIsOpen((prev) => !prev)}
        >
          {isOpen ? "Hide Chat" : "Chat"}
        </button>
      </div>
    </>
  );
}

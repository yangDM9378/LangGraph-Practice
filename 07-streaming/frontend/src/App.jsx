import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import MessageInput from "./components/MessageInput";
import { sendMessage } from "./api/client";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSend = async (text) => {
    setError(null);
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setIsLoading(true);

    try {
      const data = await sendMessage(text);
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: data.answer,
          category: data.category,
          nodesVisited: data.nodes_visited,
          retryCount: data.retry_count,
        },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>FAQ 자동응답 봇</h1>
        <p className="subtitle">LangGraph + Claude Haiku</p>
      </header>
      <main className="app-main">
        <ChatWindow messages={messages} isLoading={isLoading} />
        {error && <div className="error-banner">{error}</div>}
        <MessageInput onSend={handleSend} isLoading={isLoading} />
      </main>
    </div>
  );
}

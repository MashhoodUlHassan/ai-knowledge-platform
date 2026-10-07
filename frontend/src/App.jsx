import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message.trim();

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat/stream",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: userMessage,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Server returned ${response.status}`
        );
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let result = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        result += decoder.decode(value, {
          stream: true,
        });
      }

      const lines = result.split("\n");

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;

        try {
          const data = JSON.parse(line.substring(6));

          if (data.status === "success") {
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: data.answer,
                sources: data.sources || [],
              },
            ]);
          } else {
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: `Error: ${data.detail}`,
              },
            ]);
          }
        } catch (error) {
          console.error("Invalid SSE data:", error);
        }
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Connection error: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setMessage("");
  };

  return (
    <div className="app">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="logo">
          <div className="logo-icon">
            AI
          </div>

          <div>
            <h2>AI Knowledge</h2>
            <span>Platform</span>
          </div>
        </div>

        <button
          className="new-chat"
          onClick={startNewChat}
        >
          + New Chat
        </button>

        <div className="sidebar-bottom">
          <span>AI Knowledge Platform</span>

          <small>
            RAG • LangGraph • Gemini
          </small>
        </div>

      </aside>

      {/* Main Chat */}
      <main className="chat-container">

        {/* Header */}
        <header className="chat-header">

          <div>
            <h1>
              AI Knowledge Assistant
            </h1>

            <p>
              Ask questions about your knowledge base
            </p>
          </div>

          <div className="status">
            <span></span>
            Online
          </div>

        </header>

        {/* Messages */}
        <section className="messages">

          {messages.length === 0 ? (

            <div className="welcome">

              <div className="welcome-icon">
                ✦
              </div>

              <h2>
                How can I help you?
              </h2>

              <p>
                Ask a question and I'll search your
                knowledge base for relevant information.
              </p>

              <div className="suggestions">

                <button
                  onClick={() =>
                    setMessage(
                      "What is the AI Knowledge Platform?"
                    )
                  }
                >
                  What is the AI Knowledge Platform?
                </button>

                <button
                  onClick={() =>
                    setMessage(
                      "Explain the available documents"
                    )
                  }
                >
                  Explain the available documents
                </button>

              </div>

            </div>

          ) : (

            messages.map((msg, index) => (

              <div
                className={`message-row ${msg.role}`}
                key={index}
              >

                {/* Avatar */}
                <div className="avatar">
                  {msg.role === "user"
                    ? "You"
                    : "AI"}
                </div>

                {/* Message */}
                <div className="message-content">

                  <strong>
                    {msg.role === "user"
                      ? "You"
                      : "AI Assistant"}
                  </strong>

                  <p>
                    {msg.content}
                  </p>

                  {/* Sources */}
                  {msg.sources &&
                    msg.sources.length > 0 && (

                      <div className="sources">

                        <strong>
                          📚 Sources
                        </strong>

                        {msg.sources.map(
                          (source, sourceIndex) => (

                            <div
                              className="source"
                              key={sourceIndex}
                            >

                              <span className="source-number">
                                {sourceIndex + 1}
                              </span>

                              <div>
                                <strong>
                                  Document{" "}
                                  {source.document_id ||
                                    "Unknown"}
                                </strong>

                                {source.score !==
                                  undefined && (
                                  <small>
                                    Relevance:{" "}
                                    {(
                                      source.score * 100
                                    ).toFixed(1)}
                                    %
                                  </small>
                                )}
                              </div>

                            </div>

                          )
                        )}

                      </div>

                    )}

                </div>

              </div>

            ))

          )}

          {/* Loading */}
          {loading && (

            <div className="message-row assistant">

              <div className="avatar">
                AI
              </div>

              <div className="message-content">

                <strong>
                  AI Assistant
                </strong>

                <p className="thinking">
                  AI is thinking...
                </p>

              </div>

            </div>

          )}

        </section>

        {/* Input */}
        <div className="input-area">

          <div className="input-box">

            <input
              type="text"
              value={message}
              disabled={loading}
              onChange={(e) =>
                setMessage(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
              placeholder="Ask something about your knowledge base..."
            />

            <button
              onClick={sendMessage}
              disabled={loading}
            >
              {loading
                ? "Thinking..."
                : "Send"}
            </button>

          </div>

          <small>
            AI Knowledge Platform can make mistakes.
            Verify important information.
          </small>

        </div>

      </main>

    </div>
  );
}

export default App;
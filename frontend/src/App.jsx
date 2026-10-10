import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/+$/, "");

function normalizeMarkdown(content) {
  if (typeof content !== "string") return "";

  return content.replace(/\\([*_`#>])/g, "$1");
}

// Normalize extracted document text for display only.
// This does not modify the original document or database content.
function normalizeSourceText(content) {
  if (typeof content !== "string") return "";

  return content
    .replace(/&#x20;|&#32;/gi, " ")
    .replace(/&#160;|&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/\\([*_`#>])/g, "$1")
    .replace(/(\d+)\\\./g, "$1.")
    .replace(/[ \t]+\n/g, "\n")
    .trim();
}

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const [uploadError, setUploadError] = useState(false);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);
  const audioUrlRef = useRef(null);
  const fileInputRef = useRef(null);

  // PLAY AI AUDIO
  const playBase64Audio = async (base64Audio, mimeType = "audio/wav") => {
    if (!base64Audio) {
      throw new Error("No audio data received.");
    }

    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }

    if (audioUrlRef.current) {
      URL.revokeObjectURL(audioUrlRef.current);
      audioUrlRef.current = null;
    }

    const binaryString = window.atob(base64Audio);
    const bytes = new Uint8Array(binaryString.length);

    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    const audioBlob = new Blob([bytes], { type: mimeType });
    const audioUrl = URL.createObjectURL(audioBlob);
    audioUrlRef.current = audioUrl;

    const audio = new Audio(audioUrl);
    audioRef.current = audio;

    audio.onended = () => {
      URL.revokeObjectURL(audioUrl);

      if (audioUrlRef.current === audioUrl) {
        audioUrlRef.current = null;
      }
    };

    await audio.play();
  };

  // TEXT TO SPEECH
  const speakText = async (text) => {
    if (!text?.trim()) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/voice/synthesize`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: text.trim() }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);

        throw new Error(
          errorData?.detail || `TTS server returned ${response.status}`
        );
      }

      const data = await response.json();

      if (data.status !== "success" || !data.audio) {
        throw new Error("No audio was returned from TTS API.");
      }

      await playBase64Audio(data.audio, data.mime_type || "audio/wav");
    } catch (error) {
      console.error("Text-to-speech failed:", error);
    }
  };

  // UPLOAD DOCUMENT
  const uploadDocument = async (event) => {
    const file = event.target.files?.[0];

    if (!file) return;

    const allowedExtensions = [".pdf", ".docx", ".txt"];
    const extension = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();

    if (!allowedExtensions.includes(extension)) {
      setUploadError(true);
      setUploadStatus("Unsupported file type. Choose a PDF, DOCX, or TXT file.");
      event.target.value = "";
      return;
    }

    if (file.size === 0) {
      setUploadError(true);
      setUploadStatus("The selected file is empty.");
      event.target.value = "";
      return;
    }

    setUploading(true);
    setUploadError(false);
    setUploadStatus(`Uploading ${file.name}...`);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_BASE_URL}/api/v1/documents/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        throw new Error(
          data?.detail || `Upload failed with status ${response.status}`
        );
      }

      if (data?.status !== "success") {
        throw new Error(data?.message || "Document upload failed.");
      }

      const document = data.data || {};

      setUploadError(false);
      setUploadStatus(
        `Successfully processed: ${document.filename || file.name}`
      );
    } catch (error) {
      console.error("Document upload failed:", error);
      setUploadError(true);
      setUploadStatus(`Upload failed: ${error.message}`);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  // SEND CHAT MESSAGE
  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);

        throw new Error(
          errorData?.detail || `Server returned ${response.status}`
        );
      }

      if (!response.body) {
        throw new Error("The server did not return a response stream.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let result = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        result += decoder.decode(value, { stream: true });
      }

      result += decoder.decode();

      const lines = result.split(/\r?\n/);

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;

        try {
          const data = JSON.parse(line.substring(6));

          if (data.status === "success") {
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: data.answer || "No answer was returned.",
                sources: Array.isArray(data.sources) ? data.sources : [],
              },
            ]);

            if (data.answer) {
              await speakText(data.answer);
            }
          } else if (data.detail || data.status === "error") {
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: `Error: ${data.detail || "The request failed."}`,
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

  // START VOICE RECORDING
  const startRecording = async () => {
    if (loading || isRecording) return;

    try {
      if (
        !navigator.mediaDevices?.getUserMedia ||
        typeof MediaRecorder === "undefined"
      ) {
        throw new Error(
          "Voice recording is not supported by this browser or connection."
        );
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      const preferredType = "audio/webm";
      const options = MediaRecorder.isTypeSupported(preferredType)
        ? { mimeType: preferredType }
        : {};

      const mediaRecorder = new MediaRecorder(stream, options);
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onerror = (event) => {
        console.error("Media recorder error:", event.error);
        stream.getTracks().forEach((track) => track.stop());
        setIsRecording(false);
      };

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());

        const audioBlob = new Blob(audioChunksRef.current, {
          type: mediaRecorder.mimeType || "audio/webm",
        });

        setIsRecording(false);

        if (audioBlob.size > 0) {
          await transcribeAudio(audioBlob);
        } else {
          alert("No audio was recorded. Please try again.");
        }
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Microphone access error:", error);
      alert(
        error.message ||
          "Unable to access microphone. Please allow microphone permission."
      );
    }
  };

  // STOP VOICE RECORDING
  const stopRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !== "inactive"
    ) {
      mediaRecorderRef.current.stop();
    } else {
      setIsRecording(false);
    }
  };

  const toggleVoiceInput = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  // SPEECH TO TEXT
  const transcribeAudio = async (audioBlob) => {
    try {
      const formData = new FormData();
      formData.append("audio", audioBlob, "voice.webm");

      const response = await fetch(
        `${API_BASE_URL}/api/v1/voice/transcribe`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);

        throw new Error(
          errorData?.detail || `Server returned ${response.status}`
        );
      }

      const data = await response.json();

      if (data.status === "success" && data.transcript) {
        setMessage((prev) => {
          const current = prev.trim();

          return current
            ? `${current} ${data.transcript}`
            : data.transcript;
        });
      } else {
        throw new Error("No transcription was returned.");
      }
    } catch (error) {
      console.error("Voice transcription failed:", error);
      alert(`Voice transcription failed: ${error.message}`);
    }
  };

  // NEW CHAT
  const startNewChat = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }

    if (audioUrlRef.current) {
      URL.revokeObjectURL(audioUrlRef.current);
      audioUrlRef.current = null;
    }

    setMessages([]);
    setMessage("");
    setUploadStatus("");
    setUploadError(false);
  };

  // CLEANUP
  useEffect(() => {
    return () => {
      if (
        mediaRecorderRef.current &&
        mediaRecorderRef.current.state !== "inactive"
      ) {
        mediaRecorderRef.current.stop();
      }

      if (audioRef.current) {
        audioRef.current.pause();
      }

      if (audioUrlRef.current) {
        URL.revokeObjectURL(audioUrlRef.current);
      }
    };
  }, []);

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">AI</div>
          <div>
            <h2>AI Knowledge</h2>
            <span>Platform</span>
          </div>
        </div>

        <button className="new-chat" onClick={startNewChat}>
          + New Chat
        </button>

        <div className="sidebar-bottom">
          <span>AI Knowledge Platform</span>
          <small>RAG • LangGraph • Gemini</small>
        </div>
      </aside>

      <main className="chat-container">
        <header className="chat-header">
          <div>
            <h1>AI Knowledge Assistant</h1>
            <p>Ask questions about your knowledge base</p>
          </div>

          <div className="status">
            <span></span>
            Online
          </div>
        </header>

        <section className="messages">
          {messages.length === 0 ? (
            <div className="welcome">
              <div className="welcome-icon">✦</div>
              <h2>How can I help you?</h2>
              <p>
                Ask a question and I'll search your knowledge base for
                relevant information.
              </p>

              <div className="suggestions">
                <button
                  onClick={() =>
                    setMessage("What is the AI Knowledge Platform?")
                  }
                >
                  What is the AI Knowledge Platform?
                </button>

                <button
                  onClick={() =>
                    setMessage("Explain the available documents")
                  }
                >
                  Explain the available documents
                </button>
              </div>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div className={`message-row ${msg.role}`} key={index}>
                <div className="avatar">
                  {msg.role === "user" ? "You" : "AI"}
                </div>

                <div className="message-content">
                  <strong>
                    {msg.role === "user" ? "You" : "AI Assistant"}
                  </strong>

                  {msg.role === "assistant" ? (
                    <div className="markdown-content">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {normalizeMarkdown(msg.content)}
                      </ReactMarkdown>
                    </div>
                  ) : (
                    <p>{msg.content}</p>
                  )}

                  {msg.sources && msg.sources.length > 0 && (
                    <div className="sources">
                      <strong>Sources</strong>

                      {msg.sources.map((source, sourceIndex) => (
                        <div
                          className="source"
                          key={source.document_id ?? sourceIndex}
                        >
                          <span className="source-number">
                            {sourceIndex + 1}
                          </span>

                          <div className="source-details">
                            <strong>
                              Document {source.document_id ?? "Unknown"}
                            </strong>

                            {source.score != null && (
                              <small>
                                Relevance: {(source.score * 100).toFixed(1)}%
                              </small>
                            )}

                            {source.chunks?.length > 0 ? (
                              <>
                                <small>
                                  {source.chunks.length} relevant chunk(s)
                                </small>

                                {source.chunks.slice(0, 2).map(
                                  (chunk, chunkIndex) => (
                                    <p
                                      className="source-preview"
                                      key={chunk.chunk_index ?? chunkIndex}
                                    >
                                      {normalizeSourceText(chunk.text)}
                                    </p>
                                  )
                                )}
                              </>
                            ) : source.text ? (
                              <p className="source-preview">
                                {normalizeSourceText(source.text)}
                              </p>
                            ) : null}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {loading && (
            <div className="message-row assistant">
              <div className="avatar">AI</div>

              <div className="message-content">
                <strong>AI Assistant</strong>
                <p className="thinking">AI is thinking...</p>
              </div>
            </div>
          )}
        </section>

        <div className="input-area">
          <div className="document-upload">
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
              onChange={uploadDocument}
              disabled={uploading}
              hidden
            />

            <button
              type="button"
              className="upload-button"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
            >
              {uploading ? "Uploading..." : "＋ Upload Document"}
            </button>

            <span className="upload-hint">PDF, DOCX, TXT</span>
          </div>

          {uploadStatus && (
            <p
              className={`upload-status ${uploadError ? "error" : "success"}`}
              role="status"
            >
              {uploadStatus}
            </p>
          )}

          <div className="input-box">
            <input
              type="text"
              value={message}
              disabled={loading}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
              placeholder="Ask something about your knowledge base..."
            />

            <button
              type="button"
              className="voice-button"
              disabled={loading}
              onClick={toggleVoiceInput}
              title={isRecording ? "Stop recording" : "Start voice input"}
            >
              {isRecording ? "🔴 Recording..." : "🎤"}
            </button>

            <button onClick={sendMessage} disabled={loading}>
              {loading ? "Thinking..." : "Send"}
            </button>
          </div>

          <small>
            AI Knowledge Platform can make mistakes. Verify important
            information.
          </small>
        </div>
      </main>
    </div>
  );
}

export default App;

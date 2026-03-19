import { useState } from "react";

export default function MessageInput({ onSend, isLoading }) {
  const [value, setValue] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!value.trim() || isLoading) return;
    onSend(value.trim());
    setValue("");
  };

  return (
    <form className="message-input-form" onSubmit={handleSubmit}>
      <input
        className="message-input"
        type="text"
        placeholder="질문을 입력하세요..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={isLoading}
      />
      <button className="send-btn" type="submit" disabled={isLoading || !value.trim()}>
        전송
      </button>
    </form>
  );
}

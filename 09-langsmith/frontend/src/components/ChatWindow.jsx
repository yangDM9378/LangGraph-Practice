import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import NodeStatus from "./NodeStatus";

export default function ChatWindow({ messages, isLoading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="chat-window">
      {messages.length === 0 && (
        <div className="empty-state">
          <p>궁금한 점을 물어보세요!</p>
          <div className="example-questions">
            <span>배송이 언제 오나요?</span>
            <span>결제가 안 돼요</span>
            <span>앱이 자꾸 튕겨요</span>
          </div>
        </div>
      )}
      {messages.map((msg, i) => (
        <MessageBubble key={i} msg={msg} />
      ))}
      {isLoading && (
        <div className="bubble-wrapper bot">
          <div className="bubble bubble-bot loading-bubble">
            <NodeStatus isLoading={true} />
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}

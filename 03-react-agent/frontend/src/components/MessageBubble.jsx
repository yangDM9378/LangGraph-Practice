import NodeStatus from "./NodeStatus";

const CATEGORY_COLORS = {
  기술지원: "#3b82f6",
  결제: "#f59e0b",
  배송: "#10b981",
  기타: "#8b5cf6",
};

export default function MessageBubble({ msg }) {
  const isUser = msg.role === "user";

  return (
    <div className={`bubble-wrapper ${isUser ? "user" : "bot"}`}>
      <div className={`bubble ${isUser ? "bubble-user" : "bubble-bot"}`}>
        {!isUser && msg.category && (
          <span
            className="category-badge"
            style={{ background: CATEGORY_COLORS[msg.category] || "#6b7280" }}
          >
            {msg.category}
          </span>
        )}
        <p>{msg.content}</p>
        {!isUser && (
          <NodeStatus nodesVisited={msg.nodesVisited} isLoading={false} />
        )}
      </div>
    </div>
  );
}

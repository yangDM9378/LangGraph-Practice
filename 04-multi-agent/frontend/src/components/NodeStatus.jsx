const NODE_LABELS = {
  classify_question: "질문 분류 중",
  generate_answer: "답변 생성 중",
  check_satisfaction: "품질 검토 중",
};

const NODE_ORDER = ["classify_question", "generate_answer", "check_satisfaction"];

export default function NodeStatus({ nodesVisited, isLoading }) {
  if (!isLoading && (!nodesVisited || nodesVisited.length === 0)) return null;

  return (
    <div className="node-status">
      {isLoading ? (
        <div className="node-step active">
          <span className="spinner" />
          처리 중...
        </div>
      ) : (
        NODE_ORDER.map((node) => {
          const visitCount = nodesVisited.filter((n) => n === node).length;
          if (visitCount === 0) return null;
          return (
            <div key={node} className="node-step done">
              <span className="check">✓</span>
              {NODE_LABELS[node]}
              {node === "generate_answer" && visitCount > 1 && (
                <span className="retry-badge">재시도 {visitCount - 1}회</span>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}

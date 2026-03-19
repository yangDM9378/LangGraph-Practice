import { useState, useCallback } from 'react';
import { streamChat } from '../api/stream';

/**
 * 스트리밍 메시지 컴포넌트
 * 토큰이 들어올 때마다 텍스트를 누적해 타이핑 효과를 보여줍니다.
 */
export function StreamingMessage() {
  const [input, setInput] = useState('');
  const [streamingText, setStreamingText] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  const handleSubmit = useCallback(async () => {
    if (!input.trim() || isStreaming) return;

    setStreamingText('');
    setIsStreaming(true);

    // TODO: streamChat()을 호출해 토큰을 받을 때마다 streamingText에 누적하세요
    // streamChat(
    //   input,
    //   'user-session-1',
    //   (token) => setStreamingText(prev => prev + token),
    //   () => setIsStreaming(false),
    // );

    setInput('');
  }, [input, isStreaming]);

  return (
    <div>
      <div style={{ minHeight: 100, border: '1px solid #ccc', padding: 8 }}>
        {streamingText}
        {/* TODO: isStreaming이 true면 커서(|) 애니메이션 표시 */}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSubmit()}
        disabled={isStreaming}
        placeholder="메시지를 입력하세요..."
      />
      <button onClick={handleSubmit} disabled={isStreaming}>
        {isStreaming ? '응답 중...' : '전송'}
      </button>
    </div>
  );
}

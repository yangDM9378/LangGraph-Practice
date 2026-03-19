/**
 * SSE 스트리밍 클라이언트
 * fetch + ReadableStream으로 서버에서 토큰을 하나씩 수신합니다.
 */
export async function streamChat(message, threadId, onToken, onDone) {
  const response = await fetch('http://localhost:8000/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, thread_id: threadId }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop(); // 마지막 불완전한 줄은 버퍼에 보관

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        if (data === '[DONE]') { onDone(); return; }
        try {
          const { token } = JSON.parse(data);
          onToken(token);
        } catch {}
      }
    }
  }
}

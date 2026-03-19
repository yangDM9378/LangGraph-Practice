from langchain_core.tools import tool

# ── FAQ 데이터베이스 (예시) ────────────────────────────────────────────
FAQ_DB = {
    "환불": "구매 후 7일 이내 환불 신청이 가능합니다. 고객센터(1234-5678)로 연락해 주세요.",
    "배송기간": "일반 배송은 2-3 영업일, 빠른 배송은 익일 도착입니다.",
    "비밀번호": "로그인 페이지 하단 '비밀번호 찾기'를 클릭하여 재설정할 수 있습니다.",
}

# ── 주문 데이터베이스 (예시) ──────────────────────────────────────────
ORDER_DB = {
    "12345": "배송 중 (예상 도착: 내일)",
    "67890": "배송 완료",
    "11111": "결제 확인 중",
}


@tool
def search_faq(query: str) -> str:
    """FAQ 데이터베이스에서 사용자 질문과 관련된 항목을 검색합니다.

    Args:
        query: 검색할 키워드 (예: '환불', '배송기간', '비밀번호')
    """
    # TODO: query와 FAQ_DB 키를 매칭하여 관련 항목 반환
    # 힌트: 키워드가 query에 포함돼 있는지 확인
    raise NotImplementedError("search_faq를 구현해 주세요")


@tool
def get_order_status(order_id: str) -> str:
    """주문 번호로 현재 배송/처리 상태를 조회합니다.

    Args:
        order_id: 주문 번호 (예: '12345')
    """
    # TODO: ORDER_DB에서 order_id를 조회하여 상태 반환
    # 없는 주문 번호면 적절한 메시지 반환
    raise NotImplementedError("get_order_status를 구현해 주세요")


# 그래프에서 사용할 도구 목록
tools = [search_faq, get_order_status]

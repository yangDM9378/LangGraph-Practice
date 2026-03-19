from langchain_core.tools import tool

FAQ_DB = {
    "배송비": "기본 배송비는 3,000원입니다. 5만원 이상 구매 시 무료 배송.",
    "환불": "구매 후 7일 이내 환불 가능. 고객센터 1234-5678.",
    "교환": "상품 수령 후 3일 이내 교환 가능. 단, 개봉 상품 불가.",
}

PRODUCT_DB = {
    "노트북": {"가격": 1_200_000, "재고": "있음", "배송": "2일"},
    "마우스": {"가격": 35_000, "재고": "있음", "배송": "1일"},
    "키보드": {"가격": 80_000, "재고": "품절", "배송": "3일"},
}


@tool
def search_faq(query: str) -> str:
    """FAQ 데이터베이스에서 정책/규정 정보를 검색합니다.

    Args:
        query: 검색 키워드 (예: '배송비', '환불', '교환')
    """
    # TODO: query가 포함된 FAQ 항목을 찾아 반환하세요
    raise NotImplementedError("search_faq를 구현해 주세요")


@tool
def calculate(expression: str) -> str:
    """수학 계산식을 평가합니다. 가격 합산, 할인 계산 등에 사용.

    Args:
        expression: 계산식 문자열 (예: '35000 * 3', '1200000 * 0.9')
    """
    # TODO: expression을 안전하게 계산해 결과를 문자열로 반환하세요
    # 힌트: eval()을 사용하되, 숫자와 연산자만 허용하는 검증 추가
    # 주의: eval은 보안 위험이 있으므로 학습용으로만 사용
    raise NotImplementedError("calculate를 구현해 주세요")


@tool
def get_product_info(product_name: str) -> str:
    """상품 이름으로 가격, 재고, 배송 정보를 조회합니다.

    Args:
        product_name: 상품명 (예: '노트북', '마우스', '키보드')
    """
    # TODO: PRODUCT_DB에서 상품 정보를 찾아 포맷된 문자열로 반환하세요
    raise NotImplementedError("get_product_info를 구현해 주세요")


tools = [search_faq, calculate, get_product_info]

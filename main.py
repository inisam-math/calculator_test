import streamlit as st
import math

# 💡 페이지 설정 (선택 사항)
st.set_page_config(
    page_title="Streamlit 다기능 계산기",
    layout="wide"
)

## 🧮 계산기 웹앱 본체

st.title("간단한 계산기 웹앱 🖥️")
st.markdown("---")
st.subheader("연산 입력")

# 사용자 입력 필드
col1, col2 = st.columns(2)

with col1:
    # 첫 번째 숫자 (로그 연산 시 '진수' 역할)
    num1 = st.number_input("**첫 번째 숫자 (x)를 입력하세요.**", value=10.0, step=0.1)

with col2:
    # 두 번째 숫자 (로그 연산 시 '밑' 역할, 나누기/모듈러 연산 시 '제수' 역할)
    num2 = st.number_input("**두 번째 숫자 (y)를 입력하세요.**", value=2.0, step=0.1)

# 연산 종류 선택
operation = st.selectbox(
    "**수행할 연산 종류를 선택하세요:**",
    (
        "덧셈 (+): x + y",
        "뺄셈 (-): x - y",
        "곱셈 (*): x * y",
        "나눗셈 (/): x / y (몫)", 
        "모듈러연산 (%): x % y (나머지)",
        "지수연산 (**): x^y",
        "로그연산 (log_y(x))"
    )
)

st.markdown("---")

# 🧮 계산 로직
result = None
error_message = None

# 계산 실행 버튼
if st.button("계산하기 ⚡️", type="primary"):
    try:
        if operation == "덧셈 (+): x + y":
            result = num1 + num2
        
        elif operation == "뺄셈 (-): x - y":
            result = num1 - num2
        
        elif operation == "곱셈 (*): x * y":
            result = num1 * num2
        
        elif operation == "나눗셈 (/): x / y (몫)":
            if num2 == 0:
                error_message = "오류: 0으로 나눌 수 없습니다. (Divide by Zero)"
            else:
                result = num1 / num2
        
        elif operation == "모듈러연산 (%): x % y (나머지)":
            if num2 == 0:
                error_message = "오류: 0으로 모듈러 연산할 수 없습니다. (Modulo by Zero)"
            else:
                result = num1 % num2
        
        elif operation == "지수연산 (**): x^y":
            result = num1 ** num2
        
        elif operation == "로그연산 (log_y(x))":
            # 로그의 정의: 진수(x)는 0보다 커야 하고, 밑(y)은 1이 아닌 양수여야 함.
            if num1 <= 0:
                error_message = "오류: 로그의 진수(x)는 0보다 커야 합니다."
            elif num2 <= 0 or num2 == 1:
                error_message = "오류: 로그의 밑(y)은 1이 아닌 양수여야 합니다."
            else:
                # math.log(x, base) 사용
                result = math.log(num1, num2)
                
    except Exception as e:
        error_message = f"계산 중 예상치 못한 오류가 발생했습니다: {e}"

# 📢 결과 출력
st.subheader("계산 결과")
if error_message:
    st.error(error_message)
elif result is not None:
    st.success(f"선택하신 연산의 결과는 **{result}** 입니다.")
    st.info(f"결과 타입: **{type(result).__name__}**")

st.markdown("---")

## 🚀 GitHub와 Streamlit을 이용한 배포 가이드
st.subheader("GitHub 및 Streamlit 배포")
st.markdown("""
1.  **`app.py` 파일 저장**: 위 코드를 `app.py`라는 이름으로 저장합니다.
2.  **GitHub 저장소 생성**: 새로운 GitHub 저장소를 만듭니다.
3.  **파일 업로드**: `app.py` 파일을 GitHub 저장소에 커밋하여 업로드합니다.
4.  **Streamlit Community Cloud 배포**:
    * [Streamlit Community Cloud](https://streamlit.io/cloud)에 접속합니다.
    * 'New app'을 클릭하고, 연동할 GitHub 저장소와 `app.py` 파일의 경로를 지정합니다.
    * 'Deploy!'를 누르면 웹앱이 배포됩니다.
""")

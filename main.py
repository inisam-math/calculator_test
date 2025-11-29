import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd # 시뮬레이션 결과 처리를 위해 pandas 추가

# 💡 페이지 설정
st.set_page_config(
    page_title="다기능 수학 웹앱 (계산기/그래프/확률)",
    layout="wide"
)

# --- 사이드바: 기능 선택 ---
st.sidebar.title("앱 기능 선택 ⚙️")
selected_app = st.sidebar.selectbox(
    "원하는 기능을 선택하세요:",
    ["계산기", "함수 그래프 그리기", "확률 시뮬레이터"]
)

# --- 1. 일반 계산기 모드 ---
if selected_app == "계산기":
    st.header("🧮 일반 계산기 모드")
    
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("**첫 번째 숫자 (x)를 입력하세요.**", value=10.0, step=0.1)
    with col2:
        num2 = st.number_input("**두 번째 숫자 (y)를 입력하세요.**", value=2.0, step=0.1)

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

    result = None
    error_message = None

    if st.button("계산하기 ⚡️"):
        try:
            if "덧셈" in operation:
                result = num1 + num2
            elif "뺄셈" in operation:
                result = num1 - num2
            elif "곱셈" in operation:
                result = num1 * num2
            elif "나눗셈" in operation:
                if num2 == 0:
                    error_message = "오류: 0으로 나눌 수 없습니다."
                else:
                    result = num1 / num2
            elif "모듈러연산" in operation:
                if num2 == 0:
                    error_message = "오류: 0으로 모듈러 연산할 수 없습니다."
                else:
                    result = num1 % num2
            elif "지수연산" in operation:
                result = num1 ** num2
            elif "로그연산" in operation:
                if num1 <= 0:
                    error_message = "오류: 로그의 진수(x)는 0보다 커야 합니다."
                elif num2 <= 0 or num2 == 1:
                    error_message = "오류: 로그의 밑(y)은 1이 아닌 양수여야 합니다."
                else:
                    result = math.log(num1, num2)
                    
        except Exception as e:
            error_message = f"계산 중 오류가 발생했습니다: {e}"

    if error_message:
        st.error(error_message)
    elif result is not None:
        st.success(f"**결과:** {result}")

# --- 2. 함수 그래프 그리기 모드 ---
elif selected_app == "함수 그래프 그리기":
    st.header("📈 함수 그래프 그리기 모드")
    st.info("변수는 **x**를 사용하세요. (예: `x**2`, `np.sin(x)`)")

    equation = st.text_input("함수 식을 입력하세요:", value="np.sin(x)")
    
    col_min, col_max = st.columns(2)
    with col_min:
        x_min = st.number_input("x 최소값", value=-10.0)
    with col_max:
        x_max = st.number_input("x 최대값", value=10.0)

    if st.button("그래프 그리기 🖼️"):
        try:
            x = np.linspace(x_min, x_max, 400)
            
            # 보안을 위해 numpy 모듈 함수를 포함한 안전한 딕셔너리 생성
            safe_dict = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "log": np.log, "exp": np.exp}
            
            # eval()을 사용하여 문자열 수식을 계산
            y = eval(equation, {"__builtins__": None}, safe_dict)

            # 그래프 그리기 (Matplotlib)
            fig, ax = plt.subplots()
            ax.plot(x, y, label=f"y = {equation}")
            ax.axhline(0, color='black', linewidth=0.5) 
            ax.axvline(0, color='black', linewidth=0.5) 
            ax.grid(True, linestyle='--')
            ax.legend()
            ax.set_title(f"y = {equation}")
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"수식을 해석할 수 없습니다. 문법을 확인해주세요. 오류: {e}")

# --- 3. 확률 시뮬레이터 모드 ---
elif selected_app == "확률 시뮬레이터":
    st.header("🎲 확률 시뮬레이터")
    st.markdown("주사위 또는 동전을 던지는 시뮬레이션을 수행하고 결과를 시각화합니다.")

    sim_type = st.selectbox(
        "**시뮬레이션 대상 선택**",
        ["주사위 던지기 (1~6)", "동전 던지기 (앞/뒤)"]
    )
    
    num_trials = st.number_input("**시행 횟수를 입력하세요**", min_value=10, max_value=100000, value=1000, step=100)

    if st.button("시뮬레이션 실행 및 시각화 ✨"):
        
        st.subheader(f"{num_trials}회 시뮬레이션 결과")

        if sim_type == "주사위 던지기 (1~6)":
            # 1부터 6까지의 정수를 num_trials 횟수만큼 랜덤하게 생성
            results = np.random.randint(1, 7, size=num_trials)
            
            # 각 숫자의 출현 횟수 계산
            counts = pd.Series(results).value_counts().sort_index()
            
            # 데이터프레임으로 정리
            df_counts = pd.DataFrame(counts).rename(columns={'count': '횟수'})
            df_counts['비율 (%)'] = (df_counts['횟수'] / num_trials) * 100

            st.dataframe(df_counts, use_container_width=True)
            
            # Matplotlib 시각화
            fig, ax = plt.subplots()
            ax.bar(df_counts.index, df_counts['횟수'], color='skyblue')
            ax.set_title(f"주사위 던지기 결과 ({num_trials}회)")
            ax.set_xlabel("주사위 눈금")
            ax.set_ylabel("출현 횟수")
            ax.set_xticks(df_counts.index)
            st.pyplot(fig)
            
            st.caption(f"이론적 확률: 각 눈금별 약 {100/6:.2f}%")

        elif sim_type == "동전 던지기 (앞/뒤)":
            # 0(뒤) 또는 1(앞)을 num_trials 횟수만큼 생성
            results = np.random.randint(0, 2, size=num_trials)
            
            # 횟수 계산
            heads = np.sum(results) # 1의 개수 (앞면)
            tails = num_trials - heads # 0의 개수 (뒷면)
            
            counts = pd.Series([heads, tails], index=['앞면 (1)', '뒷면 (0)'])
            
            df_counts = pd.DataFrame(counts).rename(columns={0: '횟수'})
            df_counts['비율 (%)'] = (df_counts['횟수'] / num_trials) * 100

            st.dataframe(df_counts, use_container_width=True)
            
            # Streamlit 차트 시각화 (Matplotlib보다 간편)
            st.bar_chart(df_counts['횟수'])
            
            st.caption(f"이론적 확률: 앞면, 뒷면 각각 50.00%")

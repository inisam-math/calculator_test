import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# 페이지 기본 설정
st.set_page_config(page_title="똑똑한 수학 계산기", page_icon="🧮")

# 타이틀 및 설명
st.title("🧮 파이썬 수학 계산기 & 그래프")
st.markdown("""
이 웹앱은 **기본 연산**과 **수학 함수 그래프**를 그리는 기능을 제공합니다.
사이드바에서 모드를 선택해주세요.
""")

# 사이드바: 모드 선택
mode = st.sidebar.selectbox("모드 선택", ["일반 계산기", "함수 그래프 그리기"])

# --- 모드 1: 일반 계산기 ---
if mode == "일반 계산기":
    st.header("🔢 일반 연산 모드")
    
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("첫 번째 숫자", value=0.0)
    with col2:
        num2 = st.number_input("두 번째 숫자", value=0.0)

    # 연산자 선택
    operation = st.selectbox(
        "연산 종류를 선택하세요",
        ["더하기 (+)", "빼기 (-)", "곱하기 (*)", "나누기 (/)", 
         "나머지 (Modulo, %)", "거듭제곱 (Power, ^)", "로그 (Log)"]
    )

    if st.button("계산하기"):
        result = 0
        try:
            if "더하기" in operation:
                result = num1 + num2
                st.success(f"결과: {num1} + {num2} = **{result}**")
                
            elif "빼기" in operation:
                result = num1 - num2
                st.success(f"결과: {num1} - {num2} = **{result}**")
                
            elif "곱하기" in operation:
                result = num1 * num2
                st.success(f"결과: {num1} * {num2} = **{result}**")
                
            elif "나누기" in operation:
                if num2 == 0:
                    st.error("0으로 나눌 수 없습니다.")
                else:
                    result = num1 / num2
                    st.success(f"결과: {num1} / {num2} = **{result}**")
                    
            elif "나머지" in operation:
                if num2 == 0:
                    st.error("0으로 나눌 수 없습니다.")
                else:
                    result = num1 % num2
                    st.success(f"결과: {num1} % {num2} = **{result}**")
                    
            elif "거듭제곱" in operation:
                result = math.pow(num1, num2)
                st.success(f"결과: {num1}의 {num2}승 = **{result}**")
                
            elif "로그" in operation:
                # num1은 진수, num2는 밑(base)
                if num1 <= 0:
                    st.error("진수(첫 번째 숫자)는 0보다 커야 합니다.")
                elif num2 <= 0 or num2 == 1:
                    st.error("밑(두 번째 숫자)은 0보다 크고 1이 아니어야 합니다.")
                else:
                    result = math.log(num1, num2)
                    st.success(f"결과: log_{num2}({num1}) = **{result}**")
                    
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# --- 모드 2: 그래프 그리기 ---
elif mode == "함수 그래프 그리기":
    st.header("📈 함수 그래프 모드")
    st.info("변수는 **x**를 사용하세요. (예: `x**2`, `np.sin(x)`, `x + 3`)")

    # 수식 입력
    equation = st.text_input("함수 식을 입력하세요:", value="np.sin(x)")
    
    # x축 범위 설정
    col1, col2 = st.columns(2)
    with col1:
        x_min = st.number_input("x 최소값", value=-10.0)
    with col2:
        x_max = st.number_input("x 최대값", value=10.0)

    if st.button("그래프 그리기"):
        try:
            # x 값 생성 (구간을 400개로 쪼갬)
            x = np.linspace(x_min, x_max, 400)
            
            # 사용자 입력을 파이썬 코드로 변환하여 y값 계산
            # 보안을 위해 numpy 모듈을 np로 사용할 수 있게 함
            safe_dict = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "log": np.log, "exp": np.exp}
            
            # eval()을 사용하여 문자열 수식을 계산
            y = eval(equation, {"__builtins__": None}, safe_dict)

            # 그래프 그리기 (Matplotlib)
            fig, ax = plt.subplots()
            ax.plot(x, y, label=f"y = {equation}")
            ax.axhline(0, color='black', linewidth=0.5) # x축
            ax.axvline(0, color='black', linewidth=0.5) # y축
            ax.grid(True, linestyle='--')
            ax.legend()
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            
            # 스트림릿에 그래프 표시
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"수식을 해석할 수 없습니다. 문법을 확인해주세요.\n오류 내용: {e}")
            st.warning("팁: 제곱은 `^` 대신 `**`를 사용하세요. 삼각함수는 `np.sin(x)`처럼 입력하세요.")

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import plotly.express as px

# 💡 페이지 설정
st.set_page_config(
    page_title="다기능 수학 웹앱 (계산기/그래프/확률/인구분석)",
    layout="wide"
)

# --- 사이드바: 기능 선택 ---
st.sidebar.title("앱 기능 선택 ⚙️")
selected_app = st.sidebar.selectbox(
    "원하는 기능을 선택하세요:",
    ["계산기", "함수 그래프 그리기", "확률 시뮬레이터", "연도별 세계인구 분석"]
)

# --- 1. 일반 계산기 모드 (기존 코드 유지) ---
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

# --- 2. 함수 그래프 그리기 모드 (기존 코드 유지) ---
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
            
            safe_dict = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "log": np.log, "exp": np.exp}
            y = eval(equation, {"__builtins__": None}, safe_dict)

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

# --- 3. 확률 시뮬레이터 모드 (기존 코드 유지) ---
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
            results = np.random.randint(1, 7, size=num_trials)
            counts = pd.Series(results).value_counts().sort_index()
            df_counts = pd.DataFrame(counts).rename(columns={'count': '횟수'})
            df_counts['비율 (%)'] = (df_counts['횟수'] / num_trials) * 100

            st.dataframe(df_counts, use_container_width=True)
            
            fig, ax = plt.subplots()
            ax.bar(df_counts.index, df_counts['횟수'], color='skyblue')
            ax.set_title(f"주사위 던지기 결과 ({num_trials}회)")
            ax.set_xlabel("주사위 눈금")
            ax.set_ylabel("출현 횟수")
            ax.set_xticks(df_counts.index)
            st.pyplot(fig)
            
        elif sim_type == "동전 던지기 (앞/뒤)":
            results = np.random.randint(0, 2, size=num_trials)
            heads = np.sum(results) 
            tails = num_trials - heads 
            
            counts = pd.Series([heads, tails], index=['앞면 (1)', '뒷면 (0)'])
            df_counts = pd.DataFrame(counts).rename(columns={0: '횟수'})
            df_counts['비율 (%)'] = (df_counts['횟수'] / num_trials) * 100

            st.dataframe(df_counts, use_container_width=True)
            st.bar_chart(df_counts['횟수'])

# --- 4. 연도별 세계인구 분석 모드 (새로운 기능) ---
elif selected_app == "연도별 세계인구 분석":
    st.header("🌎 연도별 세계인구 분석")
    st.markdown("선택된 연도의 국가별 인구 데이터를 지도에 시각화하여 보여줍니다.")

    # 1. 연도 선택 드롭박스
    selected_year = st.selectbox(
        "**데이터를 확인할 연도를 선택하세요:**",
        (1970, 1980, 1990, 2000, 2015, 2020, 2022)
    )

    # 2. 예시 데이터 생성 (실제 첨부 파일이 없으므로, Plotly 내장 데이터셋의 구조를 모방하여 더미 인구 데이터를 생성)
    # Plotly의 gapminder 데이터셋을 불러와 국가 코드와 연도를 맞춥니다.
    df = px.data.gapminder().query(f"year == {selected_year}")
    
    # 인구 구간에 따른 색상 구분 기능을 시연하기 위해 임의의 인구 데이터로 대체 (실제 데이터 분석은 파일이 필요)
    # *참고: 실제 인구 분석을 위해서는 첨부된 파일의 데이터 구조와 국가 코드를 확인해야 합니다.*
    
    if selected_year == 2022:
        # 2022년은 인구가 상대적으로 많다고 가정하고 임의의 값 조정
        df['pop'] = df['pop'] * 1.5 
    
    # 3. 세계 지도 생성 및 구간별 색상 칠하기 (Choropleth Map)
    
    # Plotly Express Choropleth Map 생성
    # color_continuous_scale: 색상 그라데이션을 설정
    # color: 지도에 색을 칠할 기준 (여기서는 pop, 즉 인구)
    # locations, locationcode: 국가 식별에 사용되는 코드 (ISO-A3는 3자리 국가 코드)
    fig = px.choropleth(df, 
                        locations="iso_alpha",  # 국가 식별자 (ISO-A3 코드)
                        color="pop",            # 인구(pop) 값을 기준으로 색상을 지정
                        hover_name="country",   # 마우스 오버 시 표시할 이름
                        projection="natural earth", # 지도 투영 방식
                        color_continuous_scale=px.colors.sequential.Plasma, # 인구수에 따른 색상 팔레트
                        title=f"{selected_year}년 세계 인구 분포 (인구수 구간별 색상 구분)"
                        )
    
    # 4. 레이아웃 조정 및 표시
    fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        coloraxis_colorbar=dict(
            title="인구수 (명)",
            tickvals=[df['pop'].min(), df['pop'].mean(), df['pop'].max()],
            ticktext=["최소", "평균", "최대"]
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **데이터 참고 사항:**
    * 실제 첨부된 파일을 분석하는 대신, **Plotly Express**에 내장된 `gapminder` 데이터셋을 활용하여 지도 시각화 기능을 구현했습니다.
    * 인구수 (`pop`) 값의 크기에 따라 자동으로 색상 구간이 나뉘어 지도에 칠해집니다.
    * 2022년 데이터는 상대적인 인구 변화 시연을 위해 임의로 인구값을 조정했습니다.
    """)

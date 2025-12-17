import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import os

# 폰트 경로 설정
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NanumGothic-Regular.ttf')
font_path_bold = os.path.join(os.path.dirname(__file__), 'fonts', 'NanumGothic-Bold.ttf')

# matplotlib 한글 폰트 설정
rcParams['font.family'] = 'NanumGothic'
rcParams['axes.unicode_minus'] = False

# 폰트 파일 등록
from matplotlib.font_manager import fontManager
fontManager.addfont(font_path)
fontManager.addfont(font_path_bold)

# 페이지 설정
st.set_page_config(
    page_title="📊 초등학생 데이터 수집",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS - 파스텔 톤 색상, 큰 폰트
st.markdown("""
    <style>
    @font-face {
        font-family: 'NanumGothic';
        src: url('file:///workspaces/dbswltjd1211/fonts/NanumGothic-Regular.ttf') format('truetype');
    }
    
    @font-face {
        font-family: 'NanumGothic-Bold';
        src: url('file:///workspaces/dbswltjd1211/fonts/NanumGothic-Bold.ttf') format('truetype');
        font-weight: bold;
    }
    
    * {
        font-family: 'NanumGothic', 'Arial', sans-serif;
    }
    
    h1 {
        color: #FF6B9D;
        font-size: 50px !important;
        text-align: center;
        margin-bottom: 30px;
        font-family: 'NanumGothic-Bold', 'Arial', sans-serif;
    }
    
    h2 {
        color: #A8D8EA;
        font-size: 35px !important;
        font-family: 'NanumGothic-Bold', 'Arial', sans-serif;
    }
    
    h3 {
        color: #AA96DA;
        font-size: 28px !important;
        font-family: 'NanumGothic-Bold', 'Arial', sans-serif;
    }
    
    .big-text {
        font-size: 28px !important;
        font-weight: bold;
        font-family: 'NanumGothic', 'Arial', sans-serif;
    }
    
    .explanation-box {
        background-color: #FFF4E6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FFB6C1;
        font-size: 24px;
        margin: 15px 0;
        line-height: 1.8;
        font-family: 'NanumGothic', 'Arial', sans-serif;
    }
    
    .stat-box {
        background-color: #E0F4FF;
        padding: 15px;
        border-radius: 8px;
        font-size: 22px;
        margin: 10px 0;
        font-weight: bold;
        color: #0066CC;
        font-family: 'NanumGothic', 'Arial', sans-serif;
    }
    
    .input-label {
        font-size: 22px !important;
        font-weight: bold;
        color: #AA96DA;
        font-family: 'NanumGothic', 'Arial', sans-serif;
    }
    
    button {
        font-size: 20px !important;
        padding: 15px 30px !important;
        font-family: 'NanumGothic', 'Arial', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'data' not in st.session_state:
    st.session_state.data = []

st.title("📊 우리의 데이터를 모아봐!")

st.divider()

# 데이터 입력 섹션
st.subheader("📝 데이터 입력하기")

col1, col2, col3 = st.columns([2, 1.5, 1])

with col1:
    st.markdown("<p class='input-label'>항목 이름:</p>", unsafe_allow_html=True)
    item_name = st.text_input("", placeholder="예: 딸기, 사탕, 별", label_visibility="collapsed")

with col2:
    st.markdown("<p class='input-label'>수량:</p>", unsafe_allow_html=True)
    quantity = st.number_input("", min_value=0, max_value=100, value=0, step=1, label_visibility="collapsed")

with col3:
    st.write("")
    st.write("")
    if st.button("➕ 추가", use_container_width=True):
        if item_name.strip():
            st.session_state.data.append({"name": item_name.strip(), "count": int(quantity)})
            st.rerun()
        else:
            st.warning("⚠️ 항목 이름을 입력해주세요!")

st.divider()

# 데이터가 있을 때만 표시
if st.session_state.data:
    # 데이터 테이블
    st.subheader("📋 입력한 데이터")
    
    df = pd.DataFrame(st.session_state.data)
    
    # 데이터 표 표시 (큰 폰트)
    col1, col2 = st.columns([2, 1])
    with col1:
        # 커스텀 테이블 표시
        for idx, row in df.iterrows():
            col_name, col_count = st.columns([2, 1])
            with col_name:
                st.markdown(f"<div class='big-text'>🔹 {row['name']}</div>", unsafe_allow_html=True)
            with col_count:
                st.markdown(f"<div class='stat-box'>{row['count']}</div>", unsafe_allow_html=True)
            
            # 삭제 버튼
            if st.button(f"❌ {row['name']} 삭제", key=f"delete_{idx}"):
                st.session_state.data.pop(idx)
                st.rerun()
    
    st.divider()
    
    # 통계 계산
    total = df['count'].sum()
    max_item = df.loc[df['count'].idxmax()]
    min_item = df.loc[df['count'].idxmin()]
    difference = max_item['count'] - min_item['count']
    
    # 통계 설명
    st.subheader("📈 우리의 데이터를 분석해봐!")
    
    st.markdown(f"""
        <div class='explanation-box'>
        🌟 <b>가장 많은 것:</b> {max_item['name']}이(가) {max_item['count']}개로 제일 많아요!
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='explanation-box'>
        ✨ <b>전체 개수:</b> {max_item['name']}, {min_item['name']}을(를) 모두 합치면 {total}개예요!
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='explanation-box'>
        🎯 <b>차이:</b> {max_item['name']}이(가) {min_item['name']}보다 {difference}개 더 많아요!
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 그래프 표시
    st.subheader("📊 그래프 보기")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 파스텔 톤 색상 팔레트
    pastel_colors = [
        '#FFB6C1',  # 연한 핑크
        '#FFD700',  # 연한 노랑
        '#87CEEB',  # 하늘색
        '#DDA0DD',  # 자주색
        '#F0E68C',  # 카키색
        '#B0E0E6',  # 파우더 블루
        '#FFB6D9',  # 연한 빨강
        '#D8BFD8',  # 엷은 자주색
    ]
    
    # 막대그래프
    colors = [pastel_colors[i % len(pastel_colors)] for i in range(len(df))]
    bars = ax.bar(df['name'], df['count'], color=colors, edgecolor='white', linewidth=2)
    
    # 막대 위에 숫자 표시
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=28, fontweight='bold')
    
    ax.set_ylabel('개수', fontsize=28, fontweight='bold')
    ax.set_xlabel('항목', fontsize=28, fontweight='bold')
    ax.set_title('막대그래프', fontsize=32, fontweight='bold', pad=20)
    
    # 그래프 스타일 설정
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.tick_params(labelsize=24, colors='#333333')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    # 초기화 버튼
    st.divider()
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 모두 지우기", use_container_width=True):
            st.session_state.data = []
            st.rerun()
    
else:
    st.info("📌 위에서 항목과 수량을 입력하고 '➕ 추가' 버튼을 눌러보세요!")

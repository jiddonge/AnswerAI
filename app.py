import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="답정너AI 로그 대시보드", layout="wide")

st.title("📊 답정너AI 로그 대시보드")
csv_path = "chat_log.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)

    st.subheader("📁 저장된 대화 로그")
    st.dataframe(df, use_container_width=True)

    # 필터 기능
    with st.expander("🔍 필터링"):
        col1, col2 = st.columns(2)
        with col1:
            user_type = st.selectbox("사용자 유형", ["전체"] + sorted(df["사용자유형"].dropna().unique().tolist()))
        with col2:
            policy = st.selectbox("추천 정책", ["전체"] + sorted(df["추천정책"].dropna().unique().tolist()))

        filtered_df = df.copy()
        if user_type != "전체":
            filtered_df = filtered_df[filtered_df["사용자유형"] == user_type]
        if policy != "전체":
            filtered_df = filtered_df[filtered_df["추천정책"] == policy]

        st.write(f"🔎 {len(filtered_df)}건의 결과가 검색되었습니다.")
        st.dataframe(filtered_df, use_container_width=True)

    # CSV 다운로드
    st.download_button(
        label="📥 로그 CSV 다운로드",
        data=filtered_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="답정너AI_대화로그.csv",
        mime="text/csv"
    )
else:
    st.warning("아직 로그 파일(chat_log.csv)이 생성되지 않았습니다.")

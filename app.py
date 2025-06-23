import streamlit as st
import pandas as pd
import os
from datetime import date

CSV_FILE = "kakeibo.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["日付", "カテゴリ", "内容", "金額", "収支"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

st.title("💰 家計簿アプリ（Streamlit版）")

with st.form("entry_form"):
    date_input = st.date_input("日付", date.today())
    category = st.text_input("カテゴリ")
    memo = st.text_input("内容")
    amount = st.number_input("金額", step=100)
    submitted = st.form_submit_button("登録")
    if submitted:
        kind = "収入" if amount > 0 else "支出"
        new_row = {
            "日付": date_input.isoformat(),
            "カテゴリ": category,
            "内容": memo,
            "金額": amount,
            "収支": kind
        }
        df = load_data()
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("登録しました！")

df = load_data()
st.subheader("📊 履歴")
st.dataframe(df)

col1, col2 = st.columns(2)
col1.metric("合計収入", f"{df[df['収支']=='収入']['金額'].sum():,} 円")
col2.metric("合計支出", f"{df[df['収支']=='支出']['金額'].sum():,} 円")

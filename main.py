import streamlit as st
import sys
import json
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from SetData import setdata


def result_page():
    # ページ2の内容
    st.title('結果の表示')
    input_value = st.session_state.get('input_value')
    st.write('取得したURL:', input_value)
    st.session_state.setdata = setdata.SetData(input_value)
    for name in st.session_state.setdata.data_user_frame.keys():
        st.header(name)
        st.session_state.setdata.data_user_frame[name]=st.session_state.setdata.data_user_frame[name].replace("", pd.NA).dropna(how='all', axis=0)
        st.write(st.session_state.setdata.data_user_frame[name])

    if st.button('URL入力画面に戻る'):
        # ページ2に遷移する際に入力値を渡す
        del st.session_state['input_value']
        st.experimental_rerun()


def main_page():
    # ページ1の内容
    st.title('URL入力画面')
    text_input = st.text_input('とんとんスケジュールのURLを入力してください')

    if st.button('結果の取得'):
        # ページ2に遷移する際に入力値を渡す
        st.session_state['input_value'] = text_input
        st.experimental_rerun()  # ページ2に遷移するために再描画

    st.write('Input value:', text_input)


if __name__ == '__main__':
    # ページの切り替え
    if 'input_value' not in st.session_state:
        main_page()  # ページ1を表示
    else:
        result_page()  # ページ2を表示
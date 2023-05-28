from bs4 import BeautifulSoup
import requests
import pandas as pd
from typing import List, Tuple, Dict, Any
# import re

class SetData:
    """
    入力したとんとんurlの各種データ互換を作成・保持する。

    Parameters
    ----------
    url : str
        とんとんスケジュールのURL

    Attributes
    ----------
    schedule_lists : List[Any]
        とんとんスケジュールのHTMLを<div class="schedulelist">で区切ったもの

    data : Dict[str, Dict[str, Dict[str,str]]]
        とんとんスケジュールのデータを日付、ユーザー、時間の順に格納したもの

    data_date_frame : pd.DataFrame
        とんとんスケジュールのデータを日付ごとに集計したもの

    data_user_dict : Dict[str, Dict[str, Dict[str,str]]]
        とんとんスケジュールのデータをユーザーごとに集計したもの

    data_user_frame : pd.DataFrame
        とんとんスケジュールのデータをユーザーごとに集計したもの
    """


    def __init__(self, url:str):
        self.url: str = url
        self.schedule_lists: List[Any] = self.get_HTML()
        self.data:Dict[str, Dict[str, Dict[str,str]]] = self.get_info()
        self.data_date_frame:pd.DataFrame = self.data_date_frame()
        self.data_user_dict:Dict[str, Dict[str, Dict[str,str]]] = self.data_user_dict()
        self.data_user_frame:pd.DataFrame = self.data_user_frame()


    def get_HTML(self) -> list:
    # GETリクエストを送信してWebページを取得
        response = requests.get(self.url)

        # ステータスコードをチェック
        if response.status_code == 200:
            # 取得したWebページのパース
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.find_all("div", class_="schedulelist")
        else:
            return False

    def get_info(self) -> dict:
        # 初期化
        data:dict = {}

        for schedule_list in self.schedule_lists:
            # temp領域の定義
            data_temp:dict = {}
            time_temp:list = []
            symbol_temp:list =[]

            # html解析
            index: list = schedule_list.find_all('div', class_="nowrap")
            date = index.pop(0).find('label').get_text()

            # ユーザーごとの要素を抽出
            for schedule, name in zip(schedule_list.find_all("td", class_="timeline")[1:], index):
                # 時間:シンボル辞書の初期化
                wrap_schedule:dict = {}
                # 時間:シンボルの抽出
                for span in schedule.select("span"):
                    s_time = str(span.get('id'))[-4:]
                    s_symbol = span.get('title')
                    wrap_schedule[s_time] = s_symbol
                    # time_temp.append(s_time)
                    # symbol_temp.append(s_symbol)
                # for time, symbol in zip(time_temp, symbol_temp):
                    # wrap_schedule[time]
                # 名前との関連付け
                name = name.get_text()
                name = name.replace('\u3000', '')
                name = name.replace('\u200b', '')
                data_temp[name] = wrap_schedule
            # 日付との関連付け
            data[date] = data_temp

        return data

    # 日付ごとに集計したDataFrameを作成
    def data_date_frame(self) -> dict:
        data_date = dict()
        for date in self.data.keys():
            data_date[date] = pd.DataFrame(self.data[date])
        return data_date

    # ユーザーごとに集計した辞書を作成
    def data_user_dict(self) -> dict:
        data_user_dict = dict()
        for date, data_name_time in self.data.items():
            for name, time_data in data_name_time.items():
                if name in data_user_dict.keys():
                    data_user_dict[name][date]=time_data
                else:
                    data_user_dict[name] = dict()
                    data_user_dict[name][date]=time_data
        return data_user_dict

    # ユーザーごとに集計したDataFrameを作成
    def data_user_frame(self) -> dict:
        data_user_frame = dict()
        for name in self.data_user_dict.keys():
            data_user_frame[name] = pd.DataFrame(self.data_user_dict[name])
        return data_user_frame

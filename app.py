import networkx as nx
import matplotlib.pyplot as plt
import csv
import streamlit as st
import os
import pandas as pd

st.title("デードリ分析")

DIR_PATH = 'csvs'

st.write("まず、ファイルをアップロードしてから分析開始ボタンを押してください。最後にファイルを画像としてダウンロードできます。")

file = st.file_uploader('Upload your csv file', type=['csv'])
if file:
    st.markdown(f'{file.name} has been uploaded')
    dir_path = os.path.join(DIR_PATH, file.name)
    # ファイルを保存する
    with open(dir_path, 'wb') as f:
        f.write(file.read())
        
    # 保存したCSVを表示する
    img = pd.read_csv(dir_path)
    st.write(img)

if file is not None:
    
    keisu = st.slider('反発係数', 0.0, 2.5, 0.7)
    lineweight = st.slider('線の太さ', 0.0, 10.0, 5.0)

    H=nx.Graph()   # use ne

    csv_file = open(dir_path, "r", encoding="UTF-8", errors="", newline="" )
    #リスト形式
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    for row in f:
    # weight付でnodeとエッジも入れる
        H.add_weighted_edges_from([(row[0], row[1], float(row[2]))])

    # weightによって線の太さを変える
    edge_width = [d["weight"] * 5 for (u, v, d) in H.edges(data=True)]

    # posを定義
    pos = nx.spring_layout(H, k=keisu)  # k = node間反発係数

    # 図示
    nx.draw(H,pos, with_labels=True, width=edge_width)
    plt.savefig("exported.png")


if st.button("分析開始"):
    st.image("exported.png")

with open("exported.png", "rb") as file:
    st.download_button(
        label="Download data as image",
        data=file,
        file_name='exported.png',
        mime='',
    )
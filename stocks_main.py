
import streamlit as st
import numpy as np
import pandas as pd
from time import sleep

st.title("株取引シミュレーター")
#板情報の生成
buy_price=np.arange(100,94,-1) 
order_quantity=np.repeat(1000,6)
empty_order=[]
for i in range(0,6):
    empty_order.append("")
buy_df=pd.DataFrame({"売数量":empty_order,"価格":buy_price,"買数量":order_quantity})
sell_price=np.arange(106,100,-1)
sell_df=pd.DataFrame({"売数量":order_quantity,"価格":sell_price,"買数量":empty_order})
stocks_board=pd.concat([sell_df,buy_df],axis=0).reset_index(drop=True)
print(stocks_board)

# DataFrameをHTMLとしてレンダリングし、中央寄せを適用
def make_pretty(styler):
    styler.set_properties(**{'text-align': 'center'})
    styler.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
    return styler

#注文画面（３カラム構成）
col_1,col_2,col_3=st.columns(3)
# st.dataframeではなく、st.markdownを使用してHTMLを表示
with col_1:
    st.write("注文前の板")
    st.markdown(make_pretty(stocks_board.style).to_html(), unsafe_allow_html=True)
with col_2:
    input_quantity=st.number_input("株数を入力",value=100,min_value=100,max_value=1000,step=100)
    col_buysell,col_type=st.columns(2)
    with col_buysell:
        order_buysell=st.radio("売買種別",["買","売"])
    order=st.button("注文")
    with col_type:
        order_type=st.radio("注文方法",["成行","指値"])
        if order_type=="指値":
            if order_buysell=="買":
                order_price=st.number_input("価格を入力",value=100,min_value=95,max_value=100,step=1)
            else:
                order_price=st.number_input("価格を入力",value=101,min_value=101,max_value=106,step=1)
    
with col_3:
    if order: #注文処理
        if order_type=="成行":
            if order_buysell=="買": #買成注文
                if stocks_board.iloc[5,0]==input_quantity:
                    stocks_board.iloc[5,1]=""
                    stocks_board.iloc[5,0]=""
                    
                else:
                    stocks_board.iloc[5,0]=stocks_board.iloc[5,0]-input_quantity
            else: #売成注文
                if stocks_board.iloc[6,2]==input_quantity:
                    stocks_board.iloc[6,1]=""
                    stocks_board.iloc[6,2]=""
                else:
                    stocks_board.iloc[6,2]=stocks_board.iloc[6,2]-input_quantity
                print(stocks_board)
            st.write("注文後の板")
            st.markdown(make_pretty(stocks_board.style).to_html(), unsafe_allow_html=True)
            
        else: #指値注文の場合
            found = False  # 価格が一致する行が見つかったかどうかのフラグ
            for index, row in stocks_board.iterrows():
                if order_price == row['価格']:
                    print("ありました", row['価格'])
                    if order_buysell=="買":# 指買注文
                        stocks_board.at[index, '買数量'] = row['買数量'] + input_quantity
                        print(stocks_board.at[index, '買数量'])
                        found = True
                        st.write("注文後の板")
                        st.markdown(make_pretty(stocks_board.style).to_html(), unsafe_allow_html=True)
                        break  # 一致する行が見つかったらループを抜ける
                    else: #指売注文
                        stocks_board.at[index,"売数量"]= row["売数量"] + input_quantity
                        print(stocks_board.at[index,"売数量"])
                        found=True
                        st.write("注文後の板")
                        st.markdown(make_pretty(stocks_board.style).to_html(), unsafe_allow_html=True)
                        break  # 一致する行が見つかったらループを抜ける
            if not found:
                print("一致する価格の注文はありません")
              

st.write("-----------------------------------------------")

if order:
    sleep(1)
    st.write(f"{input_quantity}株{order_type}の{order_buysell}注文が処理されました（注文前後の板を比較）")
    sleep(1)
    st.write("注文方法によって動きが異なるので、色々なパターンを試してみよう")
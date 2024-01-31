import streamlit as st
import time

st.set_page_config(page_title='Como Calculamos',
                   page_icon='🧮',
                   layout='wide'
                   )



st.title('Forma como é calculado o Expositor')
st.divider()
st.header('A forma é por Rateio de venda x Area plana do produto:')

st.subheader('O Cálculo')
st.text_area('envolve o cadastro da Largura e profundidade do Item')

with st.spinner('Aguarde...'):
    time.sleep(3)
st.success('Boa Gabgol!')
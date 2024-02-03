import streamlit as st
import pandas as pd
import time

from xarray import align

st.set_page_config(page_title='Home',
                   page_icon='🏠',
                   layout='centered'
                   )

st.image('images\logo_bistek.png',output_format='PNG',use_column_width='never')

st.divider()
st.title("Análise Guerrilha")
st.caption('Bem vindo(a) este é um Dashboard Desenvolvido usando Python.')

with st.container(height=180):
    st.markdown('''Análise  preventiva para garantir que as lojas estejam abastecidas na medida certa, evitando quaisquer **:red[excessos]** de produtos:
                ''')
    
    st.markdown('''Que seja rápida⚡ de identificar e saber qual ação tomar para **:green[resolver]**.
                ''')

    st.markdown('''O Relatório é separado por páginas estruturadas para ser **:green[simples]** 💡 e **:green[intuitiva]** 🧠.
                ''')

    
st.subheader("Relatórios Disponíveis ✅")


relatorios_disp = {'• 🚩 Itens Mapeados Sem Saldo no CD':'&mdash; Contém os itens que foram mapeados e :red[não temos saldo no CD] ainda!',
                   '• 📦 Análise de Excesso': '&mdash; Contém os itens onde o que foram mapeados e :red[irão em excesso] para as lojas!',
                   '• 🤖 Forma de Cálculo': '&mdash; Contém a informação detalhada, método de cálculo explicado **:blue[passo-a-passo]**.',
                   '• 🕹️ Simulador de expositor': '&mdash; Aqui você pode simular   quantidade que vai enviar por produto loja, **:green[ideal para planejar exposições especiais!]**',
}
for k,v in relatorios_disp.items():
    with st.container(height=100):
        st.markdown(k)
        st.caption(v)


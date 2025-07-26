import streamlit as st
st.set_page_config(layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>RevoText</h1>",
    unsafe_allow_html=True
)

def feldolgozas():
    eredmeny1=st.session_state.text1
    # Eredményeket eltároljuk session_state-ben
    st.session_state.text2 = eredmeny1
    
# Szövegmezők létrehozása
col1,col2 ,col3 = st.columns(3)
with col1:
    st.text_area("Szövegmező 1", key="text1", height=400)

with col3:
    st.text_area("Szövegmező 2", key="text2", height=400)
# Egyszerű feldolgozás gombnyomásra
with col2:
    st.button("Feldolgozás indítása", on_click=feldolgozas,use_container_width=True)


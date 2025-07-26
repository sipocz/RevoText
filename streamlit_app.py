import streamlit as st

import json
from openai import OpenAI
st.set_page_config(layout="wide")
key = st.secrets["API_KEYS"]["OpenAI"]


def create_prompt(szoveg):
    prompt_message=[
            {"role": "system",
             "content": f'''
                    Te egy ingatlanhirdetés-elemző nyelvész vagy, komoly ingatlanhirdetési tapasztalattal.
                    Célod, hogy az ingatlan hirdetések tökéletesek legyenek ezért kidolgoztál egy hirdetés értékelési szempontrendszert.
                    Ezek a szempontok alapján tökéletes értékelést tudsz adni az adott hirdetés szövege alapján.
                    A szempontok:
                        1. Érthetőség
                        2. Részletesség / információtartalom
                        3. Szerkezet, logikai felépítés
                        4. Célcsoport megszólítása
                        5. Stílus és nyelvhelyesség
                        6. Előnyök kiemelése
                        7. Negatívumok őszinte kezelése
                        8. Eladásra ösztönzés'''},
            {"role": "user",
             "content": """
                            Értékeld az alábbi ingatlanhirdetés szöveget az alábbi szempontok alapján 1–5-ig,
                            és hozz létre egy összesített eredményt az 1-8 közötti értékek átlagaként ez legyen a 9. Összesítés :
                            A válaszod csak érvényes JSON formátumban legyen, pontosan az alábbi struktúrában:

                            {

                                "Érthetőség": <szám>,
                                "Részletesség": <szám>,
                                "Szerkezet": <szám>,
                                "Célcsoport": <szám>,
                                "Stílus": <szám>,
                                "Előnyök": <szám>,
                                "Negatívumok": <szám>,
                                "Ösztönzés": <szám>,
                                "Összesítés": <szám.tizedes>"
                            }



                    A HIRDETÉS SZÖVEGE:
                        """+f" {szoveg}"}
        ]
    return prompt_message




if 'ratings' not in st.session_state:
    st.session_state.ratings = {
        "Érthetőség": 1,
        "Részletesség": 1,
        "Szerkezet": 1,
        "Célcsoport": 1,
        "Stílus": 1,
        "Előnyök": 1,
        "Negatívumok": 1,
        "Ösztönzés": 1,
        "Összesítés": 1
            }


def get_response(szoveg:str):
    client = OpenAI(api_key=key)
    prompt_message=create_prompt(szoveg)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt_message,
        temperature=0.2,
        max_tokens=200
    )
   
    out_dict= json.loads(response.choices[0].message.content)

    return(out_dict)

st.markdown(
    "<h1 style='text-align: center;'>RevoText</h1>",
    unsafe_allow_html=True
)

def feldolgozas():
    
    user_text=st.session_state.text1
    # Eredményeket eltároljuk session_state-ben
    ai_result=get_response(user_text)
    #st.write(ai_result)
    st.session_state.ratings=ai_result
    st.session_state.text2 = "ai_result"

def ertekeles(d:dict)->str:
    for szempont, ertek in d.items():
        
        csillagok = f'{ertek}'+" - "+"⭐️" * int(ertek) + "☆" * (5 - int(ertek))
        st.markdown(f"**{szempont}**  {csillagok}", unsafe_allow_html=True)

# Szövegmezők létrehozása
col1,col2 ,col3 = st.columns(3)
with col1:
    st.text_area("Szövegmező 1", key="text1", height=400)

with col3:
    st.text_area("Szövegmező 2", key="text2", height=400)
# Egyszerű feldolgozás gombnyomásra
with col2:
    st.button("Feldolgozás indítása", on_click=feldolgozas,use_container_width=True)

with col2:
    ertekeles(st.session_state.ratings)
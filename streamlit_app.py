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
                            Értékeld az alábbi ingatlanhirdetés szöveget és az értékelést a scoring mezőbe helyezzed el.
                            Az alábbi szempontok alapján 1–5-ig pontozzad, és hozz létre egy összesített eredményt  1-8 közötti szempontok értékelésének átlagaként ez legyen a 9. Összesítés :
                            Majd a tudásod alapján adj egy alternatív javaslatot az eredeti szöveg javítására, hogy a lehető legjobban megfeleljen a szempontoknak. 
                            Az alternatív javaslatot strukturáld, és tördeld a jobb érthetőség érdekében!
                            Fontos, hogy a saját szempontrendszered szerint az alternatív javaslatod értékelése jobb legyen az eredeti értékelésnél!  
                            A válaszod csak érvényes JSON formátumban legyen, pontosan az alábbi struktúrában:

                            {"scoring":
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
                                },
                            "proposal":"Ide kerüljön a javított szöveg javaslatod"    



                    A HIRDETÉS SZÖVEGE:
                        """+f" {szoveg}"}
        ]
    return prompt_message



# ameddig nincs még értékelés minden alaphelyzeten lesz
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
        model="gpt-4o",
        messages=prompt_message,
        temperature=0.5,
        max_tokens=2900
    )
   
    content = response.choices[0].message.content

    # a gpt-4 így adja vissza a json választ, kiszedjük a jsont a felesleges keretből
    if content.startswith("```json"):
        content = content.strip("`").lstrip("json").strip()

    # 
    out_dict = json.loads(content)

    return(out_dict)

st.markdown(
    "<h1 style='text-align: center;'>RevoText</h1><h3 style='text-align: center;'>Version:0.4</h3>",
    unsafe_allow_html=True
)

def feldolgozas():
    
    user_text=st.session_state.text1
    # Eredményeket eltároljuk session_state-ben
    ai_result=get_response(user_text)
    


    print(ai_result) # server oldali kiiratás 
    #st.write(ai_result) #Debug
    st.session_state.ratings=ai_result["scoring"]
    st.session_state.text2 = ai_result["proposal"]

def ertekeles(d:dict)->str:
    for szempont, ertek in d.items():
        
        csillagok = f'{ertek}'+" - "+"⭐️" * int(ertek) + "☆" * (5 - int(ertek))
        st.markdown(f"**{szempont}**  {csillagok}", unsafe_allow_html=True)

# Szövegmezők létrehozása
col1,col2 ,col3 = st.columns(3)
with col1:
    st.text_area("Eredeti hirdetés szövege", key="text1", height=600)

with col3:
    st.text_area("AI javaslat", key="text2", height=600)
# Egyszerű feldolgozás gombnyomásra
with col2:
    st.button("Feldolgozás indítása", on_click=feldolgozas,use_container_width=True)

with col2:
    ertekeles(st.session_state.ratings)
column1,column2=st.columns(2)
with column1:
    st.markdown(st.session_state.text2)
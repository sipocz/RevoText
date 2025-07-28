import streamlit as st

import json
from openai import OpenAI


def create_prompt(commands,txt):
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
                            Az alternatív javaslat generálása során használjad STÍLUS: és a MÓD: cimkékkel megjelölt előírásokat, de markdown formátumot ne használj!
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
                        
                        Előírások:
                        """+f"{commands}"+f"Eredeti hirdetés: {txt}"}
        ]
    print(prompt_message) #Debug
    return prompt_message

def create_command(): # streamlit globális változókból dolgozik
    s=f"STÍLUS:{st.session_state.mood}\n"
    m=f"MÓD:{st.session_state.mode}\n"
    return(s+m)



def get_response(command:str, szoveg:str):
    client = OpenAI(api_key=key)
    prompt_message=create_prompt(command, szoveg)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt_message,
        temperature=0.7,
        max_tokens=3900
    )
   
    content = response.choices[0].message.content

    # a gpt-4 így adja vissza a json választ, kiszedjük a jsont a felesleges keretből
    if content.startswith("```json"):
        content = content.strip("`").lstrip("json").strip()

    # 
    out_dict = json.loads(content)

    return(out_dict)

def feldolgozas():
    
    user_text=st.session_state.text1
    # Eredményeket eltároljuk session_state-ben
    command=create_command()
    ai_result=get_response(command,user_text)
    


    print(ai_result) # server oldali kiiratás 
    #st.write(ai_result) #Debug
    st.session_state.ratings=ai_result["scoring"]
    st.session_state.text2 = ai_result["proposal"]

def csillagok(d:dict)->str:
    for _, ertek in d.items():
        
        csillagok = "⭐️" * int(ertek) + "☆" * (5 - int(ertek))
        st.markdown(f"{csillagok}", unsafe_allow_html=True)

def pontszamok(d:dict)->str:
    for _ , ertek in d.items():
        
        ertekek = f'{ertek}'
        st.markdown(f"**{ertekek}**", unsafe_allow_html=True)

def szempontok(d:dict)->str:
    for szempont, _ in d.items():
        
        st.markdown(f"**{szempont}**", unsafe_allow_html=True)



st.set_page_config(layout="wide")
key = st.secrets["API_KEYS"]["OpenAI"]
  



# vizuális elemek

# ameddig nincs még értékelés minden alaphelyzeten lesz
if 'ratings' not in st.session_state:
    st.session_state.ratings = {
        "Érthetőség": 0,
        "Részletesség": 0,
        "Szerkezet": 0,
        "Célcsoport": 0,
        "Stílus": 0,
        "Előnyök": 0,
        "Negatívumok": 0,
        "Ösztönzés": 0,
        "Összesítés": 0
            }  


if 'mood' not in st.session_state:                  #Global változó legyen
    st.session_state.mood="💼 Professzionális"

if 'mode' not in st.session_state:                  #Global változó legyen
    st.session_state.mode="Szöveges"








#st.markdown("---")  # vízszintes vonal
st.markdown("<div style='height: 3px;'></div>", unsafe_allow_html=True)  # függőleges térköz
c1,c2,c3,c4,c5 = st.columns([40,20,20,20,20])

with c1:
    with st.expander("📦 RevoText v0.5"):
        st.markdown('''## 📦 RevoText – Forradalmasítjuk az ingatlanhirdetéseket

A **RevoText** egy mesterséges intelligenciával működő **szövegasszisztens**, amely segít a hirdetőknek profi, érthető és vonzó ingatlanleírásokat készíteni – egyszerűen és gyorsan.

Legyen szó garzonlakásról vagy családi házról, a RevoText a vázlatos szövegeket meggyőző hirdetésekké alakítja, kiemelve az ingatlan valódi értékeit.

✍️ *Te csak írd le, amit szeretnél – a RevoText gondoskodik a tökéletes megfogalmazásról.*

---

### Mit nyújt a RevoText?

- ✅ Automatikus szövegjavítás, stilisztikai és nyelvtani finomítás  
- ✅ Választható hangnem: barátságos, professzionális, exkluzív... 
- ✅ Kiemelések, érthető szerkezet, jobb olvashatóság  
- ✅ SEO-barát szövegek a jobb online megjelenésért
''')
    
    #st.markdown("<h3 style='text-align: left;'>RevoText</h3>", unsafe_allow_html=True


with c5:
    with st.expander("📇 Kapcsolat"):
        st.markdown("""
            ### 📇 Kapcsolat

            **👤 Név:** Sipőcz László  
            **✉️ E-mail:** [sipoczlaszlo@gmail.com](mailto:sipoczlaszlo@gmail.com)  
            **📞 Telefon:** +36 20 47 46 47 3  
            **🔗 LinkedIn:** [linkedin.com/in/36204746473/](https://www.linkedin.com/in/36204746473/)
            """)

with c2:
    st.session_state.mood = st.selectbox("💡 Válassz hangulatot:", ["💼 Professzionális", "😊 Barátságos", "🎩 Exkluzív", "🤖 Tech", "🎨 Kreatív"],key="mood_")
    st.write(f"A választott hangulat: {st.session_state.mood }")
with c3:
    st.session_state.mode = st.selectbox("💡 Válassz módot:", ["📄 Szöveges", "✅ Tagolt"],key="mode_")
    st.write(f"A választott mód: {st.session_state.mode}")


   


col1,col2 ,col3 = st.columns(3)
with col1:
    st.text_area("Eredeti hirdetés szövege", key="text1", height=600)
    

with col3:
    st.text_area("AI javaslat", key="text2", height=600)
    
# Egyszerű feldolgozás gombnyomásra
with col2:
    st.markdown("---")  # vízszintes vonal
    st.button("⎯⎯⎯  Kérem a javaslatot! ➤➤➤ ", on_click=feldolgozas,use_container_width=True)

    st.markdown("---")  # vízszintes vonal    
    st.markdown(f"<p style='text-align:center;'>Az eredeti szöveg értékelése</p>", unsafe_allow_html=True)
   
    o1,o2,o3=st.columns([3,1,6])
    with o1:
        szempontok(st.session_state.ratings)
    with o2:
        pontszamok(st.session_state.ratings)   
    with o3:
        csillagok(st.session_state.ratings)
    
    st.markdown("---")  # vízszintes vonal

st.markdown("---")  # vízszintes vonal
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # függőleges térköz

column1,column2=st.columns(2)

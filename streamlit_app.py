import streamlit as st

import json
from openai import OpenAI


st.set_page_config(layout="wide",
                   page_title="RevoText", 
                   page_icon="📦",
                   menu_items={
        
        "Report a bug": "https://github.com/sipocz/RevoText/issues",
        "About": '''
        ## 📦 RevoText – Forradalmasítjuk az ingatlanhirdetéseket

A **RevoText** egy mesterséges intelligenciával működő **szövegasszisztens**, amely segít a hirdetőknek profi, érthető és vonzó ingatlanleírásokat készíteni – egyszerűen és gyorsan.

Legyen szó garzonlakásról vagy családi házról, a RevoText a vázlatos szövegeket meggyőző hirdetésekké alakítja, kiemelve az ingatlan valódi értékeit.

✍️ *Te csak írd le, amit szeretnél – a RevoText gondoskodik a tökéletes megfogalmazásról.*

---

### Mit nyújt a RevoText?

- ✅ Automatikus szövegjavítás, stilisztikai és nyelvtani finomítás  
- ✅ Választható hangnem: barátságos, professzionális, exkluzív... 
- ✅ Kiemelések, érthető szerkezet, jobb olvashatóság  
- ✅ SEO-barát szövegek a jobb online megjelenésért
'''})




def create_prompt(szoveg,commands="None")->str:

    content="""
                            Értékeld az alábbi ingatlanhirdetés szöveget és az értékelést a scoring mezőbe helyezzed el.
                            Az alábbi szempontok alapján 1–5-ig pontozzad, és hozz létre egy összesített eredményt  1-8 közötti szempontok értékelésének átlagaként ez legyen a 9. Összesítés :
                            Majd a tudásod alapján adj egy alternatív javaslatot az eredeti szöveg javítására, hogy a lehető legjobban megfeleljen a szempontoknak.
                            Az alternatív javaslatot strukturáld, és tördeld a jobb érthetőség érdekében, de markdown formátumot ne használj!
                            Fontos, hogy a saját szempontrendszered szerint az alternatív javaslatod értékelése jobb legyen az eredeti értékelésnél!\n
                            - A címek generálásánál vedd figyelembe a következőket:\n"
            """ +f'{commands}\n' + """    
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
                            }


                    A HIRDETÉS SZÖVEGE:
                        """+f" {szoveg}"
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
             "content": content}
        ]
    return prompt_message

def create_title_prompt(szoveg: str,commands:str)->str:
    return [
        {
            "role": "system",
            "content": (
            "Te egy tömör szövegíró vagy. KIZÁRÓLAG a megadott hirdetésszöveg alapján "
            "készíts pontosan öt ütős címajánlatot.\n\n"
            "Korlátok:\n"
            "- A kimenet KÖTELEZŐEN érvényes JSON objektum legyen pontosan ebben a formában: {\"titles\": [\"...\", \"...\", \"...\", \"...\", \"...\"]}\n"
            "- Ne használj markdown-t, kód fence-et, extra kulcsokat, magyarázatot.\n"
            "- Minden cím legfeljebb 60 karakter legyen, magyar nyelven, emojik és idézőjelek nélkül.\n"
            "- Ne találj ki a hirdetésben nem szereplő tényeket.\n"
            "- Legyenek egymástól különbözőek (más nézőpont/szövegezés), jól olvashatók és kattintásra ösztönzők.\n"
            "- A címek generálásánál vedd figyelembe a következőket:\n"
            f"-{commands}\n"    
            ),
        },
        {
            "role": "user",
            "content": f"INGATLAN HIRDETÉS SZÖVEGE:\n{szoveg}"
        }
    ]



def create_command(mood:str,lang:str,mode:str)->str: 
    s=f"Használandó STÍLUS:{mood}\n"
    
    m=f"Használandó MÓD:{mode}\n"
    if st.session_state.mode=="📄 Szöveges":
        m=m+"Csak részletes szöveges leírást használj, ne legyen benne felsorolás, ne legyen lista és ne legyen tagolás sem!\n"
    else:
        m=m+"Használj szöveg tagolást és felsorolásokat, listákat a szövegben! De ne legyen markdown formátum benne, csak kötőjellel  és soremeléssel tagolj!\n"
       
    l=f"A hirdetés szöveg nyelvéhez ezt a nyelvet használjad :{lang} !\n"
    
    return(s+m+l)

def create_title_command(mood:str,  lang:str,mode="")->str:
    s=f"Használandó STÍLUS: {mood}\n"
    l=f"A cím szöveg nyelvéhez ezt a nyelvet használjad: {lang}!\n"
    
    return(s+l)





def get_response(szoveg:str,func,command)->dict:
    '''
    A megadott szöveghez promptot készít (`create_prompt`), elküldi az OpenAI Chat
    Completions API-nak (gpt-4o), majd a választ JSON-ként beolvassa és dict-ként visszaadja.

    Paraméterek
    -----------
    szoveg : str
        A bemeneti szöveg, amelyből a `create_prompt` összeállítja a `messages` listát.

    Visszatérés
    -----------
    dict
        A modell által visszaadott JSON objektum, Python dict-be parse-olva.
    '''
    client = OpenAI(api_key=key)
    
    prompt_message=func(szoveg,command)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt_message,
        temperature=0.5,
        max_tokens=7000,
        response_format={ "type": "json_object" }   
    )

    content = response.choices[0].message.content
    out_dict = json.loads(content)

    return(out_dict)


def create_ai_proposal():
    
    user_text=st.session_state.text1
    # Eredményeket eltároljuk session_state-ben
    command=create_command(mood=st.session_state.mood,mode=st.session_state.mode,lang=st.session_state.lang)
    ai_result=get_response(user_text,create_prompt,command)
    
    print(ai_result) # server oldali kiiratás 
    #st.write(ai_result) #Debug
    st.session_state.ratings=ai_result["scoring"]
    st.session_state.ai_proposal=ai_result["proposal"]  # ezt később még használni fogjuk
    st.session_state.text2 = st.session_state.ai_proposal 


def create_title():
    
    gen_text=st.session_state.ai_proposal 
    # Eredményeket eltároljuk session_state-ben
    command=create_title_command(mood=st.session_state.mood,mode=st.session_state.mode,lang=st.session_state.lang)
    print(command)
    ai_result=get_response(gen_text,create_title_prompt,command)
    
    print(ai_result) # server oldali kiiratás 
    #st.write(ai_result) #Debug
    st.session_state.text2=ai_result["titles"][0]+"\n\n"+st.session_state.ai_proposal
    st.session_state.title_list=ai_result["titles"]

def update_title():
    print(st.session_state.selected_title)
    st.session_state.text2=st.session_state.title_list[st.session_state.selected_title]+"\n\n"+st.session_state.ai_proposal
   




def use_test():
    st.session_state.text1='''Győrtöl 14 kilometerre 3 szóbás, lakható csaldi ház eladó.

Jellemezői:

- 856 m2-es telke
- a felítmény téglából épült, kő alapos
- 78 m2-es lakótér
- a tető héjzata cseríp
- csatorna, viz és villan közművel ellátott a ház
- kázcsonk telkhatáron
- melleg vizellátás: elektronyos bolyler

- fűtése: cserépkajha
- 2007-ben felújítás keretein belül cserélték a nyílássárókat, tettőt (lícezés, fólia, héjazat), elektronyos- és vízhálózatot, burkolattokatt
- 15 m2-es karázs + tárolasra alkalmas mellékes ípületek
- ásot kut
- tellyes kifiztést követően rövides időn belül birtokba vehető

Több látnyivaló és nevezetessíg található a kösségbe, továbbá a környékén is, mint pl. a Pannonhalmi Főpátság, a pincesorr stb.
Amenyiben felkelttette érdeklődést, keressen hizalommal. '''


def csillagok(d:dict)->str:
    for _, ertek in d.items():
        
        csillagok = "⭐️" * int(float(ertek)) + "☆" * (5 - int(ertek))
        st.markdown(f"{csillagok}", unsafe_allow_html=True)

def pontszamok(d:dict)->str:
    for _ , ertek in d.items():
        
        ertekek = f'{ertek}'
        st.markdown(f"**{ertekek}**", unsafe_allow_html=True)

def szempontok(d:dict)->str:
    for szempont, _ in d.items():
        
        st.markdown(f"**{szempont}**", unsafe_allow_html=True)









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

if "text2" not in st.session_state:
    st.session_state.text2=""


if 'mood' not in st.session_state:                  #Global változó legyen
    st.session_state.mood="💼 Professzionális"

if 'mode' not in st.session_state:                  #Global változó legyen
    st.session_state.mode="Szöveges"

if 'lang' not in st.session_state:                  #Global változó legyen
    st.session_state.lang="Magyar"

if "proposed_text" not in st.session_state:
    st.session_state.proposed_text=""

#st.markdown("---")  # vízszintes vonal

head0,head1=st.columns([70,30])
with head0:
    with st.expander("📦 RevoText v0.6 - Címek ajánlása"):
        st.info('''## 📦 RevoText – Forradalmasítjuk az ingatlanhirdetéseket

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

with head1:
    with st.expander("📇 Kapcsolat"):
        st.info("""
            ### 📇 Kapcsolat

            **👤 Név:** Sipőcz László  
            **✉️ E-mail:** [sipoczlaszlo@gmail.com](mailto:sipoczlaszlo@gmail.com)  
            **📞 Telefon:** +36 20 47 46 47 3  
            **🔗 LinkedIn:** [linkedin.com/in/36204746473/](https://www.linkedin.com/in/36204746473/)
            """)




st.markdown("<div style='height: 3px;'></div>", unsafe_allow_html=True)  # függőleges térköz
c1,c2,c3,c4,c5 = st.columns([10,20,20,20,10])




with c1:
    pass
    
    #st.markdown("<h3 style='text-align: left;'>RevoText</h3>", unsafe_allow_html=True


with c5:
    pass
with c2:
    st.session_state.mood = st.selectbox("🎭 A hirdetés hangulata :", ["💼 Professzionális", "😊 Barátságos", "🎩 Exkluzív", "🤖 Tech", "🎨 Kreatív"],key="mood_", help="A generált hirdetési szöveg hangulatát ezzel a mezővel lehet befolyásolni!")
    # st.write(f"A választott hangulat: {st.session_state.mood }")
with c3:
    st.session_state.mode = st.selectbox("🧠 A hirdetés megjelenési módja:", ["📄 Szöveges", "✅ Tagolt"],key="mode_",  help="A hirdetés **megjelenésének** módja választható")
    # st.write(f"A választott mód: {st.session_state.mode}")
with c4:
    st.session_state.lang = st.selectbox("🌍 A hirdetés nyelve:",["Magyar", "Angol", "Német"],key="lang_", help="A hirdetés **nyelve** választható")
    # st.write(f"A választott nyelv: {st.session_state.lang}")


   


col1,col2 ,col3 = st.columns([2,2,3])
with col1:
    st.text_area("Eredeti hirdetés szövege", key="text1", height=600)

with col3:
    st.select_slider("Cím",options=[0,1,2,3,4],on_change=update_title,key="selected_title")
    st.text_area("AI javaslat", key="text2", height=600)
    
# Egyszerű feldolgozás gombnyomásra
with col2:
    st.markdown("---")  # vízszintes vonal
    st.button("⎯⎯⎯  Kérem a javaslatot! ➤➤➤ ", on_click=create_ai_proposal,use_container_width=True)
    
    st.button("⎯⎯⎯  Kérek egy jó címet ➤➤➤ ", on_click=create_title,use_container_width=True,disabled=len(st.session_state.text2)==0)
    
    st.button("◀◀◀ Teszt szöveg 😆 ⎯⎯⎯ ", on_click=use_test,use_container_width=True)

    #st.markdown("---")  # vízszintes vonal    
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



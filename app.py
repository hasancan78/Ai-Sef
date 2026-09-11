import streamlit as st
import google.generativeai as genai
import os
import random
import re
from dotenv import load_dotenv
from security import (
    full_security_check, sanitize_input, sanitize_ai_response,
    validate_api_key, check_session_timeout
)

load_dotenv()

import uuid
import streamlit.components.v1 as components
from fpdf import FPDF
import re

def create_recipe_pdf(recipe_text):
    # Başlığı bul
    title_match = re.search(r'###\s*(.*?)\n', recipe_text)
    title = title_match.group(1).strip() if title_match else "AIŞef Tarifi"
    title = title.replace('*', '')

    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.add_font('Roboto', '', 'Roboto-Regular.ttf')
        pdf.set_font('Roboto', size=12)
    except Exception as e:
        print(f"Font hatası: {e}")
        pdf.set_font('Helvetica', size=12)
        
    pdf.multi_cell(0, 10, text=title.upper(), align='C')
    pdf.ln(5)
    
    clean_text = recipe_text.replace('*', '').replace('#', '')
    pdf.multi_cell(0, 7, text=clean_text)
    return bytes(pdf.output())
def clean_for_tts(text):
    # Emojileri ve markdown sembollerini temizle
    # Sadece harf, rakam, boşluk ve temel noktalama işaretlerine izin ver
    text = text.replace('*', '').replace('#', '').replace('`', '').replace('$', '').replace('<', '').replace('>', '')
    text = re.sub(r'[^\w\s.,;:!?\'"%-]', '', text)
    return text

def smart_categorize(recipe_text, current_cat):
    if current_cat != txt["cat_other"]:
        return current_cat
        
    text_lower = recipe_text.lower()
    
    # Tatlı
    if any(k in text_lower for k in ["tatlı", "kek", "pasta", "kurabiye", "çikolata", "şerbet", "sütlaç", "dondurma", "puding", "cheesecake"]):
        return txt["cat_dessert"]
    # İçecek
    if any(k in text_lower for k in ["içecek", "smoothie", "çay", "kahve", "kokteyl", "limonata", "meyve suyu", "milkshake"]):
        return txt["cat_drink"]
    # Kahvaltı
    if any(k in text_lower for k in ["kahvaltı", "yumurta", "omlet", "pankek", "krep", "menemen", "sucuklu", "tost"]):
        return txt["cat_breakfast"]
    # Çorba / Sulu Yemek -> Akşam
    if any(k in text_lower for k in ["çorba", "yahni", "kızartma", "fırın", "ızgara", "kebap", "köfte", "makarna"]):
        return txt["cat_dinner"]
        
    return txt["cat_dinner"] # Default to dinner if nothing matches, usually it's a main dish.

def display_recipe_and_actions(recipe_key, category):
    recipe_text = st.session_state.get(recipe_key, "")
    if not recipe_text: return
    
    st.markdown(f'<div class="recipe-card">{recipe_text}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        # Check if already fav
        all_favs = database.get_favorites()
        is_fav = any(f['text'] == recipe_text for f in all_favs)
        if is_fav:
            st.button("❤️ " + txt["fav_success"], disabled=True, key=f"fav_{recipe_key}")
        else:
            if st.button(txt["add_fav"], key=f"fav_{recipe_key}"):
                final_cat = smart_categorize(recipe_text, category)
                database.add_favorite(recipe_text, final_cat)
                st.rerun()
                
    with col2:
        try:
            pdf_bytes = create_recipe_pdf(recipe_text)
            st.download_button(
                label=txt["download"],
                data=pdf_bytes,
                file_name=f"tarif_{recipe_key}.pdf",
                mime="application/pdf",
                key=f"dl_{recipe_key}"
            )
        except Exception as e:
            # Fallback to markdown if pdf fails
            st.download_button(
                label=txt["download"] + " (MD)",
                data=recipe_text,
                file_name=f"tarif_{recipe_key}.md",
                mime="text/markdown",
                key=f"dl_fb_{recipe_key}"
            )
            print(f"PDF Error: {e}")
        
    with col3:
        btn_id = f"tts_{recipe_key}"
        html_code = f"""
        <div style="display: flex; gap: 5px;">
            <button id="{btn_id}" style="background-color: #ff4b4b; color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-weight: bold; flex: 1;">
                {txt['read_aloud']}
            </button>
            <button id="stop_{btn_id}" style="background-color: #555; color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-weight: bold;">
                {txt['stop_read']}
            </button>
        </div>
        <script>
            document.getElementById("{btn_id}").addEventListener("click", function() {{
                var text = `{clean_for_tts(recipe_text)}`;
                var msg = new SpeechSynthesisUtterance();
                msg.text = text;
                msg.lang = "{ 'tr-TR' if st.session_state.dil_secimi == 'TR' else 'en-US' }";
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(msg);
            }});
            document.getElementById("stop_{btn_id}").addEventListener("click", function() {{
                window.speechSynthesis.cancel();
            }});
        </script>
        """
        components.html(html_code, height=50)

# ╔══════════════════════════════════════════════════════════════╗
# ║                    📱 UYGULAMA BAŞLANGIÇ                    ║
# ╚══════════════════════════════════════════════════════════════╝

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AIŞef", page_icon="🤖", layout="wide")

# --- Session Timeout Kontrolü ---
check_session_timeout()

# --- Session State ---
if "tarif_gecmisi" not in st.session_state:
    st.session_state.tarif_gecmisi = []


from themes import get_theme_css
from lang import get_text
import database

database.init_db()

# --- TEMA VE DİL SEÇİMİ (ANA EKRANDA) ---
if "dil_secimi" not in st.session_state:
    st.session_state.dil_secimi = "TR"
if "tema_secimi" not in st.session_state:
    st.session_state.tema_secimi = "🔥 Kızıl Tutku"

col_t1, col_t2, col_t3 = st.columns([5, 2, 2])
with col_t2:
    def on_lang_change():
        pass
        
    dil_secimi = st.selectbox(
        "🌐 Dil / Language", 
        ["TR", "EN"], 
        index=0 if st.session_state.dil_secimi == "TR" else 1,
        key="dil_secici",
        on_change=on_lang_change
    )
    st.session_state.dil_secimi = dil_secimi
    txt = get_text(dil_secimi)
    
with col_t3:
    tema_opts = ["🔥 Kızıl Tutku", "🌌 Gece Mavisi", "☀️ Aydınlık", "💖 Neon Fuşya"]
    
    # Callback trigger to ensure immediate rerender on theme change
    def on_theme_change():
        pass # state is automatically updated via key

    tema_secimi = st.selectbox(
        txt["theme"], 
        tema_opts,
        index=tema_opts.index(st.session_state.tema_secimi) if st.session_state.tema_secimi in tema_opts else 0,
        key="tema_secici",
        on_change=on_theme_change
    )
    # Streamlit key="tema_secici" ye yazdığı için asıl değişkene de kopyalayalım
    st.session_state.tema_secimi = tema_secimi


# Seçilen temayı uygula
st.markdown(get_theme_css(tema_secimi), unsafe_allow_html=True)


import random
import re
gunun_ipucu = random.choice([
    txt["g_tip1"], txt["g_tip2"], txt["g_tip3"], txt["g_tip4"],
    txt["g_tip5"], txt["g_tip6"], txt["g_tip7"], txt["g_tip8"],
])

st.markdown(f"""
<div class="hero-section" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
<div style="flex: 1; min-width: 250px;">
<div class="hero-title">AIŞef</div>
<div class="hero-subtitle">{txt["hero_sub"]}</div>
<div class="hero-badge">⚡ POWERED BY AI</div>
</div>
<div style="flex: 0 1 550px; background: rgba(0,0,0,0.15); backdrop-filter: blur(5px); padding: 20px 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); z-index: 1; margin-left: auto;">
<div style="font-size: 0.9rem; font-weight: 700; color: inherit; opacity: 0.8; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1.5px;">
{txt['tip_title']}
</div>
<div style="display: flex; gap: 10px; align-items: start;">
<span style="font-size: 2.2rem;">{gunun_ipucu[0]}</span>
<span style="font-size: 1.05rem; color: inherit; line-height: 1.5; margin-top: 5px;">{gunun_ipucu[1]}</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# --- ÖZELLİK KARTLARI ---
st.markdown(f"""
<div class="features-row">
    <div class="feature-card">
        <div class="f-icon">🍅</div>
        <div class="f-title">{txt["feat_1_title"]}</div>
        <div class="f-desc">Elindeki malzemeleri yaz, yapay zeka sana yaratıcı bir tarif üretsin</div>
    </div>
    <div class="feature-card">
        <div class="f-icon">📖</div>
        <div class="f-title">{txt["feat_2_title"]}</div>
        <div class="f-desc">İstediğin yemeğin adını yaz, malzemeleri ve yapılışını öğren</div>
    </div>
    <div class="feature-card">
        <div class="f-icon">🎲</div>
        <div class="f-title">{txt["feat_3_title"]}</div>
        <div class="f-desc">Karar veremiyorsan AI seni şaşırtsın, yepyeni lezzetler keşfet</div>
    </div>
    <div class="feature-card">
        <div class="f-icon">🔥</div>
        <div class="f-title">{txt["feat_4_title"]}</div>
        <div class="f-desc">{txt["feat_4_desc"]}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- POPÜLER YEMEKLER ---
st.markdown(f"""
<div class="popular-section">
    <div class="popular-title">{txt["pop_recipes"]}</div>
    <div class="popular-grid">
        <div class="popular-chip">🍕 Pizza</div>
        <div class="popular-chip">🍔 Hamburger</div>
        <div class="popular-chip">🥘 Karnıyarık</div>
        <div class="popular-chip">🍝 Makarna</div>
        <div class="popular-chip">🥗 Salata</div>
        <div class="popular-chip">🍰 Cheesecake</div>
        <div class="popular-chip">🍜 Çorba</div>
        <div class="popular-chip">🥩 Köfte</div>
        <div class="popular-chip">🍣 Sushi</div>
        <div class="popular-chip">🧁 Cupcake</div>
        <div class="popular-chip">🌮 Taco</div>
        <div class="popular-chip">🥞 Krep</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- API KEY ---
api_key = os.getenv("GEMINI_API_KEY")

# --- SIDEBAR ---
try:
    st.logo("logo.jpg")
except Exception:
    pass

with st.sidebar:
    st.image("logo.jpg", use_container_width=True)
    st.markdown(txt["sidebar_title"])
    
    kisi_sayisi = st.slider(txt["people"], 1, 10, 4)
    
    yemek_turu = st.selectbox(txt["meal"], 
        txt["meal_opts"])
    
    mutfak = st.selectbox(txt["cuisine"], 
        txt["cuisine_opts"])
    
    zorluk = st.selectbox(txt["diff"], 
        txt["diff_opts"])

    diyet = st.selectbox(txt["diet"],
        txt["diet_opts"])
    
    kalori_goster = st.checkbox(txt["show_cal"], value=True)
    sure_goster = st.checkbox(txt["show_time"], value=True)

    st.markdown("---")
    st.markdown(txt["history"])
    if st.session_state.tarif_gecmisi:
        for item in reversed(st.session_state.tarif_gecmisi[-7:]):
            st.markdown(f'<div class="history-item">🍴 {item}</div>', unsafe_allow_html=True)
    else:
        st.markdown(txt["no_history"])
    
    st.markdown("---")
    st.markdown("## 🤖 AIŞef v1.0")
    st.markdown(txt["sidebar_footer"])

if api_key and api_key != "BURAYA_YAPISTIR":
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.6-flash')

    # Ek prompt
    ek_bilgiler = f"\n{txt["p_person"].format(kisi_sayisi)}"
    if yemek_turu != txt["meal_opts"][0]:
        ek_bilgiler += f"\n{txt['p_meal'].format(yemek_turu)}"
    if mutfak != txt["cuisine_opts"][0]:
        ek_bilgiler += f"\nMutfak tercihi: {mutfak}."
    if zorluk != txt["diff_opts"][0]:
        ek_bilgiler += f"\nZorluk seviyesi: {zorluk}."
    if diyet != "Fark Etmez":
        ek_bilgiler += f"\nDiyet tercihi: {diyet}. Buna uygun malzemeler kullan."
    if kalori_goster:
        ek_bilgiler += f"\n{txt['p_cal']}"
    if sure_goster:
        ek_bilgiler += f"\n{txt['p_time']}"

    # --- SEKMELER ---
    tab1, tab2, tab3, tab4 = st.tabs([txt["tab1"], txt["tab2"], txt["tab3"], txt["fav_title"]])

    # ===== TAB 1 =====
    with tab1:
        st.markdown(txt["tab1_title"])
        
        col_input, col_info = st.columns([3, 2])
        with col_input:
            malzemeler = st.text_area(txt["tab1_input"], 
                placeholder=txt["tab1_placeholder"], height=120)
            
            if st.button(txt["tab1_btn"], key="btn1"):
                # 🛡️ Tüm güvenlik kontrolleri tek seferde
                sec_ok, sec_msg = full_security_check(malzemeler)
                if not sec_ok:
                    st.error(sec_msg)
                else:
                    safe_input = sanitize_input(malzemeler)
                    with st.spinner(txt["thinking"]):
                        prompt = f"""
{txt["p_sys"]}
{txt["p_ingredients"]} {safe_input}.
{ek_bilgiler}

{txt["p_task1"]}

{txt["p_format1"].format(kisi_sayisi)}
"""
                        try:
                            response = model.generate_content(prompt)
                            safe_response = sanitize_ai_response(response.text)
                            st.session_state['recipe_t1'] = safe_response
                            st.session_state['cat_t1'] = yemek_turu if yemek_turu != txt["meal_opts"][0] else txt["cat_other"]
                            baslik = safe_input[:35] + ("..." if len(safe_input) > 35 else "")
                            st.session_state.tarif_gecmisi.append(f"Malzeme: {baslik}")
                        except Exception as e:
                            st.error(f"{txt['error']} {e}")
                            
            if st.session_state.get('recipe_t1'):
                display_recipe_and_actions('recipe_t1', st.session_state.get('cat_t1'))

        with col_info:
            st.markdown(f"""
            <div class="tips-section">
                <div class="tips-title">{txt["tips"]}</div>
                <div class="tip-item">
                    <span class="tip-icon">📝</span>
                    <span class="tip-text">{txt["tip1"]}</span>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">🌶️</span>
                    <span class="tip-text">{txt["tip2"]}</span>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">🧊</span>
                    <span class="tip-text">{txt["tip3"]}</span>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">⚙️</span>
                    <span class="tip-text">{txt["tip4"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ===== TAB 2 =====
    with tab2:
        st.markdown(txt["tab2_title"])

        col_input2, col_info2 = st.columns([3, 2])
        with col_input2:
            yemek_adi = st.text_input(txt["tab2_input"], placeholder=txt["tab2_placeholder"])
            
            if st.button(txt["tab2_btn"], key="btn2"):
                # 🛡️ Tüm güvenlik kontrolleri tek seferde
                sec_ok, sec_msg = full_security_check(yemek_adi)
                if not sec_ok:
                    st.error(sec_msg)
                else:
                    safe_input = sanitize_input(yemek_adi)
                    with st.spinner(f"🤖 AIŞef {safe_input} {txt['tab2_prep']}"):
                        prompt = f"""
{txt["p_sys2"]}
{txt["p_task2"].format(safe_input)}
{ek_bilgiler}

{txt["p_format2"].format(safe_input, kisi_sayisi)}
"""
                        try:
                            response = model.generate_content(prompt)
                            safe_response = sanitize_ai_response(response.text)
                            st.session_state['recipe_t2'] = safe_response
                            st.session_state['cat_t2'] = yemek_turu if yemek_turu != txt["meal_opts"][0] else txt["cat_other"]
                            st.session_state.tarif_gecmisi.append(f"📖 {safe_input[:20]}...")
                        except Exception as e:
                            st.error(f"{txt['error']} {e}")
                            
            if st.session_state.get('recipe_t2'):
                display_recipe_and_actions('recipe_t2', st.session_state.get('cat_t2'))

        with col_info2:
            st.markdown(f"""
            <div class="tips-section">
                <div class="tips-title">{txt["recommended"]}</div>
                <div class="tip-item">
                    <span class="tip-icon">🇹🇷</span>
                    <span class="tip-text"><strong>Mantı</strong> — {txt["rec_1"]}</span>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">🇮🇹</span>
                    <span class="tip-text"><strong>Risotto</strong> — {txt["rec_2"]}</span>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">🇯🇵</span>
                    <span class="tip-text"><strong>Ramen</strong> — {txt["rec_3"]}</span>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">🇲🇽</span>
                    <span class="tip-text"><strong>Burrito</strong> — {txt["rec_4"]}</span>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">🇰🇷</span>
                    <span class="tip-text"><strong>Bibimbap</strong> — {txt["rec_5"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ===== TAB 3 =====
    with tab3:
        st.markdown(txt["tab3_title"])
        
        col_sur1, col_sur2 = st.columns([3, 2])
        with col_sur1:
            # Öğün filtresi
            st.markdown(txt["tab3_q1"])
            surp_col1, surp_col2 = st.columns(2)
            with surp_col1:
                surpriz_ogun = st.selectbox(txt["tab3_meal"], 
                    txt["tab3_meal_opts"],
                    key="surpriz_ogun")
            with surp_col2:
                surpriz_mutfak = st.selectbox(txt["tab3_cuisine"],
                    txt["tab3_cuisine_opts"],
                    key="surpriz_mutfak")

            st.markdown(f"""
            <div class="feature-card" style="padding: 25px; margin-bottom: 20px; text-align: center;">
                <div style="font-size: 3.5rem; margin-bottom: 10px;">🎰</div>
                <div class="popular-title" style="margin-bottom: 5px;">{txt["lottery_title"]}</div>
                <div class="f-desc" style="font-size: 0.85rem;">
                    {txt["lottery_desc"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(txt["tab3_btn"], key="btn3"):
                # 🛡️ Tüm güvenlik kontrolleri
                sec_ok, sec_msg = full_security_check()
                if not sec_ok:
                    st.error(sec_msg)
                else:
                    with st.spinner(txt["tab3_thinking"]):
                        # Sürpriz öğün ve mutfak bilgisi
                        surpriz_ek = ""
                        if surpriz_ogun != txt["tab3_meal_opts"][0]:
                            ogun_adi = surpriz_ogun.split(" ", 1)[1]  # Emojiyi kaldır
                            surpriz_ek += f"\n{txt['p_meal'].format(ogun_adi)}"
                        if surpriz_mutfak != txt["tab3_cuisine_opts"][0]:
                            mutfak_adi = surpriz_mutfak.split(" ", 1)[1]
                            surpriz_ek += f"\n{txt['p_cuisine'].format(mutfak_adi)}"

                        prompt = f"""
{txt["p_sys3"]}
Kullanıcıya rastgele, beklemediği, ilginç ve lezzetli bir yemek tarifi öner.
Sıradan bir yemek olmasın, farklı ve heyecan verici bir şey olsun.
{txt["p_person"].format(kisi_sayisi)}
{surpriz_ek}
{txt["p_diet"].format(diyet) if diyet != txt["diet_opts"][0] else ""}
{txt["p_cal"] if kalori_goster else ""}
{txt["p_time"] if sure_goster else ""}

{txt["p_format3"].format(kisi_sayisi)}
"""
                        try:
                            response = model.generate_content(prompt)
                            safe_response = sanitize_ai_response(response.text)
                            st.session_state['recipe_t3'] = safe_response
                            ogun_label = surpriz_ogun.split(" ", 1)[1] if surpriz_ogun != txt["tab3_meal_opts"][0] else "Rastgele"
                            st.session_state['cat_t3'] = ogun_label if ogun_label in ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Tatlı", "İçecek"] else txt["cat_other"]
                            st.session_state.tarif_gecmisi.append(f"🎲 Sürpriz: {ogun_label}")
                        except Exception as e:
                            st.error(f"{txt['error']} {e}")
                            
            if st.session_state.get('recipe_t3'):
                display_recipe_and_actions('recipe_t3', st.session_state.get('cat_t3'))

        with col_sur2:
            st.markdown(f"""
            <div class="tips-section">
                <div class="tips-title">{txt["stats_title"]}</div>
                <div class="tip-item">
                    <span class="tip-icon">📋</span>
                    <span class="tip-text">{txt["stats_1"].format(len(st.session_state.tarif_gecmisi))}</span>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">🤖</span>
                    <span class="tip-text">{txt["stats_2"]}</span>
                </div>
                <div class="tip-item">
                    <span class="tip-icon">🌍</span>
                    <span class="tip-text">{txt["stats_3"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


    # ===== TAB 4 (FAVORİLER) =====
    with tab4:
        st.markdown(f"#### {txt['fav_title']}")
        
        all_db_favs = database.get_favorites()
        if not all_db_favs:
            st.info(txt["fav_empty"])
        else:
            # Kategoriler
            cat_list = [
                txt["cat_all"], txt["cat_breakfast"], txt["cat_lunch"], 
                txt["cat_dinner"], txt["cat_dessert"], txt["cat_drink"], txt["cat_other"]
            ]
            
            selected_cat = st.radio("Kategori Seç / Select Category:", cat_list, horizontal=True)
            
            # Filter
            if selected_cat == txt["cat_all"]:
                recipes_to_show = all_db_favs
            else:
                recipes_to_show = [r for r in all_db_favs if r.get('category') == selected_cat]
            
            if not recipes_to_show:
                st.markdown(f"*{txt['fav_empty']}*")
            else:
                # Her tarifi Custom HTML Accordion ile göster
                for fav in recipes_to_show:

                    recipe_id = fav['id']
                    
                    # Başlığı çıkar
                    title_match = re.search(r'###\s*(.*?)\n', fav["text"])
                    display_title = title_match.group(1).strip() if title_match else "Yemek Tarifi"
                    display_title = display_title.replace('*', '')

                    # Her tarif için bir container
                    st.markdown(f"""
<details class="fav-accordion">
  <summary class="fav-header">
    <span class="fav-icon">🍽️</span>
    <span class="fav-name">{display_title}</span>
    <span class="fav-arrow"></span>
  </summary>
  <div class="fav-body">
    <div class="recipe-card">{fav["text"]}</div>
  </div>
</details>
""", unsafe_allow_html=True)

                    # Butonlar - her tarif için Streamlit widget'ları
                    col0, col1, col2, col3 = st.columns([1.5, 1, 1, 2])
                    with col0:
                        edit_cat_opts = [txt["cat_breakfast"], txt["cat_lunch"], txt["cat_dinner"], txt["cat_dessert"], txt["cat_drink"], txt["cat_other"]]
                        current_idx = edit_cat_opts.index(fav["category"]) if fav["category"] in edit_cat_opts else 5
                        new_cat = st.selectbox("Kategori Değiştir", edit_cat_opts, index=current_idx, key=f"edit_cat_{recipe_id}", label_visibility="collapsed")
                        if new_cat != fav["category"]:
                            database.update_category(recipe_id, new_cat)
                            st.rerun()
                            
                    with col1:
                        if st.button(txt["remove_fav"], key=f"del_{recipe_id}"):
                            database.remove_favorite(recipe_id)
                            st.rerun()
                    with col2:
                        try:
                            pdf_bytes = create_recipe_pdf(fav["text"])
                            st.download_button(
                                label=txt["download"],
                                data=pdf_bytes,
                                file_name=f"tarif_{recipe_id[:5]}.pdf",
                                mime="application/pdf",
                                key=f"dl_{recipe_id}"
                            )
                        except Exception as e:
                            st.download_button(
                                label=txt["download"] + " (MD)",
                                data=fav["text"],
                                file_name=f"tarif_{recipe_id[:5]}.md",
                                mime="text/markdown",
                                key=f"dl_fb_{recipe_id}"
                            )
                            print(f"PDF Error: {e}")
                    with col3:
                        html_code = f"""
                        <div style="display: flex; gap: 5px;">
                            <button id="btn_{recipe_id}" style="background-color: #ff4b4b; color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-weight: bold; flex: 1;">
                                {txt['read_aloud']}
                            </button>
                            <button id="stop_{recipe_id}" style="background-color: #555; color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-weight: bold;">
                                {txt['stop_read']}
                            </button>
                        </div>
                        <script>
                            document.getElementById("btn_{recipe_id}").addEventListener("click", function() {{
                                var text = `{clean_for_tts(fav["text"])}`;
                                var msg = new SpeechSynthesisUtterance();
                                msg.text = text;
                                msg.lang = "{ 'tr-TR' if st.session_state.dil_secimi == 'TR' else 'en-US' }";
                                window.speechSynthesis.cancel();
                                window.speechSynthesis.speak(msg);
                            }});
                            document.getElementById("stop_{recipe_id}").addEventListener("click", function() {{
                                window.speechSynthesis.cancel();
                            }});
                        </script>
                        """
                        components.html(html_code, height=50)
                    
                    st.markdown("<hr style='margin: 5px 0; opacity: 0.15;'>", unsafe_allow_html=True)


    # --- FOOTER ---
    st.markdown(f"""
    <div class="footer">
        <p><span>AIŞef</span> v1.0 • {txt["footer_1"]}</p>
        <p>{txt["footer_2"]}</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error(txt["error_api"])

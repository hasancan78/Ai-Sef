def get_theme_css(theme_name: str) -> str:
    # ===== ORTAK CSS (Tüm temalarda aynı olan layout ve animasyonlar) =====
    common_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700;900&display=swap');

        .block-container { padding-top: 2.5rem; max-width: 95% !important; }
        [data-testid="stToolbar"] { visibility: hidden; }
        [data-testid="stHeader"] { background-color: transparent !important; }
        [data-testid="collapsedControl"] { display: flex !important; z-index: 999999 !important; color: #ff4b4b !important; background: rgba(0,0,0,0.2) !important; border-radius: 5px !important; }
        [data-testid="collapsedControl"] svg { fill: currentColor !important; color: currentColor !important; }

        .hero-section {
            border-radius: 25px;
            padding: 40px 50px;
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
        }
        .hero-section::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 500px;
            height: 500px;
            border-radius: 50%;
        }
        .hero-section::after {
            content: '🤖🍳';
            position: absolute;
            top: 20px;
            right: 40px;
            font-size: 4rem;
            opacity: 0.3;
        }
        .hero-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.2rem;
            font-weight: 900;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
            letter-spacing: 2px;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            margin-bottom: 0;
        }
        .hero-badge {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-top: 10px;
            letter-spacing: 1px;
        }

        .features-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }
        .feature-card {
            border-radius: 18px;
            padding: 22px 18px;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .feature-card .f-icon { font-size: 2.2rem; margin-bottom: 8px; }
        .feature-card .f-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; }
        .feature-card .f-desc { font-size: 0.75rem; line-height: 1.4; }

        .popular-section {
            border-radius: 20px;
            padding: 25px 30px;
            margin-bottom: 25px;
        }
        .popular-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }
        .popular-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .popular-chip {
            padding: 8px 18px;
            border-radius: 25px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .popular-chip:hover {
            transform: scale(1.05);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 5px;
            justify-content: center;
            border-radius: 15px;
            padding: 5px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: 600;
            border: none;
        }

        .stButton>button {
            border-radius: 30px;
            border: none;
            padding: 12px 30px;
            font-weight: 700;
            font-size: 1.05rem;
            transition: all 0.3s ease;
            width: 100%;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .stButton>button:hover {
            transform: translateY(-3px);
        }

        .recipe-card {
            padding: 35px 40px;
            border-radius: 20px;
            margin-top: 25px;
            line-height: 1.9;
            animation: slideUp 0.5s ease-out;
        }
        .recipe-card h2, .recipe-card h3 {
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        .recipe-card ul { padding-left: 20px; }
        .recipe-card li { margin-bottom: 5px; }
        .recipe-card code { padding: 2px 8px; border-radius: 5px; }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
            font-family: 'Orbitron', sans-serif !important;
            font-size: 1rem !important;
            letter-spacing: 1px;
        }

        .history-item {
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 8px;
            font-size: 0.82rem;
        }

        .tips-section {
            border-radius: 20px;
            padding: 25px 30px;
            margin-top: 25px;
        }
        .tips-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1rem;
            margin-bottom: 12px;
            letter-spacing: 1px;
        }
        .tip-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 10px;
            padding: 10px 15px;
            border-radius: 12px;
        }
        .tip-icon { font-size: 1.3rem; }
        .tip-text { font-size: 0.85rem; line-height: 1.5; }

        .stTextArea textarea, .stTextInput input {
            border-radius: 14px !important;
            transition: border 0.3s;
        }

        .footer {
            text-align: center;
            padding: 35px 0 15px 0;
            font-size: 0.8rem;
            margin-top: 40px;
        }
        .footer span { font-weight: 600; }

        @media (max-width: 992px) {
            .block-container {
                max-width: 100% !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            .features-row { grid-template-columns: repeat(2, 1fr); }
            .hero-section { padding: 30px 20px; }
            .hero-title { font-size: 2.2rem; }
            .hero-section::after { font-size: 2.5rem; right: 10px; }
        }
        
        @media (max-width: 576px) {
            .features-row { grid-template-columns: 1fr; }
            .hero-title { font-size: 1.8rem; }
            .hero-subtitle { font-size: 0.9rem; }
            .popular-chip { padding: 6px 12px; font-size: 0.75rem; }
        }

        /* ===== FAVORİLER ACCORDION ===== */
        .fav-accordion {
            margin-bottom: 8px;
            border-radius: 12px;
            overflow: hidden;
            background: transparent;
        }
        .fav-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 14px 20px;
            cursor: pointer;
            user-select: none;
            border-radius: 12px;
            transition: filter 0.2s;
            list-style: none; /* Hide default summary arrow */
        }
        .fav-header::-webkit-details-marker {
            display: none; /* Hide default summary arrow in WebKit */
        }
        .fav-header:hover { filter: brightness(1.2); }

        .fav-icon { font-size: 1.3rem; }
        .fav-name {
            flex: 1;
            font-weight: 700;
            font-size: 1.1rem;
        }
        .fav-arrow {
            font-size: 0.8rem;
            opacity: 0.7;
        }
        details .fav-arrow::after { content: '▼'; }
        details[open] .fav-arrow::after { content: '▲'; }
        .fav-body {
            padding: 0 10px 10px 10px;
        }
    """

    # ===== 1. KIZIL TUTKU (Şu Anki Yeni Kırmızı Tema) =====
    if theme_name == "🔥 Kızıl Tutku":
        theme_css = """
        /* KIZIL TUTKU */
        .stApp { background: #0d0003; font-family: 'Poppins', sans-serif; color: #e0e0e0; }
        
        .hero-section {
            background: linear-gradient(135deg, #2d0008 0%, #4a000f 40%, #8b0000 70%, #e50914 100%);
            box-shadow: 0 20px 60px rgba(229, 9, 20, 0.15);
        }
        .hero-section::before { background: radial-gradient(circle, rgba(229,9,20,0.15) 0%, transparent 70%); }
        .hero-title { background-image: linear-gradient(90deg, #ff003c, #feca57, #ff9ff3, #54a0ff); }
        .hero-subtitle { color: #aaa; }
        .hero-badge { background: linear-gradient(135deg, #e50914, #ff003c); color: white; }

        .feature-card { background: linear-gradient(145deg, #2b0005, #45000a); border: 1px solid rgba(229, 9, 20, 0.2); }
        .feature-card:hover { border-color: rgba(229, 9, 20, 0.6); box-shadow: 0 10px 30px rgba(229, 9, 20, 0.15); }
        .feature-card .f-title { color: #fff; }
        .feature-card .f-desc { color: #888; }

        .popular-section { background: linear-gradient(145deg, #2b0005, #45000a); border: 1px solid rgba(255,255,255,0.05); }
        .popular-title { color: #feca57; }
        .popular-chip { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #ccc; }
        .popular-chip:hover { background: linear-gradient(135deg, #e50914, #ff003c); color: white; border-color: transparent; }

        .stTabs [data-baseweb="tab-list"] { background: rgba(43, 0, 5, 0.8); border: 1px solid rgba(229, 9, 20, 0.15); }
        .stTabs [data-baseweb="tab"] { color: #aaa; }
        .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #e50914, #ff003c) !important; color: white !important; }

        .stButton>button { background: linear-gradient(135deg, #e50914, #ff003c); color: white; }
        .stButton>button:hover { background: linear-gradient(135deg, #ff003c, #feca57); box-shadow: 0px 8px 30px rgba(229, 9, 20, 0.5); color: white; }

        .recipe-card { background: linear-gradient(145deg, #2b0005, #45000a); border: 1px solid rgba(229, 9, 20, 0.2); box-shadow: 0px 15px 40px rgba(0,0,0,0.3); color: #e0e0e0; }
        .recipe-card h2, .recipe-card h3 { background-image: linear-gradient(90deg, #ff003c, #feca57); }
        .recipe-card strong { color: #ff9ff3; }
        .recipe-card li { color: #ccc; }
        .recipe-card code { background: rgba(229,9,20,0.15); color: #ff003c; }

        .fav-header { background: linear-gradient(135deg, #2b0005, #45000a); border-left: 4px solid #e50914; }
        .fav-name { color: #ffd6d9; }

        [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a0003 0%, #2b0005 50%, #45000a 100%); border-right: 1px solid rgba(229, 9, 20, 0.15); }
        [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 { color: #feca57 !important; }

        .history-item { background: rgba(229, 9, 20, 0.1); border-left: 3px solid #e50914; color: #ccc; }

        .tips-section { background: linear-gradient(145deg, #2b0005, #45000a); border: 1px solid rgba(254, 202, 87, 0.2); }
        .tips-title { color: #feca57; }
        .tip-item { background: rgba(255,255,255,0.03); }
        .tip-text { color: #aaa; }

        .stTextArea textarea, .stTextInput input, div[data-baseweb="select"] > div { background: #300008 !important; border: 2px solid rgba(229, 9, 20, 0.2) !important; color: #e0e0e0 !important; }
        .stTextArea textarea:focus, .stTextInput input:focus, div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within { border-color: #e50914 !important; box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.15) !important; }
        .stTextArea textarea::placeholder, .stTextInput input::placeholder { color: #555 !important; }
        div[data-baseweb="popover"] > div, ul[role="listbox"] { background: #300008 !important; }
        ul[role="listbox"] li { color: #e0e0e0 !important; }

        .footer { color: #555; border-top: 1px solid rgba(255,255,255,0.05); }
        .footer span { color: #e50914; }

        .stMarkdown h4 { color: #e0e0e0 !important; }
        .stMarkdown p { color: #bbb; }
        label { color: #ccc !important; }
        """

    # ===== 2. GECE MAVİSİ (Önceki Lacivert Tema) =====
    elif theme_name == "🌌 Gece Mavisi":
        theme_css = """
        /* GECE MAVİSİ */
        .stApp { background: #0a0a0a; font-family: 'Poppins', sans-serif; color: #e0e0e0; }
        
        .hero-section {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 70%, #e94560 100%);
            box-shadow: 0 20px 60px rgba(233, 69, 96, 0.15);
        }
        .hero-section::before { background: radial-gradient(circle, rgba(233,69,96,0.15) 0%, transparent 70%); }
        .hero-title { background-image: linear-gradient(90deg, #ff6b6b, #feca57, #ff9ff3, #54a0ff); }
        .hero-subtitle { color: #aaa; }
        .hero-badge { background: linear-gradient(135deg, #e94560, #ff6b6b); color: white; }

        .feature-card { background: linear-gradient(145deg, #1a1a2e, #16213e); border: 1px solid rgba(233, 69, 96, 0.2); }
        .feature-card:hover { border-color: rgba(233, 69, 96, 0.6); box-shadow: 0 10px 30px rgba(233, 69, 96, 0.15); }
        .feature-card .f-title { color: #fff; }
        .feature-card .f-desc { color: #888; }

        .popular-section { background: linear-gradient(145deg, #1a1a2e, #16213e); border: 1px solid rgba(255,255,255,0.05); }
        .popular-title { color: #feca57; }
        .popular-chip { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #ccc; }
        .popular-chip:hover { background: linear-gradient(135deg, #e94560, #ff6b6b); color: white; border-color: transparent; }

        .stTabs [data-baseweb="tab-list"] { background: rgba(26, 26, 46, 0.8); border: 1px solid rgba(233, 69, 96, 0.15); }
        .stTabs [data-baseweb="tab"] { color: #aaa; }
        .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #e94560, #ff6b6b) !important; color: white !important; }

        .stButton>button { background: linear-gradient(135deg, #e94560, #ff6b6b); color: white; }
        .stButton>button:hover { background: linear-gradient(135deg, #ff6b6b, #feca57); box-shadow: 0px 8px 30px rgba(233, 69, 96, 0.5); color: white; }

        .recipe-card { background: linear-gradient(145deg, #1a1a2e, #16213e); border: 1px solid rgba(233, 69, 96, 0.2); box-shadow: 0px 15px 40px rgba(0,0,0,0.3); color: #e0e0e0; }
        .recipe-card h2, .recipe-card h3 { background-image: linear-gradient(90deg, #ff6b6b, #feca57); }
        .recipe-card strong { color: #ff9ff3; }
        .recipe-card li { color: #ccc; }
        .recipe-card code { background: rgba(233,69,96,0.15); color: #ff6b6b; }

        .fav-header { background: linear-gradient(135deg, #1a1a2e, #16213e); border-left: 4px solid #e94560; }
        .fav-name { color: #e0e0e0; }


        [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 { color: #feca57 !important; }

        .history-item { background: rgba(233, 69, 96, 0.1); border-left: 3px solid #e94560; color: #ccc; }

        .tips-section { background: linear-gradient(145deg, #1a1a2e, #16213e); border: 1px solid rgba(254, 202, 87, 0.2); }
        .tips-title { color: #feca57; }
        .tip-item { background: rgba(255,255,255,0.03); }
        .tip-text { color: #aaa; }

        .stTextArea textarea, .stTextInput input, div[data-baseweb="select"] > div { background: #16213e !important; border: 2px solid rgba(233, 69, 96, 0.2) !important; color: #e0e0e0 !important; }
        .stTextArea textarea:focus, .stTextInput input:focus, div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within { border-color: #e94560 !important; box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.15) !important; }
        .stTextArea textarea::placeholder, .stTextInput input::placeholder { color: #555 !important; }
        div[data-baseweb="popover"] > div, ul[role="listbox"] { background: #16213e !important; }
        ul[role="listbox"] li { color: #e0e0e0 !important; }

        .footer { color: #555; border-top: 1px solid rgba(255,255,255,0.05); }
        .footer span { color: #e94560; }

        .stMarkdown h4 { color: #e0e0e0 !important; }
        .stMarkdown p { color: #bbb; }
        label { color: #ccc !important; }
        """

    # ===== 3. AYDINLIK (Yumuşak Beyaz Tema) =====
    elif theme_name == "☀️ Aydınlık":
        theme_css = """
        /* AYDINLIK */
        .stApp { background: #f8f9fa; font-family: 'Poppins', sans-serif; color: #333333; }
        
        .hero-section {
            background: linear-gradient(135deg, #ffffff 0%, #f1f3f5 40%, #e9ecef 70%, #ffe3e3 100%);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
            border: 1px solid #e9ecef;
        }
        .hero-section::before { background: radial-gradient(circle, rgba(233,69,96,0.05) 0%, transparent 70%); }
        .hero-title { background-image: linear-gradient(90deg, #e94560, #f39c12, #8e44ad, #2980b9); }
        .hero-subtitle { color: #555; }
        .hero-badge { background: linear-gradient(135deg, #e94560, #ff6b6b); color: white; }

        .feature-card { background: #ffffff; border: 1px solid #e9ecef; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }
        .feature-card:hover { border-color: #e94560; box-shadow: 0 10px 30px rgba(233, 69, 96, 0.1); }
        .feature-card .f-title { color: #222; }
        .feature-card .f-desc { color: #666; }

        .popular-section { background: #ffffff; border: 1px solid #e9ecef; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }
        .popular-title { color: #e94560; }
        .popular-chip { background: #f1f3f5; border: 1px solid #dee2e6; color: #444; }
        .popular-chip:hover { background: linear-gradient(135deg, #e94560, #ff6b6b); color: white; border-color: transparent; }

        .stTabs [data-baseweb="tab-list"] { background: #ffffff; border: 1px solid #e9ecef; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
        .stTabs [data-baseweb="tab"] { color: #666; }
        .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #e94560, #ff6b6b) !important; color: white !important; }

        .stButton>button { background: linear-gradient(135deg, #e94560, #ff6b6b); color: white; box-shadow: 0 4px 15px rgba(233, 69, 96, 0.2); }
        .stButton>button:hover { background: linear-gradient(135deg, #ff6b6b, #feca57); box-shadow: 0px 8px 30px rgba(233, 69, 96, 0.4); color: white; }

        .recipe-card { background: #ffffff; border: 1px solid #e9ecef; box-shadow: 0px 10px 30px rgba(0,0,0,0.05); color: #333; }
        .recipe-card h2, .recipe-card h3 { background-image: linear-gradient(90deg, #e94560, #f39c12); }
                                        
                                                                                        .recipe-card strong { color: #8e44ad; }
        .recipe-card li { color: #444; }
        .recipe-card code { background: #ffe3e3; color: #e94560; }

        .fav-header { background: #f0f2f5; border-left: 4px solid #e94560; }
        .fav-name { color: #222; }


        details[data-testid="stExpander"], div[data-testid="stExpander"] { background: transparent !important; border: none !important; box-shadow: none !important; margin-bottom: 4px !important; }
        details[data-testid="stExpander"] summary, div[data-testid="stExpander"] summary { background: linear-gradient(90deg, #2b0005, #150002) !important; border-left: 3px solid #e94560 !important; padding: 12px 15px !important; border-radius: 4px !important; }
        details[data-testid="stExpander"] summary:hover, div[data-testid="stExpander"] summary:hover { background: linear-gradient(90deg, #3a0007, #1a0003) !important; }
        details[data-testid="stExpander"] summary p, div[data-testid="stExpander"] summary p { color: #ffffff !important; font-weight: 700 !important; font-size: 1.1rem !important; margin: 0 !important; }
        details[data-testid="stExpander"] summary svg, div[data-testid="stExpander"] summary svg { fill: #ffffff !important; stroke: #ffffff !important; }
        details[data-testid="stExpander"] [data-testid="stExpanderDetails"], div[data-testid="stExpander"] [data-testid="stExpanderDetails"] { background: transparent !important; padding: 15px 5px !important; border: none !important; }


        

                        

        [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e9ecef; }
        [data-testid="stSidebar"] * { color: #333 !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 { color: #e94560 !important; }

        .history-item { background: #f8f9fa; border-left: 3px solid #e94560; color: #555; }

        .tips-section { background: #ffffff; border: 1px solid #e9ecef; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }
        .tips-title { color: #f39c12; }
        .tip-item { background: #f8f9fa; border: 1px solid #f1f3f5; }
        .tip-text { color: #555; }

        .stTextArea textarea, .stTextInput input, div[data-baseweb="select"] > div { background: #ffffff !important; border: 2px solid #dee2e6 !important; color: #333 !important; }
        .stTextArea textarea:focus, .stTextInput input:focus, div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within { border-color: #e94560 !important; box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.1) !important; }
        .stTextArea textarea::placeholder, .stTextInput input::placeholder { color: #adb5bd !important; }
        div[data-baseweb="popover"] > div, ul[role="listbox"] { background: #ffffff !important; }
        ul[role="listbox"] li { color: #333 !important; }

        .footer span { color: #e94560; }
        .stMarkdown h4 { color: #333 !important; }
        .stMarkdown p { color: #555; }
        label { color: #444 !important; }
        """

    # ===== 4. NEON FUŞYA (Parlak Koyu Pembe Tema) =====
    elif theme_name == "💖 Neon Fuşya":
        theme_css = """
        /* NEON FUŞYA */
        .stApp { background: #0d0008; font-family: 'Poppins', sans-serif; color: #e0e0e0; }
        
        .hero-section {
            background: linear-gradient(135deg, #1f0014 0%, #3d002e 40%, #8a005e 70%, #ff007f 100%);
            box-shadow: 0 20px 60px rgba(255, 0, 127, 0.15);
        }
        .hero-section::before { background: radial-gradient(circle, rgba(255,0,127,0.15) 0%, transparent 70%); }
        .hero-title { background-image: linear-gradient(90deg, #ff007f, #ff00ff, #00f0ff); }
        .hero-subtitle { color: #ccc; }
        .hero-badge { background: linear-gradient(135deg, #ff007f, #d400ff); color: white; }

        .feature-card { background: linear-gradient(145deg, #1f0014, #3d002e); border: 1px solid rgba(255, 0, 127, 0.2); }
        .feature-card:hover { border-color: rgba(255, 0, 127, 0.6); box-shadow: 0 10px 30px rgba(255, 0, 127, 0.2); }
        .feature-card .f-title { color: #fff; }
        .feature-card .f-desc { color: #bbb; }

        .popular-section { background: linear-gradient(145deg, #1f0014, #3d002e); border: 1px solid rgba(255,255,255,0.05); }
        .popular-title { color: #ff00ff; }
        .popular-chip { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #ccc; }
        .popular-chip:hover { background: linear-gradient(135deg, #ff007f, #ff00ff); color: white; border-color: transparent; }

        .stTabs [data-baseweb="tab-list"] { background: rgba(31, 0, 20, 0.8); border: 1px solid rgba(255, 0, 127, 0.15); }
        .stTabs [data-baseweb="tab"] { color: #aaa; }
        .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #ff007f, #ff00ff) !important; color: white !important; }

        .stButton>button { background: linear-gradient(135deg, #ff007f, #d400ff); color: white; }
        .stButton>button:hover { background: linear-gradient(135deg, #ff00ff, #00f0ff); box-shadow: 0px 8px 30px rgba(255, 0, 127, 0.5); color: white; }

        .recipe-card { background: linear-gradient(145deg, #1f0014, #3d002e); border: 1px solid rgba(255, 0, 127, 0.2); box-shadow: 0px 15px 40px rgba(0,0,0,0.3); color: #e0e0e0; }
        .recipe-card h2, .recipe-card h3 { background-image: linear-gradient(90deg, #ff007f, #00f0ff); }
                                                .recipe-card strong { color: #ff00ff; }
        .recipe-card li { color: #ccc; }
        .recipe-card code { background: rgba(255,0,127,0.15); color: #ff007f; }

        .fav-header { background: linear-gradient(135deg, #1f0014, #3d002e); border-left: 4px solid #ff007f; }
        .fav-name { color: #ffb3e6; }


        details[data-testid="stExpander"], div[data-testid="stExpander"] { background: transparent !important; border: none !important; box-shadow: none !important; margin-bottom: 4px !important; }
        details[data-testid="stExpander"] summary, div[data-testid="stExpander"] summary { background: linear-gradient(90deg, #3d002e, #1f0014) !important; border-left: 3px solid #ff007f !important; padding: 12px 15px !important; border-radius: 4px !important; }
        details[data-testid="stExpander"] summary:hover, div[data-testid="stExpander"] summary:hover { background: linear-gradient(90deg, #5c0047, #1f0014) !important; }
        details[data-testid="stExpander"] summary p, div[data-testid="stExpander"] summary p { color: #ffffff !important; font-weight: 700 !important; font-size: 1.1rem !important; margin: 0 !important; }
        details[data-testid="stExpander"] summary svg, div[data-testid="stExpander"] summary svg { fill: #ffffff !important; stroke: #ffffff !important; }
        details[data-testid="stExpander"] [data-testid="stExpanderDetails"], div[data-testid="stExpander"] [data-testid="stExpanderDetails"] { background: transparent !important; padding: 15px 5px !important; border: none !important; }


        

                        

        [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d0008 0%, #1f0014 50%, #3d002e 100%); border-right: 1px solid rgba(255, 0, 127, 0.15); }
        [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 { color: #ff00ff !important; }

        .history-item { background: rgba(255, 0, 127, 0.1); border-left: 3px solid #ff007f; color: #ccc; }

        .tips-section { background: linear-gradient(145deg, #1f0014, #3d002e); border: 1px solid rgba(255, 0, 127, 0.2); }
        .tips-title { color: #ff00ff; }
        .tip-item { background: rgba(255,255,255,0.03); }
        .tip-text { color: #aaa; }

        .stTextArea textarea, .stTextInput input, div[data-baseweb="select"] > div { background: #24001b !important; border: 2px solid rgba(255, 0, 127, 0.2) !important; color: #e0e0e0 !important; }
        .stTextArea textarea:focus, .stTextInput input:focus, div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within { border-color: #ff007f !important; box-shadow: 0 0 0 3px rgba(255, 0, 127, 0.2) !important; }
        .stTextArea textarea::placeholder, .stTextInput input::placeholder { color: #666 !important; }
        div[data-baseweb="popover"] > div, ul[role="listbox"] { background: #24001b !important; }
        ul[role="listbox"] li { color: #e0e0e0 !important; }

        .footer { color: #666; border-top: 1px solid rgba(255,255,255,0.05); }
        .footer span { color: #ff007f; }

        .stMarkdown h4 { color: #e0e0e0 !important; }
        .stMarkdown p { color: #bbb; }
        label { color: #ccc !important; }
        """

    return common_css + theme_css + "</style>"

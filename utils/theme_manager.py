"""
SiberKalkan Akademi - Tema Yöneticisi
======================================

10 profesyonel karanlık tema içeren modül.
Mevcut görünüm birebir korunmuştur.

Temalar:
    1. Matrix Yeşil (varsayılan)
    2. Orman Yeşili
    3. Nane Yeşili
    4. Askeri Yeşil
    5. Zümrüt Yeşili
    6. Okyanus (Mavi)
    7. Mor
    8. Alev (Turuncu)
    9. Gece Yarısı (Gri)
    10. Kömür Yeşili

Kullanım:
    from utils.theme_manager import ThemeManager
    
    # Tema seçim arayüzü
    ThemeManager.render_theme_selector()
    
    # CSS uygula
    ThemeManager.apply_theme(current_theme)
"""

import streamlit as st
from typing import Dict, List


class ThemeManager:
    """
    Tema yönetim sınıfı.
    
    Bu sınıf, 10 farklı profesyonel karanlık tema sunar.
    Her tema; arka plan, metin, buton, terminal, sidebar ve grafik
    renklerini kapsar.
    """
    
    # ============================================
    # TEMA LİSTESİ
    # ============================================
    
    THEMES: List[str] = [
        "Matrix Yeşil",
        "Orman Yeşili",
        "Nane Yeşili",
        "Askeri Yeşil",
        "Zümrüt Yeşili",
        "Okyanus",
        "Mor",
        "Alev",
        "Gece Yarısı",
        "Kömür Yeşili",
    ]
    
    DEFAULT_THEME: str = "Matrix Yeşil"
    
    # ============================================
    # TEMA CSS TANIMLARI
    # ============================================
    
    THEME_CSS: Dict[str, str] = {
        # ========================================
        # 1. MATRIX YEŞİL (Orijinal)
        # ========================================
        "Matrix Yeşil": """
            .stApp {background: linear-gradient(135deg, #0a0e17 0%, #0d1117 50%, #0a0e17 100%);}
            h1, h2 {color: #00ff41 !important; text-shadow: 0 0 15px rgba(0,255,65,0.4);}
            h3 {color: #00cc33 !important;}
            .terminal {color: #00ff41; border-color: #00ff41; box-shadow: 0 0 25px rgba(0,255,65,0.12); background: linear-gradient(180deg, #080c14, #0d1018);}
            .scenario-desc {border-left: 5px solid #00ff41; box-shadow: 0 6px 20px rgba(0,255,65,0.08); background: linear-gradient(135deg, #111827, #1a2332);}
            .stButton>button {background: linear-gradient(135deg, #1e3a5f, #2d5a8e); border-color: #3d7ab5; color: #fff;}
            .stButton>button:hover {border-color: #5a9ed4; box-shadow: 0 6px 20px rgba(61,122,181,0.6);}
            .highlight {color: #ffaa00 !important;}
            .success {color: #00ff41 !important;}
            .danger {color: #ff4444 !important;}
            .streamlit-expanderHeader {color: #00ff41 !important; background: linear-gradient(135deg, #111827, #1a2332); border-color: #2d4a6e;}
            .stMetric {background: linear-gradient(135deg, #111827, #1a2332); border: 1px solid #2d4a6e;}
            .stMetric [data-testid="stMetricValue"] {color: #00ff41 !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #00ff41, #5a9ed4);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #1a2332; border: 1px solid #2d4a6e; color: #00ff41;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #111827 0%, #0f172a 100%); border-right: 1px solid #1e3a5f;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(15,23,42,0.85); border: 1px solid rgba(30,58,95,0.4);}
            .panel-box {background: linear-gradient(180deg, #111827 0%, #1a2332 100%); border: 1px solid #1e3a5f;}
            .panel-title {color: #00ff41 !important;}
        """,
        
        # ========================================
        # 2. ORMAN YEŞİLİ
        # ========================================
        "Orman Yeşili": """
            .stApp {background: linear-gradient(135deg, #0a1a0f 0%, #0d1f13 50%, #0a1a0f 100%);}
            h1, h2 {color: #4caf50 !important; text-shadow: 0 0 15px rgba(76,175,80,0.4);}
            h3 {color: #388e3c !important;}
            .terminal {color: #4caf50; border-color: #4caf50; box-shadow: 0 0 25px rgba(76,175,80,0.12); background: linear-gradient(180deg, #0a1a0f, #0d1f13);}
            .scenario-desc {border-left: 5px solid #4caf50; box-shadow: 0 6px 20px rgba(76,175,80,0.08); background: linear-gradient(135deg, #132a18, #1a3320);}
            .stButton>button {background: linear-gradient(135deg, #1b5e20, #2e7d32); border-color: #4caf50; color: #fff;}
            .stButton>button:hover {border-color: #66bb6a; box-shadow: 0 6px 20px rgba(76,175,80,0.6);}
            .highlight {color: #ffd600 !important;}
            .success {color: #4caf50 !important;}
            .danger {color: #e57373 !important;}
            .streamlit-expanderHeader {color: #4caf50 !important; background: linear-gradient(135deg, #132a18, #1a3320); border-color: #2e7d32;}
            .stMetric {background: linear-gradient(135deg, #132a18, #1a3320); border: 1px solid #2e7d32;}
            .stMetric [data-testid="stMetricValue"] {color: #4caf50 !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #4caf50, #66bb6a);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #1a3320; border: 1px solid #2e7d32; color: #4caf50;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #132a18 0%, #0f1f13 100%); border-right: 1px solid #1b5e20;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(19,42,24,0.85); border: 1px solid rgba(46,125,50,0.4);}
            .panel-box {background: linear-gradient(180deg, #132a18 0%, #1a3320 100%); border: 1px solid #1b5e20;}
            .panel-title {color: #4caf50 !important;}
        """,
        
        # ========================================
        # 3. NANE YEŞİLİ
        # ========================================
        "Nane Yeşili": """
            .stApp {background: linear-gradient(135deg, #0a1a15 0%, #0d1f1a 50%, #0a1a15 100%);}
            h1, h2 {color: #00e676 !important; text-shadow: 0 0 15px rgba(0,230,118,0.4);}
            h3 {color: #00c853 !important;}
            .terminal {color: #00e676; border-color: #00e676; box-shadow: 0 0 25px rgba(0,230,118,0.12); background: linear-gradient(180deg, #0a1a15, #0d1f1a);}
            .scenario-desc {border-left: 5px solid #00e676; box-shadow: 0 6px 20px rgba(0,230,118,0.08); background: linear-gradient(135deg, #132a22, #1a332b);}
            .stButton>button {background: linear-gradient(135deg, #00695c, #00897b); border-color: #00e676; color: #fff;}
            .stButton>button:hover {border-color: #69f0ae; box-shadow: 0 6px 20px rgba(0,230,118,0.6);}
            .highlight {color: #ffea00 !important;}
            .success {color: #00e676 !important;}
            .danger {color: #ff5252 !important;}
            .streamlit-expanderHeader {color: #00e676 !important; background: linear-gradient(135deg, #132a22, #1a332b); border-color: #00897b;}
            .stMetric {background: linear-gradient(135deg, #132a22, #1a332b); border: 1px solid #00897b;}
            .stMetric [data-testid="stMetricValue"] {color: #00e676 !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #00e676, #69f0ae);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #1a332b; border: 1px solid #00897b; color: #00e676;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #132a22 0%, #0f1f1a 100%); border-right: 1px solid #00695c;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(19,42,34,0.85); border: 1px solid rgba(0,137,123,0.4);}
            .panel-box {background: linear-gradient(180deg, #132a22 0%, #1a332b 100%); border: 1px solid #00695c;}
            .panel-title {color: #00e676 !important;}
        """,
        
        # ========================================
        # 4. ASKERİ YEŞİL
        # ========================================
        "Askeri Yeşil": """
            .stApp {background: linear-gradient(135deg, #0f1a0f 0%, #131f13 50%, #0f1a0f 100%);}
            h1, h2 {color: #8bc34a !important; text-shadow: 0 0 15px rgba(139,195,74,0.4);}
            h3 {color: #689f38 !important;}
            .terminal {color: #8bc34a; border-color: #8bc34a; box-shadow: 0 0 25px rgba(139,195,74,0.12); background: linear-gradient(180deg, #0f1a0f, #131f13);}
            .scenario-desc {border-left: 5px solid #8bc34a; box-shadow: 0 6px 20px rgba(139,195,74,0.08); background: linear-gradient(135deg, #1a2a1a, #213321);}
            .stButton>button {background: linear-gradient(135deg, #33691e, #558b2f); border-color: #8bc34a; color: #fff;}
            .stButton>button:hover {border-color: #aed581; box-shadow: 0 6px 20px rgba(139,195,74,0.6);}
            .highlight {color: #ffd600 !important;}
            .success {color: #8bc34a !important;}
            .danger {color: #ef5350 !important;}
            .streamlit-expanderHeader {color: #8bc34a !important; background: linear-gradient(135deg, #1a2a1a, #213321); border-color: #558b2f;}
            .stMetric {background: linear-gradient(135deg, #1a2a1a, #213321); border: 1px solid #558b2f;}
            .stMetric [data-testid="stMetricValue"] {color: #8bc34a !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #8bc34a, #aed581);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #213321; border: 1px solid #558b2f; color: #8bc34a;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #1a2a1a 0%, #131f13 100%); border-right: 1px solid #33691e;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(26,42,26,0.85); border: 1px solid rgba(85,139,47,0.4);}
            .panel-box {background: linear-gradient(180deg, #1a2a1a 0%, #213321 100%); border: 1px solid #33691e;}
            .panel-title {color: #8bc34a !important;}
        """,
        
        # ========================================
        # 5. ZÜMRÜT YEŞİLİ
        # ========================================
        "Zümrüt Yeşili": """
            .stApp {background: linear-gradient(135deg, #0a1616 0%, #0d1c1c 50%, #0a1616 100%);}
            h1, h2 {color: #00bfa5 !important; text-shadow: 0 0 15px rgba(0,191,165,0.4);}
            h3 {color: #00897b !important;}
            .terminal {color: #00bfa5; border-color: #00bfa5; box-shadow: 0 0 25px rgba(0,191,165,0.12); background: linear-gradient(180deg, #0a1616, #0d1c1c);}
            .scenario-desc {border-left: 5px solid #00bfa5; box-shadow: 0 6px 20px rgba(0,191,165,0.08); background: linear-gradient(135deg, #122828, #193333);}
            .stButton>button {background: linear-gradient(135deg, #004d40, #00695c); border-color: #00bfa5; color: #fff;}
            .stButton>button:hover {border-color: #64ffda; box-shadow: 0 6px 20px rgba(0,191,165,0.6);}
            .highlight {color: #ffd740 !important;}
            .success {color: #00bfa5 !important;}
            .danger {color: #ff6e6e !important;}
            .streamlit-expanderHeader {color: #00bfa5 !important; background: linear-gradient(135deg, #122828, #193333); border-color: #00695c;}
            .stMetric {background: linear-gradient(135deg, #122828, #193333); border: 1px solid #00695c;}
            .stMetric [data-testid="stMetricValue"] {color: #00bfa5 !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #00bfa5, #64ffda);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #193333; border: 1px solid #00695c; color: #00bfa5;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #122828 0%, #0d1c1c 100%); border-right: 1px solid #004d40;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(18,40,40,0.85); border: 1px solid rgba(0,105,92,0.4);}
            .panel-box {background: linear-gradient(180deg, #122828 0%, #193333 100%); border: 1px solid #004d40;}
            .panel-title {color: #00bfa5 !important;}
        """,
        
        # ========================================
        # 6. OKYANUS (Mavi)
        # ========================================
        "Okyanus": """
            .stApp {background: linear-gradient(135deg, #0a1628 0%, #0d1a33 50%, #0a1628 100%);}
            h1, h2 {color: #00b4d8 !important; text-shadow: 0 0 15px rgba(0,180,216,0.4);}
            h3 {color: #0096c7 !important;}
            .terminal {color: #00b4d8; border-color: #00b4d8; box-shadow: 0 0 25px rgba(0,180,216,0.12); background: linear-gradient(180deg, #0a1628, #0d1a33);}
            .scenario-desc {border-left: 5px solid #00b4d8; box-shadow: 0 6px 20px rgba(0,180,216,0.08); background: linear-gradient(135deg, #122640, #1a3350);}
            .stButton>button {background: linear-gradient(135deg, #023e8a, #0077b6); border-color: #00b4d8; color: #fff;}
            .stButton>button:hover {border-color: #48cae4; box-shadow: 0 6px 20px rgba(0,180,216,0.6);}
            .highlight {color: #ffd166 !important;}
            .success {color: #06d6a0 !important;}
            .danger {color: #ef476f !important;}
            .streamlit-expanderHeader {color: #00b4d8 !important; background: linear-gradient(135deg, #122640, #1a3350); border-color: #0077b6;}
            .stMetric {background: linear-gradient(135deg, #122640, #1a3350); border: 1px solid #0077b6;}
            .stMetric [data-testid="stMetricValue"] {color: #00b4d8 !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #00b4d8, #48cae4);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #1a3350; border: 1px solid #0077b6; color: #00b4d8;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #122640 0%, #0d1a33 100%); border-right: 1px solid #023e8a;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(18,38,64,0.85); border: 1px solid rgba(0,119,182,0.4);}
            .panel-box {background: linear-gradient(180deg, #122640 0%, #1a3350 100%); border: 1px solid #023e8a;}
            .panel-title {color: #00b4d8 !important;}
        """,
        
        # ========================================
        # 7. MOR
        # ========================================
        "Mor": """
            .stApp {background: linear-gradient(135deg, #0f0a1a 0%, #120d1f 50%, #0f0a1a 100%);}
            h1, h2 {color: #c77dff !important; text-shadow: 0 0 15px rgba(199,125,255,0.4);}
            h3 {color: #b06cf5 !important;}
            .terminal {color: #c77dff; border-color: #c77dff; box-shadow: 0 0 25px rgba(199,125,255,0.12); background: linear-gradient(180deg, #0f0a1a, #120d1f);}
            .scenario-desc {border-left: 5px solid #c77dff; box-shadow: 0 6px 20px rgba(199,125,255,0.08); background: linear-gradient(135deg, #1a1230, #221840);}
            .stButton>button {background: linear-gradient(135deg, #4a0e8f, #7209b7); border-color: #c77dff; color: #fff;}
            .stButton>button:hover {border-color: #e0aaff; box-shadow: 0 6px 20px rgba(199,125,255,0.6);}
            .highlight {color: #ffd60a !important;}
            .success {color: #9d4edd !important;}
            .danger {color: #ff477e !important;}
            .streamlit-expanderHeader {color: #c77dff !important; background: linear-gradient(135deg, #1a1230, #221840); border-color: #7209b7;}
            .stMetric {background: linear-gradient(135deg, #1a1230, #221840); border: 1px solid #7209b7;}
            .stMetric [data-testid="stMetricValue"] {color: #c77dff !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #c77dff, #e0aaff);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #221840; border: 1px solid #7209b7; color: #c77dff;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #1a1230 0%, #120d1f 100%); border-right: 1px solid #4a0e8f;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(26,18,48,0.85); border: 1px solid rgba(114,9,183,0.4);}
            .panel-box {background: linear-gradient(180deg, #1a1230 0%, #221840 100%); border: 1px solid #4a0e8f;}
            .panel-title {color: #c77dff !important;}
        """,
        
        # ========================================
        # 8. ALEV (Turuncu/Kırmızı)
        # ========================================
        "Alev": """
            .stApp {background: linear-gradient(135deg, #1a0a0a 0%, #1f0d0d 50%, #1a0a0a 100%);}
            h1, h2 {color: #ff6b35 !important; text-shadow: 0 0 15px rgba(255,107,53,0.4);}
            h3 {color: #e85d28 !important;}
            .terminal {color: #ff6b35; border-color: #ff6b35; box-shadow: 0 0 25px rgba(255,107,53,0.12); background: linear-gradient(180deg, #1a0a0a, #1f0d0d);}
            .scenario-desc {border-left: 5px solid #ff6b35; box-shadow: 0 6px 20px rgba(255,107,53,0.08); background: linear-gradient(135deg, #2a1515, #331c1c);}
            .stButton>button {background: linear-gradient(135deg, #8b0000, #cc3700); border-color: #ff6b35; color: #fff;}
            .stButton>button:hover {border-color: #ff8c42; box-shadow: 0 6px 20px rgba(255,107,53,0.6);}
            .highlight {color: #ffd700 !important;}
            .success {color: #ffaa00 !important;}
            .danger {color: #ff4444 !important;}
            .streamlit-expanderHeader {color: #ff6b35 !important; background: linear-gradient(135deg, #2a1515, #331c1c); border-color: #cc3700;}
            .stMetric {background: linear-gradient(135deg, #2a1515, #331c1c); border: 1px solid #cc3700;}
            .stMetric [data-testid="stMetricValue"] {color: #ff6b35 !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #ff6b35, #ff8c42);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #331c1c; border: 1px solid #cc3700; color: #ff6b35;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #2a1515 0%, #1f0d0d 100%); border-right: 1px solid #8b0000;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(42,21,21,0.85); border: 1px solid rgba(204,55,0,0.4);}
            .panel-box {background: linear-gradient(180deg, #2a1515 0%, #331c1c 100%); border: 1px solid #8b0000;}
            .panel-title {color: #ff6b35 !important;}
        """,
        
        # ========================================
        # 9. GECE YARISI (Gri/Beyaz)
        # ========================================
        "Gece Yarısı": """
            .stApp {background: linear-gradient(135deg, #0d0d0d 0%, #111111 50%, #0d0d0d 100%);}
            h1, h2 {color: #e0e0e0 !important; text-shadow: 0 0 15px rgba(255,255,255,0.2);}
            h3 {color: #b0b0b0 !important;}
            .terminal {color: #cccccc; border-color: #555555; box-shadow: 0 0 25px rgba(255,255,255,0.05); background: linear-gradient(180deg, #0d0d0d, #111111);}
            .scenario-desc {border-left: 5px solid #888888; box-shadow: 0 6px 20px rgba(255,255,255,0.03); background: linear-gradient(135deg, #1a1a1a, #222222);}
            .stButton>button {background: linear-gradient(135deg, #333333, #555555); border-color: #777777; color: #fff;}
            .stButton>button:hover {border-color: #999999; box-shadow: 0 6px 20px rgba(255,255,255,0.2);}
            .highlight {color: #ffcc00 !important;}
            .success {color: #66cc66 !important;}
            .danger {color: #ff6666 !important;}
            .streamlit-expanderHeader {color: #cccccc !important; background: linear-gradient(135deg, #1a1a1a, #222222); border-color: #555555;}
            .stMetric {background: linear-gradient(135deg, #1a1a1a, #222222); border: 1px solid #555555;}
            .stMetric [data-testid="stMetricValue"] {color: #ffffff !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #888888, #aaaaaa);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #222222; border: 1px solid #555555; color: #cccccc;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #1a1a1a 0%, #111111 100%); border-right: 1px solid #333333;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(26,26,26,0.85); border: 1px solid rgba(85,85,85,0.4);}
            .panel-box {background: linear-gradient(180deg, #1a1a1a 0%, #222222 100%); border: 1px solid #333333;}
            .panel-title {color: #e0e0e0 !important;}
        """,
        
        # ========================================
        # 10. KÖMÜR YEŞİLİ
        # ========================================
        "Kömür Yeşili": """
            .stApp {background: linear-gradient(135deg, #0f1410 0%, #121712 50%, #0f1410 100%);}
            h1, h2 {color: #aed581 !important; text-shadow: 0 0 15px rgba(174,213,129,0.3);}
            h3 {color: #9ccc65 !important;}
            .terminal {color: #aed581; border-color: #aed581; box-shadow: 0 0 25px rgba(174,213,129,0.10); background: linear-gradient(180deg, #0f1410, #121712);}
            .scenario-desc {border-left: 5px solid #aed581; box-shadow: 0 6px 20px rgba(174,213,129,0.06); background: linear-gradient(135deg, #1a221a, #212921);}
            .stButton>button {background: linear-gradient(135deg, #2e3b2e, #3d4f3d); border-color: #aed581; color: #fff;}
            .stButton>button:hover {border-color: #c5e1a5; box-shadow: 0 6px 20px rgba(174,213,129,0.5);}
            .highlight {color: #ffeb3b !important;}
            .success {color: #aed581 !important;}
            .danger {color: #ff7043 !important;}
            .streamlit-expanderHeader {color: #aed581 !important; background: linear-gradient(135deg, #1a221a, #212921); border-color: #3d4f3d;}
            .stMetric {background: linear-gradient(135deg, #1a221a, #212921); border: 1px solid #3d4f3d;}
            .stMetric [data-testid="stMetricValue"] {color: #aed581 !important;}
            .stProgress > div > div {background: linear-gradient(90deg, #aed581, #c5e1a5);}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {background: #212921; border: 1px solid #3d4f3d; color: #aed581;}
            section[data-testid="stSidebar"] {background: linear-gradient(180deg, #1a221a 0%, #121712 100%); border-right: 1px solid #2e3b2e;}
            div[data-testid="stVerticalBlock"] > div {background: rgba(26,34,26,0.85); border: 1px solid rgba(61,79,61,0.4);}
            .panel-box {background: linear-gradient(180deg, #1a221a 0%, #212921 100%); border: 1px solid #2e3b2e;}
            .panel-title {color: #aed581 !important;}
        """,
    }
    
    # ============================================
    # ORTAK DARK STİLLERİ (Tüm temalarda geçerli)
    # ============================================
    
    COMMON_DARK_STYLES: str = """
        [data-testid="stSidebar"] {min-width: 300px !important; max-width: 300px !important;}
        .terminal {
            font-family: 'Courier New', monospace;
            padding: 18px;
            border-radius: 10px;
            height: 280px;
            overflow-y: auto;
            white-space: pre-wrap;
            line-height: 1.4;
            box-shadow: inset 0 0 40px rgba(0,0,0,0.6);
        }
        .scenario-desc {
            border-radius: 10px;
            padding: 24px;
            margin: 20px 0;
            font-size: 1.02rem;
            line-height: 1.9;
            text-align: justify;
        }
        .streamlit-expanderHeader {border-radius: 8px; font-weight: bold;}
        .stSelectbox>div>div>div {border-radius: 6px;}
        .stButton>button {
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
            letter-spacing: 0.5px;
        }
        .stButton>button:hover {transform: translateY(-2px);}
        .stMetric {
            border-radius: 10px;
            padding: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        .panel-box {
            border-radius: 12px;
            padding: 15px;
            margin: 5px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .panel-title {
            font-size: 1rem;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
        }
        .step-dot {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .step-active {background: #00ff41; box-shadow: 0 0 8px #00ff41;}
        .step-done {background: #4f8bc9;}
        .step-pending {background: #333333;}
        p, li, span:not(.stException) {color: #d0d8e0 !important;}
        @keyframes pulse {
            0%{box-shadow:0 0 0 0 rgba(0,255,65,0.4)}
            70%{box-shadow:0 0 0 20px rgba(0,255,65,0)}
            100%{box-shadow:0 0 0 0 rgba(0,255,65,0)}
        }
        .pulse {animation: pulse 2s infinite;}
    """
    
    # ============================================
    # METOT 1: SESSION STATE BAŞLAT
    # ============================================
    
    @classmethod
    def init_session_state(cls) -> None:
        """Session state'i başlatır"""
        if 'selected_theme' not in st.session_state:
            st.session_state.selected_theme = cls.DEFAULT_THEME
    
    # ============================================
    # METOT 2: TEMA SEÇİCİ RENDER
    # ============================================
    
    @classmethod
    def render_theme_selector(cls, location: str = "sidebar") -> str:
        """
        Tema seçim arayüzünü render eder.
        
        Args:
            location: "sidebar" veya "main"
        
        Returns:
            Seçilen tema adı
        """
        cls.init_session_state()
        
        current = st.session_state.get('selected_theme', cls.DEFAULT_THEME)
        
        if location == "sidebar":
            st.sidebar.markdown("### 🎨 TEMA")
            try:
                current_idx = cls.THEMES.index(current)
            except ValueError:
                current_idx = 0
            
            theme_choice = st.sidebar.selectbox(
                "Tema seçin:",
                cls.THEMES,
                index=current_idx,
                key="theme_selector_widget",
                label_visibility="collapsed"
            )
        else:
            theme_choice = st.selectbox(
                "Tema:",
                cls.THEMES,
                index=cls.THEMES.index(current) if current in cls.THEMES else 0,
                key="theme_selector_main"
            )
        
        if theme_choice != current:
            st.session_state.selected_theme = theme_choice
            st.rerun()
        
        return theme_choice
    
    # ============================================
    # METOT 3: TEMA UYGULA
    # ============================================
    
    @classmethod
    def apply_theme(cls, theme_name: str = None) -> None:
        """
        Seçilen temayı uygular (CSS inject eder).
        
        Args:
            theme_name: Tema adı (None ise session state'ten alır)
        """
        if theme_name is None:
            theme_name = st.session_state.get('selected_theme', cls.DEFAULT_THEME)
        
        # Tema yoksa varsayılanı kullan
        if theme_name not in cls.THEME_CSS:
            theme_name = cls.DEFAULT_THEME
        
        theme_css = cls.THEME_CSS[theme_name]
        common_css = cls.COMMON_DARK_STYLES
        
        # CSS'i birleştir ve inject et
        full_css = f"<style>{common_css}\n{theme_css}</style>"
        st.markdown(full_css, unsafe_allow_html=True)
    
    # ============================================
    # METOT 4: TEMA RENGİ AL
    # ============================================
    
    @classmethod
    def get_theme_color(cls, theme_name: str = None, color_type: str = "primary") -> str:
        """
        Tema için renk döndürür.
        
        Args:
            theme_name: Tema adı
            color_type: "primary", "secondary", "text", "background"
        
        Returns:
            Hex renk kodu
        """
        if theme_name is None:
            theme_name = st.session_state.get('selected_theme', cls.DEFAULT_THEME)
        
        # Tema renk paleti
        color_palette = {
            "Matrix Yeşil": {
                "primary": "#00ff41",
                "secondary": "#5a9ed4",
                "text": "#d0d8e0",
                "background": "#0a0e17",
                "warning": "#ffaa00",
                "danger": "#ff4444"
            },
            "Orman Yeşili": {
                "primary": "#4caf50",
                "secondary": "#66bb6a",
                "text": "#d0d8e0",
                "background": "#0a1a0f",
                "warning": "#ffd600",
                "danger": "#e57373"
            },
            "Nane Yeşili": {
                "primary": "#00e676",
                "secondary": "#69f0ae",
                "text": "#d0d8e0",
                "background": "#0a1a15",
                "warning": "#ffea00",
                "danger": "#ff5252"
            },
            "Askeri Yeşil": {
                "primary": "#8bc34a",
                "secondary": "#aed581",
                "text": "#d0d8e0",
                "background": "#0f1a0f",
                "warning": "#ffd600",
                "danger": "#ef5350"
            },
            "Zümrüt Yeşili": {
                "primary": "#00bfa5",
                "secondary": "#64ffda",
                "text": "#d0d8e0",
                "background": "#0a1616",
                "warning": "#ffd740",
                "danger": "#ff6e6e"
            },
            "Okyanus": {
                "primary": "#00b4d8",
                "secondary": "#48cae4",
                "text": "#d0d8e0",
                "background": "#0a1628",
                "warning": "#ffd166",
                "danger": "#ef476f"
            },
            "Mor": {
                "primary": "#c77dff",
                "secondary": "#e0aaff",
                "text": "#d0d8e0",
                "background": "#0f0a1a",
                "warning": "#ffd60a",
                "danger": "#ff477e"
            },
            "Alev": {
                "primary": "#ff6b35",
                "secondary": "#ff8c42",
                "text": "#d0d8e0",
                "background": "#1a0a0a",
                "warning": "#ffd700",
                "danger": "#ff4444"
            },
            "Gece Yarısı": {
                "primary": "#e0e0e0",
                "secondary": "#aaaaaa",
                "text": "#cccccc",
                "background": "#0d0d0d",
                "warning": "#ffcc00",
                "danger": "#ff6666"
            },
            "Kömür Yeşili": {
                "primary": "#aed581",
                "secondary": "#c5e1a5",
                "text": "#d0d8e0",
                "background": "#0f1410",
                "warning": "#ffeb3b",
                "danger": "#ff7043"
            },
        }
        
        palette = color_palette.get(theme_name, color_palette["Matrix Yeşil"])
        return palette.get(color_type, palette["primary"])
    
    # ============================================
    # METOT 5: TEMA ÖNİZLEME (Küçük kart)
    # ============================================
    
    @classmethod
    def render_theme_preview(cls, theme_name: str, selected: bool = False) -> str:
        """
        Tema önizleme kartı HTML'i döndürür.
        
        Args:
            theme_name: Tema adı
            selected: Seçili mi?
        
        Returns:
            HTML string
        """
        colors = {
            "primary": cls.get_theme_color(theme_name, "primary"),
            "secondary": cls.get_theme_color(theme_name, "secondary"),
            "background": cls.get_theme_color(theme_name, "background"),
        }
        
        border = "2px solid #00ff41" if selected else "1px solid #333"
        
        return f"""
        <div style="
            background: {colors['background']};
            border: {border};
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            text-align: center;
        ">
            <div style="
                color: {colors['primary']};
                font-weight: bold;
                font-size: 0.9rem;
            ">{theme_name}</div>
            <div style="
                display: flex;
                justify-content: center;
                gap: 3px;
                margin-top: 5px;
            ">
                <div style="width: 15px; height: 15px; background: {colors['primary']}; border-radius: 3px;"></div>
                <div style="width: 15px; height: 15px; background: {colors['secondary']}; border-radius: 3px;"></div>
            </div>
        </div>
        """
    
    # ============================================
    # METOT 6: PLOTLY TEMA AYARLARI
    # ============================================
    
    @classmethod
    def get_plotly_layout(cls, theme_name: str = None) -> dict:
        """
        Plotly grafikleri için layout ayarları döndürür.
        
        Args:
            theme_name: Tema adı
        
        Returns:
            Plotly layout dict
        """
        if theme_name is None:
            theme_name = st.session_state.get('selected_theme', cls.DEFAULT_THEME)
        
        primary = cls.get_theme_color(theme_name, "primary")
        text_color = cls.get_theme_color(theme_name, "text")
        
        return {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"color": text_color, "family": "Courier New, monospace"},
            "title": {"font": {"color": primary, "size": 16}},
            "margin": {"t": 45, "b": 20, "l": 20, "r": 20},
        }


# ============================================
# YARDIMCI FONKSİYONLAR
# ============================================

def get_current_theme() -> str:
    """Mevcut temayı döndürür"""
    return st.session_state.get('selected_theme', ThemeManager.DEFAULT_THEME)


def get_color(color_type: str = "primary") -> str:
    """Mevcut temanın belirtilen rengini döndürür"""
    return ThemeManager.get_theme_color(get_current_theme(), color_type)


def apply_current_theme() -> None:
    """Mevcut temayı uygular (kısayol)"""
    ThemeManager.apply_theme()


# ============================================
# MODÜL TESTİ
# ============================================

if __name__ == "__main__":
    # Basit test
    print("✅ ThemeManager yüklendi")
    print(f"Toplam tema: {len(ThemeManager.THEMES)}")
    for theme in ThemeManager.THEMES:
        print(f"  - {theme}")
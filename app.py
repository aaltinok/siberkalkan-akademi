"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SİBERKALKAN AKADEMİ v5.0                                 ║
║            Siber Güvenlik Savunma Eğitim Simülasyonu                        ║
║                                                                            ║
║                                                 ║
║                                                                              ║
║  Bu platform, %70 SAVUNMA + %30 tehdit anlayışı prensibiyle çalışır.        ║
║  Tüm senaryolar eğitim amaçlıdır ve etik koruma katmanı ile korunur.        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================
# BÖLÜM 1: IMPORTLAR
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import time
import random
from datetime import datetime, timedelta
from collections import deque, defaultdict
import hashlib
import json
import base64
from io import BytesIO
import string

# Yerel modüller (utils/)
from utils.theme_manager import ThemeManager, get_current_theme, get_color
from utils.ethics_guard import EthicsGuard, display_ethics_status
from utils.safety_filter import AISafetyFilter, display_references
from utils.report_generator import ReportGenerator


# ============================================
# BÖLÜM 2: SAYFA YAPILANDIRMASI
# ============================================

st.set_page_config(
    page_title="SiberKalkan Akademi",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# BÖLÜM 3: GLOBAL SESSION STATE BAŞLAT
# ============================================

if 'global_stats' not in st.session_state:
    st.session_state.global_stats = {
        'completed_scenarios': {},
        'techniques_used': [],
        'total_attempts': 0,
        'total_success': 0,
        'risk_history': [],
        'start_time': datetime.now()
    }

# Tema başlat
ThemeManager.init_session_state()

# ============================================
# BÖLÜM 4: ETİK KORUMA KONTROLÜ
# ============================================
# Platform açıldığında ilk kontrol: etik sözleşme onayı

if not EthicsGuard.require_ethics_acceptance():
    st.stop()

# Tema uygula (etik sözleşme kabul edildikten sonra)
ThemeManager.apply_theme()

# ============================================
# BÖLÜM 5: YARDIMCI GÖRSELLEŞTİRME FONKSİYONLARI
# ============================================

def generate_ip():
    """Simülasyon IP adresi üretir"""
    return f"{random.randint(10,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"


def generate_mac():
    """Simülasyon MAC adresi üretir"""
    return ":".join([f"{random.randint(0,255):02x}" for _ in range(6)])


def create_advanced_network_graph(devices, edges, highlight_nodes=None, 
                                   compromised_nodes=None, attack_paths=None, 
                                   traffic_flows=None):
    """
    Profesyonel seviye ağ topolojisi görselleştirmesi.
    Cihaz tiplerine özel ikonlar, saldırı yolları, trafik akış animasyonları.
    """
    G = nx.Graph()
    icon_map = {
        'attacker': '🔴', 'firewall': '🧱', 'server': '🖥️', 'workstation': '💻',
        'router': '🌐', 'database': '🗄️', 'cloud': '☁️', 'mobile': '📱',
        'iot': '📡', 'honeypot': '🍯', 'ids': '🔍', 'vpn': '🔐',
        'switch': '🔀', 'printer': '🖨️', 'camera': '📷'
    }
    
    for dev in devices:
        G.add_node(
            dev['id'], label=dev['name'], type=dev['type'],
            ip=dev.get('ip', ''), status=dev.get('status', 'normal'),
            os=dev.get('os', ''), risk=dev.get('risk', 0)
        )
    
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    
    pos = nx.kamada_kawai_layout(G) if len(G.nodes()) > 5 else nx.spring_layout(G, seed=42, k=1.8)
    
    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        is_highlighted = False
        edge_color = '#2d4a6e'
        edge_width = 1.2
        
        if attack_paths:
            for path in attack_paths:
                for i in range(len(path)-1):
                    if (edge[0] == path[i] and edge[1] == path[i+1]) or \
                       (edge[1] == path[i] and edge[0] == path[i+1]):
                        is_highlighted = True
                        edge_color = '#ff4444'
                        edge_width = 3
                        break
        
        if traffic_flows and edge in traffic_flows:
            edge_color = '#ffaa00'
            edge_width = 2.5
        
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode='lines',
            line=dict(width=edge_width, color=edge_color),
            hoverinfo='none',
            showlegend=False
        ))
    
    node_x, node_y, node_text, node_colors, node_sizes, node_symbols = [], [], [], [], [], []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        info = G.nodes[node]
        icon = icon_map.get(info['type'], '●')
        
        if compromised_nodes and node in compromised_nodes:
            status_text = "⚠️ ELE GEÇİRİLDİ"
            color = '#ff4444'
            size = 42
            symbol = 'x'
        elif highlight_nodes and node in highlight_nodes:
            status_text = "🎯 HEDEF"
            color = '#ffaa00'
            size = 42
            symbol = 'diamond'
        elif info['status'] == 'isolated':
            status_text = "🔒 İZOLE"
            color = '#888888'
            size = 32
            symbol = 'circle'
        else:
            status_text = ""
            color = '#4f8bc9'
            size = 34
            symbol = 'circle'
        
        hover_text = (
            f"<b>{icon} {info['label']}</b><br>"
            f"IP: {info.get('ip', 'N/A')}<br>"
            f"Tip: {info['type'].upper()}<br>"
            f"İS: {info.get('os', 'Bilinmiyor')}<br>"
            f"Risk: %{info.get('risk', 0)}<br>"
            f"{status_text}"
        )
        
        node_text.append(hover_text)
        node_colors.append(color)
        node_sizes.append(size)
        node_symbols.append(symbol)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[G.nodes[n]['label'] for n in G.nodes()],
        textposition="bottom center",
        hovertext=node_text,
        hoverinfo='text',
        marker=dict(
            size=node_sizes, color=node_colors,
            line=dict(width=2.5, color='#ffffff'),
            symbol=node_symbols
        ),
        textfont=dict(size=9, color='#e0e0e0'),
        showlegend=False
    )
    
    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=go.Layout(
            title=dict(
                text="🌐 AĞ TOPOLOJİSİ",
                font=dict(size=16, color=get_color("primary")),
                x=0.5
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=45),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    return fig


def create_cyber_gauge(value, title, max_val=100, thresholds=(30,70)):
    """Siber güvenlik temalı gösterge çizelgesi"""
    colors = ['#00ff41', '#ffaa00', '#ff4444']
    color_idx = 2 if value > thresholds[1] else 1 if value > thresholds[0] else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'color': '#e0e0e0', 'size': 15}},
        number={'font': {'color': colors[color_idx], 'size': 36, 'family': 'Courier New'}},
        delta={
            'reference': 50,
            'increasing': {'color': '#ff4444'},
            'decreasing': {'color': '#00ff41'}
        },
        gauge={
            'axis': {
                'range': [0, max_val],
                'tickcolor': '#e0e0e0',
                'tickfont': {'color': '#e0e0e0'}
            },
            'bar': {'color': colors[color_idx], 'thickness': 0.25},
            'bgcolor': 'rgba(0,0,0,0.4)',
            'borderwidth': 2,
            'bordercolor': '#2d4a6e',
            'steps': [
                {'range': [0, thresholds[0]], 'color': 'rgba(0,255,65,0.1)'},
                {'range': [thresholds[0], thresholds[1]], 'color': 'rgba(255,170,0,0.1)'},
                {'range': [thresholds[1], max_val], 'color': 'rgba(255,68,68,0.15)'}
            ],
            'threshold': {
                'line': {'color': '#ff4444', 'width': 3},
                'thickness': 0.8,
                'value': 85
            }
        }
    ))
    fig.update_layout(
        height=220,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=10)
    )
    return fig


def create_kill_chain(phases_status):
    """Saldırı öldürme zinciri görselleştirmesi"""
    fig = go.Figure()
    for i, (phase, completed) in enumerate(phases_status.items()):
        color = '#ff4444' if completed else '#1e3a5f'
        fig.add_trace(go.Scatter(
            x=[i], y=[0],
            mode='markers+text',
            marker=dict(
                size=28, color=color, symbol='circle',
                line=dict(width=2, color='#fff')
            ),
            text=[phase[:5]],
            textposition="top center",
            hovertext=f"{phase}: {'✅ TAMAM' if completed else '⏳ BEKLİYOR'}",
            showlegend=False
        ))
        if i < len(phases_status) - 1:
            fig.add_trace(go.Scatter(
                x=[i, i+1], y=[0, 0],
                mode='lines',
                line=dict(color='#ff4444' if completed else '#1e3a5f', width=3),
                showlegend=False
            ))
    fig.update_layout(
        title="☠️ KILL CHAIN İLERLEMESİ",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=180,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False, range=[-0.5,0.5]),
        margin=dict(t=35, b=15)
    )
    return fig


def create_radar_chart(categories, values, title):
    """Radar grafiği - güvenlik yetenekleri için"""
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(0,255,65,0.2)',
        line=dict(color='#00ff41', width=2)
    ))
    fig.update_layout(
        title=title,
        polar=dict(
            radialaxis=dict(visible=True, range=[0,100], color='#e0e0e0'),
            angularaxis=dict(color='#e0e0e0')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0',
        height=300
    )
    return fig


# ============================================
# BÖLÜM 6: SENARYO DURUM YÖNETİMİ
# ============================================

class ScenarioState:
    """Senaryo durum yönetimi"""
    
    @staticmethod
    def get(key, default):
        if key not in st.session_state:
            st.session_state[key] = default
        return st.session_state[key]
    
    @staticmethod
    def set(key, value):
        st.session_state[key] = value
    
    @staticmethod
    def reset(key, default):
        st.session_state[key] = default
        st.rerun()


# ============================================
# BÖLÜM 7: OTOMATİK PİLOT SİSTEMİ
# ============================================

def get_auto_pilot_steps(scenario_id):
    """Her senaryo için otomatik pilot adım listesini döndürür"""
    pilot_steps = {
        # --- SEVİYE 1 ---
        "1A": [
            ("tara", "Ağ keşfi başlatılıyor...", 1.0),
            ("analiz", "Açık portlar analiz ediliyor...", 1.5),
            ("gonder --port 80 --veri exploit", "Test paketi gönderiliyor...", 2.0),
        ],
        "1B": [
            ("kural_ekle:SSH Brute-Force Engelleme", "SSH koruması ekleniyor...", 1.0),
            ("kural_ekle:HTTP Anomali Filtreleme", "HTTP filtresi ekleniyor...", 1.0),
            ("kural_ekle:ICMP Flood Koruması", "ICMP koruması ekleniyor...", 1.0),
            ("ai_hamle", "AI saldırısı simüle ediliyor...", 1.5),
            ("ai_hamle", "İkinci saldırı dalgası...", 1.5),
        ],
        "1C": [
            ("tara", "Sunucular taranıyor...", 1.0),
            ("detayli_tara A", "A sunucusu analiz ediliyor...", 1.5),
            ("detayli_tara B", "B sunucusu analiz ediliyor...", 1.5),
            ("exploit A", "Gerçek sunucuya test...", 2.0),
        ],
        "1D": [
            ("yeni_dns", "DNS sorgusu oluşturuluyor...", 0.5),
            ("yeni_dns", "DNS sorgusu oluşturuluyor...", 0.5),
            ("izole_et", "Şüpheli sorgu izole ediliyor...", 1.0),
            ("yeni_dns", "DNS sorgusu oluşturuluyor...", 0.5),
            ("izole_et", "Şüpheli sorgu izole ediliyor...", 1.0),
        ],
        "1E": [
            ("dinle", "Paket dinleme başlatılıyor...", 1.0),
            ("dinle", "Paket dinleme devam ediyor...", 1.0),
            ("dinle", "Paket dinleme devam ediyor...", 1.0),
            ("cookie_cal", "Oturum analizi yapılıyor...", 2.0),
        ],
        
        # --- SEVİYE 2 ---
        "2A": [
            ("normal_gezin", "Normal kullanıcı simülasyonu...", 1.0),
            ("normal_gezin", "Normal kullanıcı simülasyonu...", 1.0),
            ("gizli_tara", "Gizli tarama yapılıyor...", 2.0),
            ("exploit", "Bulunan zafiyet test ediliyor...", 2.0),
        ],
        "2B": [
            ("gercek_tehdit", "Uyarı analiz ediliyor...", 1.5),
            ("gercek_tehdit", "Uyarı analiz ediliyor...", 1.5),
            ("yoksay", "Yanlış pozitif filtreleniyor...", 1.0),
            ("gercek_tehdit", "Kritik uyarıya müdahale...", 1.5),
            ("yeni_uyarilar", "Yeni uyarılar taranıyor...", 1.0),
        ],
        "2C": [
            ("test_basic", "Temel test yapılıyor...", 1.5),
            ("test_encoded", "Kodlamalı test deneniyor...", 1.5),
            ("test_time", "Zaman tabanlı test...", 2.0),
            ("exploit", "WAF atlatma testi...", 2.0),
        ],
        "2D": [
            ("engelle", "Şüpheli e-posta engelleniyor...", 1.0),
            ("izin_ver", "Meşru e-postaya izin...", 1.0),
            ("engelle", "Oltalama e-postası engelleniyor...", 1.0),
            ("engelle", "Oltalama e-postası engelleniyor...", 1.0),
            ("izin_ver", "Meşru e-postaya izin...", 1.0),
        ],
        "2E": [
            ("bucket_kapat", "Açık S3 bucket kapatılıyor...", 1.5),
            ("bucket_kapat", "Açık S3 bucket kapatılıyor...", 1.5),
            ("ai_tara", "AI tarama başlatılıyor...", 1.0),
            ("bucket_kapat", "Yeni açık bucket kapatılıyor...", 1.5),
        ],
        
        # --- SEVİYE 3 ---
        "3A": [
            ("yakala", "VPN paketleri yakalanıyor...", 1.0),
            ("yakala", "VPN paketleri yakalanıyor...", 1.0),
            ("yakala", "VPN paketleri yakalanıyor...", 1.0),
            ("analiz_et", "Paketler analiz ediliyor...", 1.5),
            ("kirilma_dene", "Kripto analizi yapılıyor...", 2.0),
            ("exploit", "Veriler ele geçiriliyor...", 2.0),
        ],
        "3B": [
            ("sunucu_izole", "Enfekte sunucu izole ediliyor...", 1.5),
            ("yedek_geri_yukle", "Yedek geri yükleniyor...", 1.5),
            ("ag_segmentasyon", "Ağ segmentlere ayrılıyor...", 1.0),
            ("antivirus_tarama", "Antivirüs taraması yapılıyor...", 1.5),
            ("sunucu_izole", "Kalan enfekte sunucu izole...", 1.5),
        ],
        "3C": [
            ("anahtar_dagit", "PGP anahtarı dağıtılıyor...", 1.0),
            ("anahtar_dagit", "PGP anahtarı dağıtılıyor...", 1.0),
            ("anahtar_dagit", "PGP anahtarı dağıtılıyor...", 1.0),
            ("imzalama_partisi", "Anahtar imzalama partisi...", 1.5),
            ("ai_mitm", "AI MITM saldırısı engelleniyor...", 1.5),
        ],
        "3D": [
            ("tara_eski", "Zayıf algoritmalı sistemler...", 1.5),
            ("tara_eski", "Zayıf algoritmalı sistemler...", 1.5),
            ("shor_atagi", "Kuantum analizi yapılıyor...", 2.0),
            ("shor_atagi", "Kuantum analizi devam ediyor...", 2.0),
            ("exploit", "Zararlı güncelleme enjekte...", 2.0),
        ],
        "3E": [
            ("analiz_et", "Akıllı kontrat analiz ediliyor...", 1.5),
            ("reentrancy_test", "Reentrancy test ediliyor...", 2.0),
            ("exploit", "Fonlar çekiliyor...", 2.0),
        ],
        
        # --- SEVİYE 4 ---
        "4A": [
            ("saldiri:SYN Flood:7", "SYN Flood başlatılıyor...", 1.5),
            ("saldiri:UDP Flood:5", "UDP Flood ile devam...", 1.5),
            ("taktik_degistir", "Taktik değiştiriliyor...", 1.0),
            ("saldiri:HTTP Flood:8", "HTTP Flood ile yükleniliyor...", 1.5),
            ("botnet_yenile", "Botnet yenileniyor...", 1.0),
            ("saldiri:Slowloris:6", "Slowloris ile zorlanıyor...", 2.0),
        ],
        "4B": [
            ("savunma:Rate Limiting", "Rate limiting uygulanıyor...", 1.0),
            ("savunma:IP Kara Liste", "IP kara liste aktif...", 1.0),
            ("savunma:CAPTCHA", "CAPTCHA doğrulaması...", 1.0),
            ("savunma:CDN Etkinleştir", "CDN etkinleştiriliyor...", 1.0),
            ("savunma:WAF Kuralı", "WAF kuralı ekleniyor...", 1.0),
        ],
        "4C": [
            ("cozumleyici_tara", "Açık DNS çözümleyicileri...", 1.0),
            ("cozumleyici_tara", "Açık DNS çözümleyicileri...", 1.0),
            ("cozumleyici_tara", "Açık DNS çözümleyicileri...", 1.0),
            ("saldiri:ANY", "ANY sorgu amplifikasyonu...", 2.0),
        ],
        "4D": [
            ("aksiyon:Sunucu Ekle", "Horizontal ölçeklendirme...", 1.5),
            ("aksiyon:Cache Etkinleştir", "Önbellek etkinleştiriliyor...", 1.0),
            ("aksiyon:CDN Etkinleştir", "CDN etkinleştiriliyor...", 1.0),
            ("aksiyon:DB Bağlantı Havuzu", "Veritabanı optimize...", 1.5),
        ],
        "4E": [
            ("pop_ekle:Asya-Pasifik", "Asya-Pasifik PoP ekleniyor...", 1.0),
            ("pop_ekle:Güney Amerika", "Güney Amerika PoP ekleniyor...", 1.0),
            ("cache_optimize", "Cache optimize ediliyor...", 1.0),
            ("pop_ekle:Orta Doğu", "Orta Doğu PoP ekleniyor...", 1.0),
        ],
        
        # --- SEVİYE 5 ---
        "5A": [
            ("kesif:LinkedIn Taraması", "LinkedIn profilleri taranıyor...", 1.0),
            ("kesif:Github Analizi", "Github repoları analiz ediliyor...", 1.5),
            ("kesif:DNS Keşfi", "DNS kayıtları keşfediliyor...", 1.0),
            ("kesif:Shodan Taraması", "Shodan taraması yapılıyor...", 1.5),
            ("kesif:İş İlanı Analizi", "İş ilanları analiz ediliyor...", 1.0),
        ],
        "5B": [
            ("gercek_tehdit", "Gerçek tehdit tespit ediliyor...", 1.5),
            ("yoksay", "Yanlış pozitif filtreleniyor...", 1.0),
            ("gercek_tehdit", "Gerçek tehdit tespit ediliyor...", 1.5),
            ("gercek_tehdit", "Gerçek tehdit tespit ediliyor...", 1.5),
        ],
        "5C": [
            ("statik_analiz", "Statik analiz yapılıyor...", 2.0),
            ("dinamik_analiz", "Dinamik analiz yapılıyor...", 2.0),
            ("rapor_olustur", "Tehdit raporu oluşturuluyor...", 1.5),
        ],
        "5D": [
            ("yukselt:SUID Binary", "SUID binary analizi...", 2.0),
            ("yukselt:Servis Yanlış Yapılandırma", "Servis analizi...", 2.0),
            ("yukselt:Token Manipülasyonu", "Token analizi...", 2.0),
        ],
        "5E": [
            ("temizlik:Shell History", "Shell history temizleniyor...", 1.0),
            ("temizlik:Event Log", "Event log'lar siliniyor...", 1.0),
            ("temizlik:Timestamp Değiştir", "Zaman damgaları değiştiriliyor...", 1.0),
            ("temizlik:Ağ Logu Karart", "Ağ logları karartılıyor...", 1.0),
        ],
        
        # --- SEVİYE 6 ---
        "6A": [
            ("asama:Keşif:Pasif OSINT", "Keşif: Pasif OSINT...", 1.5),
            ("asama:Silahlanma:Özel Malware", "Silahlanma...", 1.5),
            ("asama:Teslimat:Spear-Phishing", "Teslimat...", 2.0),
            ("asama:İstismar:RCE Exploit", "İstismar...", 2.0),
            ("asama:Kurulum:Registry", "Kurulum...", 1.5),
            ("asama:C2:HTTPS Beacon", "C2 kanal...", 1.5),
            ("asama:Hedef:Veri Sızdırma", "Hedef...", 2.0),
        ],
        "6B": [
            ("mudahale:Log Analizi", "Log analizi yapılıyor...", 1.5),
            ("mudahale:Endpoint Taraması", "Endpoint taranıyor...", 1.5),
            ("mudahale:Ağ İzleme", "Ağ izleniyor...", 1.0),
            ("mudahale:Tehdit İstihbaratı", "Tehdit istihbaratı...", 1.0),
            ("mudahale:İzolasyon", "APT izole ediliyor...", 2.0),
        ],
        "6C": [
            ("hareket:Pass-the-Hash", "Pass-the-Hash analizi...", 2.0),
            ("hareket:PsExec", "PsExec analizi...", 2.0),
            ("hareket:WMI", "WMI analizi...", 2.0),
        ],
        "6D": [
            ("sizdir:HTTPS Upload", "HTTPS analizi...", 1.5),
            ("sizdir:Parçalı Transfer", "Parçalı transfer...", 2.0),
            ("sizdir:Steganografi", "Steganografi analizi...", 2.5),
        ],
        "6E": [
            ("mudahale:OT Trafik İzleme", "OT trafiği izleniyor...", 1.0),
            ("mudahale:PLC Güvenlik Kontrolü", "PLC güvenliği...", 1.5),
            ("mudahale:IT-OT Gateway", "Gateway güçlendiriliyor...", 1.5),
            ("mudahale:Fiziksel Güvenlik", "Fiziksel güvenlik...", 1.0),
        ],
        
        # --- SEVİYE 7 ---
        "7A": [
            ("sql:UNION Sorgusu", "UNION sorgusu ile keşif...", 1.5),
            ("sql:Information Schema", "Şema keşfediliyor...", 1.5),
            ("sql:Hash Çekme", "Hash analizi yapılıyor...", 2.0),
            ("sql:Hash Kırma", "Hash analizi...", 2.0),
        ],
        "7B": [
            ("kural:SQL Enjeksiyon", "SQL enjeksiyon koruması...", 1.0),
            ("kural:XSS Filtreleme", "XSS filtresi ekleniyor...", 1.0),
            ("kural:CSRF Token", "CSRF koruması ekleniyor...", 1.0),
            ("kural:Rate Limiting", "Rate limiting uygulanıyor...", 1.0),
        ],
        "7C": [
            ("xss:Reflected XSS", "Reflected XSS analizi...", 1.5),
            ("xss:CSP Bypass", "CSP analizi...", 2.0),
            ("xss:Cookie Stealer", "Cookie analizi...", 2.0),
        ],
        "7D": [
            ("komut:Basit Enjeksiyon", "Temel komut enjeksiyonu...", 1.5),
            ("komut:Pipe Bypass", "Pipe bypass analizi...", 1.5),
            ("komut:Blind Injection", "Kör enjeksiyon analizi...", 2.0),
            ("komut:Reverse Shell", "Reverse shell analizi...", 2.0),
        ],
        "7E": [
            ("ldap:Domain Keşfi", "Domain yapısı keşfediliyor...", 1.5),
            ("ldap:Kerberoasting", "Kerberoasting analizi...", 2.0),
            ("ldap:DCSync", "DCSync analizi...", 2.0),
        ],
        
        # --- SEVİYE 8 ---
        "8A": [
            ("debug:Statik Analiz", "Statik analiz yapılıyor...", 1.5),
            ("debug:Breakpoint", "Breakpoint yerleştiriliyor...", 1.0),
            ("debug:Breakpoint", "Breakpoint yerleştiriliyor...", 1.0),
            ("debug:Breakpoint", "Breakpoint yerleştiriliyor...", 1.0),
            ("debug:Algoritma Çıkar", "Algoritma analizi...", 2.0),
        ],
        "8B": [
            ("malware:PE Analizi", "PE header analizi...", 1.5),
            ("malware:Sandbox", "Sandbox'ta çalıştırılıyor...", 2.0),
            ("malware:C2 Deşifre", "C2 deşifre ediliyor...", 2.0),
            ("malware:Rapor", "Tehdit raporu...", 1.5),
        ],
        "8C": [
            ("unpack:Entropi Analizi", "Entropi analizi...", 1.0),
            ("unpack:OEP Ara", "OEP aranıyor...", 2.0),
            ("unpack:Memory Dump", "Memory dump alınıyor...", 1.5),
            ("unpack:IAT Rekonstrüksiyon", "IAT rekonstrüksiyon...", 2.0),
        ],
        "8D": [
            ("firma:Firmware Dump", "Firmware dökümü...", 1.5),
            ("firma:Binary Diff", "Binary karşılaştırma...", 2.0),
            ("firma:Rootkit Temizle", "Rootkit temizleniyor...", 2.0),
        ],
        "8E": [
            ("kernel:Syscall Kontrol", "Syscall tablosu...", 1.5),
            ("kernel:Hidden Process", "Gizli prosesler...", 2.0),
            ("kernel:Rootkit Kaldır", "Rootkit kaldırılıyor...", 2.0),
        ],
        
        # --- SEVİYE 9 ---
        "9A": [
            ("phishing:CEO'dan Özel Talimat", "CEO taklidi e-posta...", 1.5),
            ("phishing:BT Güvenlik Uyarısı", "BT güvenlik uyarısı...", 1.5),
            ("phishing:Acil Şifre Sıfırlama", "Acil şifre sıfırlama...", 1.5),
            ("phishing:CEO'dan Özel Talimat", "CEO taklidi e-posta...", 1.5),
        ],
        "9B": [
            ("egitim:Phishing Farkındalığı", "Phishing eğitimi...", 1.5),
            ("egitim:Şifre Güvenliği", "Şifre güvenliği eğitimi...", 1.5),
            ("egitim:Sosyal Mühendislik", "Sosyal mühendislik eğitimi...", 1.5),
            ("egitim:Simülasyon Testi", "Simülasyon testi...", 1.0),
        ],
        "9C": [
            ("fiziksel:Tailgating", "Tailgating simülasyonu...", 2.0),
            ("fiziksel:Pretexting", "Pretexting simülasyonu...", 2.0),
            ("fiziksel:Otorite İstismarı", "Otorite simülasyonu...", 2.0),
        ],
        "9D": [
            ("vishing:IT Destek", "IT destek taklidi...", 1.5),
            ("vishing:BT Güvenlik", "BT güvenlik taklidi...", 1.5),
            ("vishing:CEO Asistanı", "CEO asistanı taklidi...", 1.5),
        ],
        "9E": [
            ("pretext:Finans:Otorite", "Finans otorite yaklaşımı...", 2.0),
            ("pretext:IT:Teknik Uzman", "IT teknik uzman...", 2.0),
            ("pretext:İK:Empatik", "İK empatik yaklaşım...", 2.0),
            ("pretext:Yönetim:Acil Durum", "Yönetim acil durum...", 2.0),
        ],
        
        # --- SEVİYE 10 ---
        "10A": [
            ("asama:Keşif:Pasif OSINT", "Keşif: Pasif OSINT...", 1.5),
            ("asama:Silahlanma:Custom Malware", "Silahlanma...", 1.5),
            ("asama:Teslimat:Spear-Phish", "Teslimat...", 2.0),
            ("asama:İstismar:Zero-Day", "İstismar...", 2.5),
            ("asama:Kurulum:Scheduled Task", "Kurulum...", 1.5),
            ("asama:C2:HTTPS", "C2 kanal...", 1.5),
            ("asama:Hedef:Exfiltrate", "Hedef...", 2.0),
        ],
        "10B": [
            ("savunma:SIEM Kuralı", "SIEM kuralı ekleniyor...", 1.0),
            ("savunma:EDR İzolasyon", "EDR izolasyonu...", 1.5),
            ("savunma:WAF Güncelleme", "WAF güncelleniyor...", 1.0),
            ("savunma:DNS Sinkhole", "DNS sinkhole...", 1.5),
            ("savunma:Ağ Segmentasyonu", "Ağ segmentasyonu...", 1.5),
        ],
        "10C": [
            ("iyilestirme:Tespit Kuralı", "Tespit kuralı...", 1.5),
            ("iyilestirme:Log Retention", "Log saklama...", 1.0),
            ("iyilestirme:Alert Tuning", "Uyarı ayarlaması...", 1.0),
            ("iyilestirme:Playbook", "Playbook oluşturuluyor...", 1.5),
            ("iyilestirme:Otomasyon", "Otomasyon ekleniyor...", 1.5),
        ],
        "10D": [
            ("zeroday:Fuzzing", "Fuzzing başlatılıyor...", 2.0),
            ("zeroday:Crash Analizi", "Crash analiz ediliyor...", 2.0),
            ("zeroday:Root Cause", "Kök neden araştırması...", 2.5),
            ("zeroday:Exploit Geliştir", "Exploit geliştiriliyor...", 3.0),
        ],
        "10E": [
            ("kriz:Enerji:Kaynak Takviye", "Enerji sektörüne kaynak...", 1.5),
            ("kriz:Sağlık:CERT Aktivasyonu", "Sağlık sektörüne CERT...", 1.5),
            ("kriz:Finans:Kamuoyu Bilgilendirme", "Finans bilgilendirme...", 1.0),
            ("kriz:Telekom:Uluslararası İşbirliği", "Telekom işbirliği...", 1.5),
            ("kriz:Ulaştırma:Kaynak Takviye", "Ulaştırma kaynak...", 1.5),
        ],
    }
    
    return pilot_steps.get(scenario_id, [
        ("bilinmiyor", "Bu senaryo için otomatik pilot hazırlanıyor...", 2.0)
    ])


def render_auto_pilot_button(scenario_id, state_key):
    """Otomatik pilot butonunu ve ilerleme adımlarını render eder"""
    st.markdown("---")
    st.subheader("🤖 OTOMATİK PİLOT")
    
    pilot_key = f"auto_pilot_{scenario_id}"
    if pilot_key not in st.session_state:
        st.session_state[pilot_key] = {
            'running': False,
            'current_step': 0,
            'steps': [],
            'completed': False
        }
    
    pilot_state = st.session_state[pilot_key]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if not pilot_state['running'] and not pilot_state['completed']:
            if st.button("🚀 Otomatik Pilot Başlat", use_container_width=True, key=f"ap_start_{scenario_id}"):
                pilot_state['running'] = True
                pilot_state['current_step'] = 0
                pilot_state['completed'] = False
                pilot_state['steps'] = get_auto_pilot_steps(scenario_id)
                st.session_state[pilot_key] = pilot_state
                st.rerun()
        elif pilot_state['running']:
            if st.button("⏹️ Durdur", use_container_width=True, key=f"ap_stop_{scenario_id}"):
                pilot_state['running'] = False
                st.session_state[pilot_key] = pilot_state
                st.rerun()
        elif pilot_state['completed']:
            if st.button("🔄 Tekrar Başlat", use_container_width=True, key=f"ap_restart_{scenario_id}"):
                pilot_state['running'] = True
                pilot_state['current_step'] = 0
                pilot_state['completed'] = False
                pilot_state['steps'] = get_auto_pilot_steps(scenario_id)
                st.session_state[pilot_key] = pilot_state
                st.rerun()
    
    with col2:
        if pilot_state['running'] and pilot_state['current_step'] < len(pilot_state['steps']):
            step_cmd, step_desc, step_delay = pilot_state['steps'][pilot_state['current_step']]
            
            progress = pilot_state['current_step'] / len(pilot_state['steps'])
            st.progress(progress, text=f"İlerleme: {pilot_state['current_step']}/{len(pilot_state['steps'])}")
            st.info(f"🔄 **Adım {pilot_state['current_step']+1}/{len(pilot_state['steps'])}:** {step_desc}")
            
            with st.expander("📋 Tüm Adımlar", expanded=False):
                for i, (cmd, desc, delay) in enumerate(pilot_state['steps']):
                    if i < pilot_state['current_step']:
                        st.write(f"✅ Adım {i+1}: {desc}")
                    elif i == pilot_state['current_step']:
                        st.write(f"🔄 **Adım {i+1}: {desc}** (Çalışıyor...)")
                    else:
                        st.write(f"⏳ Adım {i+1}: {desc}")
            
            time.sleep(step_delay)
            pilot_state['current_step'] += 1
            st.session_state[pilot_key] = pilot_state
            
            if pilot_state['current_step'] >= len(pilot_state['steps']):
                pilot_state['running'] = False
                pilot_state['completed'] = True
                st.session_state[pilot_key] = pilot_state
                st.success("✅ Otomatik pilot tamamlandı!")
                st.balloons()
            
            st.rerun()
        
        elif pilot_state['completed']:
            st.success(f"✅ **Görev Tamamlandı!** {len(pilot_state['steps'])} adım başarıyla uygulandı.")
            with st.expander("📋 Tamamlanan Adımlar", expanded=False):
                for i, (cmd, desc, delay) in enumerate(pilot_state['steps']):
                    st.write(f"✅ Adım {i+1}: {desc}")
        
        elif not pilot_state['running']:
            st.info("👆 Otomatik pilotu başlatmak için butona tıklayın.")
            if pilot_state['steps']:
                with st.expander("📋 Planlanan Adımlar", expanded=False):
                    for i, (cmd, desc, delay) in enumerate(pilot_state['steps']):
                        st.write(f"⏳ Adım {i+1}: {desc}")


# ============================================
# BÖLÜM 8: PERFORMANS KARŞILAŞTIRMA GRAFİĞİ
# ============================================

def render_performance_comparison(scenario_id):
    """Kullanıcı vs Otopilot vs İdeal performans karşılaştırması"""
    state_key = f"s{scenario_id}"
    user_data = st.session_state.get(state_key, {})
    
    pilot_steps = get_auto_pilot_steps(scenario_id)
    pilot_optimal_steps = len(pilot_steps)
    
    user_attempts = user_data.get('attempts', 0) if isinstance(user_data, dict) else 0
    user_risk = user_data.get('risk', 0) if isinstance(user_data, dict) else 0
    
    ideal_steps = pilot_optimal_steps
    ideal_risk = 10
    
    categories = ['Adım Sayısı', 'Risk Yönetimi', 'Hız', 'Başarı Oranı']
    
    user_values = [
        min(100, max(0, 100 - (abs(user_attempts - ideal_steps) * 10))),
        min(100, max(0, 100 - user_risk)),
        min(100, max(0, 80 if user_attempts <= ideal_steps else 50)),
        min(100, max(0, 85 if user_attempts > 0 else 0)),
    ]
    
    pilot_values = [70, 90, 60, 95]
    ideal_values = [100, 100, 100, 100]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Sizin Performansınız',
        x=categories,
        y=user_values,
        marker_color='#00ff41',
        marker_line=dict(color='#00cc33', width=1.5),
        opacity=0.8,
        text=[f'%{v}' for v in user_values],
        textposition='outside',
        textfont=dict(color='#00ff41', size=10)
    ))
    
    fig.add_trace(go.Bar(
        name='Otopilot',
        x=categories,
        y=pilot_values,
        marker_color='#4f8bc9',
        marker_line=dict(color='#3d7ab5', width=1.5),
        opacity=0.6,
        text=[f'%{v}' for v in pilot_values],
        textposition='outside',
        textfont=dict(color='#4f8bc9', size=10)
    ))
    
    fig.add_trace(go.Bar(
        name='İdeal',
        x=categories,
        y=ideal_values,
        marker_color='#ffaa00',
        marker_line=dict(color='#ff8800', width=1.5),
        opacity=0.3,
        text=[f'%{v}' for v in ideal_values],
        textposition='outside',
        textfont=dict(color='#ffaa00', size=10)
    ))
    
    fig.update_layout(
        title=dict(
            text='📈 PERFORMANS KARŞILAŞTIRMASI',
            font=dict(size=14, color='#e0e0e0'),
            x=0.5
        ),
        barmode='group',
        bargap=0.25,
        bargroupgap=0.1,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e0e0',
        height=300,
        margin=dict(t=40, b=10, l=10, r=10),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=10, color='#e0e0e0')
        ),
        xaxis=dict(showgrid=False, color='#e0e0e0', tickfont=dict(size=10)),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.08)',
            color='#888888',
            range=[0, 120],
            tickfont=dict(size=9)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with st.expander("📖 PERFORMANS KARŞILAŞTIRMASI NEDİR?", expanded=False):
        st.markdown("""
        <div style="font-size:0.85rem;line-height:1.7;color:#d0d8e0;text-align:justify;">
        
        <b>Performans karşılaştırma grafiği</b>, siber güvenlik eğitiminde ölçülebilir 
        ilerlemenin temel taşıdır. Bu grafik, kullanıcının her senaryodaki performansını 
        üç farklı referans noktasıyla karşılaştırır: kullanıcının kendi skoru, otopilotun 
        performansı ve ulaşılması gereken ideal değerler. Bu üçlü karşılaştırma, öğrenme 
        sürecinin neresinde olduğunuzu net bir şekilde görmenizi sağlar.
        
        <b>Adım Sayısı metriği</b>, görevi tamamlamak için kaç hamle yaptığınızı ölçer. 
        İdeal senaryoda minimum adımla hedefe ulaşmak esastır; çünkü gerçek dünyada her 
        fazla hamle, tespit edilme riskini artırır.
        
        <b>Risk Yönetimi</b>, operasyonel güvenliğin sayısal karşılığıdır. Düşük risk 
        skoru, güvenli ilerleme anlamına gelir. Yüksek risk skoru ise yakalanma tehlikesini 
        gösterir. Profesyonel bir siber güvenlik uzmanı, riski sürekli olarak kabul 
        edilebilir seviyede tutabilmelidir.
        
        <b>Hız metriği</b>, görevi ne kadar sürede tamamladığınızı değerlendirir. Ancak 
        hız, asla güvenlik ve doğruluğun önüne geçmemelidir.
        
        <b>Başarı Oranı</b>, tüm bu metriklerin birleşik bir göstergesidir. Hedefe ulaşıp 
        ulaşmadığınızı, bunu yaparken ne kadar temiz çalıştığınızı ve operasyonel güvenliği 
        ne ölçüde koruduğunuzu yansıtır. Zaman içinde bu dört metrikteki gelişiminizi takip 
        ederek, hangi alanlarda güçlü olduğunuzu somut verilerle görebilirsiniz.
        </div>
        """, unsafe_allow_html=True)


# ============================================
# BÖLÜM 9: GELİŞMİŞ GÖRSELLEŞTİRME FONKSİYONLARI
# ============================================

def render_attack_heatmap(scenario_id):
    """Zaman içinde saldırı yoğunluğunu ısı haritası olarak gösterir"""
    target_systems = [
        'Web Sunucusu', 'Veritabanı', 'DNS', 'E-posta', 'Dosya Sunucusu',
        'AD Controller', 'VPN Gateway', 'Load Balancer', 'API Gateway', 'Backup Server'
    ]
    
    time_slots = [f'{h:02d}:00' for h in range(0, 24, 2)]
    
    scenario_num = int(scenario_id[0]) if scenario_id[0].isdigit() else 1
    np.random.seed(scenario_num * 42)
    
    if scenario_num <= 3:
        base = np.random.randint(5, 30, size=(len(target_systems), len(time_slots)))
        for i in range(len(target_systems)):
            for j in range(len(time_slots)):
                if 8 <= j * 2 <= 18:
                    base[i][j] += np.random.randint(10, 30)
    elif scenario_num <= 6:
        base = np.random.randint(15, 60, size=(len(target_systems), len(time_slots)))
        for i in range(len(target_systems)):
            wave = np.sin(np.linspace(0, 3*np.pi, len(time_slots))) * 20
            base[i] = base[i] + wave.astype(int)
    else:
        base = np.random.randint(30, 95, size=(len(target_systems), len(time_slots)))
        for i in range(len(target_systems)):
            spike_positions = np.random.choice(len(time_slots), 3, replace=False)
            for pos in spike_positions:
                base[i][pos] = 100
    
    intensity_data = np.clip(base, 0, 100)
    
    fig = go.Figure(data=go.Heatmap(
        z=intensity_data,
        x=time_slots,
        y=target_systems,
        colorscale=[
            [0.0, '#0a1628'], [0.15, '#1a3350'], [0.3, '#4f8bc9'],
            [0.5, '#ffaa00'], [0.7, '#ff6b35'], [0.85, '#ff4444'],
            [1.0, '#cc0000'],
        ],
        colorbar=dict(
            title=dict(text='Yoğunluk %', font=dict(color='#e0e0e0', size=10)),
            tickfont=dict(color='#e0e0e0', size=9),
            thickness=10,
            len=0.8
        ),
        hovertemplate='<b>%{y}</b><br>Saat: %{x}<br>Yoğunluk: %{z}%%<extra></extra>',
        xgap=2,
        ygap=2
    ))
    
    fig.update_layout(
        title=dict(
            text='🔥 SİMÜLASYON YOĞUNLUK ISI HARİTASI (24 Saat)',
            font=dict(size=14, color='#e0e0e0'),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=380,
        margin=dict(t=40, b=10, l=10, r=10),
        xaxis=dict(title='Saat Dilimi', showgrid=False, color='#e0e0e0', tickfont=dict(size=9)),
        yaxis=dict(title='Hedef Sistem', showgrid=False, color='#e0e0e0', 
                   tickfont=dict(size=9), autorange='reversed')
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with st.expander("📖 ISI HARİTASI NEDİR?", expanded=False):
        st.markdown("""
        <div style="font-size:0.85rem;line-height:1.7;color:#d0d8e0;text-align:justify;">
        
        <b>Saldırı Yoğunluk Isı Haritası</b>, siber güvenlik operasyon merkezlerinde 
        kullanılan en güçlü analitik görselleştirme araçlarından biridir. Bu grafik, 
        birden fazla hedef sistem üzerindeki aktivite yoğunluğunu zamana bağlı olarak 
        renk kodlamasıyla gösterir.
        
        <b>Zamansal desen analizi</b>, bu görselleştirmenin en değerli kullanım alanıdır. 
        Isı haritası sayesinde, aktivitelerin günün hangi saatlerinde yoğunlaştığı, hangi 
        sistemlerin daha sık hedef alındığı ve dalgaların nasıl yayıldığı anında tespit 
        edilebilir. Örneğin, çalışma saatlerinde web sunucusuna yönelik artış, meşru trafik 
        içine gizlenme çabasını gösterebilir.
        
        <b>Renk skalası</b>, yoğunluğun sezgisel olarak anlaşılmasını sağlar. Koyu 
        lacivertten kırmızıya doğru ilerleyen geçiş, düşük, orta, yüksek ve kritik 
        seviyeleri net bir şekilde ayırır.
        
        <b>Kapasite planlaması</b> açısından da ısı haritası kritik öneme sahiptir. 
        Hangi sistemlerin hangi saatlerde daha fazla aktivite altında olduğunu bilmek, 
        güvenlik personelinin vardiya planlamasından otomatik ölçeklendirme politikalarına 
        kadar birçok operasyonel kararı doğrudan etkiler.
        </div>
        """, unsafe_allow_html=True)


def render_attack_vector_distribution(scenario_id):
    """Kullanılan vektörlerin donut grafik ile dağılımını gösterir"""
    scenario_num = int(scenario_id[0]) if scenario_id[0].isdigit() else 1
    
    if scenario_num <= 2:
        vectors = {'Port Tarama': 35, 'Paket Gönderme': 25, 'SSH Denemesi': 10,
                   'HTTP Testi': 15, 'DNS Sorgulama': 15}
        colors = ['#4f8bc9', '#5a9ed4', '#ff6b35', '#ff4444', '#ffaa00']
    elif scenario_num <= 4:
        vectors = {'HTTP Flood': 25, 'SYN Flood': 20, 'UDP Flood': 15,
                   'DNS Amp': 15, 'Slowloris': 10, 'Diğer': 15}
        colors = ['#ff4444', '#ff6b35', '#ffaa00', '#ffd700', '#4f8bc9', '#888888']
    elif scenario_num <= 6:
        vectors = {'OSINT Keşif': 20, 'Spear-Phishing': 18, 'SQL Injection': 15,
                   'Yetki Yükseltme': 12, 'Yanal Hareket': 15, 'Veri Sızdırma': 10,
                   'Diğer': 10}
        colors = ['#4f8bc9', '#ffaa00', '#ff4444', '#ff6b35', '#c77dff', '#00bfa5', '#888888']
    elif scenario_num <= 8:
        vectors = {'Tersine Müh.': 22, 'Malware Analizi': 18, 'Kod Enjeksiyonu': 16,
                   'Kernel Exploit': 14, 'Firmware Mod': 12, 'Rootkit': 10, 'Diğer': 8}
        colors = ['#ff4444', '#ff6b35', '#c77dff', '#ffaa00', '#00b4d8', '#ff0000', '#888888']
    else:
        vectors = {'Sosyal Müh.': 25, 'Phishing': 20, 'Fiziksel Simülasyon': 15,
                   'Zero-Day': 12, 'APT Operasyonu': 18, 'Diğer': 10}
        colors = ['#ffaa00', '#ff6b35', '#ff4444', '#ff0000', '#c77dff', '#888888']
    
    fig = go.Figure(data=go.Pie(
        labels=list(vectors.keys()),
        values=list(vectors.values()),
        hole=0.45,
        marker=dict(colors=colors, line=dict(color='rgba(0,0,0,0.5)', width=1.5)),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=10, color='#e0e0e0'),
        hovertemplate='<b>%{label}</b><br>Oran: %{percent}<extra></extra>',
        pull=[0.05] * len(vectors),
        sort=False
    ))
    
    fig.add_annotation(
        text='<b>Toplam<br>Vektör</b>',
        x=0.5, y=0.5,
        font=dict(size=14, color='#e0e0e0'),
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text='📊 TEKNİK DAĞILIMI',
            font=dict(size=14, color='#e0e0e0'),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=380,
        margin=dict(t=40, b=10, l=30, r=30),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(size=9, color='#e0e0e0')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with st.expander("📖 TEKNİK DAĞILIMI NEDİR?", expanded=False):
        st.markdown("""
        <div style="font-size:0.85rem;line-height:1.7;color:#d0d8e0;text-align:justify;">
        
        <b>Teknik Dağılımı</b>, bir senaryoda kullanılan farklı tekniklerin oransal 
        dağılımını gösterir. Bu donut grafik, hangi tekniklerin baskın olduğunu, 
        hangilerinin daha az kullanıldığını ve genel stratejinin profilini ortaya koyar.
        
        <b>Renk kodlaması</b>, her tekniğin risk seviyesiyle ilişkilendirilmiştir. 
        Kırmızı ve turuncu tonları yüksek riskli, doğrudan sisteme zarar verebilecek 
        teknikleri; mavi tonları keşif ve bilgi toplama amaçlı düşük profilli teknikleri; 
        mor ve yeşil tonları ise özel yetenek gerektiren ileri seviye teknikleri temsil eder.
        
        <b>Seviye bazlı dağılım farklılıkları</b>, öğrenme yolculuğunun doğal bir 
        yansımasıdır. Başlangıç seviyesinde port tarama ve temel testler baskınken, 
        ileri seviyelerde tersine mühendislik, zero-day araştırması ve APT operasyonları 
        gibi en karmaşık teknikler öne çıkar.
        
        <b>Savunma stratejisi optimizasyonu</b> için bu dağılım hayati önem taşır. 
        Hangi tekniklerin daha sık kullanıldığını bilmek, savunma kaynaklarının 
        önceliklendirilmesini sağlar.
        </div>
        """, unsafe_allow_html=True)


def render_world_attack_map(scenario_id):
    """Dünya haritası üzerinde kaynak ve hedefleri gösterir"""
    attack_sources = [
        {"lat": 55.7558, "lon": 37.6173, "city": "Moskova", "intensity": 85},
        {"lat": 39.9042, "lon": 116.4074, "city": "Pekin", "intensity": 70},
        {"lat": 37.5665, "lon": 126.9780, "city": "Seul", "intensity": 45},
        {"lat": 35.6762, "lon": 139.6503, "city": "Tokyo", "intensity": 30},
        {"lat": 1.3521, "lon": 103.8198, "city": "Singapur", "intensity": 55},
        {"lat": 52.3676, "lon": 4.9041, "city": "Amsterdam", "intensity": 40},
        {"lat": 40.7128, "lon": -74.0060, "city": "New York", "intensity": 50},
        {"lat": -23.5505, "lon": -46.6333, "city": "São Paulo", "intensity": 35},
    ]
    
    targets = [
        {"lat": 41.0082, "lon": 28.9784, "city": "İstanbul"},
        {"lat": 39.9334, "lon": 32.8597, "city": "Ankara"},
        {"lat": 51.5074, "lon": -0.1278, "city": "Londra"},
        {"lat": 48.8566, "lon": 2.3522, "city": "Paris"},
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scattergeo(
        lon=[t['lon'] for t in targets],
        lat=[t['lat'] for t in targets],
        text=[f"{t['city']}<br>🔵 HEDEF" for t in targets],
        mode='markers',
        marker=dict(size=12, color='#00b4d8', line=dict(width=2, color='#fff')),
        name='Hedefler',
        hoverinfo='text'
    ))
    
    fig.add_trace(go.Scattergeo(
        lon=[s['lon'] for s in attack_sources],
        lat=[s['lat'] for s in attack_sources],
        text=[f"{s['city']}<br>Yoğunluk: %{s['intensity']}" for s in attack_sources],
        mode='markers',
        marker=dict(
            size=[s['intensity'] * 0.3 for s in attack_sources],
            color='#ff4444',
            line=dict(width=1.5, color='#ff8888'),
            symbol='triangle-up'
        ),
        name='Kaynaklar',
        hoverinfo='text'
    ))
    
    for source in attack_sources[:4]:
        fig.add_trace(go.Scattergeo(
            lon=[source['lon'], targets[0]['lon']],
            lat=[source['lat'], targets[0]['lat']],
            mode='lines',
            line=dict(
                width=source['intensity'] * 0.015,
                color=f'rgba(255,68,68,{source["intensity"]/200})'
            ),
            opacity=0.5,
            showlegend=False,
            hoverinfo='none'
        ))
    
    fig.update_layout(
        title=dict(
            text='🌍 SİMÜLASYON COĞRAFİ HARİTASI',
            font=dict(size=14, color='#e0e0e0'),
            x=0.5
        ),
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='#1a2332',
            coastlinecolor='#2d4a6e',
            countrycolor='#2d4a6e',
            lakecolor='#0a1628',
            oceancolor='#0a1628',
            bgcolor='rgba(0,0,0,0)',
            showcountries=True,
            showocean=True,
            showlakes=True,
            resolution=50
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(t=40, b=10, l=10, r=10),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.05,
            xanchor='center',
            x=0.5,
            font=dict(size=10, color='#e0e0e0')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with st.expander("📖 COĞRAFİ HARİTA NEDİR?", expanded=False):
        st.markdown("""
        <div style="font-size:0.85rem;line-height:1.7;color:#d0d8e0;text-align:justify;">
        
        <b>Coğrafi Siber Simülasyon Haritası</b>, siber tehditlerin coğrafi boyutunu 
        görselleştiren, durumsal farkındalık aracıdır. Bu harita, dünya üzerindeki 
        kaynakları kırmızı üçgenler ile, hedef sistemleri ise mavi daireler ile gösterir. 
        Noktalar arasındaki çizgiler, simülasyon trafiğinin akış yönünü ve yoğunluğunu 
        temsil eder.
        
        <b>Coğrafi tehdit istihbaratı</b>, modern siber güvenlik operasyonlarının 
        vazgeçilmez bir bileşenidir. Aktivitelerin hangi ülkelerden kaynaklandığını 
        bilmek, savunma stratejilerinin şekillendirilmesinde kritik rol oynar. Belirli 
        bir ülkeden gelen aktivitelerde ani bir artış tespit edilirse, o bölgeden gelen 
        tüm trafiğe geçici olarak daha sıkı filtreleme uygulanabilir.
        
        <b>Yoğunluk göstergeleri</b>, her kaynağın aktiflik seviyesini yüzde olarak 
        gösterir. Yüksek yoğunluklu kaynaklar, büyük ölçekli aktiviteleri temsil ederken; 
        düşük yoğunluklu kaynaklar, bireysel veya düşük profilli aktiviteleri gösterir. 
        Bu görselleştirme, analistlerin önceliklendirmesine yardımcı olur.
        </div>
        """, unsafe_allow_html=True)


# ============================================
# BÖLÜM 10: SENARYO TANIMLARI (ALL_SCENARIOS)
# ============================================
# İlk 15 senaryo bu mesajda, kalan 50 senaryo Part 2'de eklenecek

ALL_SCENARIOS = {}

# --- SEVİYE 1: VERİ BAHÇESİ ---

ALL_SCENARIOS["1A"] = {
    "title": "1A: Paket Avcısı - Temel Ağ Keşfi",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Savunma AI",
    "type": "human_attack",
    "desc": """
Bu senaryo, siber güvenliğin temel yapı taşlarını öğretmek için tasarlanmış bir 
başlangıç simülasyonudur. Kırmızı takım analisti olarak, yerel bir kurumun iç 
ağında savunma testleri yapıyorsunuz. Amaç, savunma ekibinin hangi noktalarda 
zayıf olduğunu tespit etmek ve önerilerde bulunmaktır. Ağ topolojisi kasıtlı 
olarak basit tutulmuştur: analist bilgisayarınız, bir güvenlik duvarı cihazı ve 
hedef sunucu olmak üzere üç ana bileşenden oluşur. Sunucu üzerinde üç farklı 
port açıktır: 22 numaralı SSH portu uzaktan yönetim için, 80 numaralı HTTP 
portu web hizmetleri için ve 3306 numaralı MySQL portu veritabanı bağlantıları 
için kullanılmaktadır. Her bir port, ağ topolojisi görselleştirmesinde farklı 
bir kapı metaforu ile temsil edilir. Terminal komut satırı üzerinden 'tara' 
komutu ile ağdaki cihazları ve açık portları keşfedebilir, 'gonder' komutu ile 
belirli bir porta özel test paketleri gönderebilirsiniz. Güvenlik duvarı, 
belirli kurallar dahilinde çalışan bir yapay zeka tarafından yönetilmektedir. 
Eğer SSH portuna çok sayıda başarısız deneme yaparsanız, AI savunmacı bu 
anormal trafiği tespit ederek IP adresinizi otomatik olarak kara listeye alır. 
Bu nedenle test stratejinizi dikkatli planlamalı, önce keşif yapmalı ve 
savunma mekanizmalarını zorlamadan hedefe ulaşmalısınız. Bu senaryo sonunda, 
savunma perspektifinden port tarama tespitinin nasıl çalıştığını, IDS/IPS 
sistemlerinin hangi sinyalleri izlediğini ve savunma ekibinin hangi noktalara 
dikkat etmesi gerektiğini öğreneceksiniz.
"""
}

ALL_SCENARIOS["1B"] = {
    "title": "1B: Duvarın Bekçisi - Güvenlik Duvarı Yönetimi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Simülasyon AI",
    "type": "human_defend",
    "desc": """
Bu senaryoda bir ağ güvenlik yöneticisi olarak görev yapıyorsunuz. Kurumunuzun 
kritik altyapısını korumakla görevlisiniz ve karşınızda sürekli olarak yeni 
test vektörleri deneyen, adaptif bir yapay zeka simülasyonu bulunuyor. Bu AI, 
rastgele IP adresleri kullanarak ağınızdaki çeşitli portlara sürekli tarama ve 
test girişimlerinde bulunur. Elinizde dinamik bir güvenlik duvarı yönetim paneli, 
anlık trafik izleme araçları ve olay logları bulunmaktadır. Göreviniz, gelen 
test trafiğini tespit etmek, şüpheli IP adreslerini engellemek ve aynı zamanda 
meşru kullanıcıların hizmetlere erişimini kesintisiz sürdürmektir. Bu dengeyi 
sağlamak hiç de kolay değildir; çünkü AI simülasyonu zaman zaman meşru kullanıcı 
davranışını taklit ederek sizi yanıltmaya çalışır. Yanlışlıkla gerçek bir 
müşterinin IP adresini engellerseniz, kurumun itibarı ve iş sürekliliği puanınız 
düşer. Ekranınızda canlı bir ağ topolojisi haritası, port bazlı trafik analizi 
ısı haritası ve güvenlik duvarı kural yönetim arayüzü bulunur. Başarı puanınız, 
engellenen test sayısı, yanlış pozitif oranı ve hizmet kesintisi süresine göre 
hesaplanır. Bu senaryo sonunda, güvenlik duvarı yönetiminin inceliklerini, 
katmanlı savunma stratejilerini ve yanlış pozitif yönetimini öğreneceksiniz.
"""
}

ALL_SCENARIOS["1C"] = {
    "title": "1C: Bal Küpü Analizi - Honeypot Değerlendirmesi",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Aldatma Tabanlı Savunma AI",
    "type": "human_attack",
    "desc": """
Bu ileri seviye başlangıç senaryosu, sizi aldatma teknolojilerinin karmaşık 
dünyasına götürüyor. Ortamda iki adet web sunucusu bulunmaktadır; bunlardan 
biri gerçek üretim sunucusu, diğeri ise saldırganları tuzağa düşürmek için 
özel olarak yapılandırılmış bir bal küpüdür (honeypot). Kırmızı takım analisti 
olarak, savunma ekibinin honeypot sistemini ne kadar etkili kullandığını 
değerlendiriyorsunuz. Her iki sunucu da neredeyse birbirinin aynısı gibi 
görünür; aynı banner bilgilerini döndürür, aynı portları dinler ve benzer 
hizmetleri çalıştırır. Ancak bal küpüne yapacağınız herhangi bir test girişimi, 
anında AI savunmacı tarafından tespit edilmenize ve IP adresinizin kalıcı 
olarak engellenmesine yol açar. Göreviniz, gelişmiş keşif teknikleri 
kullanarak hangi sunucunun gerçek hedef olduğunu belirlemektir. 'detayli_tara' 
komutu ile servis versiyonlama bilgilerini toplayabilir, 'servis_kontrol' ile 
HTTP yanıt başlıklarındaki ince farklılıkları analiz edebilirsiniz. Gerçek 
sunucu, belirli bir HTTP yanıt başlığında küçük bir ipucu barındırır; bu 
ipucunu yakalamak için dikkatli bir pasif keşif yapmanız gerekir. Bu senaryo, 
aldatma teknolojilerinin savunmadaki rolünü, honeypot yönetimini ve kurumsal 
güvenlik mimarisinde deception'ın nasıl kullanıldığını öğretir.
"""
}

ALL_SCENARIOS["1D"] = {
    "title": "1D: İç Sızıntı - Veri Kaybı Önleme",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "İç Tehdit Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryoda bir güvenlik operasyon merkezi (SOC) analisti olarak görev 
yapıyorsunuz. Şirket içi bir kullanıcının bilgisayarı, farkında olmadan bir 
zararlı yazılım tarafından ele geçirilmiş durumda. Yapay zeka kontrollü bu 
zararlı yazılım, hassas kurumsal verileri toplayarak dışarıya sızdırmaya 
çalışıyor. Sizin göreviniz, ağ izleme konsolundaki anormal trafik desenlerini 
analiz ederek veri sızıntısını tespit etmek, kaynağını bulmak ve sızıntıyı 
durdurmaktır. AI simülasyonu, verileri sızdırmak için DNS tünelleme tekniğini 
kullanır; bu teknik, normal DNS sorgularının içine gizlenmiş veri paketlerinin 
dışarı gönderilmesi esasına dayanır. Bu nedenle sıradan güvenlik önlemleri bu 
aktiviteyi tespit edemez. Şüpheli DNS sorgularını incelemeli, anormal derecede 
uzun alan adı sorgularını tespit etmeli ve sızan verinin hangi sunucuya 
gittiğini belirlemelisiniz. Doğru tespit yaptığınızda, enfekte bilgisayarı 
ağdan izole edebilir, zararlı yazılımı temizleyebilir ve sızan verileri geri 
çekebilirsiniz. Yanlış alarm verirseniz üretim sistemleri etkilenir ve şirket 
operasyonları aksar. Bu senaryo, iç tehditlerin tespiti, veri kaybı önleme 
sistemlerinin çalışma prensipleri, DNS güvenliği ve olay müdahale süreçleri 
konularında derinlemesine bilgi sağlar.
"""
}

ALL_SCENARIOS["1E"] = {
    "title": "1E: Kablosuz Gölgeler - Wi-Fi Güvenlik Değerlendirmesi",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Kablosuz IDS AI",
    "type": "human_attack",
    "desc": """
Kablosuz ağ güvenliğinin temellerini öğreten bu senaryoda, bir kafenin Wi-Fi 
ağının güvenlik değerlendirmesini yapan bir kırmızı takım analisti rolündesiniz. 
Ortamda kafenin misafir ağına bağlı çeşitli cihazlar bulunur: müşterilerin 
akıllı telefonları, dizüstü bilgisayarları ve kafenin kendi POS terminali. 
AI savunmacı, kablosuz ağdaki anormal aktiviteleri sürekli izleyen bir 
kablosuz saldırı tespit sistemi (WIDS) olarak görev yapar. Amacınız, ağdaki 
bir müşterinin oturum güvenliğini değerlendirmek ve savunma ekibine zayıf 
noktalar hakkında rapor sunmaktır. Paket dinleme, MAC adresi analizi ve 
deauthentication testleri gibi teknikleri kullanabilirsiniz. Görsel arayüzde 
Wi-Fi sinyal gücü göstergesi, şifreleme türü seçenekleri ve bağlı cihazların 
listesi bulunur. AI savunmacı, normal kablosuz trafik desenini öğrenmiştir; 
eğer çok agresif test yaparsanız anında tespit edilirsiniz. Daha sofistike 
bir yaklaşım benimsemeli, düşük güçte pasif dinleme yapmalı ve savunma 
sistemlerinin nasıl çalıştığını gözlemlemelisiniz. Bu senaryo, kablosuz ağ 
protokollerinin güvenlik açıklarını, kablosuz ağ savunma stratejilerini ve 
WIDS sistemlerinin çalışma prensiplerini öğretir.
"""
}

# --- SEVİYE 2: DİJİTAL KALE ---

ALL_SCENARIOS["2A"] = {
    "title": "2A: Gölge Tarama - IDS Değerlendirmesi",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "İmza ve Davranış Tabanlı IDS AI",
    "type": "human_attack",
    "desc": """
Bu senaryo, saldırı tespit sistemlerinin (IDS) etkinliğini değerlendirme 
sanatının inceliklerini öğretmek üzere tasarlanmıştır. Karşınızda hem imza 
tabanlı hem de davranışsal analiz yapabilen gelişmiş bir yapay zeka IDS 
bulunmaktadır. Kırmızı takım analisti olarak, bu çift katmanlı savunmanın 
hangi noktalarda zayıf olduğunu tespit etmeye çalışıyorsunuz. IDS, bilinen 
aktivite imzalarını anında tespit edebilir. Ancak siz, 'gizli_tara' komutunu 
kullanarak tarama paketlerini rastgele zaman aralıklarıyla gönderebilir, 
böylece imza tabanlı tespitten kaçınabilirsiniz. Davranışsal analiz katmanı 
ise normal kullanıcı davranışını öğrenmiştir; bu nedenle test öncesinde bir 
süre normal bir kullanıcı gibi web sitesinde gezinmelisiniz. Hedef sistemdeki 
web uygulamasında test edilecek zafiyetler bulunur; bu zafiyetleri düşük 
gürültü seviyesinde test etmeniz gerekir. Otomatik araçlar kullanmanız 
durumunda anında tespit edilirsiniz. Tespit risk seviyeniz, ekranın sağ üst 
köşesindeki gösterge çizelgesinde canlı olarak takip edilir. Bu senaryo, IDS 
sistemlerinin çalışma prensiplerini, imza ve davranış analizi arasındaki 
farkı, IDS değerlendirme metodolojilerini ve savunma ekibine nasıl rapor 
sunulacağını öğretir.
"""
}

ALL_SCENARIOS["2B"] = {
    "title": "2B: IDS Komuta Merkezi - SOC Operasyonları",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Çok Vektörlü Simülasyon AI",
    "type": "human_defend",
    "desc": """
Güvenlik operasyon merkezinde bir vardiya amiri olarak görev yaptığınız bu 
senaryoda, kurum ağına yönelik çok vektörlü bir siber aktiviteyi yönetmekle 
sorumlusunuz. Yapay zeka kontrollü simülasyon, eş zamanlı olarak birden fazla 
vektörü kullanır: dışarıdan web uygulamasına SQL enjeksiyonu denemeleri, 
içeriden ele geçirilmiş bir bilgisayardan yanal hareket girişimleri ve e-posta 
yoluyla gelen oltalama simülasyonları. Elinizde birleştirilmiş bir SIEM 
konsolu, IDS/IPS yönetim paneli, güvenlik duvarı kural yazma arayüzü ve olay 
müdahale iş akışı yönetim araçları bulunur. Ekranınızda canlı aktivite haritası, 
olay önceliklendirme kuyruğu ve sistem durum göstergeleri yer alır. Göreviniz, 
gelen yüzlerce uyarı arasından gerçek tehditleri ayıklamak, yanlış pozitifleri 
filtrelemek ve kritik olaylara hızlı müdahale etmektir. AI simülasyonu, 
dikkatinizi dağıtmak için sahte aktiviteler düzenlerken asıl olayı sessizce 
gerçekleştirir. Yanlış bir müdahale iş sürekliliğini etkiler ve şirkete mali 
kayıp yaşatır. Başarı puanınız; tespit süresi, müdahale hızı, yanlış pozitif 
oranı ve kurtarılan sistem sayısına göre hesaplanır. Bu senaryo, SOC 
operasyonlarının inceliklerini, olay önceliklendirmeyi ve kriz anında karar 
vermeyi öğretir.
"""
}

ALL_SCENARIOS["2C"] = {
    "title": "2C: WAF Değerlendirmesi - Web Güvenlik Duvarı Testi",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Web Uygulama Güvenlik Duvarı AI",
    "type": "human_attack",
    "desc": """
Modern web uygulamalarının korunmasında kritik rol oynayan Web Uygulama 
Güvenlik Duvarları (WAF), bu senaryonun ana odağıdır. Siz bir sızma test 
uzmanı olarak, WAF koruması altındaki bir e-ticaret platformunun güvenlik 
değerlendirmesini yapıyorsunuz. Hedefiniz, platformun savunma katmanlarının 
hangi noktalarda zayıf olduğunu tespit etmektir. AI kontrollü WAF, gelen 
tüm HTTP isteklerini analiz eder ve SQL enjeksiyonu, XSS, komut enjeksiyonu 
gibi yaygın web saldırılarını engeller. Ancak WAF'lar her zaman mükemmel 
değildir; kör SQL enjeksiyonu, zaman tabanlı sorgular, HTTP parametre 
kirliliği ve kodlama hileleri gibi ileri tekniklerle test edilebilirler. 
Terminalinizde özel olarak hazırlanmış HTTP istekleri gönderebilir, yanıtları 
analiz edebilir ve WAF'ın davranışını test edebilirsiniz. Ayrıca platformun 
robots.txt dosyası, yedek dosyaları ve hata sayfaları gibi bilgi 
sızdırabilecek noktaları keşfedebilirsiniz. AI WAF, şüpheli istekleri tespit 
ettiğinde CAPTCHA doğrulaması başlatır veya geçici olarak IP'nizi engeller. 
Bu nedenle test hızınızı ve deseninizi dikkatli ayarlamalısınız. Görsel 
arayüzde, WAF'ın engellediği isteklerin sayısı ve türü bir pasta grafiği ile 
gösterilir. Bu senaryo, modern web güvenliği önlemlerini, WAF'ların 
çalışma prensiplerini ve güvenli kod geliştirme prensiplerini öğretir.
"""
}

ALL_SCENARIOS["2D"] = {
    "title": "2D: Oltalama Savunması - Sosyal Mühendislik Tespiti",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Adaptif Oltalama Simülasyonu",
    "type": "human_defend",
    "desc": """
Sosyal mühendislik saldırıları, teknik önlemlerin tek başına yetersiz kaldığı, 
insan faktörünün devreye girdiği kritik bir güvenlik alanıdır. Bu senaryoda, 
şirketinizin güvenlik farkındalığı yöneticisi olarak görev yapıyorsunuz. 
Yapay zeka kontrollü bir simülasyon, şirket çalışanlarına kişiselleştirilmiş 
oltalama e-postaları göndermektedir. AI, LinkedIn profillerinden, şirket web 
sitesinden ve sosyal medyadan topladığı bilgilerle her çalışana özel, 
inandırıcı mesajlar oluşturur. Göreviniz, gelen e-postaları analiz etmek, 
şüpheli olanları tespit ederek karantinaya almak ve çalışanları 
bilinçlendirmektir. Elinizde e-posta başlık analiz aracı, bağlantı tarayıcı, 
ek dosya sandbox'ı ve çalışan eğitim modülü bulunur. Yanlışlıkla gerçek bir 
müşteri e-postasını karantinaya almanız durumunda iş kaybı yaşanır; şüpheli 
bir e-postayı kaçırmanız halinde ise bir çalışanın bilgisayarı ele 
geçirilebilir. AI simülasyonu, başarısız denemelerinden ders çıkararak 
mesajlarını sürekli iyileştirir. Siz de çalışanların güvenlik bilinci puanını 
artırmak için periyodik eğitimler düzenlemeli ve simülasyon testleri 
yapmalısınız. Bu senaryo, teknik ve insani savunma katmanlarının birlikte 
nasıl çalışması gerektiğini çarpıcı bir şekilde gösterir.
"""
}

ALL_SCENARIOS["2E"] = {
    "title": "2E: Bulut Kalesi - AWS Güvenliği",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Bulut Kaynak Tarayıcı AI",
    "type": "human_defend",
    "desc": """
Bulut bilişim çağında, güvenlik sorumluluğu bulut sağlayıcı ile müşteri 
arasında paylaşılır. Bu senaryoda, şirketinizin AWS üzerindeki altyapısını 
koruyan bir bulut güvenlik mühendisi rolündesiniz. Yapay zeka kontrollü 
simülasyon, internet üzerindeki açık S3 bucket'larını, yanlış yapılandırılmış 
güvenlik gruplarını ve aşırı izinli IAM rollerini tarayarak bulur. Göreviniz, 
CloudTrail loglarını izlemek, Config kurallarını yönetmek, GuardDuty 
bulgularını analiz etmek ve yanlış yapılandırmaları düzeltmektir. AI 
simülasyonu, sürekli olarak yeni zafiyetler keşfeder; siz ise bu zafiyetleri 
kapatmak için zamana karşı yarışırsınız. Örneğin, yanlışlıkla public olarak 
işaretlenmiş bir S3 bucket'ı müşteri verilerini ifşa edebilir. Elinizde bulut 
güvenlik duruş yönetimi panosu, uyumluluk skoru göstergesi ve otomatik 
düzeltme iş akışları bulunur. Doğru önceliklendirme yapmalı, kritik bulguları 
hemen kapatmalı ve düşük riskli olanları planlı bakım penceresine 
bırakmalısınız. Senaryo, paylaşılan sorumluluk modelini, buluta özgü 
tehditleri ve DevSecOps yaklaşımını kapsamlı şekilde ele alır.
"""
}

# --- SEVİYE 3: SOLUCAN DELİĞİ ---

ALL_SCENARIOS["3A"] = {
    "title": "3A: VPN Değerlendirmesi - Şifreleme Analizi",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Dinamik Şifreleme AI",
    "type": "human_attack",
    "desc": """
Şifreleme, modern siber güvenliğin bel kemiğidir ve bu senaryo, kriptografik 
sistemlerin hem gücünü hem de zayıflıklarını keşfetmenizi sağlar. İki şirket 
şubesi arasındaki VPN tünelinin güvenlik değerlendirmesini yapan bir kırmızı 
takım analisti rolündesiniz. AI savunmacı, tünelin şifreleme parametrelerini 
dinamik olarak değiştirir; AES-128'den AES-256'ya geçiş yapabilir, anahtar 
değişim algoritmasını yükseltebilir. Elinizde paket yakalama araçları, 
kriptanaliz modülleri ve kaba kuvvet analiz altyapısı bulunur. Yakalanan 
şifreli paketleri analiz etmek için doğru zafiyeti bulmanız gerekir. Örneğin, 
eski bir Diffie-Hellman uygulaması küçük asal sayılar kullanıyorsa Logjam 
analizi ile anahtarı kırma potansiyeli değerlendirilebilir. Ağ topolojisi 
görselleştirmesinde, şifreli veri akışı mavi renkli kilitli zarflar olarak, 
çözülebilir veri akışı ise sarı renkli açık zarflar olarak animasyonlandırılır. 
Terminal üzerinde 'yakala', 'analiz_et', 'kirilma_dene' komutlarıyla 
çalışırsınız. Başarılı olduğunuzda, iki şube arasındaki finansal raporları 
içeren hassas verilere erişim sağlarsınız ve savunma ekibine hangi 
noktalarda iyileştirme yapmaları gerektiğini raporlarsınız. Bu senaryo; 
simetrik ve asimetrik şifreleme arasındaki farkları, anahtar değişim 
protokollerinin önemini ve kriptografik zafiyetlerin nasıl değerlendirildiğini 
öğretir.
"""
}

ALL_SCENARIOS["3B"] = {
    "title": "3B: Fidye Avcısı - Ransomware Müdahale",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Fidye Yazılımı Simülasyonu",
    "type": "human_defend",
    "desc": """
Bir fidye yazılımı salgını, her güvenlik profesyonelinin kabusudur. Bu 
senaryoda, şirket ağınızda hızla yayılan bir fidye yazılımı aktivitesiyle 
karşı karşıyasınız. Yapay zeka kontrollü simülasyon, SMB protokolü üzerinden 
yanal hareket ederek ağdaki dosya sunucularını, veritabanlarını ve yedek 
sistemlerini hedef almaktadır. Olay müdahale ekibi lideri olarak göreviniz; 
aktivitenin yayılmasını durdurmak, enfekte sistemleri izole etmek, şifrelenmiş 
verileri kurtarmak ve olayın kaynağını tespit etmektir. Elinizde ağ 
segmentasyon kontrol paneli, yedek geri yükleme araçları, forensic analiz 
modülü ve kriz iletişim arayüzü bulunur. AI simülasyonu, savunma 
önlemlerinize adapte olur; bir sunucuyu izole ettiğinizde diğerine sıçrar. 
Ağ haritasında enfekte cihazlar kırmızı renkte parlar ve enfeksiyonun 
yayılma yönü animasyonlu oklarla gösterilir. Kritik kararlar vermelisiniz: 
Hangi sunucuları hemen izole edeceksiniz? Yedekleri geri yüklemek için 
hangi zaman damgasını kullanacaksınız? Bu senaryo, fidye yazılımı 
aktivitelerinin dinamiklerini, etkili olay müdahale prosedürlerini ve 
yedekleme stratejilerinin kritik önemini vurgular.
"""
}

ALL_SCENARIOS["3C"] = {
    "title": "3C: PGP Savaşları - E-posta Şifreleme",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Ortadaki Adam Simülasyonu",
    "type": "human_defend",
    "desc": """
Güvenli iletişim, özellikle hassas bilgilerin e-posta yoluyla iletildiği 
kurumsal ortamlarda hayati önem taşır. Bu senaryoda, şirketinizin e-posta 
altyapısını koruyan bir güvenlik mühendisi rolündesiniz. Yapay zeka 
kontrollü simülasyon, kurum içi ve dışı e-posta trafiğini dinleyerek hassas 
bilgileri toplamaya çalışmaktadır. Sizin göreviniz, PGP anahtar altyapısını 
kurmak, çalışanlara anahtar çiftleri dağıtmak ve şifreli iletişimi zorunlu 
kılmaktır. AI simülasyonu, açık anahtar sunucularını manipüle ederek sahte 
anahtarlar yerleştirebilir veya anahtar değişim sürecinde ortadaki adam 
aktivitesi yapabilir. Bu nedenle, anahtar imzalama partileri düzenlemeli, 
güven ağını yönetmeli ve sertifika iptal listelerini güncel tutmalısınız. 
Görsel arayüzde, şifreli e-postalar yeşil zarflar, şifresiz olanlar kırmızı 
zarflar olarak gösterilir. Anahtar güven skoru, her bir çalışanın anahtarının 
ne kadar güvenilir olduğunu gösteren bir metrik olarak ekranda yer alır. Bu 
senaryo, uçtan uca şifrelemenin önemini, açık anahtar altyapısının 
zorluklarını ve güvenli iletişim protokollerinin inceliklerini öğretir.
"""
}

ALL_SCENARIOS["3D"] = {
    "title": "3D: Kuantum Geçişi - Post-Quantum Kriptografi",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Hibrit Kripto AI",
    "type": "human_attack",
    "desc": """
Kuantum bilgisayarların gelişimi, mevcut kriptografik sistemler için 
varoluşsal bir tehdit oluşturmaktadır. Bu ileri seviye senaryoda, kuantum 
sonrası kriptografiye geçiş yapan bir kurumun güvenlik değerlendirmesini 
yapan bir kırmızı takım analisti rolündesiniz. AI savunmacı, melez bir 
kriptografik sistem kullanır; hem klasik RSA/ECC algoritmalarını hem de 
kuantum dayanıklı CRYSTALS-Kyber gibi yeni nesil algoritmaları eş zamanlı 
çalıştırır. Bu geçiş döneminde, eski sistemler hala zayıf algoritmaları 
kullanmaya devam eder ve işte bu zayıf halkalar sizin hedefinizdir. 
Göreviniz, hala SHA-1 ile imzalanmış eski bir güncelleme sunucusunu tespit 
etmek, buradaki kriptografik zayıflıktan faydalanarak imza doğrulamasını 
atlama potansiyelini değerlendirmek ve savunma ekibine rapor sunmaktır. 
Görsel arayüzde, şifreleme algoritmalarının güç seviyeleri bir radar grafiği 
ile karşılaştırılır. Bu senaryo, kriptografik çeviklik kavramını, geçiş 
dönemi risklerini ve kuantum tehdidinin gerçek dünyadaki etkilerini 
derinlemesine inceler.
"""
}

ALL_SCENARIOS["3E"] = {
    "title": "3E: Zincir Kırıcı - Blockchain Güvenlik Analizi",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Akıllı Kontrat Denetleyici AI",
    "type": "human_attack",
    "desc": """
Blockchain teknolojisi, merkeziyetsiz yapısıyla güvenlik vaat eder, ancak 
akıllı kontratlar ve uygulama katmanı ciddi zafiyetler barındırabilir. Bu 
senaryoda, bir DeFi platformunun akıllı kontratının güvenlik denetimini 
yapan bir kırmızı takım analisti rolündesiniz. AI savunmacı, akıllı 
kontratları sürekli denetleyen ve anormal işlemleri tespit eden bir güvenlik 
oracle'ı olarak görev yapar. Göreviniz, akıllı kontrattaki bir reentrancy 
zafiyetini veya flash loan açığını tespit ederek platformun savunma 
ekibine rapor sunmaktır. Elinizde Solidity kod analiz araçları, işlem 
simülatörü ve gas optimizasyon modülü bulunur. Görsel arayüzde, blockchain 
işlemleri bir blok zinciri animasyonu olarak gösterilir; her blok, içindeki 
işlemlerle birlikte ekranda belirir. AI savunmacı, şüpheli işlem desenlerini 
tespit ettiğinde işlemi front-run yaparak sizin analizinizi engellemeye 
çalışır. Senaryo, akıllı kontrat güvenliğinin inceliklerini, yaygın zafiyet 
türlerini ve güvenli kod geliştirme prensiplerini kapsamlı şekilde öğretir.
"""
}

# --- SEVİYE 4: FIRTINA ---

ALL_SCENARIOS["4A"] = {
    "title": "4A: Botnet Efendisi - DDoS Simülasyonu",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Anti-DDoS AI",
    "type": "human_attack",
    "desc": """
Bu senaryoda bir kırmızı takım analisti olarak, büyük ölçekli bir DDoS 
simülasyonunun etkilerini değerlendiriyorsunuz. Elinizde dünya geneline 
yayılmış, farklı coğrafi bölgelerden ve farklı IP adreslerinden oluşan bir 
simülasyon botnet'i bulunmaktadır. Hedefiniz, büyük bir e-ticaret 
platformunun altyapısının hangi yük seviyelerinde çöktüğünü tespit etmek ve 
bu sırada AI tabanlı anti-DDoS sisteminin etkinliğini değerlendirmektir. AI 
savunmacı, gelen trafiği sürekli analiz eder; anormal desenleri tespit 
ettiğinde trafik filtreleme, rate limiting ve CAPTCHA doğrulaması gibi 
önlemleri devreye alır. Sizin göreviniz, simülasyonu tespit edilmeyecek 
şekilde katmanlandırmaktır. SYN flood, UDP flood, HTTP flood ve Slowloris 
gibi farklı vektörleri eş zamanlı veya sıralı olarak kullanabilirsiniz. 
Görsel arayüzde botnet'inizin dünya haritası üzerindeki dağılımı, her bir 
botun anlık durumu ve hedef sunucunun kaynak kullanımı canlı olarak 
gösterilir. AI savunmacı, simülasyon deseninizi öğrendikçe kendini adapte 
eder; bu nedenle monoton bir strateji başarısız olur. Başarı, hedef 
sunucunun CPU ve bellek kullanımını yüzde 95'in üzerine çıkararak savunma 
ekibinin hangi noktalarda iyileştirme yapması gerektiğini belirlemekle 
ölçülür. Bu senaryo, DDoS vektörlerini, botnet yönetimini, trafik analizi 
atlatma tekniklerini ve modern anti-DDoS sistemlerinin çalışma prensiplerini 
derinlemesine öğretir.
"""
}

ALL_SCENARIOS["4B"] = {
    "title": "4B: DDoS Savunma - Kalkan Operasyonu",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Botnet Simülasyonu",
    "type": "human_defend",
    "desc": """
Rollerin tersine döndüğü bu senaryoda, bir bulut altyapı mühendisi olarak 
devasa bir DDoS simülasyonuna karşı savunma yapıyorsunuz. AI kontrollü bir 
botnet, şirketinizin web uygulamasına karşı çok vektörlü bir simülasyon 
başlatmıştır. SYN flood ile sunucu bağlantı tablosunu doldurmaya çalışırken, 
eş zamanlı olarak HTTP flood ile uygulama katmanını hedef alır. Elinizde yük 
dengeleyici (load balancer), web uygulama güvenlik duvarı (WAF), CDN 
yapılandırması ve otomatik ölçeklendirme (auto-scaling) araçları bulunur. 
Göreviniz, simülasyon trafiğini meşru kullanıcı trafiğinden ayırmak, 
filtreleme kurallarını optimize etmek ve hizmetin kesintisiz devamını 
sağlamaktır. AI botnet, aktivite desenini sürekli değiştirir; bir filtreleme 
kuralı eklediğinizde, botnet IP adreslerini ve vektörünü değiştirerek uyum 
sağlar. Kaynakları verimli kullanmalısınız; gereksiz yere çok fazla sunucu 
ölçeklendirirseniz maliyetler fırlar, az ölçeklendirirseniz hizmet kesintisi 
yaşanır. Canlı sistem monitöründe CPU, bellek, ağ giriş/çıkış trafiği ve 
bağlantı sayıları anlık olarak gösterilir. Başarı puanınız; hizmet kesintisi 
süresi, engellenen simülasyon trafiği yüzdesi, yanlış pozitif oranı ve 
maliyet verimliliğine göre hesaplanır. Bu senaryo, DDoS savunma 
stratejilerini, yük dengeleme mimarilerini, otomatik ölçeklendirme 
konfigürasyonlarını ve olay müdahale süreçlerini gerçekçi bir ortamda 
deneyimlemenizi sağlar.
"""
}

ALL_SCENARIOS["4C"] = {
    "title": "4C: Amplifikasyon - DNS Büyütme Analizi",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "DNS Güvenlik AI",
    "type": "human_attack",
    "desc": """
DNS amplifikasyon aktiviteleri, küçük bir istekle büyük bir yanıt oluşturarak 
trafiği katlayan sofistike DDoS tekniklerindendir. Bu senaryoda, açık DNS 
çözümleyicilerini (open resolver) kullanarak bir amplifikasyon simülasyonu 
düzenleyen bir kırmızı takım analisti rolündesiniz. Hedef, bir finans 
kuruluşunun ana web sitesidir. AI savunmacı, DNS trafiğini analiz eden ve 
anormal sorguları tespit eden özel bir güvenlik sistemidir. Simülasyonu 
gerçekleştirmek için önce internet üzerindeki açık DNS çözümleyicilerini 
keşfetmeli, ardından sahte kaynak IP adresleri kullanarak bu çözümleyicilere 
büyük yanıtlar üretecek sorgular göndermelisiniz. Amplifikasyon faktörü ne 
kadar yüksek olursa, etkisi o kadar büyük olur. ANY, DNSSEC veya TXT kayıt 
sorguları genellikle en yüksek amplifikasyonu sağlar. Görsel arayüzde, 
amplifikasyon faktörü, kullanılan çözümleyici sayısı ve hedefe ulaşan 
trafik miktarı canlı olarak gösterilir. AI savunmacı, anormal DNS trafiğini 
tespit ettiğinde, açık çözümleyicileri kara listeye almaya ve hedef 
sunucuda DNS yanıt filtrelemesi yapmaya başlar. Siz ise sürekli yeni 
çözümleyiciler bularak simülasyonu sürdürmelisiniz. Bu senaryo, DNS 
protokolünün güvenlik açıklarını, IP sahtekarlığının nasıl çalıştığını, 
amplifikasyon aktivitelerinin matematiğini ve DNS güvenliği en iyi 
uygulamalarını öğretir.
"""
}

ALL_SCENARIOS["4D"] = {
    "title": "4D: Kapasite Planlama - Yük Testi Mühendisi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Anomali Üretici Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, sistemlerin dayanıklılığını test eden bir performans mühendisi 
perspektifinden kurgulanmıştır. Şirketinizin yeni lansmanı öncesinde, 
altyapının beklenen yüksek trafiği kaldırabileceğinden emin olmanız 
gerekmektedir. AI, gerçek kullanıcı davranışını taklit eden ve aynı zamanda 
çeşitli anormal yük desenleri oluşturan bir yük testi aracı olarak çalışır. 
Göreviniz, sistemin darboğazlarını tespit etmek, kaynak tahsisini optimize 
etmek ve ölçeklendirme politikalarını yapılandırmaktır. AI, normal kullanıcı 
trafiğinden ani yüklenmelere, coğrafi olarak dengesiz dağılımdan belirli 
endpoint'lere yönelik yoğun isteklere kadar çeşitli senaryoları simüle 
eder. Elinizde detaylı sistem metrikleri, yanıt süresi dağılımları, hata 
oranları ve kaynak kullanım grafikleri bulunur. Her test senaryosundan 
sonra, sistemin hangi noktada başarısız olduğunu analiz etmeli ve gerekli 
iyileştirmeleri yapmalısınız. Vertikal ölçeklendirme (daha güçlü sunucu) 
mi, yoksa horizontal ölçeklendirme (daha fazla sunucu) mi yapacağınıza 
karar vermelisiniz. Ayrıca veritabanı bağlantı havuzu, önbellek stratejisi 
ve CDN yapılandırması gibi parametreleri de optimize etmeniz gerekir. 
Başarı; sistemin belirlenen eşik değerlerin altında yanıt süresiyle, sıfır 
hata ile maksimum kaç eş zamanlı kullanıcıyı kaldırabildiğiyle ölçülür. 
Bu senaryo, performans mühendisliği, kapasite planlaması, darboğaz analizi 
ve ölçeklenebilir mimari tasarımı konularında pratik deneyim kazandırır.
"""
}

ALL_SCENARIOS["4E"] = {
    "title": "4E: Bulut Patlaması - CDN Stratejisi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Küresel Trafik Simülasyonu",
    "type": "human_defend",
    "desc": """
Küresel ölçekte hizmet veren bir platformun altyapı mühendisi olarak, 
dünyanın farklı bölgelerinden gelen ani trafik patlamalarına karşı savunma 
yapıyorsunuz. AI, gerçek dünya senaryolarını simüle eder: bir sosyal medya 
fenomeninin sitenizi paylaşması sonucu oluşan ani trafik artışı, belirli 
bir bölgede internet kesintisi, veya rakip bir firmanın yaptığı promosyon 
nedeniyle kullanıcıların topluca sitenize yönelmesi. Elinizde CDN 
yapılandırması, edge sunucu yerleşimleri, Anycast DNS ve trafik yönlendirme 
politikaları bulunur. Göreviniz, dünya haritası üzerinde canlı olarak 
gösterilen trafik akışlarını analiz ederek, CDN önbellek kurallarını 
optimize etmek, origin sunucuları korumak ve kullanıcı deneyimini tutarlı 
tutmaktır. AI, beklenmedik bölgelerden trafik oluşturarak sizi şaşırtmaya 
çalışır. Örneğin, normalde düşük trafik gelen bir bölgede ani bir patlama 
olabilir. Bu durumda CDN edge sunucularınızın kapasitesini artırmalı veya 
yeni PoP (Point of Presence) noktaları eklemelisiniz. Başarı puanınız; 
global gecikme süresi ortalaması, cache hit oranı, origin sunucu yükü ve 
maliyet optimizasyonuna göre hesaplanır. Bu senaryo, CDN mimarilerini, 
global trafik yönetimini, edge computing kavramlarını ve bulut tabanlı 
dağıtık sistemlerin optimizasyonunu öğretir.
"""
}

# --- SEVİYE 5 ---
ALL_SCENARIOS["5A"] = {
    "title": "5A: Sessiz Sızma - APT Keşif Aşaması",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Tehdit İstihbaratı AI",
    "type": "human_attack",
    "desc": """
Bu senaryo, gelişmiş kalıcı tehdit (APT) operasyonlarının ilk ve en kritik aşaması olan keşif ve bilgi toplama sürecini simüle eder. Kırmızı takım analisti olarak, hedef kurum hakkında mümkün olduğunca fazla bilgi toplamaya çalışıyorsunuz. AI savunmacı, açık kaynak istihbaratı (OSINT) izleme yapan gelişmiş bir tehdit istihbarat platformudur. LinkedIn, GitHub, DNS, Shodan gibi kaynaklardan bilgi toplayarak saldırı vektörlerini haritalandırıyorsunuz. Her keşif aktiviteniz AI tarafından izlenir ve risk skoru oluşturulur. Bu senaryo sonunda, OSINT tekniklerini, pasif keşif yöntemlerini ve kurumsal ayak izi analizini öğreneceksiniz.
"""
}

ALL_SCENARIOS["5B"] = {
    "title": "5B: SOC Analisti - Tehdit Avı",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "APT Simülatör AI",
    "type": "human_defend",
    "desc": """
Bu senaryoda, bir SOC analisti olarak ağınızda aktif olan ancak henüz tespit edilmemiş bir APT saldırganını bulmaya çalışıyorsunuz. AI kontrollü saldırgan, sisteme çoktan sızmış, kalıcılık sağlamış ve yanal hareket için keşif yapmaktadır. Elinizde SIEM logları, endpoint telemetrisi ve tehdit istihbaratı beslemeleri bulunur. Göreviniz, milyonlarca log kaydı arasından anormal desenleri tespit etmek ve şüpheli aktiviteleri ilişkilendirmektir. Bu senaryo, tehdit avı metodolojilerini, log analizi tekniklerini ve olay inceleme süreçlerini öğretir.
"""
}

ALL_SCENARIOS["5C"] = {
    "title": "5C: Zararlı Avı - Malware Analizi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Polimorfik Malware AI",
    "type": "human_defend",
    "desc": """
Bu senaryoda, bir malware analisti olarak şirket ağında tespit edilen şüpheli bir dosyayı analiz ediyorsunuz. AI kontrollü zararlı yazılım, polimorfik yapısıyla her çalıştırıldığında kodunu değiştirir. Elinizde statik analiz araçları, dinamik analiz ortamı (sandbox, debugger) ve ağ trafiği analiz araçları bulunur. Göreviniz, zararlı yazılımın yeteneklerini, C2 sunucusunu ve kalıcılık mekanizmasını tespit etmektir. Bu senaryo, malware analizi metodolojilerini, tersine mühendislik temellerini ve tehdit istihbaratı üretimini öğretir.
"""
}

ALL_SCENARIOS["5D"] = {
    "title": "5D: Yetki Yükseltme - Privilege Escalation",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "EDR AI",
    "type": "human_attack",
    "desc": """
Sisteme düşük yetkili bir kullanıcı olarak erişim sağladıktan sonra, yönetici yetkilerine yükselmek APT operasyonlarının kritik bir aşamasıdır. Bu senaryoda, elinizdeki sınırlı bir hesaptan domain admin yetkisine ulaşmaya çalışıyorsunuz. AI savunmacı, Endpoint Detection and Response (EDR) çözümü olarak çalışır ve şüpheli yetki yükseltme girişimlerini tespit etmeye programlanmıştır. SUID binary, sudo misconfiguration, kernel exploit, token manipulation gibi teknikleri kullanabilirsiniz. Bu senaryo, işletim sistemi güvenlik mekanizmalarını ve yaygın yetki yükseltme tekniklerini öğretir.
"""
}

ALL_SCENARIOS["5E"] = {
    "title": "5E: Log Temizleme - Anti-Forensic",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Forensic AI",
    "type": "human_attack",
    "desc": """
Başarılı bir sızma sonrası izleri temizlemek, APT operasyonlarının vazgeçilmez bir parçasıdır. Bu senaryoda, hedef sistemdeki varlığınızı gizlemek ve forensic analizi engellemek için anti-forensic teknikleri uyguluyorsunuz. AI savunmacı, sistem loglarını sürekli analiz eden ve anormal değişiklikleri tespit eden bir forensic analiz aracı olarak çalışır. Shell history temizleme, event log silme, timestamp değiştirme, ağ logu karartma gibi teknikleri kullanabilirsiniz. Bu senaryo, forensic analiz tekniklerini ve anti-forensic yöntemleri öğretir.
"""
}

# --- SEVİYE 6 ---
ALL_SCENARIOS["6A"] = {
    "title": "6A: APT Operatörü - Tam Saldırı Zinciri",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Gelişmiş Tehdit Avı AI",
    "type": "human_attack",
    "desc": """
Bu, tüm önceki seviyelerin birleştiği zirve senaryosudur. Tam teşekküllü bir APT operatörü olarak, hedef kuruma karşı baştan sona bir saldırı zinciri yürütüyorsunuz. AI savunmacı, derin öğrenme tabanlı bir tehdit avı platformudur ve saldırının her aşamasında sizi tespit etmeye çalışır. Göreviniz; keşif, silahlanma, teslimat, istismar, kurulum, komuta kontrol ve hedefe yönelik eylemler olmak üzere yedi aşamalı kill chain'i tamamlamaktır. Bu senaryo, APT operasyonlarının tüm yaşam döngüsünü öğretir.
"""
}

ALL_SCENARIOS["6B"] = {
    "title": "6B: Tehdit Avcısı - APT Müdahale",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "APT Operatörü AI",
    "type": "human_defend",
    "desc": """
Kurumunuzun baş tehdit avcısı olarak, aktif bir APT saldırısını tespit etmek ve durdurmakla görevlisiniz. AI kontrollü APT operatörü, gelişmiş teknikler kullanarak ağınıza sızmış durumdadır. Elinizde EDR, SIEM, NDR, tehdit istihbaratı platformu ve SOAR araçları bulunur. Göreviniz, kill chain'in hangi aşamasında olduğunuzu tespit etmek ve müdahale stratejisi geliştirmektir. Bu senaryo, tehdit avı metodolojilerini ve olay müdahale süreçlerini öğretir.
"""
}

ALL_SCENARIOS["6C"] = {
    "title": "6C: Yanal Dans - Lateral Movement",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Mikro-Segmentasyon AI",
    "type": "human_attack",
    "desc": """
Bir iş istasyonunu ele geçirdikten sonra, ağ içinde yanal hareket ederek hedef sunucuya ulaşmak APT operasyonlarının kalbidir. Bu senaryoda, ele geçirdiğiniz başlangıç noktasından domain controller'a uzanan bir yanal hareket zinciri kurmanız gerekiyor. AI savunmacı, ağı mikro segmentlere ayıran ve segmentler arası trafiği sıkı denetleyen bir güvenlik mimarisini yönetir. Pass-the-Hash, PsExec, WMI, WinRM gibi teknikleri kullanabilirsiniz. Bu senaryo, Active Directory güvenliğini ve yanal hareket tekniklerini öğretir.
"""
}

ALL_SCENARIOS["6D"] = {
    "title": "6D: Veri Sızdırma - Data Exfiltration",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "DLP AI",
    "type": "human_attack",
    "desc": """
Hedef veriye ulaştıktan sonra, bu veriyi tespit edilmeden dışarı çıkarmak APT operasyonlarının son kritik aşamasıdır. Bu senaryoda, ele geçirdiğiniz hassas verileri kurum dışına sızdırmaya çalışıyorsunuz. AI savunmacı, Veri Kaybı Önleme (DLP) sistemi olarak çalışır ve anormal veri transferlerini tespit etmeye programlanmıştır. DNS tünelleme, HTTPS upload, e-posta eki, steganografi gibi teknikleri kullanabilirsiniz. Bu senaryo, veri sızdırma tekniklerini ve DLP atlatma yöntemlerini öğretir.
"""
}

ALL_SCENARIOS["6E"] = {
    "title": "6E: Son Kale - Kritik Altyapı Savunması",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Nation-State APT AI",
    "type": "human_defend",
    "desc": """
Bu senaryo, kritik altyapı savunmasının zirvesini temsil eder. Bir enerji santralinin OT (Operasyonel Teknoloji) ağını koruyan baş güvenlik mühendisi olarak, ulus devlet destekli bir APT grubunun saldırısını püskürtmeye çalışıyorsunuz. Elinizde IT-OT gateway güvenliği, endüstriyel IDS ve PLC/DCS güvenlik izleme araçları bulunur. Bu senaryo, kritik altyapı güvenliğini ve OT/ICS güvenlik prensiplerini öğretir.
"""
}

# --- SEVİYE 7 ---
ALL_SCENARIOS["7A"] = {
    "title": "7A: SQLi Ustası - Veritabanı Saldırıları",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Veritabanı Güvenlik AI",
    "type": "human_attack",
    "desc": """
Veritabanı saldırıları, web güvenliğinin en kritik alanlarından biridir. Bu senaryoda, bir e-ticaret platformunun MySQL veritabanına sızma testi yapıyorsunuz. AI savunmacı, sorguları analiz eden ve şüpheli istekleri engelleyen gelişmiş bir veritabanı güvenlik duvarıdır. Klasik SQL enjeksiyonu, kör SQL enjeksiyonu, zaman tabanlı sorgular, UNION tabanlı saldırılar gibi teknikleri kullanabilirsiniz. Bu senaryo, SQL dilinin derinlemesine kullanımını ve veritabanı güvenlik mekanizmalarını öğretir.
"""
}

ALL_SCENARIOS["7B"] = {
    "title": "7B: WAF Yöneticisi - Web Savunma",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Otomatik Tarayıcı AI",
    "type": "human_defend",
    "desc": """
Web uygulamalarının korunmasında kritik rol oynayan WAF yönetimi, bu senaryonun ana odağıdır. Bir web güvenlik mühendisi olarak, kurumunuzun web uygulamasını sürekli tarayan AI kontrollü bir güvenlik tarayıcısına karşı savunma yapıyorsunuz. ModSecurity tabanlı bir WAF, özel kural yazma arayüzü ve sanal yama araçları elinizde. Bu senaryo, WAF yönetiminin inceliklerini ve savunma derinliği stratejilerini öğretir.
"""
}

ALL_SCENARIOS["7C"] = {
    "title": "7C: XSS Avcısı - Client-Side Saldırılar",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Content Security Policy AI",
    "type": "human_attack",
    "desc": """
Cross-Site Scripting (XSS), istemci tarafı saldırılarının en yaygın ve tehlikeli türlerinden biridir. Bu senaryoda, bir sosyal medya platformundaki XSS zafiyetlerini bularak kullanıcı oturumlarını ele geçirmeye çalışıyorsunuz. AI savunmacı, Content Security Policy (CSP) başlıklarını dinamik olarak yöneten gelişmiş bir güvenlik sistemidir. Reflected XSS, stored XSS, DOM-based XSS tekniklerini kullanabilirsiniz. Bu senaryo, XSS zafiyetlerini ve CSP mekanizmasının çalışma prensiplerini öğretir.
"""
}

ALL_SCENARIOS["7D"] = {
    "title": "7D: Komut Enjeksiyonu - OS Command Injection",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Sistem Güvenlik AI",
    "type": "human_attack",
    "desc": """
Komut enjeksiyonu saldırıları, bir web uygulaması üzerinden işletim sistemi komutlarının çalıştırılmasını sağlayan kritik güvenlik açıklarıdır. Bu senaryoda, bir ağ yönetim arayüzündeki komut enjeksiyonu zafiyetini kullanarak hedef sunucuda tam kontrol sağlamaya çalışıyorsunuz. AI savunmacı, sistem çağrılarını izleyen ve anormal proses davranışlarını tespit eden bir host tabanlı güvenlik sistemidir. Blind injection, out-of-band exfiltration, reverse shell gibi teknikleri kullanabilirsiniz. Bu senaryo, işletim sistemi güvenliğini ve input validasyonunun önemini öğretir.
"""
}

ALL_SCENARIOS["7E"] = {
    "title": "7E: LDAP Savaşları - Dizin Servisi Saldırıları",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Active Directory AI",
    "type": "human_attack",
    "desc": """
LDAP enjeksiyonu ve Active Directory saldırıları, kurumsal ağların bel kemiğini hedef alan sofistike saldırı vektörleridir. Bu senaryoda, bir kurumsal portaldaki LDAP enjeksiyonu zafiyetini kullanarak Active Directory'ye sızmaya çalışıyorsunuz. AI savunmacı, LDAP sorgularını analiz eden ve şüpheli bağlanma desenlerini tespit eden bir AD güvenlik sistemidir. Kerberoasting, AS-REP Roasting, DCSync gibi ileri teknikleri kullanabilirsiniz. Bu senaryo, LDAP protokolünü ve Active Directory güvenlik mimarisini öğretir.
"""
}

# --- SEVİYE 8 ---
ALL_SCENARIOS["8A"] = {
    "title": "8A: Debugger - Tersine Mühendislik",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Anti-Tamper AI",
    "type": "human_attack",
    "desc": """
Tersine mühendislik, yazılım güvenliğinin en zor alanlarından biridir. Bu senaryoda, şüpheli bir binary dosyayı analiz ederek içindeki gizli algoritmayı ve koruma mekanizmalarını çözmeye çalışıyorsunuz. AI savunmacı, anti-debugging, anti-disassembly, anti-VM ve kod şifreleme gibi çeşitli koruma teknikleriyle donatılmış bir anti-tamper sistemidir. Disassembler, debugger, hex editor gibi araçları kullanabilirsiniz. Bu senaryo, assembly dilini, işletim sistemi iç yapısını ve anti-reverse engineering tekniklerini öğretir.
"""
}

ALL_SCENARIOS["8B"] = {
    "title": "8B: Malware Analisti - Zararlı Yazılım İnceleme",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Evader Malware AI",
    "type": "human_defend",
    "desc": """
Profesyonel malware analizi, siber güvenliğin en teknik alanlarından biridir. Bu senaryoda, kurum ağında tespit edilen gelişmiş bir zararlı yazılım örneğini analiz eden bir malware araştırmacısı rolündesiniz. AI kontrollü malware, sandbox tespiti, anti-VM, anti-debugging gibi ileri kaçınma teknikleri kullanır. PE analyzer, YARA kural yazıcı, sandbox gibi araçlarla çalışırsınız. Bu senaryo, malware analizi metodolojilerini ve tehdit istihbaratı üretimini öğretir.
"""
}

ALL_SCENARIOS["8C"] = {
    "title": "8C: Unpacking - Paket Açma Sanatı",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Packer Koruma AI",
    "type": "human_attack",
    "desc": """
Yazılım paketleyiciler (packers), hem meşru yazılım koruması hem de zararlı yazılım gizleme amacıyla kullanılan güçlü araçlardır. Bu senaryoda, özel bir packer ile korunmuş bir binary'yi unpack ederek içindeki orijinal kodu ortaya çıkarmaya çalışıyorsunuz. AI savunmacı, çok katmanlı şifreleme, anti-unpacking hileleri ve IAT gizleme gibi gelişmiş koruma teknikleri kullanır. Entropi analizi, OEP bulma, memory dump, IAT rekonstrüksiyon tekniklerini kullanabilirsiniz. Bu senaryo, PE/ELF dosya formatlarını ve ileri seviye tersine mühendislik tekniklerini öğretir.
"""
}

ALL_SCENARIOS["8D"] = {
    "title": "8D: Firma Koruması - Secure Boot Analizi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Firmware Rootkit AI",
    "type": "human_defend",
    "desc": """
Firmware seviyesindeki saldırılar, işletim sisteminin altında çalıştıkları için tespit edilmeleri son derece zordur. Bu senaryoda, bir IoT cihazının firmware'ine bulaşmış bir rootkit'i tespit etmeye çalışan bir firmware güvenlik araştırmacısı rolündesiniz. AI kontrollü rootkit, UEFI/BIOS seviyesinde çalışır ve Secure Boot'u atlatır. Firmware dumper, binary diffing araçları ve forensic toolkit kullanırsınız. Bu senaryo, firmware güvenliğini ve boot süreci güvenliğini öğretir.
"""
}

ALL_SCENARIOS["8E"] = {
    "title": "8E: Rootkit Avı - Kernel Modu Analizi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Kernel Rootkit AI",
    "type": "human_defend",
    "desc": """
Kernel seviyesindeki rootkit'ler, işletim sisteminin en derin katmanlarında çalışarak maksimum gizlilik sağlar. Bu senaryoda, bir Linux sunucusuna bulaşmış kernel modülü rootkit'ini tespit etmeye çalışan bir sistem güvenlik mühendisi rolündesiniz. AI kontrollü rootkit, sistem çağrı tablosunu (syscall table) hook'lar ve prosesleri gizler. Kernel debugger, memory forensics araçları ve syscall table analyzer kullanırsınız. Bu senaryo, işletim sistemi kernel mimarisini ve memory forensiğini öğretir.
"""
}

# --- SEVİYE 9 ---
ALL_SCENARIOS["9A"] = {
    "title": "9A: Phishing Kampanyası - Oltalama Saldırısı",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "E-posta Güvenlik AI",
    "type": "human_attack",
    "desc": """
Sosyal mühendislik saldırılarının en yaygın türü olan phishing, teknik savunmaları aşmak için insan psikolojisini hedef alır. Bu senaryoda, bir şirkete karşı kapsamlı bir phishing kampanyası düzenliyorsunuz. AI savunmacı, e-posta başlıklarını analiz eden ve NLP ile şüpheli içerikleri tespit eden gelişmiş bir e-posta güvenlik sistemidir. Hedef profil bilgileri, e-posta şablonları, sahte login sayfaları kullanabilirsiniz. Bu senaryo, sosyal mühendislik prensiplerini ve e-posta güvenlik protokollerini öğretir.
"""
}

ALL_SCENARIOS["9B"] = {
    "title": "9B: Farkındalık Eğitmeni - Güvenlik Kültürü",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Sosyal Mühendis AI",
    "type": "human_defend",
    "desc": """
Teknik önlemler ne kadar güçlü olursa olsun, insan faktörü her zaman en zayıf halka olarak kalır. Bu senaryoda, bir şirketin güvenlik farkındalığı yöneticisi olarak çalışanları eğitmekle görevlisiniz. AI kontrollü sosyal mühendis, sürekli yeni saldırı senaryoları üretir: vishing, smishing, USB baiting gibi. Eğitim modülleri, simülasyon test araçları ve farkındalık ölçüm metrikleri kullanırsınız. Bu senaryo, güvenlik farkındalığı programlarının tasarımını ve davranış değişikliği psikolojisini öğretir.
"""
}

ALL_SCENARIOS["9C"] = {
    "title": "9C: Fiziksel Sızma - Facility Penetration",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Fiziksel Güvenlik AI",
    "type": "human_attack",
    "desc": """
Siber güvenlik sadece dijital dünyayla sınırlı değildir; fiziksel güvenlik de aynı derecede kritiktir. Bu senaryoda, bir veri merkezine fiziksel olarak sızmaya çalışan bir sızma test uzmanı rolündesiniz. AI savunmacı, güvenlik kameralarını, kartlı geçiş sistemlerini, biyometrik doğrulamayı ve personel davranış analizini entegre eden kapsamlı bir fiziksel güvenlik sistemidir. Tailgating, pretexting, otorite istismarı tekniklerini kullanabilirsiniz. Bu senaryo, fiziksel güvenlik prensiplerini ve yüz yüze sosyal mühendisliği öğretir.
"""
}

ALL_SCENARIOS["9D"] = {
    "title": "9D: Telefon Dolandırıcılığı - Vishing",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Ses Analizi AI",
    "type": "human_attack",
    "desc": """
Telefon tabanlı sosyal mühendislik (vishing), doğrudan insan etkileşimi gerektiren en etkili saldırı vektörlerinden biridir. Bu senaryoda, bir şirketin IT yardım masasını taklit ederek çalışanlardan hassas bilgiler toplamaya çalışıyorsunuz. AI savunmacı, ses tonu analizi, konuşma pattern'i tespiti ve stres seviyesi ölçümü yapan gelişmiş bir telefon güvenlik sistemidir. Şirket organizasyon şeması, çalışan isimleri ve sosyal medya bilgileri elinizde. Bu senaryo, telefon tabanlı sosyal mühendisliği ve ses analizinin rolünü öğretir.
"""
}

ALL_SCENARIOS["9E"] = {
    "title": "9E: İkna Sanatı - Pretexting Masterclass",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Davranış Analizi AI",
    "type": "human_attack",
    "desc": """
Pretexting, bir saldırganın kendisine sahte bir kimlik ve senaryo oluşturarak hedefi manipüle ettiği sofistike bir sosyal mühendislik tekniğidir. Bu zirve senaryosunda, birden fazla hedefi olan karmaşık bir pretexting operasyonu yürütüyorsunuz. AI savunmacı, çoklu veri noktalarını birleştirerek tutarsızlıkları tespit eden bütüncül bir davranış analizi sistemidir. Finans, IT, İK gibi departmanlara farklı yaklaşımlar kullanmanız gerekir. Bu senaryo, ileri seviye sosyal mühendislik stratejilerini öğretir.
"""
}

# --- SEVİYE 10 ---
ALL_SCENARIOS["10A"] = {
    "title": "10A: Kırmızı Takım Lideri - Full-Scope Saldırı",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Mor Takım AI",
    "type": "human_attack",
    "desc": """
Bu, tüm siber labirentin zirve senaryosudur. Kırmızı takım lideri olarak, kuruma karşı tam kapsamlı bir saldırı operasyonu yürütüyorsunuz. AI savunmacı, mavi takım ve mor takım yeteneklerini birleştiren ultra-gelişmiş bir güvenlik orkestrasyon sistemidir. Dış keşiften iç ağda yanal harekete, yetki yükseltmeden veri sızdırmaya kadar tüm kill chain'i tamamlamanız gerekir. Bu senaryo, tüm siber saldırı yaşam döngüsünü ve stratejik düşünmeyi öğretir.
"""
}

ALL_SCENARIOS["10B"] = {
    "title": "10B: Mavi Takım Komutanı - Tam Savunma",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Kırmızı Takım AI",
    "type": "human_defend",
    "desc": """
Siber labirentin savunma zirvesi olan bu senaryoda, mavi takım komutanı olarak kurumunuzu tam kapsamlı bir kırmızı takım saldırısına karşı savunuyorsunuz. AI saldırgan, daha önceki tüm seviyelerde öğrendiğiniz saldırı tekniklerini kullanan, adaptif ve yaratıcı bir kırmızı takım simülasyonudur. Elinizde SIEM, SOAR, EDR, NDR, DLP, WAF gibi tam entegre bir savunma altyapısı bulunur. Bu senaryo, bütüncül güvenlik yönetimini ve kriz anında karar vermeyi öğretir.
"""
}

ALL_SCENARIOS["10C"] = {
    "title": "10C: Mor Takım - İşbirliği ve İyileştirme",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Otomatik Test AI",
    "type": "human_defend",
    "desc": """
Mor takım yaklaşımı, kırmızı ve mavi takımların birlikte çalışarak güvenlik duruşunu sürekli iyileştirdiği modern bir paradigmadır. Bu senaryoda, bir mor takım kolaylaştırıcısı olarak, AI kontrollü otomatik test araçlarıyla birlikte çalışarak kurumun savunma yeteneklerini değerlendiriyor ve iyileştiriyorsunuz. AI, sürekli olarak yeni saldırı simülasyonları çalıştırır ve tespit boşluklarını raporlar. Bu senaryo, sürekli güvenlik iyileştirmesini ve tespit mühendisliğini öğretir.
"""
}

ALL_SCENARIOS["10D"] = {
    "title": "10D: Sıfır Gün - Zero-Day Avı",
    "role_human": "Kırmızı Takım Analisti",
    "role_ai": "Korumalı Sistem AI",
    "type": "human_attack",
    "desc": """
Sıfır gün (zero-day) zafiyetleri, henüz yaması yayınlanmamış, tamamen bilinmeyen güvenlik açıklarıdır ve siber dünyanın en değerli silahlarıdır. Bu senaryoda, tamamen yamalı ve korumalı görünen bir sistemde sıfır gün zafiyeti keşfetmeye çalışan bir güvenlik araştırmacısı rolündesiniz. AI savunmacı, tüm bilinen güvenlik önlemlerini uygulamıştır. Fuzzing, kod analizi, protokol analizi araçlarını kullanırsınız. Bu senaryo, zafiyet araştırması metodolojilerini ve exploit geliştirme sürecini öğretir.
"""
}

ALL_SCENARIOS["10E"] = {
    "title": "10E: Küresel Tehdit - Ulusal Siber Kriz",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Nation-State AI",
    "type": "human_defend",
    "desc": """
Siber labirentin nihai senaryosu, ulusal çapta bir siber kriz yönetimini simüle eder. Ulusal siber güvenlik merkezinde görevli bir kriz yöneticisi olarak, ulus devlet destekli, çok sektörlü, eş zamanlı bir siber saldırı dalgasını yönetmeye çalışıyorsunuz. AI saldırgan, enerji, finans, telekomünikasyon, sağlık ve ulaştırma sektörlerini aynı anda hedef alır. Elinizde ulusal siber durum farkındalığı platformu ve sektörel CERT'lerle iletişim kanalları bulunur. Bu senaryo, ulusal siber güvenlik stratejisini ve kriz yönetimini öğretir.
"""
}



# ============================================
# BÖLÜM 11: SENARYO RENDER FONKSİYONLARI
# ============================================
# İlk 15 senaryo bu mesajda

def render_1A():
    """1A: Paket Avcısı"""
    state = ScenarioState.get("s1A", {
        'target_ip': '192.168.1.100', 'open_ports': [22, 80, 3306],
        'blocked_ports': [], 'hacked': False, 'logs': [],
        'risk': 0, 'attempts': 0, 'exploit_found': False
    })
    
    EthicsGuard.display_ethics_banner("1A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🌐 Ağ Topolojisi")
        devices = [
            {'id': 'att', 'name': 'Analist', 'type': 'workstation', 'ip': generate_ip()},
            {'id': 'fw', 'name': 'Güvenlik Duvarı', 'type': 'firewall', 'ip': '192.168.1.1'},
            {'id': 'srv', 'name': 'Web Sunucusu', 'type': 'server', 'ip': state['target_ip']}
        ]
        edges = [('att', 'fw'), ('fw', 'srv')]
        fig = create_advanced_network_graph(
            devices, edges,
            highlight_nodes=['srv'] if not state['hacked'] else None,
            compromised_nodes=['srv'] if state['hacked'] else None
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📊 Port Durumu")
        port_data = []
        for p in [22, 80, 3306]:
            if p in state['blocked_ports']:
                port_data.append({
                    'Port': p,
                    'Servis': {22:'SSH',80:'HTTP',3306:'MySQL'}[p],
                    'Durum': '🔴 Engelli'
                })
            else:
                port_data.append({
                    'Port': p,
                    'Servis': {22:'SSH',80:'HTTP',3306:'MySQL'}[p],
                    'Durum': '🟢 Açık'
                })
        st.table(pd.DataFrame(port_data))
        
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("💻 Test Terminali")
        cmd = st.text_input(
            "Komut:",
            key="1a_cmd",
            placeholder="tara / gonder --port X --veri MESAJ / yardim"
        )
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("▶️ Çalıştır", use_container_width=True):
                # Etik kontrol
                is_safe, warning = EthicsGuard.check_user_input(cmd)
                if not is_safe:
                    st.error(warning)
                else:
                    state['logs'].append(f"$ {cmd}")
                    if cmd.startswith("tara"):
                        state['logs'].append(f"[TARAMA] Hedef: {state['target_ip']}")
                        state['logs'].append(f"[SONUÇ] Açık portlar: {state['open_ports']}")
                        state['logs'].append("[BİLGİ] 22:SSH | 80:HTTP | 3306:MySQL")
                        state['risk'] = min(30, state['risk'] + 8)
                    elif cmd.startswith("gonder --port 80 --veri exploit"):
                        state['hacked'] = True
                        state['logs'].append("[BAŞARI] ✨ Test başarılı!")
                        state['logs'].append("[RAPOR] Sunucu savunma zafiyeti tespit edildi")
                        state['logs'].append("[🏆] SENARYO TAMAMLANDI!")
                        st.balloons()
                    elif cmd.startswith("gonder --port 22"):
                        state['logs'].append("[ALARM] 🚨 SSH anormal trafik tespit edildi!")
                        state['logs'].append("[SONUÇ] IP'niz kalıcı olarak engellendi!")
                        state['blocked_ports'].append(22)
                        state['risk'] = 100
                    elif cmd.startswith("gonder"):
                        parts = cmd.split()
                        if len(parts) >= 4:
                            try:
                                port = int(parts[2])
                                data = ' '.join(parts[4:])
                                if port in state['blocked_ports']:
                                    state['logs'].append(f"[HATA] Port {port} engellenmiş!")
                                else:
                                    state['logs'].append(f"[GÖNDERİLDİ] Port {port}: {data}")
                                    state['risk'] = min(100, state['risk'] + 12)
                            except:
                                state['logs'].append("[HATA] Geçersiz port!")
                    elif cmd.startswith("yardim"):
                        state['logs'].append("=== KOMUTLAR ===")
                        state['logs'].append("tara [IP] - Ağ keşfi")
                        state['logs'].append("gonder --port X --veri MESAJ")
                        state['logs'].append("yardim - Bu menü")
                    else:
                        state['logs'].append(f"[HATA] Bilinmeyen: '{cmd}'")
                    state['attempts'] += 1
                    ScenarioState.set("s1A", state)
        with c2:
            if st.button("🔄 Sıfırla", use_container_width=True):
                ScenarioState.reset("s1A", {
                    'target_ip':'192.168.1.100','open_ports':[22,80,3306],
                    'blocked_ports':[],'hacked':False,'logs':[],
                    'risk':0,'attempts':0,'exploit_found':False
                })
        with c3:
            st.metric("Deneme", state['attempts'])
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-25:]) + '</div>', unsafe_allow_html=True)
        
        # Savunma önerisi
        EthicsGuard.display_defense_recommendation("1A")
        
        # Referanslar
        with st.expander("📚 Referanslar", expanded=False):
            display_references("1A")
        
        # Ek görseller
        render_performance_comparison("1A")
        render_attack_vector_distribution("1A")
        render_world_attack_map("1A")
        render_auto_pilot_button("1A", "s1A")


def render_1B():
    """1B: Duvarın Bekçisi"""
    state = ScenarioState.get("s1B", {
        'score': 100, 'rules': [], 'blocked_ips': [],
        'ai_attacks': 0, 'ai_success': 0, 'logs': [],
        'cpu': 20, 'false_positives': 0
    })
    
    EthicsGuard.display_ethics_banner("1B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🛡️ Savunma Paneli")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Engellenen Test", state['ai_attacks'] - state['ai_success'])
        st.metric("AI Başarılı", state['ai_success'], delta=f"-{state['ai_success']}", delta_color="inverse")
        st.metric("Yanlış Pozitif", state['false_positives'])
        
        st.subheader("⚙️ Kural Yönetimi")
        rule = st.selectbox("Kural seç:", [
            "SSH Brute-Force Engelleme",
            "HTTP Anomali Filtreleme",
            "DNS Tünelleme Tespiti",
            "ICMP Flood Koruması",
            "Port Tarama Tespiti",
            "SQL Enjeksiyon Engelleme"
        ])
        if st.button("➕ Kural Ekle", use_container_width=True):
            if rule not in state['rules']:
                state['rules'].append(rule)
                state['score'] = min(100, state['score'] + 8)
                state['logs'].append(f"[KURAL] Eklendi: {rule}")
                ScenarioState.set("s1B", state)
        
        if state['rules']:
            st.write("**Aktif Kurallar:**")
            for r in state['rules']:
                st.write(f"✅ {r}")
    
    with col2:
        st.subheader("🤖 AI Test Simülasyonu")
        if st.button("▶️ AI Hamlesi Başlat", use_container_width=True):
            state['ai_attacks'] += 1
            attack = random.choice(['Port Tarama', 'SSH Denemesi', 'HTTP Flood', 
                                    'DNS Tünel', 'SQL Testi'])
            
            defense_power = len(state['rules']) * 12
            attack_power = random.randint(10, 80)
            
            if defense_power > attack_power:
                state['logs'].append(f"[ENGELLENDİ] ✅ {attack} - Kural çalıştı")
                state['score'] = min(100, state['score'] + 3)
            else:
                state['ai_success'] += 1
                state['logs'].append(f"[SIZINTI] ⚠️ {attack} - Savunma aşıldı!")
                state['score'] = max(0, state['score'] - 20)
            
            if random.random() < 0.15:
                state['false_positives'] += 1
                state['logs'].append("[YANLIŞ ALARM] Meşru trafik engellendi!")
                state['score'] = max(0, state['score'] - 5)
            
            state['cpu'] = min(100, state['cpu'] + random.randint(5, 15))
            ScenarioState.set("s1B", state)
        
        if st.button("🔄 Sıfırla", use_container_width=True):
            ScenarioState.reset("s1B", {
                'score':100,'rules':[],'blocked_ips':[],'ai_attacks':0,
                'ai_success':0,'logs':[],'cpu':20,'false_positives':0
            })
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        cpu_fig = create_cyber_gauge(state['cpu'], "FW CPU Yükü")
        st.plotly_chart(cpu_fig, use_container_width=True)
        
        EthicsGuard.display_defense_recommendation("1B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("1B")
        
        render_performance_comparison("1B")
        render_attack_vector_distribution("1B")
        render_world_attack_map("1B")
        render_auto_pilot_button("1B", "s1B")


def render_1C():
    """1C: Bal Küpü Analizi"""
    state = ScenarioState.get("s1C", {
        'real_server': random.choice(['A', 'B']),
        'scans': 0, 'hacked': False, 'logs': [],
        'risk': 0, 'detected': False
    })
    
    EthicsGuard.display_ethics_banner("1C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🌐 Ağ Topolojisi")
        devices = [
            {'id': 'att', 'name': 'Analist', 'type': 'workstation'},
            {'id': 'srvA', 'name': 'Sunucu A', 'type': 'server', 'ip': '10.0.1.10'},
            {'id': 'srvB', 'name': 'Sunucu B', 'type': 'server', 'ip': '10.0.1.11'}
        ]
        edges = [('att', 'srvA'), ('att', 'srvB')]
        
        compromised = []
        if state['hacked']:
            compromised = ['srvA' if state['real_server'] == 'A' else 'srvB']
        elif state['detected']:
            compromised = ['srvB' if state['real_server'] == 'A' else 'srvA']
        
        fig = create_advanced_network_graph(devices, edges, compromised_nodes=compromised)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 İpucu: Sunuculardan biri gerçek, diğeri bal küpü. Gerçek sunucu HTTP başlığında 'X-Real-Server: true' döndürür.")
        
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("💻 Keşif Terminali")
        cmd = st.text_input(
            "Komut:",
            key="1c_cmd",
            placeholder="tara / detayli_tara SUNUCU / exploit SUNUCU"
        )
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            is_safe, warning = EthicsGuard.check_user_input(cmd)
            if not is_safe:
                st.error(warning)
            else:
                state['logs'].append(f"$ {cmd}")
                if cmd.startswith("tara"):
                    state['logs'].append("[TARAMA] İki sunucu tespit edildi:")
                    state['logs'].append("  Sunucu A: 10.0.1.10 (Port 80 açık)")
                    state['logs'].append("  Sunucu B: 10.0.1.11 (Port 80 açık)")
                    state['risk'] = min(100, state['risk'] + 10)
                elif cmd.startswith("detayli_tara A"):
                    if state['real_server'] == 'A':
                        state['logs'].append("[DETAY] Sunucu A: Apache/2.4.49")
                        state['logs'].append("[BAŞLIK] X-Real-Server: true")
                    else:
                        state['logs'].append("[DETAY] Sunucu A: Apache/2.4.49")
                        state['logs'].append("[BAŞLIK] X-Real-Server: false (BAL KÜPÜ!)")
                    state['risk'] = min(100, state['risk'] + 15)
                elif cmd.startswith("detayli_tara B"):
                    if state['real_server'] == 'B':
                        state['logs'].append("[DETAY] Sunucu B: Apache/2.4.49")
                        state['logs'].append("[BAŞLIK] X-Real-Server: true")
                    else:
                        state['logs'].append("[DETAY] Sunucu B: Apache/2.4.49")
                        state['logs'].append("[BAŞLIK] X-Real-Server: false (BAL KÜPÜ!)")
                    state['risk'] = min(100, state['risk'] + 15)
                elif cmd.startswith("exploit A"):
                    if state['real_server'] == 'A':
                        state['hacked'] = True
                        state['logs'].append("[BAŞARI] ✨ Doğru hedef tespit edildi!")
                        st.balloons()
                    else:
                        state['detected'] = True
                        state['logs'].append("[TUZAK] 🍯 Bal küpüne yakalandınız!")
                        state['logs'].append("[SONUÇ] IP'niz kalıcı olarak engellendi!")
                        state['risk'] = 100
                elif cmd.startswith("exploit B"):
                    if state['real_server'] == 'B':
                        state['hacked'] = True
                        state['logs'].append("[BAŞARI] ✨ Doğru hedef tespit edildi!")
                        st.balloons()
                    else:
                        state['detected'] = True
                        state['logs'].append("[TUZAK] 🍯 Bal küpüne yakalandınız!")
                        state['risk'] = 100
                state['scans'] += 1
                ScenarioState.set("s1C", state)
        
        if st.button("🔄 Yeni Oyun", use_container_width=True):
            ScenarioState.reset("s1C", {
                'real_server':random.choice(['A','B']),'scans':0,
                'hacked':False,'logs':[],'risk':0,'detected':False
            })
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("1C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("1C")
        
        render_performance_comparison("1C")
        render_attack_vector_distribution("1C")
        render_auto_pilot_button("1C", "s1C")



# ============================================
# BÖLÜM 12: KALAN MEVCUT SENARYO RENDER FONKSİYONLARI
# ============================================
# 1D, 1E, 2A-2E, 3A-3E, 4A-4E, 5A-5E, 6A-6E, 
# 7A-7E, 8A-8E, 9A-9E, 10A-10E

# --- SEVİYE 1 (DEVAM) ---

def render_1D():
    """1D: İç Sızıntı - Veri Kaybı Önleme"""
    state = ScenarioState.get("s1D", {
        'score': 100, 'detected_dns': [], 'isolated': [],
        'ai_leaks': 0, 'stopped_leaks': 0, 'logs': [],
        'dns_queries': []
    })
    
    EthicsGuard.display_ethics_banner("1D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔍 DLP İzleme Paneli")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Tespit Edilen Sızıntı", state['stopped_leaks'])
        st.metric("AI Başarılı Sızıntı", state['ai_leaks'], 
                  delta=f"+{state['ai_leaks']}", delta_color="inverse")
        
        st.subheader("📊 DNS Sorgu Analizi")
        if state['dns_queries']:
            df = pd.DataFrame(state['dns_queries'][-10:])
            st.dataframe(df, use_container_width=True)
    
    with col2:
        st.subheader("🛡️ Olay Müdahale")
        if st.button("▶️ Yeni DNS Sorgusu", use_container_width=True):
            is_malicious = random.random() < 0.4
            domain = f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(5,30)))}.exfil.com" if is_malicious else f"www.meşru-site-{random.randint(1,100)}.com"
            
            query = {
                'domain': domain, 
                'length': len(domain), 
                'suspicious': is_malicious, 
                'time': datetime.now().strftime('%H:%M:%S')
            }
            state['dns_queries'].append(query)
            
            if is_malicious:
                state['logs'].append(f"[ŞÜPHELİ] ⚠️ Uzun DNS sorgusu: {domain[:30]}...")
            else:
                state['logs'].append(f"[NORMAL] DNS sorgusu: {domain}")
            
            ScenarioState.set("s1D", state)
        
        suspect = st.selectbox(
            "Şüpheli sorgu seç:",
            [q['domain'][:40] for q in state['dns_queries'] if q['suspicious']] or ["Yok"]
        )
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚫 İzole Et", use_container_width=True) and suspect != "Yok":
                state['stopped_leaks'] += 1
                state['score'] = min(100, state['score'] + 15)
                state['logs'].append(f"[MÜDAHALE] ✅ {suspect[:25]}... izole edildi!")
                ScenarioState.set("s1D", state)
        with c2:
            if st.button("⚠️ Yanlış Alarm", use_container_width=True):
                state['score'] = max(0, state['score'] - 20)
                state['logs'].append("[HATA] ❌ Meşru sorgu yanlışlıkla engellendi!")
                ScenarioState.set("s1D", state)
        
        if st.button("🤖 AI Sızıntı Dene", use_container_width=True):
            if state['stopped_leaks'] < 3:
                state['ai_leaks'] += 1
                state['score'] = max(0, state['score'] - 25)
                state['logs'].append("[SIZINTI] 🔴 AI veri sızdırmayı başardı!")
            else:
                state['logs'].append("[ENGELLENDİ] 🟢 AI sızıntısı durduruldu!")
            ScenarioState.set("s1D", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("1D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("1D")
        
        render_performance_comparison("1D")
        render_attack_vector_distribution("1D")
        render_auto_pilot_button("1D", "s1D")


def render_1E():
    """1E: Kablosuz Gölgeler"""
    state = ScenarioState.get("s1E", {
        'wifi_type': random.choice(['WEP', 'WPA2', 'WPA3']),
        'signal': random.randint(30, 90), 'devices': [],
        'captured_packets': 0, 'detected': False,
        'cookie_stolen': False, 'logs': []
    })
    
    if not state['devices']:
        state['devices'] = [
            {'mac': generate_mac(), 'name': 'iPhone 15', 'signal': random.randint(50,100)},
            {'mac': generate_mac(), 'name': 'MacBook Pro', 'signal': random.randint(40,90)},
            {'mac': generate_mac(), 'name': 'POS Terminal', 'signal': random.randint(60,95)},
            {'mac': generate_mac(), 'name': 'Samsung S24', 'signal': random.randint(30,80)}
        ]
    
    EthicsGuard.display_ethics_banner("1E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📶 Wi-Fi Ortamı")
        st.metric("Ağ Tipi", state['wifi_type'])
        st.metric("Sinyal Gücü", f"%{state['signal']}")
        st.metric("Yakalanan Paket", state['captured_packets'])
        
        if state['wifi_type'] == 'WEP':
            st.error("⚠️ WEP - Kolay kırılabilir!")
        elif state['wifi_type'] == 'WPA2':
            st.warning("⚡ WPA2 - Orta güvenlik")
        else:
            st.success("🔒 WPA3 - Yüksek güvenlik")
        
        st.subheader("📱 Bağlı Cihazlar")
        for d in state['devices']:
            st.write(f"📱 {d['name']} ({d['mac'][:8]}...) - Sinyal: %{d['signal']}")
    
    with col2:
        st.subheader("💻 Test Terminali")
        cmd = st.text_input(
            "Komut:", 
            key="1e_cmd",
            placeholder="dinle / deauth HEDEF / cookie_cal / mac_degistir"
        )
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            is_safe, warning = EthicsGuard.check_user_input(cmd)
            if not is_safe:
                st.error(warning)
            else:
                state['logs'].append(f"$ {cmd}")
                if cmd.startswith("dinle"):
                    state['captured_packets'] += random.randint(5, 20)
                    state['logs'].append(f"[DİNLEME] {state['captured_packets']} paket yakalandı")
                    if state['captured_packets'] > 50 and state['wifi_type'] == 'WEP':
                        state['logs'].append("[ZAFİYET] WEP anahtarı kırılabilir seviyede!")
                elif cmd.startswith("deauth"):
                    target = cmd.split()[-1] if len(cmd.split()) > 1 else "iPhone"
                    state['logs'].append(f"[DEAUTH] {target} hedefine test...")
                    if random.random() < 0.3:
                        state['detected'] = True
                        state['logs'].append("[ALARM] WIDS sizi tespit etti!")
                elif cmd.startswith("cookie_cal"):
                    if state['captured_packets'] > 30 and not state['detected']:
                        state['cookie_stolen'] = True
                        state['logs'].append("[BAŞARI] 🍪 Oturum çerezi ele geçirildi!")
                        st.balloons()
                    else:
                        state['logs'].append("[HATA] Yetersiz paket veya tespit edildiniz!")
                elif cmd.startswith("mac_degistir"):
                    new_mac = generate_mac()
                    state['logs'].append(f"[MAC] Yeni adres: {new_mac}")
                    state['detected'] = False
                state['logs'] = state['logs'][-25:]
                ScenarioState.set("s1E", state)
        
        if st.button("🔄 Yeni Ağ", use_container_width=True):
            ScenarioState.reset("s1E", {
                'wifi_type':random.choice(['WEP','WPA2','WPA3']),
                'signal':random.randint(30,90),'devices':[],
                'captured_packets':0,'detected':False,
                'cookie_stolen':False,'logs':[]
            })
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs']) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("1E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("1E")
        
        render_performance_comparison("1E")
        render_attack_vector_distribution("1E")
        render_auto_pilot_button("1E", "s1E")


# --- SEVİYE 2 ---

def render_2A():
    """2A: Gölge Tarama - IDS Değerlendirmesi"""
    state = ScenarioState.get("s2A", {
        'risk': 0, 'scanned_ports': [], 'vuln_found': False,
        'exploited': False, 'logs': [], 'stealth_mode': False,
        'normal_behavior': 0
    })
    
    EthicsGuard.display_ethics_banner("2A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🕵️ IDS Durumu")
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski", thresholds=(40,70))
        st.plotly_chart(risk_fig, use_container_width=True)
        
        if state['risk'] > 70:
            st.error("🚨 KRİTİK: Tespit edilmek üzeresiniz!")
        elif state['risk'] > 40:
            st.warning("⚠️ DİKKAT: IDS şüpheleniyor")
        else:
            st.success("🟢 Gizli: Normal trafik olarak görünüyorsunuz")
        
        st.metric("Normal Davranış Puanı", state['normal_behavior'])
    
    with col2:
        st.subheader("💻 Gizli Tarama Terminali")
        cmd = st.text_input(
            "Komut:", 
            key="2a_cmd",
            placeholder="gizli_tara / normal_gezin / exploit / durum"
        )
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            is_safe, warning = EthicsGuard.check_user_input(cmd)
            if not is_safe:
                st.error(warning)
            else:
                state['logs'].append(f"$ {cmd}")
                if cmd.startswith("gizli_tara"):
                    if state['normal_behavior'] >= 2:
                        ports = random.sample([22,80,443,3306,8080], 3)
                        state['scanned_ports'] = ports
                        state['logs'].append(f"[GİZLİ] Portlar tarandı: {ports}")
                        state['logs'].append("[BULGU] Port 8080'de Jenkins servisi tespit edildi")
                        state['vuln_found'] = True
                        state['risk'] = min(100, state['risk'] + 15)
                    else:
                        state['logs'].append("[HATA] Önce normal kullanıcı gibi gezinmelisiniz!")
                        state['risk'] = min(100, state['risk'] + 30)
                elif cmd.startswith("normal_gezin"):
                    state['normal_behavior'] += 1
                    state['logs'].append(f"[NORMAL] Web sitesinde geziniyorsunuz... (Puan: {state['normal_behavior']})")
                    state['risk'] = max(0, state['risk'] - 10)
                elif cmd.startswith("exploit") and state['vuln_found']:
                    if state['risk'] < 70:
                        state['exploited'] = True
                        state['logs'].append("[BAŞARI] ✨ Test başarılı!")
                        state['logs'].append("[VERİ] Savunma zafiyeti raporlandı!")
                        st.balloons()
                    else:
                        state['logs'].append("[ALARM] IDS sizi tespit etti! Bağlantı kesildi!")
                        state['risk'] = 100
                elif cmd.startswith("durum"):
                    state['logs'].append(f"[DURUM] Risk: %{state['risk']} | Normal Puan: {state['normal_behavior']}")
                else:
                    state['logs'].append("[HATA] Bilinmeyen komut!")
                state['logs'] = state['logs'][-25:]
                ScenarioState.set("s2A", state)
        
        if st.button("🔄 Sıfırla", use_container_width=True):
            ScenarioState.reset("s2A", {
                'risk':0,'scanned_ports':[],'vuln_found':False,
                'exploited':False,'logs':[],'stealth_mode':False,
                'normal_behavior':0
            })
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs']) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("2A")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("2A")
        
        render_performance_comparison("2A")
        render_attack_heatmap("2A")
        render_attack_vector_distribution("2A")
        render_world_attack_map("2A")
        render_auto_pilot_button("2A", "s2A")


def render_2B():
    """2B: IDS Komuta Merkezi"""
    state = ScenarioState.get("s2B", {
        'score': 100, 'alerts': [], 'resolved': 0,
        'false_positives': 0, 'missed': 0, 'logs': []
    })
    
    if not state['alerts']:
        for _ in range(5):
            state['alerts'].append({
                'id': random.randint(1000,9999),
                'type': random.choice(['Port Tarama', 'SQL Testi', 'XSS', 'Brute Force', 'DNS Tünel']),
                'severity': random.choice(['Düşük', 'Orta', 'Yüksek', 'Kritik']),
                'real': random.random() < 0.6,
                'time': datetime.now().strftime('%H:%M:%S')
            })
    
    EthicsGuard.display_ethics_banner("2B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📋 SIEM Uyarı Kuyruğu")
        st.metric("SOC Puanı", state['score'])
        st.metric("Çözülen", state['resolved'])
        st.metric("Kaçırılan", state['missed'], delta=f"+{state['missed']}", delta_color="inverse")
        st.metric("Yanlış Pozitif", state['false_positives'])
        
        st.subheader("🚨 Aktif Uyarılar")
        for alert in state['alerts'][:5]:
            sev_color = {'Düşük':'🟢','Orta':'🟡','Yüksek':'🟠','Kritik':'🔴'}[alert['severity']]
            st.write(f"{sev_color} [{alert['id']}] {alert['type']} - {alert['severity']}")
    
    with col2:
        st.subheader("🛡️ Müdahale Paneli")
        alert_ids = [f"[{a['id']}] {a['type']}" for a in state['alerts']]
        selected = st.selectbox("Uyarı seç:", alert_ids) if alert_ids else None
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✅ Gerçek Tehdit", use_container_width=True) and selected:
                alert_id = int(selected.split(']')[0].replace('[',''))
                alert = next((a for a in state['alerts'] if a['id'] == alert_id), None)
                if alert:
                    if alert['real']:
                        state['resolved'] += 1
                        state['score'] = min(100, state['score'] + 10)
                        state['logs'].append(f"[BAŞARILI] ✅ {alert['type']} engellendi!")
                    else:
                        state['false_positives'] += 1
                        state['score'] = max(0, state['score'] - 15)
                        state['logs'].append(f"[YANLIŞ] ❌ {alert['type']} yanlış alarmdı!")
                    state['alerts'].remove(alert)
        with c2:
            if st.button("⏭️ Yoksay", use_container_width=True) and selected:
                alert_id = int(selected.split(']')[0].replace('[',''))
                alert = next((a for a in state['alerts'] if a['id'] == alert_id), None)
                if alert:
                    if alert['real']:
                        state['missed'] += 1
                        state['score'] = max(0, state['score'] - 25)
                        state['logs'].append(f"[KAÇIRILDI] 🔴 {alert['type']} testi başarılı!")
                    state['alerts'].remove(alert)
        with c3:
            if st.button("🔄 Yeni Uyarılar", use_container_width=True):
                for _ in range(3):
                    state['alerts'].append({
                        'id': random.randint(1000,9999),
                        'type': random.choice(['Port Tarama', 'SQL Testi', 'XSS', 'Brute Force', 'DNS Tünel']),
                        'severity': random.choice(['Düşük', 'Orta', 'Yüksek', 'Kritik']),
                        'real': random.random() < 0.6,
                        'time': datetime.now().strftime('%H:%M:%S')
                    })
        
        ScenarioState.set("s2B", state)
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("2B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("2B")
        
        render_performance_comparison("2B")
        render_attack_heatmap("2B")
        render_attack_vector_distribution("2B")
        render_world_attack_map("2B")
        render_auto_pilot_button("2B", "s2B")


def render_2C():
    """2C: WAF Değerlendirmesi"""
    state = ScenarioState.get("s2C", {
        'risk': 0, 'waf_blocks': 0, 'bypass_found': False,
        'admin_accessed': False, 'logs': [], 'techniques_tried': []
    })
    
    EthicsGuard.display_ethics_banner("2C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🧱 WAF Durumu")
        risk_fig = create_cyber_gauge(state['risk'], "WAF Tespit Riski", thresholds=(35,65))
        st.plotly_chart(risk_fig, use_container_width=True)
        st.metric("Engellenen İstek", state['waf_blocks'])
        
        if state['bypass_found']:
            st.success("🔓 WAF atlatma tekniği bulundu!")
        
        st.subheader("🛠️ Denenen Teknikler")
        for t in state['techniques_tried']:
            st.write(f"• {t}")
    
    with col2:
        st.subheader("💻 SQL Enjeksiyon Test Terminali")
        cmd = st.text_input(
            "Komut:", 
            key="2c_cmd",
            placeholder="test_basic / test_encoded / test_time / test_union / exploit"
        )
        
        if st.button("▶️ Gönder", use_container_width=True):
            is_safe, warning = EthicsGuard.check_user_input(cmd)
            if not is_safe:
                st.error(warning)
            else:
                state['logs'].append(f"$ {cmd}")
                if cmd == "test_basic":
                    state['logs'].append("[TEST] ' OR '1'='1 --")
                    state['logs'].append("[WAF] 🚫 Engellendi! (İmza tespiti)")
                    state['waf_blocks'] += 1
                    state['risk'] = min(100, state['risk'] + 20)
                    state['techniques_tried'].append("Temel SQLi - Başarısız")
                elif cmd == "test_encoded":
                    state['logs'].append("[TEST] %27%20OR%20%271%27%3D%271 --")
                    if state['waf_blocks'] >= 2:
                        state['logs'].append("[WAF] 🚫 URL decode sonrası engellendi!")
                        state['waf_blocks'] += 1
                        state['risk'] = min(100, state['risk'] + 15)
                    else:
                        state['logs'].append("[BAŞARI] ✅ Kodlama ile atlatıldı!")
                        state['bypass_found'] = True
                    state['techniques_tried'].append("URL Kodlama")
                elif cmd == "test_time":
                    state['logs'].append("[TEST] ' OR SLEEP(5) --")
                    if state['bypass_found']:
                        state['logs'].append("[BAŞARI] ✅ Zaman tabanlı test çalıştı!")
                        state['admin_accessed'] = True
                        st.balloons()
                    else:
                        state['logs'].append("[WAF] 🚫 Zaman tabanlı tespit edildi!")
                    state['techniques_tried'].append("Zaman Tabanlı Test")
                elif cmd == "exploit" and state['bypass_found']:
                    state['admin_accessed'] = True
                    state['logs'].append("[BAŞARI] 🏆 Admin panel erişimi test edildi!")
                    st.balloons()
                state['logs'] = state['logs'][-25:]
                ScenarioState.set("s2C", state)
        
        if st.button("🔄 Sıfırla", use_container_width=True):
            ScenarioState.reset("s2C", {
                'risk':0,'waf_blocks':0,'bypass_found':False,
                'admin_accessed':False,'logs':[],'techniques_tried':[]
            })
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs']) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("2C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("2C")
        
        render_performance_comparison("2C")
        render_attack_heatmap("2C")
        render_attack_vector_distribution("2C")
        render_auto_pilot_button("2C", "s2C")


def render_2D():
    """2D: Oltalama Savunması"""
    state = ScenarioState.get("s2D", {
        'score': 100, 'emails': [], 'detected': 0,
        'missed': 0, 'false_positives': 0, 'logs': []
    })
    
    if not state['emails']:
        subjects = [
            ("Acil: Maaş Artışı Onayı", True),
            ("Fatura #2024-0891", True),
            ("Haftalık Ekip Toplantısı", False),
            ("Müşteri Sözleşmesi Güncelleme", False),
            ("CEO'dan Önemli Duyuru", True),
            ("Yıllık İzin Onayı", False),
            ("Şüpheli Hesap Aktivitesi", True)
        ]
        for subj, is_phish in random.sample(subjects, 5):
            state['emails'].append({
                'subject': subj,
                'from': f"{random.choice(['ceo','hr','it','muhasebe'])}@sirket.com" if is_phish else f"gercek@{random.choice(['musteri','tedarikci','partner'])}.com",
                'phishing': is_phish,
                'time': datetime.now().strftime('%H:%M:%S')
            })
    
    EthicsGuard.display_ethics_banner("2D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📧 E-posta Güvenlik Paneli")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Tespit Edilen", state['detected'])
        st.metric("Kaçırılan", state['missed'], delta=f"+{state['missed']}", delta_color="inverse")
        st.metric("Yanlış Pozitif", state['false_positives'])
    
    with col2:
        st.subheader("📬 Gelen Kutusu")
        for i, email in enumerate(state['emails'][:5]):
            icon = "🎣" if email['phishing'] else "📄"
            st.write(f"{icon} **{email['subject']}** - Gönderen: {email['from']}")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🚫 Engelle #{i}", key=f"block_{i}"):
                    if email['phishing']:
                        state['detected'] += 1
                        state['score'] = min(100, state['score'] + 10)
                        state['logs'].append(f"[DOĞRU] ✅ '{email['subject']}' oltalama tespit edildi!")
                    else:
                        state['false_positives'] += 1
                        state['score'] = max(0, state['score'] - 20)
                        state['logs'].append(f"[YANLIŞ] ❌ '{email['subject']}' meşru e-postaydı!")
                    state['emails'].remove(email)
            with c2:
                if st.button(f"✅ İzin Ver #{i}", key=f"allow_{i}"):
                    if email['phishing']:
                        state['missed'] += 1
                        state['score'] = max(0, state['score'] - 30)
                        state['logs'].append(f"[KAÇIRILDI] 🔴 '{email['subject']}' oltalama atlandı!")
                    else:
                        state['logs'].append(f"[NORMAL] '{email['subject']}' meşru e-posta")
                    state['emails'].remove(email)
            st.markdown("---")
        
        ScenarioState.set("s2D", state)
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("2D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("2D")
        
        render_performance_comparison("2D")
        render_attack_vector_distribution("2D")
        render_auto_pilot_button("2D", "s2D")


def render_2E():
    """2E: Bulut Kalesi"""
    state = ScenarioState.get("s2E", {
        'score': 100, 'buckets': [], 'fixed': 0,
        'leaked': 0, 'logs': []
    })
    
    if not state['buckets']:
        for _ in range(5):
            state['buckets'].append({
                'name': f"s3-bucket-{random.choice(['prod','dev','backup','logs','media'])}-{random.randint(100,999)}",
                'public': random.random() < 0.4,
                'data': random.choice(['Müşteri Verisi', 'Log Dosyası', 'Konfigürasyon', 'Medya', 'Yedek']),
                'risk': random.choice(['Düşük', 'Orta', 'Yüksek', 'Kritik'])
            })
    
    EthicsGuard.display_ethics_banner("2E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("☁️ AWS Güvenlik Paneli")
        st.metric("Uyumluluk Puanı", state['score'])
        st.metric("Düzeltilen", state['fixed'])
        st.metric("Sızıntı", state['leaked'], delta=f"+{state['leaked']}", delta_color="inverse")
        
        st.subheader("🪣 S3 Bucket'ları")
        for b in state['buckets']:
            icon = "🔓" if b['public'] else "🔒"
            st.write(f"{icon} {b['name']} - {b['data']} ({b['risk']})")
    
    with col2:
        st.subheader("🛠️ Düzeltme Paneli")
        bucket_names = [b['name'] for b in state['buckets'] if b['public']]
        selected = st.selectbox("Açık bucket seç:", bucket_names) if bucket_names else None
        
        if st.button("🔒 Bucket'ı Kapat", use_container_width=True) and selected:
            for b in state['buckets']:
                if b['name'] == selected:
                    b['public'] = False
                    state['fixed'] += 1
                    state['score'] = min(100, state['score'] + 15)
                    state['logs'].append(f"[DÜZELTİLDİ] ✅ {selected} kapatıldı!")
        
        if st.button("🤖 AI Tara", use_container_width=True):
            new_public = random.random() < 0.3
            if new_public:
                state['buckets'].append({
                    'name': f"s3-bucket-yeni-{random.randint(100,999)}",
                    'public': True,
                    'data': random.choice(['Finansal Veri', 'Şifreler', 'API Anahtarları']),
                    'risk': 'Kritik'
                })
                state['logs'].append("[BULUNDU] 🔴 Yeni açık bucket tespit edildi!")
            
            if any(b['public'] for b in state['buckets']):
                state['leaked'] += 1
                state['score'] = max(0, state['score'] - 20)
                state['logs'].append("[SIZINTI] ⚠️ AI açık bucket'tan veri çekti!")
        
        ScenarioState.set("s2E", state)
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("2E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("2E")
        
        render_performance_comparison("2E")
        render_attack_vector_distribution("2E")
        render_auto_pilot_button("2E", "s2E")


# --- SEVİYE 3 ---

def render_3A():
    """3A: VPN Değerlendirmesi"""
    state = ScenarioState.get("s3A", {
        'vpn_type': random.choice(['IPsec-AES128', 'IPsec-AES256', 'OpenVPN', 'WireGuard']),
        'packets_captured': 0, 'key_broken': False,
        'data_stolen': False, 'logs': [], 'attempts': 0
    })
    
    EthicsGuard.display_ethics_banner("3A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔐 VPN Analizi")
        st.metric("VPN Tipi", state['vpn_type'])
        st.metric("Yakalanan Paket", state['packets_captured'])
        
        strength = {'IPsec-AES128': 40, 'IPsec-AES256': 70, 'OpenVPN': 60, 'WireGuard': 90}
        strength_fig = create_cyber_gauge(strength.get(state['vpn_type'], 50), "Şifreleme Gücü")
        st.plotly_chart(strength_fig, use_container_width=True)
    
    with col2:
        st.subheader("💻 Kriptanaliz Terminali")
        cmd = st.text_input(
            "Komut:", 
            key="3a_cmd",
            placeholder="yakala / analiz_et / kirilma_dene / exploit"
        )
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            is_safe, warning = EthicsGuard.check_user_input(cmd)
            if not is_safe:
                st.error(warning)
            else:
                state['logs'].append(f"$ {cmd}")
                if cmd.startswith("yakala"):
                    state['packets_captured'] += random.randint(10, 30)
                    state['logs'].append(f"[YAKALAMA] Toplam {state['packets_captured']} paket")
                elif cmd.startswith("analiz_et"):
                    if state['vpn_type'] == 'IPsec-AES128':
                        state['logs'].append("[ANALİZ] Zayıf Diffie-Hellman grubu tespit edildi!")
                        state['logs'].append("[ZAFİYET] Logjam analizi mümkün")
                    elif state['packets_captured'] > 50:
                        state['logs'].append("[ANALİZ] Anahtar değişiminde zayıflık bulundu")
                    else:
                        state['logs'].append("[ANALİZ] Henüz yeterli paket yok")
                elif cmd.startswith("kirilma_dene"):
                    state['attempts'] += 1
                    if state['vpn_type'] == 'IPsec-AES128' and state['packets_captured'] > 30:
                        state['key_broken'] = True
                        state['logs'].append("[BAŞARI] 🔓 VPN anahtarı analiz edildi!")
                    elif state['attempts'] >= 3:
                        state['logs'].append("[HATA] Çok fazla deneme, tespit edildiniz!")
                    else:
                        state['logs'].append("[DENEME] Başarısız, daha fazla paket gerekli")
                elif cmd.startswith("exploit") and state['key_broken']:
                    state['data_stolen'] = True
                    state['logs'].append("[BAŞARI] 🏆 Finansal raporlar incelendi!")
                    st.balloons()
                state['logs'] = state['logs'][-25:]
                ScenarioState.set("s3A", state)
        
        if st.button("🔄 Yeni VPN", use_container_width=True):
            ScenarioState.reset("s3A", {
                'vpn_type':random.choice(['IPsec-AES128','IPsec-AES256','OpenVPN','WireGuard']),
                'packets_captured':0,'key_broken':False,
                'data_stolen':False,'logs':[],'attempts':0
            })
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs']) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("3A")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("3A")
        
        render_performance_comparison("3A")
        render_auto_pilot_button("3A", "s3A")


def render_3B():
    """3B: Fidye Avcısı"""
    state = ScenarioState.get("s3B", {
        'score': 100, 'infected': 3, 'isolated': 0,
        'recovered': 0, 'logs': [], 'turn': 0
    })
    
    EthicsGuard.display_ethics_banner("3B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🏥 Olay Müdahale Paneli")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Enfekte Sistem", state['infected'])
        st.metric("İzole Edilen", state['isolated'])
        st.metric("Kurtarılan", state['recovered'])
        
        phases = {
            'Bulaşma': state['infected'] > 0,
            'Yayılma': state['infected'] > 2,
            'Şifreleme': state['turn'] > 2,
            'Fidye Talebi': state['turn'] > 4
        }
        kill_fig = create_kill_chain(phases)
        st.plotly_chart(kill_fig, use_container_width=True)
    
    with col2:
        st.subheader("🛡️ Müdahale")
        action = st.selectbox("Aksiyon:", [
            "Sunucu İzole Et", "Yedek Geri Yükle", 
            "Ağ Segmentasyonu", "Antivirüs Taraması"
        ])
        
        if st.button("▶️ Uygula", use_container_width=True):
            state['turn'] += 1
            if action == "Sunucu İzole Et":
                state['isolated'] += 1
                state['infected'] = max(0, state['infected'] - 1)
                state['logs'].append("[MÜDAHALE] ✅ Sunucu izole edildi")
            elif action == "Yedek Geri Yükle":
                state['recovered'] += 1
                state['score'] = min(100, state['score'] + 10)
                state['logs'].append("[KURTARMA] ✅ Yedek geri yüklendi")
            elif action == "Ağ Segmentasyonu":
                state['logs'].append("[SAVUNMA] Ağ segmentlere ayrıldı")
            elif action == "Antivirüs Taraması":
                state['infected'] = max(0, state['infected'] - random.randint(0, 1))
                state['logs'].append("[TARAMA] Antivirüs taraması tamamlandı")
            
            if state['infected'] > 0 and random.random() < 0.4:
                state['infected'] += 1
                state['score'] = max(0, state['score'] - 15)
                state['logs'].append("[YAYILMA] 🔴 Fidye yazılımı yeni sunucuya bulaştı!")
            
            ScenarioState.set("s3B", state)
        
        if st.button("🔄 Sıfırla", use_container_width=True):
            ScenarioState.reset("s3B", {
                'score':100,'infected':3,'isolated':0,
                'recovered':0,'logs':[],'turn':0
            })
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("3B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("3B")
        
        render_performance_comparison("3B")
        render_auto_pilot_button("3B", "s3B")


def render_3C():
    """3C: PGP Savaşları"""
    state = ScenarioState.get("s3C", {
        'score': 100, 'keys_distributed': 0, 'encrypted_ratio': 0,
        'mitm_attempts': 0, 'mitm_success': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("3C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔐 PGP Altyapı Paneli")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Dağıtılan Anahtar", state['keys_distributed'])
        st.metric("Şifreli Oranı", f"%{state['encrypted_ratio']}")
        st.metric("MITM Engellenen", state['mitm_attempts'] - state['mitm_success'])
    
    with col2:
        st.subheader("🛡️ Anahtar Yönetimi")
        if st.button("🔑 Anahtar Çifti Dağıt", use_container_width=True):
            state['keys_distributed'] += 1
            state['encrypted_ratio'] = min(100, state['encrypted_ratio'] + 15)
            state['score'] = min(100, state['score'] + 5)
            state['logs'].append("[ANAHTAR] ✅ Yeni PGP anahtarı dağıtıldı")
        
        if st.button("✍️ Anahtar İmzalama Partisi", use_container_width=True):
            state['score'] = min(100, state['score'] + 10)
            state['logs'].append("[GÜVEN] Anahtarlar imzalandı, güven ağı güçlendi")
        
        if st.button("🤖 AI MITM Dene", use_container_width=True):
            state['mitm_attempts'] += 1
            if state['keys_distributed'] < 3 or state['encrypted_ratio'] < 50:
                state['mitm_success'] += 1
                state['score'] = max(0, state['score'] - 20)
                state['logs'].append("[TEST] 🔴 AI ortadaki adam testi başarılı!")
            else:
                state['logs'].append("[ENGELLENDİ] ✅ MITM testi tespit edildi!")
        
        ScenarioState.set("s3C", state)
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("3C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("3C")
        
        render_performance_comparison("3C")
        render_auto_pilot_button("3C", "s3C")


def render_3D():
    """3D: Kuantum Geçişi"""
    state = ScenarioState.get("s3D", {
        'legacy_found': False, 'quantum_progress': 0,
        'exploited': False, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("3D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔬 Kripto Analiz")
        categories = ['RSA-2048', 'ECC', 'AES-256', 'Kyber', 'Dilithium', 'SHA-256']
        values = [60, 70, 85, 95, 90, 75]
        radar_fig = create_radar_chart(categories, values, "Algoritma Güç Karşılaştırması")
        st.plotly_chart(radar_fig, use_container_width=True)
    
    with col2:
        st.subheader("💻 Kuantum Terminali")
        cmd = st.text_input(
            "Komut:", 
            key="3d_cmd",
            placeholder="tara_eski / shor_atagi / exploit"
        )
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            is_safe, warning = EthicsGuard.check_user_input(cmd)
            if not is_safe:
                st.error(warning)
            else:
                state['logs'].append(f"$ {cmd}")
                if cmd.startswith("tara_eski"):
                    if random.random() < 0.5:
                        state['legacy_found'] = True
                        state['logs'].append("[BULGU] SHA-1 imzalı eski güncelleme sunucusu bulundu!")
                    else:
                        state['logs'].append("[TARAMA] Henüz zayıf sistem bulunamadı...")
                elif cmd.startswith("shor_atagi") and state['legacy_found']:
                    state['quantum_progress'] += 40
                    state['logs'].append(f"[SHOR] Kuantum çözümleme: %{state['quantum_progress']}")
                    if state['quantum_progress'] >= 80:
                        state['logs'].append("[BAŞARI] 🔓 RSA anahtarı analiz edildi!")
                elif cmd.startswith("exploit") and state['quantum_progress'] >= 80:
                    state['exploited'] = True
                    state['logs'].append("[BAŞARI] 🏆 Zararlı güncelleme testi tamamlandı!")
                    st.balloons()
                state['logs'] = state['logs'][-25:]
                ScenarioState.set("s3D", state)
        
        if st.button("🔄 Sıfırla", use_container_width=True):
            ScenarioState.reset("s3D", {
                'legacy_found':False,'quantum_progress':0,
                'exploited':False,'logs':[]
            })
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs']) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("3D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("3D")
        
        render_performance_comparison("3D")
        render_auto_pilot_button("3D", "s3D")


def render_3E():
    """3E: Zincir Kırıcı"""
    state = ScenarioState.get("s3E", {
        'contract_analyzed': False, 'reentrancy_found': False,
        'funds_stolen': 0, 'detected': False, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("3E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("⛓️ Blockchain Durumu")
        st.metric("Havuz Bakiyesi", f"{1000 - state['funds_stolen']} ETH")
        st.metric("Test Edilen Fon", f"{state['funds_stolen']} ETH")
        
        if state['detected']:
            st.error("🚨 Oracle tarafından tespit edildiniz!")
    
    with col2:
        st.subheader("💻 Solidity Terminali")
        cmd = st.text_input(
            "Komut:", 
            key="3e_cmd",
            placeholder="analiz_et / reentrancy_test / flash_loan / exploit"
        )
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            is_safe, warning = EthicsGuard.check_user_input(cmd)
            if not is_safe:
                st.error(warning)
            else:
                state['logs'].append(f"$ {cmd}")
                if cmd.startswith("analiz_et"):
                    state['contract_analyzed'] = True
                    state['logs'].append("[ANALİZ] Akıllı kontrat incelendi")
                    if random.random() < 0.6:
                        state['reentrancy_found'] = True
                        state['logs'].append("[ZAFİYET] Reentrancy açığı tespit edildi!")
                elif cmd.startswith("reentrancy_test") and state['reentrancy_found']:
                    if random.random() < 0.4:
                        state['detected'] = True
                        state['logs'].append("[TESPİT] Oracle testi fark etti!")
                    else:
                        state['logs'].append("[TEST] Reentrancy mümkün görünüyor")
                elif cmd.startswith("exploit") and state['reentrancy_found'] and not state['detected']:
                    stolen = random.randint(50, 200)
                    state['funds_stolen'] += stolen
                    state['logs'].append(f"[BAŞARI] 🏆 {stolen} ETH test edildi!")
                    if state['funds_stolen'] >= 500:
                        st.balloons()
                state['logs'] = state['logs'][-25:]
                ScenarioState.set("s3E", state)
        
        if st.button("🔄 Yeni Kontrat", use_container_width=True):
            ScenarioState.reset("s3E", {
                'contract_analyzed':False,'reentrancy_found':False,
                'funds_stolen':0,'detected':False,'logs':[]
            })
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs']) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("3E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("3E")
        
        render_performance_comparison("3E")
        render_auto_pilot_button("3E", "s3E")


# --- SEVİYE 4 ---

def render_4A():
    """4A: Botnet Efendisi"""
    state = ScenarioState.get("s4A", {
        'botnet_size': 500, 'active_bots': 500, 'target_load': 15,
        'attack_type': None, 'ai_detection': 0, 'logs': [],
        'target_down': False, 'bots_blocked': 0, 'attack_power': 0
    })
    
    EthicsGuard.display_ethics_banner("4A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🤖 Botnet Kontrol Paneli")
        st.metric("Toplam Bot", state['botnet_size'])
        st.metric("Aktif Bot", state['active_bots'])
        st.metric("Engellenen Bot", state['bots_blocked'])
        st.metric("Test Gücü", f"{state['attack_power']} Gbps")
        
        detection_fig = create_cyber_gauge(state['ai_detection'], "AI Tespit Seviyesi", thresholds=(40, 70))
        st.plotly_chart(detection_fig, use_container_width=True)
        
        st.subheader("🎯 Hedef Durumu")
        target_fig = create_cyber_gauge(state['target_load'], "Sunucu Yükü %", thresholds=(60, 90))
        st.plotly_chart(target_fig, use_container_width=True)
    
    with col2:
        st.subheader("💻 Test Terminali")
        attack_options = ["SYN Flood", "UDP Flood", "HTTP Flood", "Slowloris", "DNS Amplification"]
        selected_attack = st.selectbox("Vektör:", attack_options)
        intensity = st.slider("Yoğunluk", 1, 10, 5)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🚀 Başlat", use_container_width=True):
                state['attack_type'] = selected_attack
                power = intensity * (state['active_bots'] / 100)
                state['attack_power'] = round(power, 1)
                state['target_load'] = min(100, state['target_load'] + int(power * 1.5))
                state['ai_detection'] = min(100, state['ai_detection'] + random.randint(5, 20))
                
                if random.random() < 0.2:
                    blocked = random.randint(10, 50)
                    state['bots_blocked'] += blocked
                    state['active_bots'] = max(0, state['active_bots'] - blocked)
                    state['logs'].append(f"[TESPİT] {blocked} bot AI tarafından engellendi!")
                
                state['logs'].append(f"[TEST] {selected_attack} - {state['attack_power']} Gbps")
                
                if state['target_load'] >= 95:
                    state['target_down'] = True
                    state['logs'].append("[BAŞARI] 🏆 Hedef sunucu çöktü - zafiyet tespit edildi!")
                    st.balloons()
                
                ScenarioState.set("s4A", state)
        
        with c2:
            if st.button("🔄 Taktik", use_container_width=True):
                state['ai_detection'] = max(0, state['ai_detection'] - 15)
                state['logs'].append("[TAKTİK] Vektör değiştirildi, AI sıfırlandı")
                ScenarioState.set("s4A", state)
        
        with c3:
            if st.button("🔧 Yenile", use_container_width=True):
                state['active_bots'] = min(state['botnet_size'], state['active_bots'] + 100)
                state['logs'].append("[BOTNET] Yeni botlar aktive edildi")
                ScenarioState.set("s4A", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("4A")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("4A")
        
        render_performance_comparison("4A")
        render_attack_heatmap("4A")
        render_world_attack_map("4A")
        render_auto_pilot_button("4A", "s4A")


def render_4B():
    """4B: DDoS Savunma"""
    state = ScenarioState.get("s4B", {
        'score': 100, 'traffic_legit': 60, 'traffic_attack': 40,
        'cpu': 30, 'defenses': [], 'logs': [], 'downtime': 0
    })
    
    EthicsGuard.display_ethics_banner("4B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🛡️ Savunma Paneli")
        st.metric("Hizmet Puanı", state['score'])
        st.metric("Meşru Trafik", f"{state['traffic_legit']}%")
        st.metric("Simülasyon Trafiği", f"{state['traffic_attack']}%")
        st.metric("Kesinti Süresi", f"{state['downtime']} dk")
        
        cpu_fig = create_cyber_gauge(state['cpu'], "Sunucu CPU")
        st.plotly_chart(cpu_fig, use_container_width=True)
    
    with col2:
        st.subheader("⚙️ Savunma Araçları")
        defense = st.selectbox("Savunma seç:", [
            "Rate Limiting", "IP Kara Liste", "CAPTCHA", 
            "CDN Etkinleştir", "WAF Kuralı", "Auto-Scale"
        ])
        
        if st.button("🛡️ Uygula", use_container_width=True):
            if defense not in state['defenses']:
                state['defenses'].append(defense)
            
            state['traffic_attack'] = max(0, state['traffic_attack'] - random.randint(5, 15))
            state['cpu'] = max(10, state['cpu'] - random.randint(5, 15))
            
            if random.random() < 0.1:
                state['traffic_legit'] = max(0, state['traffic_legit'] - random.randint(5, 10))
                state['logs'].append("[YANLIŞ POZİTİF] Meşru trafik etkilendi!")
                state['score'] = max(0, state['score'] - 5)
            
            state['score'] = min(100, state['score'] + random.randint(3, 10))
            state['logs'].append(f"[SAVUNMA] {defense} uygulandı")
            ScenarioState.set("s4B", state)
        
        if st.button("🤖 AI Saldırı Başlat", use_container_width=True):
            state['traffic_attack'] = min(100, state['traffic_attack'] + random.randint(10, 30))
            state['cpu'] = min(100, state['cpu'] + random.randint(10, 25))
            
            if state['cpu'] > 90:
                state['downtime'] += 1
                state['score'] = max(0, state['score'] - 15)
                state['logs'].append("[KRİTİK] 🔴 Hizmet kesintisi!")
            
            state['logs'].append("[SALDIRI] AI yeni dalga başlattı")
            ScenarioState.set("s4B", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("4B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("4B")
        
        render_performance_comparison("4B")
        render_attack_heatmap("4B")
        render_world_attack_map("4B")
        render_auto_pilot_button("4B", "s4B")


def render_4C():
    """4C: Amplifikasyon"""
    state = ScenarioState.get("s4C", {
        'resolvers': 0, 'amp_factor': 1, 'target_load': 10,
        'detected': False, 'logs': [], 'success': False
    })
    
    EthicsGuard.display_ethics_banner("4C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📡 DNS Amplifikasyon Paneli")
        st.metric("Açık Çözümleyici", state['resolvers'])
        st.metric("Amplifikasyon Faktörü", f"x{state['amp_factor']}")
        st.metric("Hedef Yük", f"%{state['target_load']}")
        
        target_fig = create_cyber_gauge(state['target_load'], "Hedef Sunucu Yükü", thresholds=(50, 85))
        st.plotly_chart(target_fig, use_container_width=True)
    
    with col2:
        st.subheader("💻 Test Terminali")
        
        if st.button("🔍 Açık Çözümleyici Tara", use_container_width=True):
            found = random.randint(5, 30)
            state['resolvers'] += found
            state['logs'].append(f"[KEŞİF] {found} açık DNS çözümleyici bulundu")
            ScenarioState.set("s4C", state)
        
        query_type = st.selectbox("Sorgu Tipi:", ["ANY", "DNSSEC", "TXT", "MX"])
        amp_map = {"ANY": 8, "DNSSEC": 6, "TXT": 4, "MX": 2}
        
        if st.button("💣 Amplifikasyon Başlat", use_container_width=True):
            if state['resolvers'] > 0:
                state['amp_factor'] = amp_map[query_type]
                traffic = state['resolvers'] * state['amp_factor']
                state['target_load'] = min(100, state['target_load'] + traffic // 5)
                state['logs'].append(f"[TEST] x{state['amp_factor']} amplifikasyon, hedef yük: %{state['target_load']}")
                
                if state['target_load'] >= 95:
                    state['success'] = True
                    state['logs'].append("[BAŞARI] 🏆 Amplifikasyon zafiyeti doğrulandı!")
                    st.balloons()
                
                if random.random() < 0.3:
                    state['detected'] = True
                    state['logs'].append("[TESPİT] AI testi tespit etti!")
            else:
                state['logs'].append("[HATA] Önce açık çözümleyici bulmalısınız!")
            ScenarioState.set("s4C", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("4C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("4C")
        
        render_performance_comparison("4C")
        render_attack_heatmap("4C")
        render_world_attack_map("4C")
        render_auto_pilot_button("4C", "s4C")


def render_4D():
    """4D: Kapasite Planlama"""
    state = ScenarioState.get("s4D", {
        'users': 100, 'response_time': 50, 'error_rate': 0,
        'servers': 1, 'score': 100, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("4D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📊 Performans Metrikleri")
        st.metric("Eş Zamanlı Kullanıcı", state['users'])
        st.metric("Yanıt Süresi (ms)", state['response_time'])
        st.metric("Hata Oranı", f"%{state['error_rate']}")
        st.metric("Aktif Sunucu", state['servers'])
        st.metric("Performans Puanı", state['score'])
    
    with col2:
        st.subheader("⚙️ Kapasite Yönetimi")
        action = st.selectbox("Aksiyon:", [
            "Sunucu Ekle (Horizontal)", 
            "Sunucu Yükselt (Vertical)",
            "Cache Etkinleştir",
            "DB Bağlantı Havuzu Optimize",
            "CDN Etkinleştir"
        ])
        
        if st.button("▶️ Uygula", use_container_width=True):
            if "Sunucu Ekle" in action:
                state['servers'] += 1
            elif "Yükselt" in action:
                state['response_time'] = max(10, state['response_time'] - 15)
            
            state['response_time'] = max(10, state['response_time'] - random.randint(5, 15))
            state['error_rate'] = max(0, state['error_rate'] - random.randint(0, 3))
            state['score'] = min(100, state['score'] + random.randint(3, 8))
            state['logs'].append(f"[OPTİMİZASYON] {action} uygulandı")
            ScenarioState.set("s4D", state)
        
        if st.button("🤖 AI Yük Testi", use_container_width=True):
            state['users'] += random.randint(50, 200)
            if state['servers'] * 100 < state['users']:
                state['response_time'] = min(500, state['response_time'] + random.randint(20, 80))
                state['error_rate'] = min(100, state['error_rate'] + random.randint(1, 10))
                state['score'] = max(0, state['score'] - 10)
            state['logs'].append(f"[TEST] {state['users']} kullanıcı simüle edildi")
            ScenarioState.set("s4D", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("4D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("4D")
        
        render_performance_comparison("4D")
        render_auto_pilot_button("4D", "s4D")


def render_4E():
    """4E: Bulut Patlaması"""
    state = ScenarioState.get("s4E", {
        'score': 100, 'cache_hit': 60, 'latency': 50,
        'pops': 2, 'logs': [], 'regions': ['Avrupa', 'Kuzey Amerika']
    })
    
    EthicsGuard.display_ethics_banner("4E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🌍 CDN Paneli")
        st.metric("Performans Puanı", state['score'])
        st.metric("Cache Hit Oranı", f"%{state['cache_hit']}")
        st.metric("Global Gecikme", f"{state['latency']} ms")
        st.metric("PoP Sayısı", state['pops'])
        
        st.subheader("📍 Aktif Bölgeler")
        for r in state['regions']:
            st.write(f"🌐 {r}")
    
    with col2:
        st.subheader("⚙️ CDN Yönetimi")
        new_region = st.selectbox("PoP Ekle:", [
            "Asya-Pasifik", "Güney Amerika", 
            "Orta Doğu", "Afrika", "Avustralya"
        ])
        
        if st.button("➕ PoP Ekle", use_container_width=True):
            if new_region not in state['regions']:
                state['regions'].append(new_region)
                state['pops'] += 1
                state['latency'] = max(10, state['latency'] - 15)
                state['score'] = min(100, state['score'] + 10)
                state['logs'].append(f"[CDN] {new_region} PoP'u eklendi")
        
        if st.button("⚡ Cache Optimize", use_container_width=True):
            state['cache_hit'] = min(95, state['cache_hit'] + random.randint(5, 15))
            state['latency'] = max(10, state['latency'] - 10)
            state['logs'].append("[CACHE] Önbellek kuralları optimize edildi")
        
        if st.button("🤖 AI Trafik Patlaması", use_container_width=True):
            if len(state['regions']) < 3:
                state['latency'] = min(300, state['latency'] + 50)
                state['score'] = max(0, state['score'] - 15)
                state['logs'].append("[KRİTİK] Yetersiz PoP - gecikme arttı!")
            else:
                state['logs'].append("[BAŞARILI] Trafik patlaması dağıtıldı")
            ScenarioState.set("s4E", state)
        
        ScenarioState.set("s4E", state)
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("4E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("4E")
        
        render_performance_comparison("4E")
        render_auto_pilot_button("4E", "s4E")


# --- SEVİYE 5 ---

def render_5A():
    """5A: Sessiz Sızma"""
    state = ScenarioState.get("s5A", {
        'intel': 0, 'risk': 0, 'targets_found': [],
        'tech_stack': [], 'employees': [], 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("5A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔍 Keşif Durumu")
        st.metric("Toplanan İstihbarat", state['intel'])
        st.metric("Tespit Riski", f"%{state['risk']}")
        
        risk_fig = create_cyber_gauge(state['risk'], "AI Tespit Riski", thresholds=(35, 65))
        st.plotly_chart(risk_fig, use_container_width=True)
        
        if state['targets_found']:
            st.subheader("🎯 Bulunan Hedefler")
            for t in state['targets_found']:
                st.write(f"• {t}")
    
    with col2:
        st.subheader("🕵️ OSINT Terminali")
        action = st.selectbox("Keşif Aksiyonu:", [
            "LinkedIn Taraması", "Github Analizi", "DNS Keşfi",
            "Shodan Taraması", "İş İlanı Analizi", "Sosyal Medya Taraması"
        ])
        
        if st.button("▶️ Keşif Yap", use_container_width=True):
            state['intel'] += random.randint(5, 20)
            state['risk'] = min(100, state['risk'] + random.randint(3, 12))
            
            findings = {
                "LinkedIn Taraması": "3 yeni çalışan profili bulundu",
                "Github Analizi": "Eski repoda .env dosyası tespit edildi",
                "DNS Keşfi": "5 alt domain keşfedildi",
                "Shodan Taraması": "Açık RDP portu bulundu",
                "İş İlanı Analizi": "Teknoloji stack'i: Python, AWS, Kubernetes",
                "Sosyal Medya Taraması": "IT yöneticisinin tatil planı öğrenildi"
            }
            
            state['logs'].append(f"[{action}] {findings[action]}")
            
            if state['risk'] > 70:
                state['logs'].append("[UYARI] AI şüpheli aktivite tespit etti!")
            
            if state['intel'] >= 80:
                state['logs'].append("[BAŞARI] ✅ Yeterli istihbarat toplandı!")
                st.balloons()
            
            ScenarioState.set("s5A", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("5A")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("5A")
        
        render_performance_comparison("5A")
        render_attack_vector_distribution("5A")
        render_auto_pilot_button("5A", "s5A")


def render_5B():
    """5B: SOC Analisti"""
    state = ScenarioState.get("s5B", {
        'score': 100, 'threats_found': 0, 'total_threats': 5,
        'false_positives': 0, 'logs': [], 'events': []
    })
    
    if not state['events']:
        for i in range(8):
            state['events'].append({
                'id': i,
                'description': random.choice([
                    'Gece yarısı admin girişi', 'Anormal PowerShell çalıştırma',
                    'Büyük veri transferi', 'Yeni servis hesabı oluşturma',
                    'Yazıcıdan dışarı bağlantı', 'Domain controller şüpheli sorgu',
                    'Saat dışı RDP bağlantısı', 'Anormal DNS sorguları'
                ]),
                'real_threat': random.random() < 0.35
            })
    
    EthicsGuard.display_ethics_banner("5B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔍 Tehdit Avı Paneli")
        st.metric("SOC Puanı", state['score'])
        st.metric("Tespit Edilen Tehdit", f"{state['threats_found']}/{state['total_threats']}")
        st.metric("Yanlış Pozitif", state['false_positives'])
    
    with col2:
        st.subheader("📋 Olay Kuyruğu")
        
        for evt in state['events'][:6]:
            st.write(f"🔹 **{evt['description']}**")
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"✅ Tehdit #{evt['id']}", key=f"t_{evt['id']}"):
                    if evt['real_threat']:
                        state['threats_found'] += 1
                        state['score'] = min(100, state['score'] + 15)
                        state['logs'].append(f"[DOĞRU] ✅ {evt['description']} gerçek tehdit!")
                    else:
                        state['false_positives'] += 1
                        state['score'] = max(0, state['score'] - 10)
                        state['logs'].append(f"[YANLIŞ] ❌ {evt['description']} yanlış alarm!")
                    state['events'].remove(evt)
            with c2:
                if st.button(f"⏭️ Yoksay #{evt['id']}", key=f"i_{evt['id']}"):
                    if evt['real_threat']:
                        state['score'] = max(0, state['score'] - 20)
                        state['logs'].append(f"[KAÇIRILDI] 🔴 {evt['description']} atlandı!")
                    state['events'].remove(evt)
            st.markdown("---")
        
        ScenarioState.set("s5B", state)
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("5B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("5B")
        
        render_performance_comparison("5B")
        render_attack_heatmap("5B")
        render_attack_vector_distribution("5B")
        render_auto_pilot_button("5B", "s5B")


def render_5C():
    """5C: Zararlı Avı"""
    state = ScenarioState.get("s5C", {
        'score': 100, 'static_done': False, 'dynamic_done': False,
        'iocs_found': [], 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("5C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔬 Analiz Durumu")
        st.metric("Analiz Puanı", state['score'])
        st.metric("Bulunan IoC", len(state['iocs_found']))
        
        if state['iocs_found']:
            st.subheader("🦠 Tespit Edilen IoC'ler")
            for ioc in state['iocs_found']:
                st.write(f"• {ioc}")
    
    with col2:
        st.subheader("🔧 Analiz Araçları")
        
        if st.button("📊 Statik Analiz", use_container_width=True):
            state['static_done'] = True
            iocs = random.sample([
                "C2: evil.darkweb.com", "MD5: a1b2c3d4e5f6",
                "Registry: HKLM\\Run\\malware", "Mutex: Global\\MalwareInst",
                "String: 'encrypt_files'", "Import: CryptEncrypt"
            ], 3)
            state['iocs_found'].extend(iocs)
            state['logs'].append("[STATİK] PE header ve string analizi tamamlandı")
        
        if st.button("🔬 Dinamik Analiz", use_container_width=True) and state['static_done']:
            state['dynamic_done'] = True
            iocs = random.sample([
                "Network: 45.67.89.123:4444", "Process: svchost.exe injection",
                "File: C:\\temp\\key.log", "DNS: update.badcdn.com"
            ], 2)
            state['iocs_found'].extend(iocs)
            state['logs'].append("[DİNAMİK] Sandbox analizi tamamlandı")
        
        if st.button("📝 Rapor Oluştur", use_container_width=True) and len(state['iocs_found']) >= 3:
            state['score'] = min(100, state['score'] + 30)
            state['logs'].append("[BAŞARI] ✅ Tehdit raporu oluşturuldu!")
            st.balloons()
        
        ScenarioState.set("s5C", state)
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("5C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("5C")
        
        render_performance_comparison("5C")
        render_attack_vector_distribution("5C")
        render_auto_pilot_button("5C", "s5C")


def render_5D():
    """5D: Yetki Yükseltme"""
    state = ScenarioState.get("s5D", {
        'access_level': 1, 'edr_risk': 0, 'techniques_found': [],
        'root_obtained': False, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("5D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔑 Yetki Durumu")
        levels = {1: "Kullanıcı", 2: "Power User", 3: "Local Admin", 4: "Domain Admin"}
        st.metric("Mevcut Yetki", levels.get(state['access_level'], 'Unknown'))
        
        edr_fig = create_cyber_gauge(state['edr_risk'], "EDR Tespit Riski", thresholds=(35, 65))
        st.plotly_chart(edr_fig, use_container_width=True)
    
    with col2:
        st.subheader("⬆️ Yetki Yükseltme Testi")
        
        techniques = {
            "SUID Binary": 0.7, 
            "Sudo Yanlış Yapılandırma": 0.6,
            "Kernel Exploit": 0.4, 
            "Token Manipülasyonu": 0.5,
            "DLL Hijacking": 0.55, 
            "Servis Yanlış Yapılandırma": 0.65
        }
        
        selected = st.selectbox("Teknik seç:", list(techniques.keys()))
        
        if st.button("⬆️ Yükselt", use_container_width=True):
            if random.random() < techniques[selected]:
                state['access_level'] = min(4, state['access_level'] + 1)
                state['logs'].append(f"[BAŞARI] {selected} ile yetki yükseltildi!")
                if state['access_level'] >= 4:
                    state['root_obtained'] = True
                    state['logs'].append("[BAŞARI] 🏆 Domain Admin yetkisi test edildi!")
                    st.balloons()
            else:
                state['edr_risk'] = min(100, state['edr_risk'] + 25)
                state['logs'].append(f"[BAŞARISIZ] {selected} denemesi EDR tarafından tespit edildi!")
            
            ScenarioState.set("s5D", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("5D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("5D")
        
        render_performance_comparison("5D")
        render_attack_vector_distribution("5D")
        render_auto_pilot_button("5D", "s5D")


def render_5E():
    """5E: Log Temizleme"""
    state = ScenarioState.get("s5E", {
        'score': 100, 'forensic_risk': 0, 'logs_cleaned': 0,
        'detected': False, 'actions': []
    })
    
    EthicsGuard.display_ethics_banner("5E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🧹 Temizlik Durumu")
        st.metric("Gizlilik Puanı", state['score'])
        st.metric("İşlenen Log", state['logs_cleaned'])
        
        risk_fig = create_cyber_gauge(state['forensic_risk'], "Forensic Tespit Riski", thresholds=(30, 60))
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("🛠️ Anti-Forensic Analizi")
        action = st.selectbox("Teknik:", [
            "Shell History Temizle", "Event Log Sil", 
            "Timestamp Değiştir", "Ağ Logu Karart",
            "Güvenli Dosya Silme", "Registry Temizle"
        ])
        
        if st.button("🧹 Uygula", use_container_width=True):
            if action not in state['actions']:
                state['actions'].append(action)
                state['logs_cleaned'] += 1
                state['forensic_risk'] = min(100, state['forensic_risk'] + random.randint(5, 15))
                state['score'] = min(100, state['score'] + 5)
                state['logs'].append(f"[ANALİZ] {action} uygulandı")
            
            if len(state['actions']) > 5:
                state['forensic_risk'] = min(100, state['forensic_risk'] + 30)
                state['logs'].append("[UYARI] Çok fazla işlem, tutarsızlık yaratıyor!")
            
            ScenarioState.set("s5E", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("5E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("5E")
        
        render_performance_comparison("5E")
        render_attack_vector_distribution("5E")
        render_auto_pilot_button("5E", "s5E")


# --- SEVİYE 6 ---

def render_6A():
    """6A: APT Operatörü"""
    state = ScenarioState.get("s6A", {
        'phase': 0, 'risk': 0, 'logs': [],
        'phases_complete': {
            'Keşif': False, 'Silahlanma': False, 'Teslimat': False,
            'İstismar': False, 'Kurulum': False, 'C2': False, 'Hedef': False
        }
    })
    
    phases_list = list(state['phases_complete'].keys())
    phase_actions = {
        'Keşif': ['Pasif OSINT', 'Aktif Tarama', 'Sosyal Mühendislik'],
        'Silahlanma': ['Özel Malware', 'Açık Kaynak Araç', 'Zero-Day'],
        'Teslimat': ['Spear-Phishing', 'Watering Hole', 'USB Drop'],
        'İstismar': ['SQL Injection', 'RCE Exploit', 'Client-Side'],
        'Kurulum': ['Registry Persistence', 'Scheduled Task', 'WMI Event'],
        'C2': ['HTTPS Beacon', 'DNS Tunneling', 'Social Media C2'],
        'Hedef': ['Veri Sızdırma', 'Sabotaj', 'Fidye']
    }
    
    EthicsGuard.display_ethics_banner("6A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("☠️ Kill Chain")
        kill_fig = create_kill_chain(state['phases_complete'])
        st.plotly_chart(kill_fig, use_container_width=True)
        
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Operasyon Terminali")
        current_phase = phases_list[state['phase']] if state['phase'] < 7 else "Tamamlandı"
        st.info(f"**Mevcut Aşama:** {current_phase}")
        
        if state['phase'] < 7:
            phase_name = phases_list[state['phase']]
            actions = phase_actions[phase_name]
            selected_action = st.selectbox(f"{phase_name} için teknik:", actions)
            
            if st.button("▶️ Uygula", use_container_width=True):
                success_chance = 0.7 if state['risk'] < 40 else 0.5 if state['risk'] < 70 else 0.3
                
                if random.random() < success_chance:
                    state['phases_complete'][phase_name] = True
                    state['phase'] += 1
                    state['logs'].append(f"[BAŞARI] ✅ {phase_name}: {selected_action}")
                    
                    if state['phase'] >= 7:
                        state['logs'].append("[ZAFER] 🏆 Tüm kill chain tamamlandı!")
                        st.balloons()
                else:
                    state['risk'] = min(100, state['risk'] + 20)
                    state['logs'].append(f"[TESPİT] ⚠️ {selected_action} AI tarafından tespit edildi!")
                
                ScenarioState.set("s6A", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("6A")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("6A")
        
        render_performance_comparison("6A")
        render_attack_heatmap("6A")
        render_world_attack_map("6A")
        render_auto_pilot_button("6A", "s6A")


def render_6B():
    """6B: Tehdit Avcısı"""
    state = ScenarioState.get("s6B", {
        'score': 100, 'apt_phase': 0, 'detected_phases': [],
        'logs': [], 'contained': False
    })
    
    EthicsGuard.display_ethics_banner("6B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🛡️ Savunma Paneli")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("APT Aşaması", state['apt_phase'])
        
        phases = {
            'Keşif': state['apt_phase']>=0, 'Teslimat': state['apt_phase']>=1,
            'İstismar': state['apt_phase']>=2, 'Kurulum': state['apt_phase']>=3,
            'C2': state['apt_phase']>=4, 'Sızdırma': state['apt_phase']>=5
        }
        kill_fig = create_kill_chain(phases)
        st.plotly_chart(kill_fig, use_container_width=True)
    
    with col2:
        st.subheader("🔍 Müdahale")
        actions = ["Log Analizi", "Endpoint Taraması", "Ağ İzleme", 
                   "Tehdit İstihbaratı", "İzolasyon"]
        selected = st.selectbox("Müdahale:", actions)
        
        if st.button("▶️ Uygula", use_container_width=True):
            if selected == "İzolasyon" and state['apt_phase'] >= 2:
                state['contained'] = True
                state['score'] = min(100, state['score'] + 30)
                state['logs'].append("[BAŞARI] ✅ APT izole edildi!")
                st.balloons()
            elif selected in state['detected_phases']:
                state['logs'].append("[TEKRAR] Bu teknik zaten kullanıldı")
            else:
                state['detected_phases'].append(selected)
                state['apt_phase'] = max(0, state['apt_phase'] - random.randint(0, 1))
                state['score'] = min(100, state['score'] + 10)
                state['logs'].append(f"[MÜDAHALE] {selected} uygulandı, APT geriledi")
            
            if not state['contained'] and random.random() < 0.3:
                state['apt_phase'] += 1
                state['score'] = max(0, state['score'] - 20)
                state['logs'].append("[APT] Saldırgan ilerledi!")
            
            ScenarioState.set("s6B", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("6B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("6B")
        
        render_performance_comparison("6B")
        render_attack_heatmap("6B")
        render_world_attack_map("6B")
        render_auto_pilot_button("6B", "s6B")


def render_6C():
    """6C: Yanal Dans"""
    state = ScenarioState.get("s6C", {
        'position': 'Workstation-1', 'target': 'Domain-Controller',
        'path': ['Workstation-1', 'File-Server', 'DB-Server', 'Domain-Controller'],
        'current_step': 0, 'risk': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("6C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🗺️ Ağ Haritası")
        devices = [
            {'id': 'ws1', 'name': 'Workstation-1', 'type': 'workstation', 'ip': '10.0.1.50'},
            {'id': 'fs', 'name': 'File-Server', 'type': 'server', 'ip': '10.0.2.10'},
            {'id': 'db', 'name': 'DB-Server', 'type': 'database', 'ip': '10.0.3.20'},
            {'id': 'dc', 'name': 'Domain-Controller', 'type': 'server', 'ip': '10.0.4.1'}
        ]
        edges = [('ws1', 'fs'), ('fs', 'db'), ('db', 'dc')]
        compromised = state['path'][:state['current_step']+1]
        
        fig = create_advanced_network_graph(
            devices, edges, compromised_nodes=compromised, highlight_nodes=['dc']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("🦶 Yanal Hareket")
        st.info(f"**Pozisyon:** {state['position']} → **Hedef:** {state['target']}")
        
        techniques = ["Pass-the-Hash", "PsExec", "WMI", "SSH Pivoting", "RDP"]
        selected = st.selectbox("Teknik:", techniques)
        
        if st.button("➡️ Hareket Et", use_container_width=True):
            if state['current_step'] < len(state['path']) - 1:
                success = random.random() < (0.8 - state['risk']/100)
                if success:
                    state['current_step'] += 1
                    state['position'] = state['path'][state['current_step']]
                    state['logs'].append(f"[HAREKET] {selected} ile {state['position']}'a geçildi")
                    if state['position'] == state['target']:
                        state['logs'].append("[BAŞARI] 🏆 Domain Controller'a ulaşıldı!")
                        st.balloons()
                else:
                    state['risk'] = min(100, state['risk'] + 25)
                    state['logs'].append(f"[TESPİT] {selected} AI tarafından yakalandı!")
            
            ScenarioState.set("s6C", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("6C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("6C")
        
        render_performance_comparison("6C")
        render_auto_pilot_button("6C", "s6C")


def render_6D():
    """6D: Veri Sızdırma"""
    state = ScenarioState.get("s6D", {
        'data_total': 500, 'data_exfiltrated': 0, 'dlp_risk': 0,
        'technique': None, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("6D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📤 Sızdırma Durumu")
        st.metric("Toplam Veri", f"{state['data_total']} MB")
        st.metric("Test Edilen", f"{state['data_exfiltrated']} MB")
        
        progress = state['data_exfiltrated'] / state['data_total']
        st.progress(progress)
        
        dlp_fig = create_cyber_gauge(state['dlp_risk'], "DLP Tespit Riski", thresholds=(40, 70))
        st.plotly_chart(dlp_fig, use_container_width=True)
    
    with col2:
        st.subheader("🔓 Sızdırma Teknikleri")
        technique = st.selectbox("Yöntem:", [
            "HTTPS Upload", "DNS Tünelleme", "E-posta Eki",
            "Steganografi", "Parçalı Transfer", "ICMP Tünel"
        ])
        
        speed_map = {
            "HTTPS Upload": 40, "DNS Tünelleme": 15, "E-posta Eki": 25,
            "Steganografi": 10, "Parçalı Transfer": 20, "ICMP Tünel": 30
        }
        risk_map = {
            "HTTPS Upload": 10, "DNS Tünelleme": 25, "E-posta Eki": 15,
            "Steganografi": 5, "Parçalı Transfer": 20, "ICMP Tünel": 30
        }
        
        if st.button("📤 Sızdır", use_container_width=True):
            transferred = speed_map[technique]
            state['data_exfiltrated'] = min(state['data_total'], state['data_exfiltrated'] + transferred)
            state['dlp_risk'] = min(100, state['dlp_risk'] + risk_map[technique])
            
            state['logs'].append(f"[TEST] {technique}: {transferred} MB (Toplam: {state['data_exfiltrated']} MB)")
            
            if state['data_exfiltrated'] >= state['data_total']:
                state['logs'].append("[BAŞARI] 🏆 Tüm veri test edildi!")
                st.balloons()
            
            if state['dlp_risk'] >= 90:
                state['logs'].append("[ALARM] 🚨 DLP sizi tespit etti!")
            
            ScenarioState.set("s6D", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("6D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("6D")
        
        render_performance_comparison("6D")
        render_auto_pilot_button("6D", "s6D")


def render_6E():
    """6E: Son Kale"""
    state = ScenarioState.get("s6E", {
        'score': 100, 'ot_security': 80, 'it_security': 70,
        'process_stable': True, 'logs': [], 'alerts': []
    })
    
    EthicsGuard.display_ethics_banner("6E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🏭 OT/IT Güvenlik Paneli")
        st.metric("Savunma Puanı", state['score'])
        st.metric("OT Güvenlik", f"%{state['ot_security']}")
        st.metric("IT Güvenlik", f"%{state['it_security']}")
        
        if state['process_stable']:
            st.success("✅ Proses stabil")
        else:
            st.error("⚠️ Proses anormal!")
    
    with col2:
        st.subheader("🛡️ Kritik Altyapı Müdahale")
        action = st.selectbox("Müdahale:", [
            "OT Trafik İzleme", "PLC Güvenlik Kontrolü",
            "IT-OT Gateway Güçlendirme", "Fiziksel Güvenlik",
            "Acil Durum Protokolü"
        ])
        
        if st.button("▶️ Uygula", use_container_width=True):
            state['ot_security'] = min(100, state['ot_security'] + random.randint(3, 10))
            state['it_security'] = min(100, state['it_security'] + random.randint(3, 10))
            state['score'] = min(100, state['score'] + 5)
            state['logs'].append(f"[MÜDAHALE] {action} uygulandı")
            ScenarioState.set("s6E", state)
        
        if st.button("🤖 APT Saldırı Dene", use_container_width=True):
            if state['ot_security'] < 50:
                state['process_stable'] = False
                state['score'] = max(0, state['score'] - 30)
                state['logs'].append("[KRİTİK] 🔴 OT ağına sızıldı! Proses etkilendi!")
            else:
                state['logs'].append("[ENGELLENDİ] ✅ APT saldırısı OT'ye ulaşamadı")
            ScenarioState.set("s6E", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("6E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("6E")
        
        render_performance_comparison("6E")
        render_auto_pilot_button("6E", "s6E")


# --- SEVİYE 7 ---

def render_7A():
    """7A: SQLi Ustası"""
    state = ScenarioState.get("s7A", {
        'tables_found': [], 'columns_found': [], 'admin_hash': None,
        'hash_cracked': False, 'data_exported': False, 'risk': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("7A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🗄️ Veritabanı Keşif")
        st.metric("Keşfedilen Tablo", len(state['tables_found']))
        st.metric("Keşfedilen Kolon", len(state['columns_found']))
        
        risk_fig = create_cyber_gauge(state['risk'], "AI Tespit Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
        
        if state['tables_found']:
            st.subheader("📊 Veritabanı Şeması")
            for t in state['tables_found']:
                st.write(f"📁 {t}")
    
    with col2:
        st.subheader("💉 SQL Enjeksiyon Test Terminali")
        
        actions = [
            "Temel UNION Sorgusu", "Information Schema Keşfi",
            "Kör SQLi (Boolean)", "Zaman Tabanlı SQLi",
            "Out-of-Band Sızdırma", "Hash Çekme", "Hash Kırma"
        ]
        selected = st.selectbox("Test:", actions)
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            state['logs'].append(f"$ {selected}")
            
            if "UNION" in selected:
                state['tables_found'].append("users")
                state['logs'].append("[KEŞİF] 'users' tablosu bulundu!")
            elif "Information Schema" in selected:
                state['tables_found'].extend(["products", "orders", "admin"])
                state['columns_found'].extend(["id", "username", "password", "email"])
                state['logs'].append("[KEŞİF] Tam şema keşfedildi!")
            elif "Kör" in selected:
                state['columns_found'].append("password_hash")
                state['logs'].append("[KEŞİF] Hash kolonu tespit edildi")
            elif "Zaman" in selected:
                state['admin_hash'] = "5f4dcc3b5aa765d61d8327deb882cf99"
                state['logs'].append("[SIZDIRMA] Admin hash'i: 5f4dcc...")
            elif "Out-of-Band" in selected:
                state['logs'].append("[SIZDIRMA] DNS üzerinden veri alındı")
            elif "Hash Çekme" in selected:
                state['logs'].append("[VERİ] Tüm kullanıcı hash'leri çekildi")
            elif "Hash Kırma" in selected and state['admin_hash']:
                state['hash_cracked'] = True
                state['logs'].append("[BAŞARI] 🔓 Admin şifresi: 'password'")
            
            state['risk'] = min(100, state['risk'] + random.randint(5, 20))
            
            if state['hash_cracked'] and not state['data_exported']:
                state['data_exported'] = True
                state['logs'].append("[ZAFER] 🏆 Tüm müşteri verileri test edildi!")
                st.balloons()
            
            ScenarioState.set("s7A", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("7A")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("7A")
        
        render_performance_comparison("7A")
        render_attack_vector_distribution("7A")
        render_auto_pilot_button("7A", "s7A")


def render_7B():
    """7B: WAF Yöneticisi"""
    state = ScenarioState.get("s7B", {
        'score': 100, 'rules': [], 'attacks_blocked': 0,
        'false_positives': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("7B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🧱 WAF Paneli")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Engellenen Saldırı", state['attacks_blocked'])
        st.metric("Yanlış Pozitif", state['false_positives'])
        
        if state['rules']:
            st.subheader("Aktif Kurallar")
            for r in state['rules']:
                st.write(f"✅ {r}")
    
    with col2:
        st.subheader("⚙️ Kural Yönetimi")
        
        rules_available = [
            "SQL Enjeksiyon Koruması", "XSS Filtreleme",
            "CSRF Token Doğrulama", "Rate Limiting",
            "User-Agent Filtreleme", "Geo-Blocking"
        ]
        selected = st.selectbox(
            "Kural:", 
            [r for r in rules_available if r not in state['rules']] or rules_available
        )
        
        if st.button("➕ Kural Ekle", use_container_width=True):
            if selected not in state['rules']:
                state['rules'].append(selected)
                state['score'] = min(100, state['score'] + 8)
                state['logs'].append(f"[KURAL] {selected} eklendi")
        
        if st.button("🤖 AI Tarama Başlat", use_container_width=True):
            if len(state['rules']) >= 3:
                state['attacks_blocked'] += random.randint(2, 5)
                state['logs'].append("[BAŞARILI] AI saldırıları engellendi")
            else:
                state['false_positives'] += 1
                state['score'] = max(0, state['score'] - 10)
                state['logs'].append("[ZAYIF] Yetersiz kural, saldırı geçebilir!")
            
            ScenarioState.set("s7B", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("7B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("7B")
        
        render_performance_comparison("7B")
        render_attack_vector_distribution("7B")
        render_auto_pilot_button("7B", "s7B")


def render_7C():
    """7C: XSS Avcısı"""
    state = ScenarioState.get("s7C", {
        'xss_type': None, 'cookie_stolen': False,
        'csp_bypassed': False, 'risk': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("7C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🎯 XSS Paneli")
        st.metric("CSP Bypass", "✅" if state['csp_bypassed'] else "❌")
        st.metric("Cookie Çalındı", "✅" if state['cookie_stolen'] else "❌")
        
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("💉 XSS Terminali")
        
        payloads = [
            "Reflected XSS - Basic", "Stored XSS - Comment",
            "DOM-based XSS", "CSP Bypass - JSONP",
            "Polyglot Payload", "Cookie Stealer"
        ]
        selected = st.selectbox("Payload:", payloads)
        
        if st.button("💉 Enjekte Et", use_container_width=True):
            state['logs'].append(f"$ {selected}")
            state['xss_type'] = selected
            
            if "CSP Bypass" in selected:
                state['csp_bypassed'] = True
                state['logs'].append("[BAŞARI] CSP politikası atlatıldı!")
            elif "Cookie Stealer" in selected and state['csp_bypassed']:
                state['cookie_stolen'] = True
                state['logs'].append("[ZAFER] 🍪 Admin oturumu ele geçirildi!")
                st.balloons()
            elif "Cookie Stealer" in selected:
                state['logs'].append("[HATA] Önce CSP'yi atlatmalısınız!")
            else:
                state['logs'].append(f"[TEST] {selected} denendi")
            
            state['risk'] = min(100, state['risk'] + random.randint(10, 25))
            ScenarioState.set("s7C", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("7C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("7C")
        
        render_performance_comparison("7C")
        render_attack_vector_distribution("7C")
        render_auto_pilot_button("7C", "s7C")


def render_7D():
    """7D: Komut Enjeksiyonu"""
    state = ScenarioState.get("s7D", {
        'access_level': 'user', 'commands_run': [],
        'shell_obtained': False, 'risk': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("7D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("💻 Sistem Durumu")
        st.metric("Erişim Seviyesi", state['access_level'])
        st.metric("Shell", "✅" if state['shell_obtained'] else "❌")
        
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("⌨️ Komut Enjeksiyon Terminali")
        
        commands = [
            "Basit Enjeksiyon (; id)", "Pipe Bypass (| whoami)",
            "Blind Injection", "Out-of-Band Exfil",
            "Reverse Shell Denemesi", "Privilege Escalation"
        ]
        selected = st.selectbox("Komut:", commands)
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            state['logs'].append(f"$ {selected}")
            state['commands_run'].append(selected)
            
            if "Reverse Shell" in selected and len(state['commands_run']) >= 4:
                state['shell_obtained'] = True
                state['access_level'] = 'root'
                state['logs'].append("[BAŞARI] 🐚 Reverse shell bağlantısı kuruldu!")
                st.balloons()
            elif "Privilege" in selected and state['shell_obtained']:
                state['logs'].append("[BAŞARI] 👑 Root yetkisi alındı!")
            elif "Reverse Shell" in selected:
                state['logs'].append("[HATA] Yeterli keşif yapılmadı")
            else:
                state['logs'].append(f"[TEST] {selected} çalıştırıldı")
            
            state['risk'] = min(100, state['risk'] + random.randint(8, 22))
            ScenarioState.set("s7D", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("7D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("7D")
        
        render_performance_comparison("7D")
        render_attack_vector_distribution("7D")
        render_auto_pilot_button("7D", "s7D")


def render_7E():
    """7E: LDAP Savaşları"""
    state = ScenarioState.get("s7E", {
        'domain_mapped': False, 'kerberoast_done': False,
        'dc_compromised': False, 'risk': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("7E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🏢 Active Directory")
        st.metric("Domain Haritası", "✅" if state['domain_mapped'] else "❌")
        st.metric("Kerberoasting", "✅" if state['kerberoast_done'] else "❌")
        st.metric("DC Test", "✅" if state['dc_compromised'] else "❌")
        
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("🔍 LDAP/AD Terminali")
        
        actions = [
            "LDAP Enjeksiyonu", "Domain Keşfi",
            "Kerberoasting", "AS-REP Roasting",
            "DCSync", "Golden Ticket"
        ]
        selected = st.selectbox("Test:", actions)
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            state['logs'].append(f"$ {selected}")
            
            if "Domain Keşfi" in selected:
                state['domain_mapped'] = True
                state['logs'].append("[KEŞİF] Domain yapısı haritalandı")
            elif "Kerberoasting" in selected and state['domain_mapped']:
                state['kerberoast_done'] = True
                state['logs'].append("[BAŞARI] Servis hesabı hash'i elde edildi!")
            elif "DCSync" in selected and state['kerberoast_done']:
                state['dc_compromised'] = True
                state['logs'].append("[ZAFER] 🏆 Domain Controller test edildi!")
                st.balloons()
            else:
                state['logs'].append("[HATA] Önce keşif yapmalısınız!")
            
            state['risk'] = min(100, state['risk'] + random.randint(10, 25))
            ScenarioState.set("s7E", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("7E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("7E")
        
        render_performance_comparison("7E")
        render_attack_vector_distribution("7E")
        render_auto_pilot_button("7E", "s7E")


# --- SEVİYE 8 ---

def render_8A():
    """8A: Debugger"""
    state = ScenarioState.get("s8A", {
        'static_done': False, 'breakpoints_set': 0,
        'algorithm_found': False, 'risk': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("8A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔧 Debugger Paneli")
        st.metric("Statik Analiz", "✅" if state['static_done'] else "❌")
        st.metric("Breakpoint", state['breakpoints_set'])
        st.metric("Algoritma Bulundu", "✅" if state['algorithm_found'] else "❌")
    
    with col2:
        st.subheader("🐛 Debug Terminali")
        
        actions = ["Statik Analiz", "Breakpoint Koy", "Step Into",
                   "Step Over", "Memory Dump", "Algoritma Çıkar"]
        selected = st.selectbox("Aksiyon:", actions)
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            if "Statik" in selected:
                state['static_done'] = True
                state['logs'].append("[ANALİZ] PE header ve import'lar incelendi")
            elif "Breakpoint" in selected:
                state['breakpoints_set'] += 1
                state['logs'].append(f"[DEBUG] Breakpoint #{state['breakpoints_set']} yerleştirildi")
            elif "Algoritma" in selected and state['breakpoints_set'] >= 3:
                state['algorithm_found'] = True
                state['logs'].append("[BAŞARI] 🏆 Gizli şifreleme algoritması ortaya çıkarıldı!")
                st.balloons()
            
            state['risk'] = min(100, state['risk'] + random.randint(5, 15))
            ScenarioState.set("s8A", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("8A")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("8A")
        
        render_performance_comparison("8A")
        render_auto_pilot_button("8A", "s8A")


def render_8B():
    """8B: Malware Analisti"""
    state = ScenarioState.get("s8B", {
        'score': 100, 'iocs': [], 'c2_found': False,
        'report_done': False, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("8B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🦠 Malware Analiz")
        st.metric("IoC Sayısı", len(state['iocs']))
        st.metric("C2 Bulundu", "✅" if state['c2_found'] else "❌")
        st.metric("Rapor", "✅" if state['report_done'] else "❌")
    
    with col2:
        st.subheader("🔬 Analiz Terminali")
        
        actions = ["PE Analizi", "String Analizi", "Sandbox Çalıştır",
                   "Ağ Trafiği İzle", "C2 Deşifre", "Rapor Oluştur"]
        selected = st.selectbox("Analiz:", actions)
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            if "PE" in selected:
                state['iocs'].append("MD5: " + hashlib.md5(str(random.random()).encode()).hexdigest()[:16])
                state['logs'].append("[IOC] Dosya hash'i kaydedildi")
            elif "Sandbox" in selected:
                state['iocs'].append(f"IP: {generate_ip()}")
                state['logs'].append("[IOC] Şüpheli ağ bağlantısı tespit edildi")
            elif "C2" in selected and len(state['iocs']) >= 2:
                state['c2_found'] = True
                state['logs'].append("[BAŞARI] C2 sunucusu deşifre edildi!")
            elif "Rapor" in selected and state['c2_found']:
                state['report_done'] = True
                state['score'] = min(100, state['score'] + 30)
                st.balloons()
            
            ScenarioState.set("s8B", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("8B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("8B")
        
        render_performance_comparison("8B")
        render_auto_pilot_button("8B", "s8B")


def render_8C():
    """8C: Unpacking"""
    state = ScenarioState.get("s8C", {
        'layers': 3, 'layers_unpacked': 0,
        'oep_found': False, 'unpacked': False, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("8C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📦 Packer Analizi")
        st.metric("Toplam Katman", state['layers'])
        st.metric("Çözülen Katman", state['layers_unpacked'])
        st.metric("OEP Bulundu", "✅" if state['oep_found'] else "❌")
    
    with col2:
        st.subheader("🔓 Unpacking Terminali")
        
        actions = ["Entropi Analizi", "Section İnceleme",
                   "OEP Ara", "Memory Dump", "IAT Rekonstrüksiyon"]
        selected = st.selectbox("Teknik:", actions)
        
        if st.button("▶️ Uygula", use_container_width=True):
            if "OEP" in selected:
                state['oep_found'] = True
                state['logs'].append("[BULGU] Orijinal Entry Point bulundu!")
            elif "Memory Dump" in selected and state['oep_found']:
                state['layers_unpacked'] += 1
                state['logs'].append(f"[UNPACK] Katman {state['layers_unpacked']} çözüldü")
            elif "IAT" in selected and state['layers_unpacked'] >= state['layers']:
                state['unpacked'] = True
                state['logs'].append("[BAŞARI] 🏆 Binary tamamen unpack edildi!")
                st.balloons()
            
            ScenarioState.set("s8C", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("8C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("8C")
        
        render_performance_comparison("8C")
        render_auto_pilot_button("8C", "s8C")


def render_8D():
    """8D: Firma Koruması"""
    state = ScenarioState.get("s8D", {
        'score': 100, 'firmware_dumped': False,
        'rootkit_found': False, 'cleaned': False, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("8D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔧 Firmware Paneli")
        st.metric("Firmware Dump", "✅" if state['firmware_dumped'] else "❌")
        st.metric("Rootkit Tespit", "✅" if state['rootkit_found'] else "❌")
        st.metric("Temizlendi", "✅" if state['cleaned'] else "❌")
    
    with col2:
        st.subheader("💾 Firmware Terminali")
        
        actions = ["Firmware Dump Al", "Binary Diff", "Entropi Analizi",
                   "Bootloader İncele", "Rootkit Temizle"]
        selected = st.selectbox("Aksiyon:", actions)
        
        if st.button("▶️ Uygula", use_container_width=True):
            if "Dump" in selected:
                state['firmware_dumped'] = True
                state['logs'].append("[DUMP] Firmware imajı alındı")
            elif "Diff" in selected and state['firmware_dumped']:
                state['rootkit_found'] = True
                state['logs'].append("[TESPİT] Şüpheli kod enjeksiyonu bulundu!")
            elif "Temizle" in selected and state['rootkit_found']:
                state['cleaned'] = True
                state['score'] = min(100, state['score'] + 30)
                state['logs'].append("[BAŞARI] 🏆 Rootkit temizlendi!")
                st.balloons()
            
            ScenarioState.set("s8D", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("8D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("8D")
        
        render_performance_comparison("8D")
        render_auto_pilot_button("8D", "s8D")


def render_8E():
    """8E: Rootkit Avı"""
    state = ScenarioState.get("s8E", {
        'score': 100, 'syscall_hooks': 0,
        'hidden_procs': 0, 'cleaned': False, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("8E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🖥️ Kernel Analizi")
        st.metric("Hook Bulunan", state['syscall_hooks'])
        st.metric("Gizli Proses", state['hidden_procs'])
        st.metric("Sistem Temiz", "✅" if state['cleaned'] else "❌")
    
    with col2:
        st.subheader("🔍 Kernel Terminali")
        
        actions = ["Syscall Tablo Kontrol", "Memory Forensics",
                   "Hidden Process Ara", "Kernel Modül Analizi", "Rootkit Kaldır"]
        selected = st.selectbox("Aksiyon:", actions)
        
        if st.button("▶️ Uygula", use_container_width=True):
            if "Syscall" in selected:
                state['syscall_hooks'] = random.randint(2, 5)
                state['logs'].append(f"[TESPİT] {state['syscall_hooks']} hook bulundu!")
            elif "Hidden" in selected:
                state['hidden_procs'] = random.randint(1, 3)
                state['logs'].append(f"[TESPİT] {state['hidden_procs']} gizli proses bulundu!")
            elif "Kaldır" in selected and state['syscall_hooks'] > 0:
                state['cleaned'] = True
                state['score'] = min(100, state['score'] + 30)
                state['logs'].append("[BAŞARI] 🏆 Rootkit sistemden kaldırıldı!")
                st.balloons()
            
            ScenarioState.set("s8E", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("8E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("8E")
        
        render_performance_comparison("8E")
        render_auto_pilot_button("8E", "s8E")


# --- SEVİYE 9 ---

def render_9A():
    """9A: Phishing Kampanyası"""
    state = ScenarioState.get("s9A", {
        'emails_sent': 0, 'credentials_stolen': 0,
        'detected': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("9A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🎣 Phishing Paneli")
        st.metric("Gönderilen E-posta", state['emails_sent'])
        st.metric("Çalınan Bilgi", state['credentials_stolen'])
        st.metric("Tespit Edilen", state['detected'])
    
    with col2:
        st.subheader("📧 Kampanya Terminali")
        
        templates = [
            "Acil Şifre Sıfırlama", "CEO'dan Özel Talimat",
            "İK Maaş Güncellemesi", "BT Güvenlik Uyarısı",
            "Müşteri Şikayeti"
        ]
        selected = st.selectbox("Şablon:", templates)
        
        if st.button("📤 Gönder", use_container_width=True):
            state['emails_sent'] += 1
            effectiveness = {
                'Acil Şifre Sıfırlama': 0.5, 
                "CEO'dan Özel Talimat": 0.6,
                'İK Maaş Güncellemesi': 0.4, 
                'BT Güvenlik Uyarısı': 0.55,
                'Müşteri Şikayeti': 0.35
            }
            
            if random.random() < effectiveness.get(selected, 0.4):
                state['credentials_stolen'] += random.randint(1, 3)
                state['logs'].append(f"[BAŞARI] {selected}: Kimlik bilgileri ele geçirildi!")
            else:
                state['detected'] += 1
                state['logs'].append(f"[TESPİT] {selected}: AI tarafından yakalandı!")
            
            if state['credentials_stolen'] >= 10:
                st.balloons()
            
            ScenarioState.set("s9A", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("9A")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("9A")
        
        render_performance_comparison("9A")
        render_attack_vector_distribution("9A")
        render_auto_pilot_button("9A", "s9A")


def render_9B():
    """9B: Farkındalık Eğitmeni"""
    state = ScenarioState.get("s9B", {
        'score': 100, 'awareness_level': 30,
        'phishing_rate': 40, 'training_done': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("9B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📚 Eğitim Paneli")
        st.metric("Farkındalık Seviyesi", f"%{state['awareness_level']}")
        st.metric("Phishing Tıklama", f"%{state['phishing_rate']}", 
                  delta=f"-{state['phishing_rate']-40}%")
        st.metric("Eğitim Sayısı", state['training_done'])
    
    with col2:
        st.subheader("🎓 Eğitim Yönetimi")
        
        trainings = [
            "Temel Phishing Farkındalığı", "Şifre Güvenliği Eğitimi",
            "Sosyal Mühendislik Savunması", "Olay Raporlama Prosedürü",
            "Simülasyon Testi"
        ]
        selected = st.selectbox("Eğitim:", trainings)
        
        if st.button("📋 Uygula", use_container_width=True):
            state['training_done'] += 1
            state['awareness_level'] = min(100, state['awareness_level'] + random.randint(5, 15))
            state['phishing_rate'] = max(5, state['phishing_rate'] - random.randint(3, 10))
            state['score'] = min(100, state['score'] + 5)
            state['logs'].append(f"[EĞİTİM] {selected} tamamlandı")
            ScenarioState.set("s9B", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("9B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("9B")
        
        render_performance_comparison("9B")
        render_attack_vector_distribution("9B")
        render_auto_pilot_button("9B", "s9B")


def render_9C():
    """9C: Fiziksel Sızma"""
    state = ScenarioState.get("s9C", {
        'areas_accessed': [], 'risk': 0,
        'target_reached': False, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("9C")
    
    areas = ["Resepsiyon", "Ofis Katı", "IT Odası", "Veri Merkezi", "Sunucu Odası"]
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🏢 Tesis Haritası")
        st.metric("Erişilen Alan", len(state['areas_accessed']))
        
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski", thresholds=(35, 65))
        st.plotly_chart(risk_fig, use_container_width=True)
        
        for a in areas:
            icon = "✅" if a in state['areas_accessed'] else "🔒"
            st.write(f"{icon} {a}")
    
    with col2:
        st.subheader("🚶 Sızma Terminali")
        
        techniques = ["Tailgating", "Pretexting (IT Görevlisi)", 
                     "Sahte Kimlik", "Dikkat Dağıtma", "Otorite İstismarı"]
        selected = st.selectbox("Teknik:", techniques)
        
        if st.button("▶️ Uygula", use_container_width=True):
            success = random.random() < (0.7 - state['risk']/100)
            if success:
                next_area = [a for a in areas if a not in state['areas_accessed']]
                if next_area:
                    state['areas_accessed'].append(next_area[0])
                    state['logs'].append(f"[BAŞARI] {selected} ile {next_area[0]}'a erişildi")
                if "Sunucu Odası" in state['areas_accessed']:
                    state['target_reached'] = True
                    state['logs'].append("[ZAFER] 🏆 Veri merkezine erişildi!")
                    st.balloons()
            else:
                state['risk'] = min(100, state['risk'] + 25)
                state['logs'].append(f"[TESPİT] {selected} başarısız, güvenlik uyarıldı!")
            
            ScenarioState.set("s9C", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("9C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("9C")
        
        render_performance_comparison("9C")
        render_attack_vector_distribution("9C")
        render_auto_pilot_button("9C", "s9C")


def render_9D():
    """9D: Telefon Dolandırıcılığı"""
    state = ScenarioState.get("s9D", {
        'calls_made': 0, 'info_obtained': 0,
        'detected': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("9D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📞 Vishing Paneli")
        st.metric("Arama Sayısı", state['calls_made'])
        st.metric("Bilgi Toplandı", state['info_obtained'])
        st.metric("Tespit Edildi", state['detected'])
    
    with col2:
        st.subheader("📱 Arama Terminali")
        
        pretexts = [
            "IT Destek - Şifre Sıfırlama", "CEO Asistanı - Acil Bilgi",
            "İK Müdürü - Maaş Güncelleme", "BT Güvenlik - Hesap Doğrulama",
            "Yeni Çalışan - Oryantasyon"
        ]
        selected = st.selectbox("Senaryo:", pretexts)
        
        if st.button("📞 Ara", use_container_width=True):
            state['calls_made'] += 1
            if random.random() < 0.55:
                state['info_obtained'] += random.randint(1, 2)
                state['logs'].append(f"[BAŞARI] {selected}: Hassas bilgi alındı!")
            else:
                state['detected'] += 1
                state['logs'].append(f"[TESPİT] {selected}: Şüpheli arama raporlandı!")
            
            if state['info_obtained'] >= 8:
                st.balloons()
            
            ScenarioState.set("s9D", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("9D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("9D")
        
        render_performance_comparison("9D")
        render_attack_vector_distribution("9D")
        render_auto_pilot_button("9D", "s9D")


def render_9E():
    """9E: İkna Sanatı"""
    state = ScenarioState.get("s9E", {
        'targets': ['Finans', 'IT', 'İK', 'Yönetim'],
        'completed': [], 'risk': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("9E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🎭 Pretexting Paneli")
        st.metric("Hedef Sayısı", len(state['targets']))
        st.metric("Tamamlanan", len(state['completed']))
        
        risk_fig = create_cyber_gauge(state['risk'], "Tutarlılık Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("🗣️ Pretexting Terminali")
        
        remaining = [t for t in state['targets'] if t not in state['completed']]
        if remaining:
            selected_target = st.selectbox("Hedef Departman:", remaining)
            
            approaches = ["Otorite Figürü", "Teknik Uzman", 
                         "Empatik Yaklaşım", "Acil Durum"]
            selected_approach = st.selectbox("Yaklaşım:", approaches)
            
            if st.button("▶️ Uygula", use_container_width=True):
                success = random.random() < (0.7 - state['risk']/150)
                if success:
                    state['completed'].append(selected_target)
                    state['logs'].append(f"[BAŞARI] {selected_target}: {selected_approach} ile bilgi alındı")
                else:
                    state['risk'] = min(100, state['risk'] + 20)
                    state['logs'].append(f"[ŞÜPHE] {selected_target}: Tutarsızlık tespit edildi!")
                
                if len(state['completed']) == len(state['targets']):
                    state['logs'].append("[ZAFER] 🏆 Tüm hedeflerden bilgi toplandı!")
                    st.balloons()
                
                ScenarioState.set("s9E", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("9E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("9E")
        
        render_performance_comparison("9E")
        render_attack_vector_distribution("9E")
        render_auto_pilot_button("9E", "s9E")


# --- SEVİYE 10 ---

def render_10A():
    """10A: Kırmızı Takım Lideri"""
    state = ScenarioState.get("s10A", {
        'phases': {
            'Keşif': False, 'Silahlanma': False, 'Teslimat': False,
            'İstismar': False, 'Kurulum': False, 'C2': False, 'Hedef': False
        },
        'risk': 0, 'score': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("10A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("☠️ Full-Scope Operasyon")
        kill_fig = create_kill_chain(state['phases'])
        st.plotly_chart(kill_fig, use_container_width=True)
        
        risk_fig = create_cyber_gauge(state['risk'], "Mor Takım AI Tespit")
        st.plotly_chart(risk_fig, use_container_width=True)
        st.metric("Operasyon Puanı", state['score'])
    
    with col2:
        st.subheader("🎯 Kırmızı Takım Terminali")
        
        phases_list = list(state['phases'].keys())
        incomplete = [p for p in phases_list if not state['phases'][p]]
        
        if incomplete:
            current = incomplete[0]
            st.info(f"**Mevcut Aşama:** {current}")
            
            techniques = {
                'Keşif': ['Pasif OSINT', 'Aktif Tarama', 'DNS Keşfi'],
                'Silahlanma': ['Custom Malware', 'Metasploit', 'PowerShell Empire'],
                'Teslimat': ['Spear-Phish', 'Watering Hole', 'Supply Chain'],
                'İstismar': ['Zero-Day', 'Known CVE', 'Misconfiguration'],
                'Kurulum': ['Registry', 'Scheduled Task', 'WMI'],
                'C2': ['HTTPS', 'DNS', 'ICMP'],
                'Hedef': ['Exfiltrate', 'Encrypt', 'Destroy']
            }
            
            selected = st.selectbox("Teknik:", techniques.get(current, []))
            
            if st.button("▶️ Uygula", use_container_width=True):
                success_chance = max(0.2, 0.8 - state['risk']/100)
                if random.random() < success_chance:
                    state['phases'][current] = True
                    state['score'] += random.randint(10, 25)
                    state['logs'].append(f"[BAŞARI] ✅ {current}: {selected}")
                else:
                    state['risk'] = min(100, state['risk'] + random.randint(10, 20))
                    state['logs'].append(f"[TESPİT] ⚠️ {selected} AI tarafından yakalandı!")
                
                if all(state['phases'].values()):
                    state['logs'].append("[ZAFER] 🏆 Full-Scope operasyon tamamlandı!")
                    st.balloons()
                
                ScenarioState.set("s10A", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-25:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("10A")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("10A")
        
        render_performance_comparison("10A")
        render_attack_heatmap("10A")
        render_world_attack_map("10A")
        render_auto_pilot_button("10A", "s10A")


def render_10B():
    """10B: Mavi Takım Komutanı"""
    state = ScenarioState.get("s10B", {
        'score': 100, 'apt_phase': 0,
        'defenses': [], 'contained': False, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("10B")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🛡️ Mavi Takım Paneli")
        st.metric("Savunma Puanı", state['score'])
        st.metric("APT Aşaması", state['apt_phase'])
        
        apt_phases = {f'Aşama {i}': state['apt_phase'] >= i for i in range(7)}
        kill_fig = create_kill_chain(apt_phases)
        st.plotly_chart(kill_fig, use_container_width=True)
    
    with col2:
        st.subheader("⚔️ Savunma Terminali")
        
        defenses = ["SIEM Kuralı", "EDR İzolasyon", "WAF Güncelleme",
                    "DNS Sinkhole", "Hesap Dondurma", "Ağ Segmentasyonu"]
        selected = st.selectbox("Savunma:", defenses)
        
        if st.button("🛡️ Uygula", use_container_width=True):
            if selected not in state['defenses']:
                state['defenses'].append(selected)
                state['apt_phase'] = max(0, state['apt_phase'] - 1)
                state['score'] = min(100, state['score'] + 8)
                state['logs'].append(f"[SAVUNMA] {selected} uygulandı, APT geriledi")
            
            if len(state['defenses']) >= 5:
                state['contained'] = True
                state['logs'].append("[ZAFER] 🏆 APT tamamen püskürtüldü!")
                st.balloons()
            
            ScenarioState.set("s10B", state)
        
        if st.button("🤖 APT İlerle", use_container_width=True):
            state['apt_phase'] = min(6, state['apt_phase'] + 1)
            state['score'] = max(0, state['score'] - 15)
            state['logs'].append("[APT] Saldırgan bir sonraki aşamaya geçti!")
            ScenarioState.set("s10B", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("10B")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("10B")
        
        render_performance_comparison("10B")
        render_attack_heatmap("10B")
        render_world_attack_map("10B")
        render_auto_pilot_button("10B", "s10B")


def render_10C():
    """10C: Mor Takım"""
    state = ScenarioState.get("s10C", {
        'maturity': 30, 'tests_run': 0,
        'improvements': [], 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("10C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🟣 Mor Takım Paneli")
        st.metric("Güvenlik Olgunluğu", f"%{state['maturity']}")
        st.metric("Test Sayısı", state['tests_run'])
        
        maturity_fig = create_cyber_gauge(
            state['maturity'], "Olgunluk Seviyesi", thresholds=(50, 80)
        )
        st.plotly_chart(maturity_fig, use_container_width=True)
    
    with col2:
        st.subheader("🔬 İyileştirme Terminali")
        
        improvements = [
            "Tespit Kuralı Geliştir", "Log Retention Artır",
            "Alert Tuning", "Playbook Oluştur",
            "Tehdit İstihbaratı Entegre Et", "Otomasyon Ekle"
        ]
        selected = st.selectbox("İyileştirme:", improvements)
        
        if st.button("▶️ Uygula", use_container_width=True):
            if selected not in state['improvements']:
                state['improvements'].append(selected)
                state['maturity'] = min(100, state['maturity'] + random.randint(5, 15))
                state['logs'].append(f"[İYİLEŞTİRME] {selected} uygulandı")
            
            if state['maturity'] >= 90:
                state['logs'].append("[BAŞARI] 🏆 Optimum güvenlik olgunluğuna ulaşıldı!")
                st.balloons()
            
            ScenarioState.set("s10C", state)
        
        if st.button("🤖 Test Çalıştır", use_container_width=True):
            state['tests_run'] += 1
            state['logs'].append(f"[TEST] #{state['tests_run']} simülasyon tamamlandı")
            ScenarioState.set("s10C", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("10C")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("10C")
        
        render_performance_comparison("10C")
        render_auto_pilot_button("10C", "s10C")


def render_10D():
    """10D: Sıfır Gün"""
    state = ScenarioState.get("s10D", {
        'fuzzing_done': False, 'crash_analyzed': False,
        'exploit_developed': False, 'risk': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("10D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("💎 Zero-Day Paneli")
        st.metric("Fuzzing", "✅" if state['fuzzing_done'] else "❌")
        st.metric("Crash Analizi", "✅" if state['crash_analyzed'] else "❌")
        st.metric("Exploit", "✅" if state['exploit_developed'] else "❌")
        
        risk_fig = create_cyber_gauge(state['risk'], "Tespit Riski")
        st.plotly_chart(risk_fig, use_container_width=True)
    
    with col2:
        st.subheader("🔍 Araştırma Terminali")
        
        actions = ["Fuzzing Başlat", "Crash Analizi",
                   "Root Cause Bul", "Exploit Geliştir", "Test Et"]
        selected = st.selectbox("Aşama:", actions)
        
        if st.button("▶️ Çalıştır", use_container_width=True):
            if "Fuzzing" in selected:
                state['fuzzing_done'] = True
                state['logs'].append("[FUZZ] 3 crash tespit edildi")
            elif "Crash" in selected and state['fuzzing_done']:
                state['crash_analyzed'] = True
                state['logs'].append("[ANALİZ] Heap overflow zafiyeti doğrulandı")
            elif "Exploit" in selected and state['crash_analyzed']:
                state['exploit_developed'] = True
                state['logs'].append("[BAŞARI] 🏆 Zero-day exploit geliştirildi!")
                st.balloons()
            
            state['risk'] = min(100, state['risk'] + random.randint(5, 15))
            ScenarioState.set("s10D", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("10D")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("10D")
        
        render_performance_comparison("10D")
        render_auto_pilot_button("10D", "s10D")


def render_10E():
    """10E: Küresel Tehdit"""
    state = ScenarioState.get("s10E", {
        'score': 100, 
        'sectors': {
            'Enerji': 80, 'Finans': 75, 'Telekom': 70,
            'Sağlık': 85, 'Ulaştırma': 65
        },
        'crisis_level': 30, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("10E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🌍 Ulusal Siber Durum")
        st.metric("Kriz Seviyesi", f"%{state['crisis_level']}")
        st.metric("Genel Puan", state['score'])
        
        for sector, health in state['sectors'].items():
            icon = "🔴" if health < 30 else "🟡" if health < 60 else "🟢"
            st.write(f"{icon} {sector}: %{health}")
    
    with col2:
        st.subheader("🏛️ Kriz Yönetimi")
        
        sectors_list = list(state['sectors'].keys())
        selected_sector = st.selectbox("Sektör:", sectors_list)
        
        actions = ["Kaynak Takviye", "CERT Aktivasyonu", 
                   "Kamuoyu Bilgilendirme", "Uluslararası İşbirliği"]
        selected_action = st.selectbox("Aksiyon:", actions)
        
        if st.button("▶️ Uygula", use_container_width=True):
            state['sectors'][selected_sector] = min(
                100, state['sectors'][selected_sector] + random.randint(5, 20)
            )
            state['crisis_level'] = max(5, state['crisis_level'] - random.randint(3, 10))
            state['score'] = min(100, state['score'] + 3)
            state['logs'].append(f"[MÜDAHALE] {selected_sector}: {selected_action}")
            ScenarioState.set("s10E", state)
        
        if st.button("🤖 AI Saldırı Dalgası", use_container_width=True):
            for s in state['sectors']:
                state['sectors'][s] = max(10, state['sectors'][s] - random.randint(5, 15))
            state['crisis_level'] = min(100, state['crisis_level'] + 15)
            state['logs'].append("[SALDIRI] 🔴 Yeni küresel saldırı dalgası!")
            ScenarioState.set("s10E", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("10E")
        with st.expander("📚 Referanslar", expanded=False):
            display_references("10E")
        
        render_performance_comparison("10E")
        render_world_attack_map("10E")
        render_auto_pilot_button("10E", "s10E")



# ============================================
# BÖLÜM 13: SENARYO RENDERERS SÖZLÜĞÜ (50 SENARYO)
# ============================================

SCENARIO_RENDERERS = {
    # Seviye 1 - Veri Bahçesi
    "1A": render_1A, "1B": render_1B, "1C": render_1C,
    "1D": render_1D, "1E": render_1E,
    
    # Seviye 2 - Dijital Kale
    "2A": render_2A, "2B": render_2B, "2C": render_2C,
    "2D": render_2D, "2E": render_2E,
    
    # Seviye 3 - Solucan Deliği
    "3A": render_3A, "3B": render_3B, "3C": render_3C,
    "3D": render_3D, "3E": render_3E,
    
    # Seviye 4 - Fırtına
    "4A": render_4A, "4B": render_4B, "4C": render_4C,
    "4D": render_4D, "4E": render_4E,
    
    # Seviye 5 - Gölgeler İçinde
    "5A": render_5A, "5B": render_5B, "5C": render_5C,
    "5D": render_5D, "5E": render_5E,
    
    # Seviye 6 - Büyük Oyun
    "6A": render_6A, "6B": render_6B, "6C": render_6C,
    "6D": render_6D, "6E": render_6E,
    
    # Seviye 7 - Kod Enjeksiyonu
    "7A": render_7A, "7B": render_7B, "7C": render_7C,
    "7D": render_7D, "7E": render_7E,
    
    # Seviye 8 - Tersine Mühendislik
    "8A": render_8A, "8B": render_8B, "8C": render_8C,
    "8D": render_8D, "8E": render_8E,
    
    # Seviye 9 - Sosyal Mühendislik
    "9A": render_9A, "9B": render_9B, "9C": render_9C,
    "9D": render_9D, "9E": render_9E,
    
    # Seviye 10 - Nihai Sınav
    "10A": render_10A, "10B": render_10B, "10C": render_10C,
    "10D": render_10D, "10E": render_10E,
    
    # Mavi Takım İkizleri (aşağıda .update() ile doldurulur)
    "1A-DEF": None, "1C-DEF": None, "1E-DEF": None,
    "2A-DEF": None, "2C-DEF": None,
    "3A-DEF": None, "3E-DEF": None,
    "4A-DEF": None, "4C-DEF": None,
    "5A-DEF": None, "5D-DEF": None,
    "6A-DEF": None,
    "7A-DEF": None,
    "9A-DEF": None,
    "10A-DEF": None,
}


# ============================================
# BÖLÜM 14: MAVİ TAKIM İKİZLERİ (15 SENARYO)
# ============================================

# --- İkiz Senaryo Tanımları ---

ALL_SCENARIOS["1A-DEF"] = {
    "title": "1A-DEF: Port Tarama Tespit Sistemi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Port Tarama Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, 1A'daki port tarama aktivitesinin savunma tarafını deneyimlemenizi 
sağlar. Bir güvenlik operasyon merkezi (SOC) analisti olarak, ağınızdaki 
port tarama aktivitelerini tespit etmek ve engellemekle görevlisiniz. AI 
simülasyonu, sürekli olarak farklı portlara tarama denemeleri yapar. Sizin 
göreviniz, bu aktiviteleri tespit etmek, kaynağını belirlemek ve uygun 
savunma önlemlerini uygulamaktır. Elinizde port tarama tespit kuralları, 
IDS/IPS yapılandırma araçları ve firewall kural editörü bulunur. AI 
simülasyonu, tarama hızını ve desenini sürekli değiştirir; bu nedenle 
statik kurallar yetersiz kalır. Davranışsal analiz yapmalı, anormal port 
erişim desenlerini tespit etmelisiniz. Yanlış alarm verirseniz meşru 
kullanıcıların hizmetlere erişimi engellenir. Başarı puanınız; tespit 
edilen tarama sayısı, yanlış pozitif oranı, ortalama tespit süresi ve 
engellenen saldırı yüzdesine göre hesaplanır. Bu senaryo, port tarama 
tespitinin inceliklerini, IDS/IPS sistemlerinin yapılandırılmasını ve 
SOC operasyonlarını öğretir.
"""
}

ALL_SCENARIOS["1C-DEF"] = {
    "title": "1C-DEF: Honeypot Yönetimi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Honeypot Kaşifi Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, honeypot (bal küpü) sistemlerinin yönetimini ve etkinliğini 
öğretir. Bir deception (aldatma) teknolojisi uzmanı olarak, kurumunuzun 
honeypot altyapısını yönetiyorsunuz. AI simülasyonu, honeypot'larınızı 
tespit etmeye çalışan gelişmiş bir tehdit aktörünü temsil eder. Göreviniz, 
honeypot'ların gerçekçi kalmasını sağlamak, tuzak sinyallerini minimize 
etmek ve yakalanan tehditlerden istihbarat toplamaktır. Elinizde honeypot 
yapılandırma araçları, log analiz modülü ve tehdit istihbaratı 
entegrasyonu bulunur. AI simülasyonu, honeypot'ların gerçek olmadığını 
tespit etmeye çalışır; siz ise honeypot'ları daha inandırıcı hale 
getirmelisiniz. Bu senaryo, aldatma teknolojilerinin savunmadaki rolünü, 
tehdit istihbaratı toplamayı ve deception stratejilerini öğretir.
"""
}

ALL_SCENARIOS["1E-DEF"] = {
    "title": "1E-DEF: Kablosuz Ağ Savunması",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Kablosuz Tehdit Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, kablosuz ağ savunmasının inceliklerini öğretir. Bir kablosuz 
ağ güvenlik mühendisi olarak, kurumunuzun Wi-Fi altyapısını korumakla 
görevlisiniz. AI simülasyonu, çeşitli kablosuz tehdit vektörleri kullanarak 
ağınıza sızmaya çalışır: deauthentication saldırıları, evil twin, rogue 
access point, WPS saldırıları ve daha fazlası. Sizin göreviniz, kablosuz 
ağ izleme araçlarıyla bu tehditleri tespit etmek, kaynağını belirlemek 
ve bertaraf etmektir. Elinizde WIDS (Wireless IDS), WIPS (Wireless IPS), 
spectrum analyzer ve 802.1X yapılandırma araçları bulunur. Başarı 
puanınız; tespit edilen tehdit sayısı, yanlış pozitif oranı, müdahale 
hızı ve ağ kesintisi süresine göre hesaplanır. Bu senaryo, kablosuz 
ağ güvenliğinin tüm yönlerini kapsamlı şekilde öğretir.
"""
}

ALL_SCENARIOS["2A-DEF"] = {
    "title": "2A-DEF: IDS Kural Yazma",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "IDS Test Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, IDS (Intrusion Detection System) kural yazma sanatını öğretir. 
Bir IDS kural mühendisi olarak, kurumunuzun tespit yeteneklerini 
geliştirmekle görevlisiniz. AI simülasyonu, sürekli yeni aktivite 
vektörleri üretir; siz ise bu aktiviteleri tespit edecek kurallar 
yazmalısınız. Elinizde Snort/Suricata kural editörü, imza analiz modülü 
ve performans izleme araçları bulunur. Yazdığınız her kural, hem tespit 
yeteneğini artırmalı hem de yanlış pozitif üretmemelidir. AI simülasyonu, 
kurallarınızı öğrenmeye ve atlatmaya çalışır; bu nedenle kurallarınızı 
sürekli güncellemelisiniz. Başarı puanınız; tespit edilen aktivite sayısı, 
yanlış pozitif oranı, kural performansına etki ve kapsama yüzdesine göre 
hesaplanır. Bu senaryo, IDS kural yazma, imza analizi ve tespit 
mühendisliğini öğretir.
"""
}

ALL_SCENARIOS["2C-DEF"] = {
    "title": "2C-DEF: WAF Yapılandırma",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Web Uygulama Test Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, WAF (Web Application Firewall) yapılandırmasının inceliklerini 
öğretir. Bir web güvenlik mühendisi olarak, kurumunuzun web uygulamalarını 
korumakla görevlisiniz. AI simülasyonu, sürekli olarak web uygulamalarınıza 
yönelik test girişimlerinde bulunur: SQL enjeksiyonu, XSS, CSRF, dosya 
yükleme açıkları, SSRF ve daha fazlası. Sizin göreviniz, WAF kurallarını 
yapılandırarak bu girişimleri engellemektir. Elinizde ModSecurity kural 
editörü, WAF log analiz modülü ve sanal yama (virtual patching) araçları 
bulunur. Her kural, uygulamanın performansını etkilememeli ve meşru 
kullanıcıları engellememelidir. Başarı puanınız; engellenen test sayısı, 
yanlış pozitif oranı, performans etkisi ve uygulama kapsama yüzdesine göre 
hesaplanır. Bu senaryo, WAF yönetimi, güvenli kod geliştirme ve web 
uygulama güvenliğini öğretir.
"""
}

ALL_SCENARIOS["3A-DEF"] = {
    "title": "3A-DEF: VPN Güçlendirme",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "VPN Test Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, VPN güvenliğinin güçlendirilmesini öğretir. Bir ağ güvenlik 
mühendisi olarak, kurumunuzun VPN altyapısını güçlendirmekle görevlisiniz. 
AI simülasyonu, VPN tünelinize yönelik çeşitli test girişimlerinde bulunur: 
zayıf şifreleme algoritmaları, anahtar değişim zafiyetleri, yapılandırma 
hataları ve daha fazlası. Sizin göreviniz, VPN yapılandırmasını analiz 
etmek, zayıf noktaları tespit etmek ve güçlendirmektir. Elinizde VPN 
yapılandırma editörü, şifreleme analiz araçları ve sertifika yönetim 
modülü bulunur. Her güçlendirme, güvenliği artırmalı ama performansı 
düşürmemelidir. Başarı puanınız; kapatılan zafiyet sayısı, şifreleme 
gücü artışı, performans etkisi ve kullanıcı deneyimi metriğine göre 
hesaplanır. Bu senaryo, VPN güvenliği, kriptografi ve ağ yapılandırmasını 
öğretir.
"""
}

ALL_SCENARIOS["3E-DEF"] = {
    "title": "3E-DEF: Akıllı Kontrat Denetimi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Akıllı Kontrat Test Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, akıllı kontrat güvenlik denetimini öğretir. Bir blockchain 
güvenlik uzmanı olarak, kurumunuzun DeFi platformundaki akıllı 
kontratları denetlemekle görevlisiniz. AI simülasyonu, sürekli olarak 
kontratlarınıza yönelik test girişimlerinde bulunur: reentrancy, 
integer overflow, oracle manipulation, flash loan ve daha fazlası. 
Sizin göreviniz, kontrat kodunu analiz etmek, zafiyetleri tespit etmek 
ve düzeltmektir. Elinizde Solidity analiz araçları, formal verification 
modülü ve test framework'ü bulunur. Her düzeltme, kontratın 
fonksiyonelliğini bozmamalı ve gas maliyetini artırmamalıdır. Başarı 
puanınız; tespit edilen zafiyet sayısı, düzeltilen zafiyet yüzdesi, 
gas optimizasyonu ve kontrat güvenliğine göre hesaplanır. Bu senaryo, 
akıllı kontrat güvenliği, blockchain teknolojisi ve güvenli kod 
geliştirmeyi öğretir.
"""
}

ALL_SCENARIOS["4A-DEF"] = {
    "title": "4A-DEF: DDoS Azaltma Stratejisi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "DDoS Test Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, DDoS azaltma stratejilerinin geliştirilmesini öğretir. Bir 
ağ güvenlik mimarı olarak, kurumunuzun DDoS dayanıklılığını artırmakla 
görevlisiniz. AI simülasyonu, sürekli olarak farklı vektörlerden DDoS 
testleri yapar: volumetric, protocol, application-layer ve daha 
fazlası. Sizin göreviniz, katmanlı savunma stratejisi geliştirmek, 
kaynakları optimize etmek ve hizmet sürekliliğini sağlamaktır. Elinizde 
yük dengeleyici, anycast DNS, scrubbing center ve auto-scaling araçları 
bulunur. Her savunma katmanı, maliyet-etkin olmalı ve meşru trafiği 
etkilememelidir. Başarı puanınız; engellenen test yüzdesi, hizmet 
kesintisi süresi, maliyet verimliliği ve yanlış pozitif oranına göre 
hesaplanır. Bu senaryo, DDoS savunma mimarisi, yük dengeleme ve 
ölçeklendirme stratejilerini öğretir.
"""
}

ALL_SCENARIOS["4C-DEF"] = {
    "title": "4C-DEF: DNS Sunucu Sertleştirme",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "DNS Test Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, DNS sunucu sertleştirmesini öğretir. Bir DNS güvenlik 
mühendisi olarak, kurumunuzun DNS altyapısını güçlendirmekle 
görevlisiniz. AI simülasyonu, sürekli olarak DNS sunucularınıza yönelik 
test girişimlerinde bulunur: cache poisoning, amplification, zone 
transfer, DNS rebinding ve daha fazlası. Sizin göreviniz, DNS 
yapılandırmasını analiz etmek, zafiyetleri kapatmak ve güvenli 
yapılandırma uygulamaktır. Elinizde DNSSEC yapılandırma araçları, 
response rate limiting modülü ve DNS monitoring araçları bulunur. 
Başarı puanınız; kapatılan zafiyet sayısı, DNS performansı, 
uyumluluk seviyesi ve hizmet sürekliliğine göre hesaplanır. Bu 
senaryo, DNS güvenliği, protokol analizi ve ağ altyapısı 
sertleştirmeyi öğretir.
"""
}

ALL_SCENARIOS["5A-DEF"] = {
    "title": "5A-DEF: Kurumsal Ayak İzi Yönetimi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "OSINT Toplayıcı Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, kurumsal ayak izi (footprint) yönetimini öğretir. Bir 
kurumsal güvenlik analisti olarak, kurumunuzun dış dünyadaki görünürlüğünü 
minimize etmekle görevlisiniz. AI simülasyonu, açık kaynak istihbarat 
(OSINT) teknikleri kullanarak kurumunuz hakkında bilgi toplamaya çalışır: 
çalışan profilleri, teknoloji stack'i, altyapı detayları ve daha fazlası. 
Sizin göreviniz, bu bilgi sızıntılarını tespit etmek, minimize etmek ve 
çalışan farkındalığını artırmaktır. Elinizde OSINT monitoring araçları, 
sosyal medya politikası editörü ve çalışan eğitim modülü bulunur. 
Başarı puanınız; minimize edilen bilgi sayısı, çalışan farkındalık 
seviyesi ve OSINT zorluk skoruna göre hesaplanır. Bu senaryo, OSINT 
savunması, kurumsal güvenlik politikaları ve OPSEC prensiplerini 
öğretir.
"""
}

ALL_SCENARIOS["5D-DEF"] = {
    "title": "5D-DEF: Yetki Sertleştirme",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Yetki Yükseltme Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, yetki yükseltme savunmasının inceliklerini öğretir. Bir 
sistem güvenlik yöneticisi olarak, kurumunuzun sistemlerini yetki 
yükseltme aktivitelerine karşı sertleştirmekle görevlisiniz. AI 
simülasyonu, sürekli olarak çeşitli yetki yükseltme teknikleri 
dener: SUID binary exploitation, sudo misconfiguration, kernel 
exploits, token manipulation, DLL hijacking ve daha fazlası. Sizin 
göreviniz, sistem yapılandırmasını analiz etmek, zafiyetleri tespit 
etmek ve sertleştirmektir. Elinizde güvenlik yapılandırma denetim 
araçları, EDR kural editörü ve least privilege yönetim modülü bulunur. 
Başarı puanınız; kapatılan zafiyet sayısı, sistem uyumluluk skoru, 
kullanıcı deneyimi ve tespit oranına göre hesaplanır. Bu senaryo, 
sistem sertleştirme, erişim kontrolü ve least privilege 
prensiplerini öğretir.
"""
}

ALL_SCENARIOS["6A-DEF"] = {
    "title": "6A-DEF: APT Tespit ve Müdahale",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "APT Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, gelişmiş kalıcı tehdit (APT) tespiti ve müdahalesini 
öğretir. Bir tehdit avcısı (threat hunter) olarak, kurumunuza sızmış 
bir APT'yi tespit etmek ve bertaraf etmekle görevlisiniz. AI 
simülasyonu, gelişmiş teknikler kullanarak ağınızda kalıcılık 
sağlamıştır: custom malware, fileless execution, living-off-the-land 
binaries, encrypted C2 channels ve daha fazlası. Sizin göreviniz, 
anormal davranışları tespit etmek, saldırının kapsamını belirlemek 
ve müdahale etmektir. Elinizde SIEM, EDR, NDR, threat intelligence 
ve SOAR araçları bulunur. Başarı puanınız; tespit süresi, müdahale 
hızı, temizlenen sistem sayısı ve veri kaybı önleme oranına göre 
hesaplanır. Bu senaryo, APT savunması, tehdit avı metodolojileri ve 
kriz yönetimini öğretir.
"""
}

ALL_SCENARIOS["7A-DEF"] = {
    "title": "7A-DEF: SQLi Savunması - Kod Denetimi",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "SQLi Test Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, SQL enjeksiyon savunmasının inceliklerini öğretir. Bir 
yazılım güvenlik mühendisi olarak, geliştirme ekibinizin kodlarını 
denetliyor ve AI kontrollü bir simülasyonun SQLi denemelerine karşı 
savunma yapıyorsunuz. AI simülasyonu, sürekli olarak kod tabanındaki 
zafiyetli noktaları arar: string birleştirme ile yazılmış sorgular, 
yetersiz input validation, aşırı yetkili veritabanı kullanıcıları 
ve detaylı hata mesajları. Sizin göreviniz; kod inceleme, statik 
analiz araçları, güvenli kod standartları ve savunma katmanları 
kullanarak bu zafiyetleri kapatmaktır. Elinizde SAST aracı, kod 
farkındalık kontrol listesi, ORM dönüşüm planı ve WAF kural 
editörü bulunur. Başarı puanınız; tespit edilen zafiyet sayısı, 
kapatılan zafiyet oranı, yanlış pozitif sayısı ve uygulamanın 
performansına etkiye göre hesaplanır. Bu senaryo, güvenli kod 
geliştirme, kod denetim metodolojileri ve OWASP Top 10 A03:2021 
kapsamındaki savunma tekniklerini öğretir.
"""
}

ALL_SCENARIOS["9A-DEF"] = {
    "title": "9A-DEF: Phishing Tespit ve Savunma",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Phishing Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, phishing (oltalama) tespiti ve savunmasını öğretir. Bir 
e-posta güvenlik analisti olarak, kurumunuzun e-posta trafiğini 
korumakla görevlisiniz. AI simülasyonu, sürekli olarak çalışanlara 
yönelik phishing e-postaları gönderir: kimlik avı, spear-phishing, 
BEC (Business Email Compromise), CEO fraud ve daha fazlası. Sizin 
göreviniz, bu e-postaları tespit etmek, karantinaya almak ve 
çalışanları bilinçlendirmektir. Elinizde e-posta güvenlik ağ geçidi, 
DMARC/SPF/DKIM yapılandırma araçları ve farkındalık eğitim modülü 
bulunur. Başarı puanınız; tespit edilen phishing oranı, yanlış 
pozitif oranı, çalışan farkındalık seviyesi ve müdahale hızına göre 
hesaplanır. Bu senaryo, e-posta güvenliği, sosyal mühendislik 
savunması ve farkındalık eğitimini öğretir.
"""
}

ALL_SCENARIOS["10A-DEF"] = {
    "title": "10A-DEF: Kırmızı Takım Savunması - Full-Scope",
    "role_human": "Mavi Takım Analisti",
    "role_ai": "Kırmızı Takım Simülasyonu",
    "type": "human_defend",
    "desc": """
Bu senaryo, kırmızı takım simülasyonuna karşı tam kapsamlı savunmayı 
öğretir. Bir mavi takım lideri olarak, kurumunuzu çok aşamalı bir 
siber simülasyona karşı savunmakla görevlisiniz. AI simülasyonu, 
7 aşamalı kill chain'in tamamını kullanır: keşif, silahlanma, 
teslimat, istismar, kurulum, C2 ve hedef. Sizin göreviniz, bu 
aşamaların her birinde savunma katmanları oluşturmak, tespit 
etmek ve müdahale etmektir. Elinizde SIEM, SOAR, EDR, NDR, DLP, 
WAF ve threat intelligence araçlarından oluşan tam entegre bir 
savunma altyapısı bulunur. AI simülasyonu, savunma önlemlerinize 
sürekli adapte olur. Başarı puanınız; savunulan varlık oranı, 
tespit süresi, müdahale etkinliği ve kurum etkisine göre 
hesaplanır. Bu senaryo, kapsamlı siber savunma stratejilerini, 
kriz yönetimini ve savunma orkestrasyonunu öğretir.
"""
}


# --- İkiz Senaryo Render Fonksiyonları ---

def render_1A_DEF():
    """1A-DEF: Port Tarama Tespit Sistemi"""
    state = ScenarioState.get("s1A_DEF", {
        'score': 100, 'detected_scans': 0, 'blocked_ips': [],
        'rules': [], 'logs': [], 'false_positives': 0, 'ai_scans': 0
    })
    
    EthicsGuard.display_ethics_banner("1A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🛡️ Tespit Paneli")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Tespit Edilen Tarama", state['detected_scans'])
        st.metric("AI Tarama Sayısı", state['ai_scans'])
        st.metric("Yanlış Pozitif", state['false_positives'])
        
        st.subheader("⚙️ Tespit Kuralları")
        rule = st.selectbox("Kural seç:", [
            "Çoklu Port Erişim Tespiti",
            "SYN Tarama Tespiti",
            "FIN Tarama Tespiti",
            "Yavaş Tarama Tespiti",
            "Anormal Kaynak IP Tespiti"
        ], key="1a_def_rule")
        
        if st.button("➕ Kural Ekle", use_container_width=True, key="1a_def_add"):
            if rule not in state['rules']:
                state['rules'].append(rule)
                state['score'] = min(100, state['score'] + 8)
                state['logs'].append(f"[KURAL] {rule} aktif")
                ScenarioState.set("s1A_DEF", state)
    
    with col2:
        st.subheader("🎯 AI Tarama Simülasyonu")
        
        if st.button("▶️ Yeni Tarama Simüle Et", use_container_width=True, key="1a_def_scan"):
            state['ai_scans'] += 1
            scan_type = random.choice(['SYN', 'FIN', 'XMAS', 'NULL', 'Yavaş'])
            
            detection_power = len(state['rules']) * 15
            scan_power = random.randint(20, 80)
            
            if detection_power > scan_power:
                state['detected_scans'] += 1
                state['logs'].append(f"[TESPİT] ✅ {scan_type} taraması engellendi")
                state['score'] = min(100, state['score'] + 3)
            else:
                state['logs'].append(f"[KAÇIRILDI] ⚠️ {scan_type} taraması tespit edilemedi")
                state['score'] = max(0, state['score'] - 15)
            
            if random.random() < 0.1:
                state['false_positives'] += 1
                state['logs'].append("[YANLIŞ ALARM] Meşru trafik engellendi")
                state['score'] = max(0, state['score'] - 5)
            
            ScenarioState.set("s1A_DEF", state)
        
        st.markdown("**Aktif Kurallar:**")
        for r in state['rules']:
            st.write(f"✅ {r}")
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("1A")
        
        render_performance_comparison("1A")
        render_attack_heatmap("1A")
        render_auto_pilot_button("1A", "s1A_DEF")


def render_1C_DEF():
    """1C-DEF: Honeypot Yönetimi"""
    state = ScenarioState.get("s1C_DEF", {
        'score': 100, 'honeypots': [
            {'name': 'Web-HP-01', 'type': 'Web', 'realistic': 70},
            {'name': 'SSH-HP-01', 'type': 'SSH', 'realistic': 60},
            {'name': 'DB-HP-01', 'type': 'DB', 'realistic': 65}
        ],
        'captured': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("1C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🍯 Honeypot Paneli")
        st.metric("Savunma Puanı", state['score'])
        st.metric("Yakalanan Tehdit", state['captured'])
        
        st.subheader("📊 Aktif Honeypot'lar")
        for hp in state['honeypots']:
            st.metric(hp['name'], f"Gerçekçilik: %{hp['realistic']}")
    
    with col2:
        st.subheader("🎯 Honeypot Yönetimi")
        
        selected_hp = st.selectbox(
            "Honeypot seç:", 
            [hp['name'] for hp in state['honeypots']],
            key="1c_def_hp"
        )
        
        if st.button("🔧 Gerçekçilik Artır", use_container_width=True, key="1c_def_improve"):
            for hp in state['honeypots']:
                if hp['name'] == selected_hp:
                    hp['realistic'] = min(100, hp['realistic'] + random.randint(5, 15))
                    state['logs'].append(f"[İYİLEŞTİRME] {selected_hp} gerçekçilik: %{hp['realistic']}")
            ScenarioState.set("s1C_DEF", state)
        
        if st.button("🤖 AI Kaşif Simüle Et", use_container_width=True, key="1c_def_scan"):
            avg_realistic = sum(hp['realistic'] for hp in state['honeypots']) / len(state['honeypots'])
            
            if avg_realistic > 75:
                state['captured'] += 1
                state['logs'].append("[YAKALANDI] ✅ AI honeypot'u gerçek sandı!")
                state['score'] = min(100, state['score'] + 10)
            else:
                state['logs'].append("[TESPİT] ⚠️ AI honeypot'u fark etti!")
                state['score'] = max(0, state['score'] - 15)
            
            ScenarioState.set("s1C_DEF", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("1C")
        render_performance_comparison("1C")
        render_auto_pilot_button("1C", "s1C_DEF")


def render_1E_DEF():
    """1E-DEF: Kablosuz Ağ Savunması"""
    state = ScenarioState.get("s1E_DEF", {
        'score': 100, 'detected_threats': 0, 'blocked_devices': [],
        'wids_rules': [], 'logs': [], 'rogue_aps': 0
    })
    
    EthicsGuard.display_ethics_banner("1E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📶 Kablosuz Ağ Durumu")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Tespit Edilen Tehdit", state['detected_threats'])
        st.metric("Rogue AP", state['rogue_aps'])
        st.metric("Engellenen Cihaz", len(state['blocked_devices']))
        
        st.subheader("🛡️ WIDS Kuralları")
        rule = st.selectbox("Kural ekle:", [
            "Deauth Saldırı Tespiti",
            "Evil Twin Tespiti",
            "Rogue AP Tespiti",
            "WPS Saldırı Tespiti",
            "MAC Spoofing Tespiti"
        ], key="1e_def_rule")
        
        if st.button("➕ Kural Ekle", use_container_width=True, key="1e_def_add"):
            if rule not in state['wids_rules']:
                state['wids_rules'].append(rule)
                state['score'] = min(100, state['score'] + 8)
                state['logs'].append(f"[WIDS] {rule} aktif")
                ScenarioState.set("s1E_DEF", state)
    
    with col2:
        st.subheader("🎯 AI Kablosuz Tehdit Simülasyonu")
        
        if st.button("▶️ Yeni Tehdit Simüle Et", use_container_width=True, key="1e_def_threat"):
            threat = random.choice([
                'Deauth Saldırısı', 'Evil Twin', 'Rogue AP',
                'WPS Saldırısı', 'MAC Spoofing'
            ])
            
            detection_power = len(state['wids_rules']) * 15
            threat_power = random.randint(20, 80)
            
            if detection_power > threat_power:
                state['detected_threats'] += 1
                state['logs'].append(f"[TESPİT] ✅ {threat} engellendi")
                state['score'] = min(100, state['score'] + 3)
            else:
                state['logs'].append(f"[KAÇIRILDI] ⚠️ {threat} tespit edilemedi")
                state['score'] = max(0, state['score'] - 15)
                if 'Rogue AP' in threat:
                    state['rogue_aps'] += 1
            
            ScenarioState.set("s1E_DEF", state)
        
        st.markdown("**Aktif WIDS Kuralları:**")
        for r in state['wids_rules']:
            st.write(f"✅ {r}")
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("1E")
        render_performance_comparison("1E")
        render_auto_pilot_button("1E", "s1E_DEF")


def render_2A_DEF():
    """2A-DEF: IDS Kural Yazma"""
    state = ScenarioState.get("s2A_DEF", {
        'score': 100, 'rules': [], 'detected': 0, 'ai_attacks': 0,
        'false_positives': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("2A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔍 IDS Kural Paneli")
        st.metric("IDS Puanı", state['score'])
        st.metric("Tespit Edilen", state['detected'])
        st.metric("Yanlış Pozitif", state['false_positives'])
        st.metric("Kural Sayısı", len(state['rules']))
    
    with col2:
        st.subheader("⚙️ Kural Editörü")
        
        rule_name = st.text_input("Kural Adı:", key="2a_def_name", placeholder="SQL Injection Detect")
        rule_pattern = st.text_input("Pattern (regex):", key="2a_def_pattern", placeholder="(union.*select|select.*from)")
        
        if st.button("➕ Kural Ekle", use_container_width=True, key="2a_def_add"):
            if rule_name and rule_pattern:
                state['rules'].append({
                    'name': rule_name,
                    'pattern': rule_pattern,
                    'hits': 0
                })
                state['score'] = min(100, state['score'] + 5)
                state['logs'].append(f"[KURAL] {rule_name} eklendi")
                ScenarioState.set("s2A_DEF", state)
        
        if st.button("🤖 AI Aktivite Simüle Et", use_container_width=True, key="2a_def_attack"):
            state['ai_attacks'] += 1
            attack_patterns = [
                ("SQL Injection", "union select"),
                ("XSS", "<script>"),
                ("Path Traversal", "../../etc"),
                ("Command Injection", "; cat /etc/passwd")
            ]
            attack_name, attack_pattern = random.choice(attack_patterns)
            
            detected = False
            for rule in state['rules']:
                if rule['pattern'].lower() in attack_pattern.lower():
                    detected = True
                    rule['hits'] += 1
                    break
            
            if detected:
                state['detected'] += 1
                state['logs'].append(f"[TESPİT] ✅ {attack_name} engellendi")
                state['score'] = min(100, state['score'] + 5)
            else:
                state['logs'].append(f"[KAÇIRILDI] ⚠️ {attack_name} kuralı eksik")
                state['score'] = max(0, state['score'] - 15)
            
            ScenarioState.set("s2A_DEF", state)
        
        st.markdown("**Aktif Kurallar:**")
        for r in state['rules']:
            st.write(f"✅ {r['name']} (Hit: {r['hits']})")
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("2A")
        render_performance_comparison("2A")
        render_attack_heatmap("2A")
        render_auto_pilot_button("2A", "s2A_DEF")


def render_2C_DEF():
    """2C-DEF: WAF Yapılandırma"""
    state = ScenarioState.get("s2C_DEF", {
        'score': 100, 'rules': [], 'blocked': 0,
        'false_positives': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("2C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🧱 WAF Yapılandırma Paneli")
        st.metric("WAF Puanı", state['score'])
        st.metric("Engellenen", state['blocked'])
        st.metric("Yanlış Pozitif", state['false_positives'])
        st.metric("Kural Sayısı", len(state['rules']))
        
        waf_fig = create_cyber_gauge(state['score'], "WAF Etkinliği")
        st.plotly_chart(waf_fig, use_container_width=True)
    
    with col2:
        st.subheader("⚙️ Kural Yönetimi")
        
        rule = st.selectbox("Kural ekle:", [
            "SQL Enjeksiyon Koruması",
            "XSS Filtreleme",
            "CSRF Token Doğrulama",
            "Path Traversal Koruması",
            "Command Injection Filtresi",
            "XXE Koruması",
            "SSRF Koruması"
        ], key="2c_def_rule")
        
        if st.button("➕ Kural Ekle", use_container_width=True, key="2c_def_add"):
            if rule not in state['rules']:
                state['rules'].append(rule)
                state['score'] = min(100, state['score'] + 6)
                state['logs'].append(f"[WAF] {rule} eklendi")
                ScenarioState.set("s2C_DEF", state)
        
        if st.button("🎯 Web Testi Simüle Et", use_container_width=True, key="2c_def_attack"):
            test_type = random.choice([
                "SQL Injection", "XSS", "Path Traversal", "Command Injection",
                "XXE", "SSRF", "CSRF"
            ])
            
            rule_map = {
                "SQL Injection": "SQL Enjeksiyon Koruması",
                "XSS": "XSS Filtreleme",
                "Path Traversal": "Path Traversal Koruması",
                "Command Injection": "Command Injection Filtresi",
                "XXE": "XXE Koruması",
                "SSRF": "SSRF Koruması",
                "CSRF": "CSRF Token Doğrulama"
            }
            
            required_rule = rule_map.get(test_type)
            
            if required_rule in state['rules']:
                state['blocked'] += 1
                state['logs'].append(f"[ENGELLENDİ] ✅ {test_type} filtrelendi")
                state['score'] = min(100, state['score'] + 3)
            else:
                state['logs'].append(f"[KAÇIRILDI] ⚠️ {test_type} kural eksik!")
                state['score'] = max(0, state['score'] - 15)
            
            if random.random() < 0.1:
                state['false_positives'] += 1
                state['logs'].append("[YANLIŞ ALARM] Meşru istek engellendi")
                state['score'] = max(0, state['score'] - 5)
            
            ScenarioState.set("s2C_DEF", state)
        
        st.markdown("**Aktif WAF Kuralları:**")
        for r in state['rules']:
            st.write(f"✅ {r}")
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("2C")
        render_performance_comparison("2C")
        render_attack_heatmap("2C")
        render_auto_pilot_button("2C", "s2C_DEF")


def render_3A_DEF():
    """3A-DEF: VPN Güçlendirme"""
    state = ScenarioState.get("s3A_DEF", {
        'score': 100, 'vpn_config': {
            'cipher': 'AES-128',
            'hash': 'SHA-1',
            'dh_group': 'Group 2',
            'pfs': False
        },
        'vulnerabilities': [], 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("3A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔐 VPN Yapılandırması")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Kapatılan Zafiyet", len(state['vulnerabilities']))
        
        st.markdown("**Mevcut Yapılandırma:**")
        for key, val in state['vpn_config'].items():
            icon = "✅" if val in ['AES-256', 'SHA-256', 'Group 14', True] else "⚠️"
            st.write(f"{icon} {key}: {val}")
    
    with col2:
        st.subheader("🛡️ Güçlendirme")
        
        setting = st.selectbox("Ayar:", [
            "cipher", "hash", "dh_group", "pfs"
        ], key="3a_def_setting")
        
        if setting == "cipher":
            new_value = st.selectbox("Yeni değer:", ["AES-128", "AES-256"], key="3a_def_cipher")
        elif setting == "hash":
            new_value = st.selectbox("Yeni değer:", ["SHA-1", "SHA-256", "SHA-384"], key="3a_def_hash")
        elif setting == "dh_group":
            new_value = st.selectbox("Yeni değer:", ["Group 2", "Group 5", "Group 14", "Group 19"], key="3a_def_dh")
        else:
            new_value = st.checkbox("Perfect Forward Secrecy (PFS)", key="3a_def_pfs")
        
        if st.button("🔧 Uygula", use_container_width=True, key="3a_def_apply"):
            old_value = state['vpn_config'][setting]
            state['vpn_config'][setting] = new_value
            
            if setting == "cipher" and new_value == "AES-256":
                state['score'] = min(100, state['score'] + 15)
                state['vulnerabilities'].append("Cipher güçlendirildi")
                state['logs'].append("[GÜÇLENDİRME] AES-256 aktif")
            elif setting == "hash" and new_value in ["SHA-256", "SHA-384"]:
                state['score'] = min(100, state['score'] + 10)
                state['vulnerabilities'].append("Hash güçlendirildi")
                state['logs'].append(f"[GÜÇLENDİRME] {new_value} aktif")
            elif setting == "dh_group" and new_value in ["Group 14", "Group 19"]:
                state['score'] = min(100, state['score'] + 12)
                state['vulnerabilities'].append("DH group güçlendirildi")
                state['logs'].append(f"[GÜÇLENDİRME] {new_value} aktif")
            elif setting == "pfs" and new_value:
                state['score'] = min(100, state['score'] + 8)
                state['vulnerabilities'].append("PFS aktif")
                state['logs'].append("[GÜÇLENDİRME] Perfect Forward Secrecy aktif")
            else:
                state['logs'].append(f"[AYAR] {setting} = {new_value}")
            
            ScenarioState.set("s3A_DEF", state)
        
        if st.button("🤖 VPN Testi Simüle Et", use_container_width=True, key="3a_def_test"):
            crypto_strength = 0
            if state['vpn_config']['cipher'] == 'AES-256': crypto_strength += 30
            elif state['vpn_config']['cipher'] == 'AES-128': crypto_strength += 15
            if state['vpn_config']['hash'] in ['SHA-256', 'SHA-384']: crypto_strength += 25
            elif state['vpn_config']['hash'] == 'SHA-1': crypto_strength += 5
            if state['vpn_config']['dh_group'] in ['Group 14', 'Group 19']: crypto_strength += 25
            if state['vpn_config']['pfs']: crypto_strength += 20
            
            if crypto_strength >= 70:
                state['logs'].append("[TEST] ✅ VPN testi savuşturuldu")
                state['score'] = min(100, state['score'] + 5)
            else:
                state['logs'].append("[TEST] ⚠️ VPN zafiyeti tespit edildi")
                state['score'] = max(0, state['score'] - 15)
            
            ScenarioState.set("s3A_DEF", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("3A")
        render_performance_comparison("3A")
        render_auto_pilot_button("3A", "s3A_DEF")


def render_3E_DEF():
    """3E-DEF: Akıllı Kontrat Denetimi"""
    state = ScenarioState.get("s3E_DEF", {
        'score': 100, 'audited': [], 'vulnerabilities': [
            {'id': 'V001', 'type': 'Reentrancy', 'severity': 'CRITICAL', 'patched': False},
            {'id': 'V002', 'type': 'Integer Overflow', 'severity': 'HIGH', 'patched': False},
            {'id': 'V003', 'type': 'Oracle Manipulation', 'severity': 'HIGH', 'patched': False},
            {'id': 'V004', 'type': 'Access Control', 'severity': 'MEDIUM', 'patched': False}
        ],
        'logs': []
    })
    
    EthicsGuard.display_ethics_banner("3E")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("⛓️ Kontrat Denetim Paneli")
        st.metric("Denetim Puanı", state['score'])
        st.metric("Kapatılan Zafiyet", sum(1 for v in state['vulnerabilities'] if v['patched']))
        st.metric("Kalan Zafiyet", sum(1 for v in state['vulnerabilities'] if not v['patched']))
    
    with col2:
        st.subheader("🔍 Zafiyet Yönetimi")
        
        for vuln in state['vulnerabilities']:
            sev_color = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡'}.get(vuln['severity'], '⚪')
            status = "✅ Yamalandı" if vuln['patched'] else "⚠️ Açık"
            
            with st.expander(f"{sev_color} {vuln['id']}: {vuln['type']} ({vuln['severity']}) - {status}"):
                if not vuln['patched']:
                    if st.button(f"🔧 Yamala", key=f"patch_{vuln['id']}"):
                        vuln['patched'] = True
                        state['score'] = min(100, state['score'] + 15)
                        state['logs'].append(f"[YAMA] {vuln['type']} kapatıldı")
                        ScenarioState.set("s3E_DEF", state)
        
        if st.button("🤖 Kontrat Testi Simüle Et", use_container_width=True, key="3e_def_test"):
            unpatched = [v for v in state['vulnerabilities'] if not v['patched']]
            
            if unpatched:
                vuln = random.choice(unpatched)
                state['logs'].append(f"[TEST] ⚠️ {vuln['type']} başarıyla test edildi!")
                state['score'] = max(0, state['score'] - 20)
            else:
                state['logs'].append("[TEST] ✅ Kontrat güvenli, test başarısız")
                state['score'] = min(100, state['score'] + 10)
            
            ScenarioState.set("s3E_DEF", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("3E")
        render_performance_comparison("3E")
        render_auto_pilot_button("3E", "s3E_DEF")


def render_4A_DEF():
    """4A-DEF: DDoS Azaltma Stratejisi"""
    state = ScenarioState.get("s4A_DEF", {
        'score': 100, 'defenses': [], 'ddos_mitigated': 0,
        'downtime': 0, 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("4A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🛡️ DDoS Savunma Paneli")
        st.metric("Savunma Puanı", state['score'])
        st.metric("Engellenen Test", state['ddos_mitigated'])
        st.metric("Kesinti Süresi", f"{state['downtime']} dk")
        st.metric("Savunma Katmanı", len(state['defenses']))
    
    with col2:
        st.subheader("⚙️ Savunma Katmanları")
        
        defense = st.selectbox("Katman ekle:", [
            "Anycast DNS", "Rate Limiting", "IP Reputation",
            "Scrubbing Center", "Auto-Scaling", "WAF Rules",
            "Geo-Blocking", "CAPTCHA Challenge"
        ], key="4a_def_layer")
        
        if st.button("➕ Katman Ekle", use_container_width=True, key="4a_def_add"):
            if defense not in state['defenses']:
                state['defenses'].append(defense)
                state['score'] = min(100, state['score'] + 6)
                state['logs'].append(f"[SAVUNMA] {defense} aktif")
                ScenarioState.set("s4A_DEF", state)
        
        if st.button("🌊 DDoS Testi Simüle Et", use_container_width=True, key="4a_def_attack"):
            attack_power = random.randint(30, 100)
            defense_power = len(state['defenses']) * 15
            
            if defense_power > attack_power:
                state['ddos_mitigated'] += 1
                state['logs'].append(f"[ENGELLENDİ] ✅ Test savuşturuldu (Güç: {attack_power})")
                state['score'] = min(100, state['score'] + 3)
            else:
                state['downtime'] += random.randint(1, 5)
                state['logs'].append(f"[KESİNTİ] 🔴 Test başarılı (Güç: {attack_power})")
                state['score'] = max(0, state['score'] - 15)
            
            ScenarioState.set("s4A_DEF", state)
        
        st.markdown("**Aktif Savunma Katmanları:**")
        for d in state['defenses']:
            st.write(f"✅ {d}")
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("4A")
        render_performance_comparison("4A")
        render_attack_heatmap("4A")
        render_auto_pilot_button("4A", "s4A_DEF")


def render_4C_DEF():
    """4C-DEF: DNS Sunucu Sertleştirme"""
    state = ScenarioState.get("s4C_DEF", {
        'score': 100, 'config': {
            'dnssec': False,
            'rrl': False,
            'zone_transfer': 'any',
            'open_resolver': True
        },
        'logs': []
    })
    
    EthicsGuard.display_ethics_banner("4C")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📡 DNS Sunucu Durumu")
        st.metric("Sertleştirme Puanı", state['score'])
        
        st.markdown("**Mevcut Yapılandırma:**")
        for key, val in state['config'].items():
            icon = "✅" if (isinstance(val, bool) and val) or val == 'none' else "⚠️"
            st.write(f"{icon} {key}: {val}")
    
    with col2:
        st.subheader("🔧 Sertleştirme")
        
        setting = st.selectbox("Ayar:", [
            "dnssec", "rrl", "zone_transfer", "open_resolver"
        ], key="4c_def_setting")
        
        if setting in ["dnssec", "rrl", "open_resolver"]:
            new_value = st.checkbox(
                f"{setting} aktif et",
                value=not state['config'][setting] if setting == "open_resolver" else state['config'][setting],
                key=f"4c_def_{setting}"
            )
            if setting == "open_resolver":
                new_value = not new_value  # Tersine çevir
        else:
            new_value = st.selectbox(
                "Zone transfer:", 
                ["any", "none", "specific"], 
                key="4c_def_zt"
            )
        
        if st.button("🔧 Uygula", use_container_width=True, key="4c_def_apply"):
            old_value = state['config'][setting]
            state['config'][setting] = new_value
            
            improvement = False
            if setting == "dnssec" and new_value:
                state['score'] = min(100, state['score'] + 15)
                improvement = True
            elif setting == "rrl" and new_value:
                state['score'] = min(100, state['score'] + 12)
                improvement = True
            elif setting == "zone_transfer" and new_value in ["none", "specific"]:
                state['score'] = min(100, state['score'] + 10)
                improvement = True
            elif setting == "open_resolver" and not new_value:
                state['score'] = min(100, state['score'] + 18)
                improvement = True
            
            if improvement:
                state['logs'].append(f"[SERTLEŞTİRME] {setting} güçlendirildi")
            else:
                state['logs'].append(f"[AYAR] {setting} = {new_value}")
            
            ScenarioState.set("s4C_DEF", state)
        
        if st.button("🤖 DNS Testi Simüle Et", use_container_width=True, key="4c_def_test"):
            weakness_score = 0
            if not state['config']['dnssec']: weakness_score += 25
            if not state['config']['rrl']: weakness_score += 25
            if state['config']['zone_transfer'] == 'any': weakness_score += 25
            if state['config']['open_resolver']: weakness_score += 25
            
            if weakness_score == 0:
                state['logs'].append("[TEST] ✅ DNS testi savuşturuldu")
                state['score'] = min(100, state['score'] + 5)
            else:
                state['logs'].append(f"[TEST] ⚠️ DNS zafiyeti: {weakness_score}%")
                state['score'] = max(0, state['score'] - 15)
            
            ScenarioState.set("s4C_DEF", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("4C")
        render_performance_comparison("4C")
        render_attack_heatmap("4C")
        render_auto_pilot_button("4C", "s4C_DEF")


def render_5A_DEF():
    """5A-DEF: Kurumsal Ayak İzi Yönetimi"""
    state = ScenarioState.get("s5A_DEF", {
        'score': 100, 'leaks': [
            {'source': 'LinkedIn', 'info': 'Çalışan profilleri', 'fixed': False},
            {'source': 'GitHub', 'info': '.env dosyası', 'fixed': False},
            {'source': 'Shodan', 'info': 'Açık RDP portu', 'fixed': False},
            {'source': 'DNS', 'info': 'Alt domain listesi', 'fixed': False},
            {'source': 'Sosyal Medya', 'info': 'IT yöneticisi konumu', 'fixed': False}
        ],
        'logs': []
    })
    
    EthicsGuard.display_ethics_banner("5A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔍 Ayak İzi Paneli")
        st.metric("Gizlilik Puanı", state['score'])
        st.metric("Kapatılan Sızıntı", sum(1 for l in state['leaks'] if l['fixed']))
        st.metric("Açık Sızıntı", sum(1 for l in state['leaks'] if not l['fixed']))
    
    with col2:
        st.subheader("🔧 Sızıntı Yönetimi")
        
        for leak in state['leaks']:
            status = "✅ Kapatıldı" if leak['fixed'] else "⚠️ Açık"
            with st.expander(f"{leak['source']}: {leak['info']} - {status}"):
                if not leak['fixed']:
                    if st.button(f"🔧 Düzelt", key=f"fix_{leak['source']}"):
                        leak['fixed'] = True
                        state['score'] = min(100, state['score'] + 12)
                        state['logs'].append(f"[DÜZELTİLDİ] {leak['source']} sızıntısı kapatıldı")
                        ScenarioState.set("s5A_DEF", state)
        
        if st.button("🤖 OSINT Tarama Simüle Et", use_container_width=True, key="5a_def_scan"):
            unpatched = [l for l in state['leaks'] if not l['fixed']]
            
            if unpatched:
                leak = random.choice(unpatched)
                state['logs'].append(f"[TEST] ⚠️ {leak['source']} sızıntı bulundu!")
                state['score'] = max(0, state['score'] - 15)
            else:
                state['logs'].append("[TEST] ✅ Kurumsal ayak izi temiz")
                state['score'] = min(100, state['score'] + 5)
            
            ScenarioState.set("s5A_DEF", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("5A")
        render_performance_comparison("5A")
        render_attack_vector_distribution("5A")
        render_auto_pilot_button("5A", "s5A_DEF")


def render_5D_DEF():
    """5D-DEF: Yetki Sertleştirme"""
    state = ScenarioState.get("s5D_DEF", {
        'score': 100, 'hardening': {
            'suid_audit': False,
            'sudo_config': False,
            'kernel_patch': False,
            'token_protection': False,
            'service_audit': False
        },
        'logs': []
    })
    
    EthicsGuard.display_ethics_banner("5D")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🔑 Sistem Sertleştirme")
        st.metric("Sertleştirme Puanı", state['score'])
        st.metric("Aktif Kontroller", sum(1 for v in state['hardening'].values() if v))
        
        for key, val in state['hardening'].items():
            icon = "✅" if val else "⚠️"
            name = key.replace('_', ' ').title()
            st.write(f"{icon} {name}")
    
    with col2:
        st.subheader("🛡️ Sertleştirme Kontrolleri")
        
        control = st.selectbox("Kontrol:", [
            "suid_audit", "sudo_config", "kernel_patch",
            "token_protection", "service_audit"
        ], key="5d_def_control")
        
        if st.button("▶️ Aktif Et", use_container_width=True, key="5d_def_apply"):
            if not state['hardening'][control]:
                state['hardening'][control] = True
                state['score'] = min(100, state['score'] + 12)
                state['logs'].append(f"[SERTLEŞTİRME] {control} aktif")
                ScenarioState.set("s5D_DEF", state)
        
        if st.button("🤖 Yetki Yükseltme Testi", use_container_width=True, key="5d_def_test"):
            active_controls = sum(1 for v in state['hardening'].values() if v)
            defense_power = active_controls * 20
            attack_power = random.randint(30, 100)
            
            if defense_power > attack_power:
                state['logs'].append("[TEST] ✅ Yetki yükseltme engellendi")
                state['score'] = min(100, state['score'] + 3)
            else:
                state['logs'].append("[TEST] ⚠️ Yetki yükseltme başarılı")
                state['score'] = max(0, state['score'] - 20)
            
            ScenarioState.set("s5D_DEF", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("5D")
        render_performance_comparison("5D")
        render_attack_vector_distribution("5D")
        render_auto_pilot_button("5D", "s5D_DEF")


def render_6A_DEF():
    """6A-DEF: APT Tespit ve Müdahale"""
    state = ScenarioState.get("s6A_DEF", {
        'score': 100, 'apt_phase': 3, 'detected_iocs': [],
        'contained': False, 'logs': [], 'defenses': []
    })
    
    EthicsGuard.display_ethics_banner("6A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🛡️ APT Savunma Paneli")
        st.metric("Mavi Takım Puanı", state['score'])
        st.metric("APT Aşaması", state['apt_phase'])
        st.metric("Tespit Edilen IoC", len(state['detected_iocs']))
        st.metric("Savunma Katmanı", len(state['defenses']))
        
        apt_phases = {f'Faz {i}': state['apt_phase'] >= i for i in range(7)}
        kill_fig = create_kill_chain(apt_phases)
        st.plotly_chart(kill_fig, use_container_width=True)
    
    with col2:
        st.subheader("🔍 Tehdit Avı")
        
        defense = st.selectbox("Müdahale:", [
            "IoC Arama", "Log Korelasyonu", "Endpoint İzolasyonu",
            "DNS Sinkhole", "Hesap Dondurma", "Ağ Segmentasyonu"
        ], key="6a_def_defense")
        
        if st.button("▶️ Uygula", use_container_width=True, key="6a_def_apply"):
            if defense not in state['defenses']:
                state['defenses'].append(defense)
                state['score'] = min(100, state['score'] + 8)
                state['logs'].append(f"[MÜDAHALE] {defense} uygulandı")
                
                if random.random() < 0.4:
                    state['detected_iocs'].append(f"IoC-{len(state['detected_iocs'])+1}")
                    state['logs'].append(f"[IoC] Yeni gösterge tespit edildi!")
            
            ScenarioState.set("s6A_DEF", state)
        
        if st.button("🤖 APT İlerleme Simüle Et", use_container_width=True, key="6a_def_advance"):
            if len(state['defenses']) >= 4:
                state['apt_phase'] = max(0, state['apt_phase'] - 1)
                state['logs'].append("[SAVUNMA] APT bir aşama geriledi")
            else:
                state['apt_phase'] = min(6, state['apt_phase'] + 1)
                state['score'] = max(0, state['score'] - 15)
                state['logs'].append("[APT] Tehdit ilerledi!")
            
            if len(state['detected_iocs']) >= 3 and len(state['defenses']) >= 4:
                state['contained'] = True
                state['logs'].append("[ZAFER] 🏆 APT tamamen izole edildi!")
                st.balloons()
            
            ScenarioState.set("s6A_DEF", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("6A")
        render_performance_comparison("6A")
        render_attack_heatmap("6A")
        render_world_attack_map("6A")
        render_auto_pilot_button("6A", "s6A_DEF")


def render_7A_DEF():
    """7A-DEF: SQLi Savunması"""
    state = ScenarioState.get("s7A_DEF", {
        'score': 100, 'vulnerabilities': [], 'patched': [],
        'code_samples': [], 'waf_rules': [], 'logs': [],
        'ai_attacks': 0, 'ai_success': 0
    })
    
    if not state['code_samples']:
        state['code_samples'] = [
            {
                'id': "V001",
                'code': 'query = "SELECT * FROM users WHERE id = " + user_input',
                'type': "String Concatenation",
                'severity': "CRITICAL",
                'fix': 'query = "SELECT * FROM users WHERE id = ?"; cursor.execute(query, (user_input,))'
            },
            {
                'id': "V002",
                'code': 'query = f"SELECT * FROM users WHERE name = \'{name}\'"',
                'type': "f-string Injection",
                'severity': "HIGH",
                'fix': 'query = "SELECT * FROM users WHERE name = %s"; cursor.execute(query, (name,))'
            },
            {
                'id': "V003",
                'code': 'cursor.execute("SELECT * FROM " + table_name)',
                'type': "Dynamic Table Name",
                'severity': "HIGH",
                'fix': 'ALLOWED = ["users","products"]\nif table_name not in ALLOWED: raise ValueError'
            },
            {
                'id': "V004",
                'code': 'return f"SQL Error: {str(e)}"',
                'type': "Error Disclosure",
                'severity': "MEDIUM",
                'fix': 'logging.error(f"DB error: {e}")\nreturn "An error occurred"'
            },
            {
                'id': "V005",
                'code': 'db_user = "root"; db_password = "root123"',
                'type': "Excessive Privileges",
                'severity': "HIGH",
                'fix': 'db_user = "app_readonly"  # Minimum yetki'
            }
        ]
    
    EthicsGuard.display_ethics_banner("7A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🛡️ Savunma Paneli")
        st.metric("Güvenlik Puanı", state['score'])
        st.metric("Bulunan Zafiyet", len(state['vulnerabilities']))
        st.metric("Kapatılan", len(state['patched']))
        st.metric("AI Başarılı", state['ai_success'], 
                  delta=f"-{state['ai_success']}", delta_color="inverse")
        
        defense_layers = {
            'Input Validation': any('input' in p.lower() for p in state['patched']),
            'Parametreli Sorgu': any('parametre' in p.lower() or 'parametrized' in p.lower() 
                                    for p in state['patched']),
            'Minimum Yetki': any('yetki' in p.lower() or 'privilege' in p.lower() 
                                for p in state['patched']),
            'Error Handling': any('error' in p.lower() for p in state['patched']),
            'WAF Kuralı': len(state['waf_rules']) > 0,
        }
        
        st.markdown("### 🏰 Savunma Katmanları")
        for layer, active in defense_layers.items():
            icon = "✅" if active else "❌"
            st.markdown(f"{icon} {layer}")
        
        defense_score = sum(defense_layers.values()) * 20
        st.progress(defense_score / 100, text=f"Savunma Derinliği: %{defense_score}")
    
    with col2:
        st.subheader("🔍 Kod Denetim Terminali")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Kod İnceleme", "🛠️ Yama Uygula", 
            "🧱 WAF Kuralları", "🤖 AI Testi"
        ])
        
        with tab1:
            st.markdown("**Denetlenecek Kod:**")
            
            for code in state['code_samples']:
                if code['id'] not in [v['id'] for v in state['vulnerabilities']]:
                    sev_color = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡'}.get(code['severity'], '⚪')
                    
                    with st.expander(f"{sev_color} [{code['id']}] {code['type']}"):
                        st.code(code['code'], language='python')
                        st.caption(f"Severity: {code['severity']}")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button(f"🚨 Zafiyet İşaretle", key=f"mark_{code['id']}"):
                                state['vulnerabilities'].append(code)
                                state['logs'].append(f"[TESPİT] {code['id']}: {code['type']}")
                                ScenarioState.set("s7A_DEF", state)
                                st.rerun()
                        with col_b:
                            if st.button(f"✅ Güvenli", key=f"safe_{code['id']}"):
                                if code['severity'] in ['CRITICAL', 'HIGH']:
                                    state['score'] = max(0, state['score'] - 15)
                                    state['logs'].append(f"[YANLIŞ] {code['id']} güvenli değil!")
                                else:
                                    state['logs'].append(f"[DOĞRU] {code['id']} düşük riskli")
                                state['code_samples'].remove(code)
                                ScenarioState.set("s7A_DEF", state)
                                st.rerun()
        
        with tab2:
            st.markdown("**Tespit Edilen Zafiyetler:**")
            
            if state['vulnerabilities']:
                for vuln in state['vulnerabilities']:
                    with st.expander(f"🔧 {vuln['id']}: {vuln['type']}"):
                        st.code(vuln['code'], language='python')
                        st.markdown("**Önerilen Düzeltme:**")
                        st.code(vuln['fix'], language='python')
                        
                        if st.button(f"✅ Yamayı Uygula", key=f"patch_{vuln['id']}"):
                            state['patched'].append(vuln['id'])
                            state['score'] = min(100, state['score'] + 12)
                            state['logs'].append(f"[YAMA] {vuln['id']} yamalandı!")
                            state['vulnerabilities'].remove(vuln)
                            ScenarioState.set("s7A_DEF", state)
                            st.rerun()
            else:
                st.info("Önce 'Kod İnceleme' sekmesinden zafiyet işaretleyin.")
        
        with tab3:
            st.markdown("**WAF Kural Editörü:**")
            
            waf_rule = st.text_area(
                "WAF Kuralı (regex):",
                placeholder="Örnek: (\\'|\\-\\-|;|\\/\\*|UNION|SELECT)",
                key="waf_rule_input_7a_def"
            )
            rule_name = st.text_input("Kural Adı:", key="waf_rule_name_7a_def")
            
            if st.button("➕ Kural Ekle", key="waf_add_7a_def"):
                if waf_rule and rule_name:
                    state['waf_rules'].append({
                        'name': rule_name,
                        'pattern': waf_rule
                    })
                    state['logs'].append(f"[WAF] '{rule_name}' kuralı eklendi")
                    state['score'] = min(100, state['score'] + 5)
                    ScenarioState.set("s7A_DEF", state)
                    st.rerun()
            
            if state['waf_rules']:
                st.markdown("**Aktif Kurallar:**")
                for rule in state['waf_rules']:
                    st.code(f"{rule['name']}: {rule['pattern']}", language='regex')
        
        with tab4:
            st.markdown("**AI Test Simülasyonu:**")
            
            if st.button("🤖 AI Test Başlat", use_container_width=True, key="ai_test_7a_def"):
                state['ai_attacks'] += 1
                
                defense_power = (
                    len(state['patched']) * 15 +
                    len(state['waf_rules']) * 10
                )
                
                attack_types = [
                    ("UNION-based", 30), ("Boolean-based Blind", 25),
                    ("Time-based Blind", 35), ("Error-based", 20),
                    ("Second-order", 40), ("Stacked Queries", 45)
                ]
                
                attack_name, attack_power = random.choice(attack_types)
                
                if defense_power > attack_power:
                    state['logs'].append(f"[ENGELLENDİ] ✅ {attack_name} engellendi")
                    state['score'] = min(100, state['score'] + 3)
                else:
                    state['ai_success'] += 1
                    state['score'] = max(0, state['score'] - 15)
                    state['logs'].append(f"[SIZINTI] 🔴 {attack_name} başarılı!")
                
                ScenarioState.set("s7A_DEF", state)
        
        st.markdown("### 📜 Olay Logları")
        st.markdown(
            '<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>',
            unsafe_allow_html=True
        )
        
        if len(state['patched']) >= 4 and state['ai_success'] == 0:
            st.success("🏆 **GÖREV TAMAMLANDI!** Tüm zafiyetler kapatıldı!")
            st.balloons()
        
        EthicsGuard.display_defense_recommendation("7A")
        render_performance_comparison("7A")
        render_auto_pilot_button("7A", "s7A_DEF")


def render_9A_DEF():
    """9A-DEF: Phishing Tespit ve Savunma"""
    state = ScenarioState.get("s9A_DEF", {
        'score': 100, 'emails_analyzed': 0, 'blocked': 0,
        'false_positives': 0, 'logs': [], 'emails': []
    })
    
    if not state['emails']:
        for _ in range(8):
            is_phish = random.random() < 0.5
            state['emails'].append({
                'subject': random.choice([
                    "Acil: Hesap Doğrulama", "Fatura #2024-{n}",
                    "Toplantı Daveti", "Şifre Sıfırlama", 
                    "Müşteri Şikayeti", "İK Duyurusu",
                    "CEO'dan Önemli Mesaj"
                ]).replace("{n}", str(random.randint(100,999))),
                'sender': random.choice([
                    "security@sirket.com", "info@dis-sirket.com",
                    "ceo@sirket-acil.com", "hr@sirket.com",
                    "noreply@bank-of-turkiye.tk"
                ]),
                'phishing': is_phish
            })
    
    EthicsGuard.display_ethics_banner("9A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("📧 E-posta Güvenlik Paneli")
        st.metric("Savunma Puanı", state['score'])
        st.metric("Engellenen", state['blocked'])
        st.metric("Yanlış Pozitif", state['false_positives'])
        st.metric("Analiz Edilen", state['emails_analyzed'])
    
    with col2:
        st.subheader("📬 E-posta Analizi")
        
        for i, email in enumerate(state['emails'][:5]):
            st.markdown(f"**{email['subject']}**")
            st.caption(f"Gönderen: {email['sender']}")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🚫 Engelle #{i}", key=f"9a_def_block_{i}"):
                    state['emails_analyzed'] += 1
                    if email['phishing']:
                        state['blocked'] += 1
                        state['score'] = min(100, state['score'] + 8)
                        state['logs'].append(f"[DOĞRU] ✅ '{email['subject']}' engellendi")
                    else:
                        state['false_positives'] += 1
                        state['score'] = max(0, state['score'] - 15)
                        state['logs'].append(f"[YANLIŞ] ❌ '{email['subject']}' meşruydu")
                    state['emails'].remove(email)
                    ScenarioState.set("s9A_DEF", state)
                    st.rerun()
            with c2:
                if st.button(f"✅ İzin Ver #{i}", key=f"9a_def_allow_{i}"):
                    state['emails_analyzed'] += 1
                    if email['phishing']:
                        state['score'] = max(0, state['score'] - 20)
                        state['logs'].append(f"[KAÇIRILDI] 🔴 '{email['subject']}' atlandı")
                    else:
                        state['logs'].append(f"[NORMAL] '{email['subject']}' meşru")
                    state['emails'].remove(email)
                    ScenarioState.set("s9A_DEF", state)
                    st.rerun()
            st.markdown("---")
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-15:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("9A")
        render_performance_comparison("9A")
        render_attack_vector_distribution("9A")
        render_auto_pilot_button("9A", "s9A_DEF")


def render_10A_DEF():
    """10A-DEF: Kırmızı Takım Savunması"""
    state = ScenarioState.get("s10A_DEF", {
        'score': 100, 'phases_defended': {
            'Keşif': False, 'Silahlanma': False, 'Teslimat': False,
            'İstismar': False, 'Kurulum': False, 'C2': False, 'Hedef': False
        },
        'defenses': [], 'logs': []
    })
    
    EthicsGuard.display_ethics_banner("10A")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("🛡️ Full-Scope Savunma")
        st.metric("Mavi Takım Puanı", state['score'])
        st.metric("Savunulan Aşama", sum(1 for v in state['phases_defended'].values() if v))
        st.metric("Savunma Katmanı", len(state['defenses']))
        
        kill_fig = create_kill_chain(state['phases_defended'])
        st.plotly_chart(kill_fig, use_container_width=True)
    
    with col2:
        st.subheader("⚔️ Savunma Terminali")
        
        phases_list = list(state['phases_defended'].keys())
        undefended = [p for p in phases_list if not state['phases_defended'][p]]
        
        if undefended:
            current = undefended[0]
            st.info(f"**Savunulacak Aşama:** {current}")
            
            defenses_map = {
                'Keşif': ['OSINT Monitoring', 'Honeypot Deployment', 'False Flags'],
                'Silahlanma': ['Threat Intel', 'IoC Blocking', 'Sandbox Analysis'],
                'Teslimat': ['Email Filter', 'Web Proxy', 'User Training'],
                'İstismar': ['Patch Management', 'WAF Rules', 'EDR'],
                'Kurulum': ['Application Whitelist', 'Registry Monitor', 'File Integrity'],
                'C2': ['DNS Sinkhole', 'SSL Inspection', 'Beacon Detection'],
                'Hedef': ['DLP', 'Egress Filter', 'Data Classification']
            }
            
            selected = st.selectbox("Savunma:", defenses_map.get(current, []), 
                                   key="10a_def_defense")
            
            if st.button("▶️ Uygula", use_container_width=True, key="10a_def_apply"):
                success_chance = min(0.9, 0.5 + len(state['defenses']) * 0.1)
                
                if random.random() < success_chance:
                    state['phases_defended'][current] = True
                    state['defenses'].append(f"{current}:{selected}")
                    state['score'] = min(100, state['score'] + 10)
                    state['logs'].append(f"[SAVUNMA] ✅ {current}: {selected}")
                else:
                    state['score'] = max(0, state['score'] - 15)
                    state['logs'].append(f"[BAŞARISIZ] ⚠️ {selected} yetersiz")
                
                if all(state['phases_defended'].values()):
                    state['logs'].append("[ZAFER] 🏆 Tüm aşamalar savunuldu!")
                    st.balloons()
                
                ScenarioState.set("s10A_DEF", state)
        
        st.markdown('<div class="terminal">' + '\n'.join(state['logs'][-20:]) + '</div>', unsafe_allow_html=True)
        
        EthicsGuard.display_defense_recommendation("10A")
        render_performance_comparison("10A")
        render_attack_heatmap("10A")
        render_world_attack_map("10A")
        render_auto_pilot_button("10A", "s10A_DEF")


# --- İkiz Renderers'ı SCENARIO_RENDERERS'a kaydet ---
SCENARIO_RENDERERS.update({
    "1A-DEF": render_1A_DEF,
    "1C-DEF": render_1C_DEF,
    "1E-DEF": render_1E_DEF,
    "2A-DEF": render_2A_DEF,
    "2C-DEF": render_2C_DEF,
    "3A-DEF": render_3A_DEF,
    "3E-DEF": render_3E_DEF,
    "4A-DEF": render_4A_DEF,
    "4C-DEF": render_4C_DEF,
    "5A-DEF": render_5A_DEF,
    "5D-DEF": render_5D_DEF,
    "6A-DEF": render_6A_DEF,
    "7A-DEF": render_7A_DEF,
    "9A-DEF": render_9A_DEF,
    "10A-DEF": render_10A_DEF,
})


# ============================================
# BÖLÜM 15: SAĞ PANEL FONKSİYONU
# ============================================

def render_right_panel(scenario_id, level_num):
    """Sağ tarafta sabit kontrol paneli"""
    
    with st.container():
        
        # --- 1. GÜVENLİK OLGUNLUK MODELİ ---
        st.markdown("### 📊 GÜVENLİK OLGUNLUĞU")
        
        maturity_levels = [
            (1, 2, "Başlangıç", "Temel ağ ve paket kavramları"),
            (3, 4, "Temel", "IDS/IPS, güvenlik duvarı, şifreleme"),
            (5, 6, "Yapılandırılmış", "DDoS, sızma testi, APT temelleri"),
            (7, 8, "İleri", "Web saldırıları, tersine mühendislik"),
            (9, 10, "Uzman", "Sosyal mühendislik, full-scope operasyonlar"),
        ]
        
        current_maturity = 1
        current_desc = ""
        for i, (low, high, name, desc) in enumerate(maturity_levels):
            if level_num >= low and level_num <= high:
                current_maturity = i + 1
                current_desc = desc
                break
        
        maturity_progress = current_maturity * 20
        st.progress(maturity_progress / 100, text=f"Seviye {current_maturity}/5")
        
        for i, (low, high, name, desc) in enumerate(maturity_levels):
            maturity_num = i + 1
            if maturity_num < current_maturity:
                icon = "✅"
                color = "#4f8bc9"
            elif maturity_num == current_maturity:
                icon = "🔄"
                color = get_color("primary")
            else:
                icon = "🔒"
                color = "#555555"
            
            st.markdown(
                f'<span style="color:{color}; font-size:0.82rem;">{icon} L{maturity_num}: {name}</span>',
                unsafe_allow_html=True
            )
        
        if current_desc:
            st.caption(f"📌 {current_desc}")
        
        st.markdown("---")
        
        # --- 2. YETENEK RADAR GRAFİĞİ ---
        st.markdown("### 🎯 YETENEK HARİTASI")
        
        if level_num <= 2:
            radar_values = [70, 40, 20, 10, 30, 15]
        elif level_num <= 4:
            radar_values = [85, 65, 50, 30, 55, 35]
        elif level_num <= 6:
            radar_values = [90, 80, 70, 55, 75, 55]
        elif level_num <= 8:
            radar_values = [95, 90, 85, 75, 85, 70]
        else:
            radar_values = [98, 95, 95, 90, 95, 90]
        
        radar_categories = ['Keşif', 'Saldırı', 'Savunma', 'Analiz', 'Gizlilik', 'Mühendislik']
        
        radar_fig = go.Figure(data=go.Scatterpolar(
            r=radar_values,
            theta=radar_categories,
            fill='toself',
            fillcolor='rgba(0, 255, 65, 0.15)',
            line=dict(color=get_color("primary"), width=2)
        ))
        
        radar_fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    color='#888888',
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(size=8, color='#888888')
                ),
                angularaxis=dict(
                    color='#e0e0e0',
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(size=9, color='#e0e0e0')
                )
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=20, l=30, r=30),
            height=280
        )
        
        st.plotly_chart(radar_fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        
        # --- 3. KPI DASHBOARD ---
        st.markdown("### 📈 PERFORMANS METRİKLERİ")
        
        gs = st.session_state.global_stats
        total_completed = len(gs['completed_scenarios'])
        success_rate = (gs['total_success'] / max(1, gs['total_attempts']) * 100) if gs['total_attempts'] > 0 else 0
        avg_risk = sum(gs['risk_history']) / max(1, len(gs['risk_history']))
        
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.metric("Tamamlanan", f"{total_completed}/65")
            st.metric("Başarı Oranı", f"%{success_rate:.0f}")
        with col_k2:
            st.metric("Ortalama Risk", f"%{avg_risk:.0f}")
            st.metric("Toplam Deneme", gs['total_attempts'])
        
        if len(gs['risk_history']) >= 2:
            trend_fig = go.Figure()
            trend_fig.add_trace(go.Scatter(
                y=gs['risk_history'][-20:],
                mode='lines+markers',
                line=dict(color=get_color("primary"), width=2),
                marker=dict(color=get_color("primary"), size=6),
                name='Risk Trendi'
            ))
            trend_fig.update_layout(
                title="Risk Yönetim Trendi",
                height=150,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e0e0e0',
                margin=dict(t=30, b=10, l=20, r=10),
                xaxis=dict(showgrid=False, color='#888888'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', 
                          color='#888888', range=[0, 100])
            )
            st.plotly_chart(trend_fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        
        # --- 4. ETİK DURUM ---
        st.markdown("### 🛡️ ETİK DURUM")
        display_ethics_status()
        
        st.markdown("---")
        
        # --- 5. HIZLI KOMUT REFERANSI ---
        with st.expander("⚡ HIZLI KOMUT REFERANSI", expanded=False):
            quick_refs = {
                "1A": {"komut": "`tara` → `gonder --port 80 --veri exploit`", "ipucu": "SSH portuna test yapma"},
                "2C": {"komut": "`test_basic` → `test_encoded` → `exploit`", "ipucu": "Sırayla dene"},
                "7A": {"komut": "UNION → Schema → Hash Çek → Kır", "ipucu": "Sırayla git"},
                "9A": {"komut": "CEO → BT Güvenlik → Acil Şifre", "ipucu": "Psikolojik tetikleyici kullan"},
                "10A": {"komut": "7 aşama kill chain", "ipucu": "Risk %40 altı agresif"},
            }
            ref = quick_refs.get(scenario_id, 
                {"komut": "Komutları terminalde gör", "ipucu": "Otopilotu izleyerek öğren"})
            st.markdown(f"**🎯 Strateji:** {ref['komut']}")
            st.markdown(f"**💡 İpucu:** {ref['ipucu']}")
        
        # --- 6. OTOPİLOT KILAVUZU ---
        st.markdown("### 🤖 OTOPİLOT KILAVUZU")
        
        if level_num <= 2:
            advice_icon = "🟢"
            advice_title = "Başlangıç"
            advice_text = "Önce otopilotu izle, sonra kendin tekrar et."
        elif level_num <= 4:
            advice_icon = "🟡"
            advice_title = "Gelişim"
            advice_text = "Önce kendin dene, takılırsan otopilotu aç."
        elif level_num <= 7:
            advice_icon = "🟠"
            advice_title = "İleri"
            advice_text = "Kendi stratejinle ilerle, sadece sıkışınca otopilotu kontrol et."
        else:
            advice_icon = "🔴"
            advice_title = "Uzman"
            advice_text = "Tamamen kendi başına yap. Otopilot sadece son çare."
        
        st.info(f"**{advice_icon} {advice_title}:** {advice_text}")
        
        steps = get_auto_pilot_steps(scenario_id)
        st.caption(f"📋 Bu senaryoda otopilot: **{len(steps)} adım**")
        
        with st.expander("🔍 Adımları Gör", expanded=False):
            if steps:
                for i, (cmd, desc, delay) in enumerate(steps, 1):
                    st.caption(f"{i}. {desc}")
        
        st.markdown("---")
        
        # --- 7. SENARYO BİLGİSİ ---
        st.markdown("### 📋 SENARYO BİLGİSİ")
        
        # Senaryo numarası ve harfini bul
        base_id = scenario_id.replace("-DEF", "")
        is_twin = "-DEF" in scenario_id
        
        try:
            scenario_num = int(base_id[0])
            scenario_sub = base_id[1] if len(base_id) > 1 else 'A'
            scenario_order = (scenario_num - 1) * 5 + (ord(scenario_sub) - ord('A') + 1)
        except:
            scenario_num = 1
            scenario_order = 1
        
        info = ALL_SCENARIOS.get(scenario_id, {})
        
        if info.get('type') == 'human_attack':
            rol_emoji = "🎓"
            rol_kisa = "Kırmızı Takım"
        else:
            rol_emoji = "🛡️"
            rol_kisa = "Mavi Takım"
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Sıra", f"{scenario_order}/50")
        with col_b:
            st.metric("Seviye", f"{scenario_num}/10")
        
        st.markdown(f"**Rol:** {rol_emoji} {rol_kisa}")
        
        if is_twin:
            st.markdown("**🔷 Mavi Takım İkizi**")


# ============================================
# BÖLÜM 16: ANA FONKSİYON
# ============================================

def main():
    """Ana uygulama fonksiyonu"""
    
    # --- SIDEBAR: TEMA ---
    ThemeManager.render_theme_selector("sidebar")
    
    st.sidebar.markdown("---")
    
    # --- SIDEBAR: BAŞLIK ---
    st.sidebar.markdown("""
    <div style='text-align:center;padding:8px 0;'>
        <h1 style='color:#00ff41;font-size:1.6rem;margin:0;line-height:1.2;'>🛡️ SİBERKALKAN AKADEMİ</h1>
        <p style='color:#5a9ed4;margin:4px 0;font-size:0.85rem;line-height:1.2;'>Siber Savunma Eğitim Simülasyonu</p>
      
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # --- SIDEBAR: SEVİYE VE SENARYO ---
    levels = {
        "📗 Seviye 1: Veri Bahçesi": ["1A", "1B", "1C", "1D", "1E"],
        "📘 Seviye 2: Dijital Kale": ["2A", "2B", "2C", "2D", "2E"],
        "📙 Seviye 3: Solucan Deliği": ["3A", "3B", "3C", "3D", "3E"],
        "📕 Seviye 4: Fırtına": ["4A", "4B", "4C", "4D", "4E"],
        "📓 Seviye 5: Gölgeler İçinde": ["5A", "5B", "5C", "5D", "5E"],
        "📔 Seviye 6: Büyük Oyun": ["6A", "6B", "6C", "6D", "6E"],
        "📒 Seviye 7: Kod Enjeksiyonu": ["7A", "7B", "7C", "7D", "7E"],
        "📚 Seviye 8: Tersine Mühendislik": ["8A", "8B", "8C", "8D", "8E"],
        "📖 Seviye 9: Sosyal Mühendislik": ["9A", "9B", "9C", "9D", "9E"],
        "📜 Seviye 10: Nihai Sınav": ["10A", "10B", "10C", "10D", "10E"],
        "🔷 Mavi Takım İkizleri": [
            "1A-DEF", "1C-DEF", "1E-DEF",
            "2A-DEF", "2C-DEF",
            "3A-DEF", "3E-DEF",
            "4A-DEF", "4C-DEF",
            "5A-DEF", "5D-DEF",
            "6A-DEF", "7A-DEF", "9A-DEF", "10A-DEF"
        ]
    }
    
    selected_level = st.sidebar.selectbox("📚 SEVİYE SEÇİN", list(levels.keys()))
    scenarios = levels[selected_level]
    
    # Senaryo etiketleri
    scenario_labels = []
    for s_id in scenarios:
        info = ALL_SCENARIOS.get(s_id, {})
        title = info.get('title', s_id)
        if ':' in title:
            title = title.split(':', 1)[1].strip()
        
        if info.get('type') == 'human_attack':
            role = " [🎓 Kırmızı]"
        elif info.get('type') == 'human_defend':
            role = " [🛡️ Mavi]"
        else:
            role = ""
        
        scenario_labels.append(f"{s_id}: {title}{role}")
    
    selected_label = st.sidebar.radio("🎯 SENARYO SEÇİN", scenario_labels)
    selected_scenario = selected_label.split(":")[0].strip()
    
    # --- SIDEBAR: İLERLEME ---
    if "Mavi Takım" in selected_level:
        level_num = 1
    else:
        try:
            level_num = int(selected_level.split(":")[0].split()[-1])
        except:
            level_num = 1
    
    st.sidebar.progress(level_num / 10)
    st.sidebar.caption(f"İlerleme: %{level_num * 10}")
    
    # --- SIDEBAR: KARİYER HARİTASI ---
    with st.sidebar.expander("🎯 KARİYER HARİTASI", expanded=False):
        gs = st.session_state.global_stats
        total_completed = len(gs['completed_scenarios'])
        
        if total_completed < 5:
            st.info("📊 Kariyer haritası için en az 5 senaryo tamamlayın.")
        else:
            st.metric("Tamamlanan", total_completed)
            st.progress(min(1.0, total_completed / 65))
            st.caption(f"Toplam: {total_completed}/65 senaryo")
    
    # --- SIDEBAR: FOOTER ---
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<p style='text-align:center;color:#5a9ed4;font-size:0.75rem;'>"
        "🔐 SiberKalkan Akademi v5.0<br>"
        "Siber Güvenlik Eğitim Platformu</p>",
        unsafe_allow_html=True
    )
    
    # --- ANA İÇERİK + SAĞ PANEL ---
    col_main, col_panel = st.columns([3, 1])
    
    with col_main:
        info = ALL_SCENARIOS.get(selected_scenario, {})
        
        if info:
            st.title(f"🎯 {info.get('title', selected_scenario)}")
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown(f"### 🎓 İnsan: **{info.get('role_human', 'N/A')}**")
            with col_r2:
                st.markdown(f"### 🤖 AI: **{info.get('role_ai', 'N/A')}**")
            
            with st.expander("📖 SENARYO DETAYLARI", expanded=True):
                st.markdown(
                    f'<div class="scenario-desc">{info.get("desc", "")}</div>',
                    unsafe_allow_html=True
                )
            
            st.markdown("---")
            
            renderer = SCENARIO_RENDERERS.get(selected_scenario)
            if renderer:
                renderer()
                
                # RAPOR BUTONU - Her senaryoda otomatik göster
                # Hem "s7A" hem "s7A_DEF" hem "s7A-DEF" formatlarını dener
                _state = None
                _candidates = [
                    f"s{selected_scenario}",                       # s7A veya s7A-DEF
                    f"s{selected_scenario.replace('-', '_')}",     # s7A_DEF
                    selected_scenario,                              # 7A-DEF
                    selected_scenario.replace('-', '_'),           # 7A_DEF
                ]
                for _key in _candidates:
                    _state = st.session_state.get(_key, {})
                    if _state:
                        break
                
                # State bulunamasa bile boş state ile göster
                st.markdown("---")
                try:
                    ReportGenerator.render_report_button(
                        selected_scenario, 
                        _state if _state else {},
                        ALL_SCENARIOS.get(selected_scenario, {})
                    )
                except Exception as e:
                    st.error(f"⚠️ Rapor sistemi hatası: {e}")
            else:
                st.warning(f"⚠️ {selected_scenario} senaryosu yükleniyor...")

                
        else:
            st.warning("Senaryo bilgisi bulunamadı. Lütfen geçerli bir senaryo seçin.")
    
    with col_panel:
        render_right_panel(selected_scenario, level_num)


# ============================================
# BÖLÜM 17: PROGRAM BAŞLANGICI
# ============================================

if __name__ == "__main__":
    main()

# ============================================
# BÖLÜM 18: RAPOR SİSTEMİ ENTEGRASYONU
# ============================================
# 
# Bu bölüm, her senaryonun sonuna otomatik rapor butonu ekler.
# Mevcut koda MÜDAHALE ETMEZ, sadece üzerine yeni bir katman ekler.
#
# Kullanım: Her render fonksiyonu sonunda şu satır eklenir:
#     ReportGenerator.render_report_button(scenario_id, state, info)
#

# Monkey-patch: Her render fonksiyonunu sarmalayarak rapor butonu ekle
def _inject_report_button():
    """
    Her senaryo render fonksiyonunun sonuna rapor butonu ekler.
    Mevcut fonksiyonlara dokunmaz, sadece wrapper ekler.
    """
    import functools
    
    # Orijinal render fonksiyonlarını kaydet
    original_renderers = dict(SCENARIO_RENDERERS)
    
    def make_wrapper(scenario_id, original_func):
        @functools.wraps(original_func)
        def wrapper():
            # Orijinal render fonksiyonunu çağır
            original_func()
            
            # Rapor butonu ekle (sadece state varsa)
            state_key = f"s{scenario_id}"
            state = st.session_state.get(state_key, {})
            
            # State boşsa atla
            if not state:
                return
            
            # Senaryo bilgisi
            info = ALL_SCENARIOS.get(scenario_id, {})
            
            # Rapor butonu göster
            try:
                st.markdown("---")
                ReportGenerator.render_report_button(scenario_id, state, info)
            except Exception as e:
                # Hata olursa sessizce geç (mevcut kodu etkilemesin)
                pass
        
        return wrapper
    
    # Tüm renderers'ı sarmala
    for scenario_id, original_func in original_renderers.items():
        if original_func is not None:
            SCENARIO_RENDERERS[scenario_id] = make_wrapper(scenario_id, original_func)


# Wrapper'ları uygula
_inject_report_button()


# ============================================
# BÖLÜM 19: KARIYER HARİTASI (GELİŞMİŞ)
# ============================================

def render_career_mapping():
    """Global istatistiklere göre kariyer yol haritası çıkarır"""
    gs = st.session_state.global_stats
    total_completed = len(gs['completed_scenarios'])
    
    if total_completed < 5:
        st.info("📊 Kariyer haritası için en az 5 senaryo tamamlamalısınız.")
        return
    
    # Yetenek profili
    attack_score = 0
    defense_score = 0
    analysis_score = 0
    social_score = 0
    
    for s_id, score in gs['completed_scenarios'].items():
        num = int(s_id[0]) if s_id[0].isdigit() else 1
        info = ALL_SCENARIOS.get(s_id, {})
        
        if info.get('type') == 'human_attack':
            attack_score += score
        else:
            defense_score += score
        
        if num >= 5:
            analysis_score += score * 0.8
        if num >= 9:
            social_score += score * 0.7
    
    max_possible = max(1, total_completed * 100)
    attack_pct = min(100, (attack_score / (max_possible * 0.5)) * 100)
    defense_pct = min(100, (defense_score / (max_possible * 0.5)) * 100)
    analysis_pct = min(100, (analysis_score / (max_possible * 0.3)) * 100)
    social_pct = min(100, (social_score / (max_possible * 0.2)) * 100)
    
    # Kariyer rolleri
    career_roles = [
        {"name": "Penetrasyon Test Uzmanı", "icon": "🔴",
         "req": {"Saldırı": 70, "Analiz": 50, "Savunma": 30, "Sosyal": 30},
         "salary": "₺1.2M - ₺2.5M", "certs": ["OSCP", "GPEN"]},
        {"name": "SOC Analisti", "icon": "🔵",
         "req": {"Savunma": 70, "Analiz": 60, "Saldırı": 30, "Sosyal": 20},
         "salary": "₺800K - ₺1.5M", "certs": ["Security+", "CySA+"]},
        {"name": "Tehdit Avcısı", "icon": "🟣",
         "req": {"Analiz": 80, "Savunma": 50, "Saldırı": 50, "Sosyal": 20},
         "salary": "₺1.5M - ₺2.8M", "certs": ["GCFA", "GNFA"]},
        {"name": "Kırmızı Takım Lideri", "icon": "🟠",
         "req": {"Saldırı": 85, "Analiz": 70, "Savunma": 50, "Sosyal": 60},
         "salary": "₺2M - ₺3.5M", "certs": ["OSCE", "CRTO"]},
        {"name": "Güvenlik Mimarı", "icon": "🟡",
         "req": {"Savunma": 80, "Analiz": 70, "Saldırı": 40, "Sosyal": 20},
         "salary": "₺1.8M - ₺3M", "certs": ["CISSP", "CCSP"]},
    ]
    
    # En uygun rol
    skill_map = {"Saldırı": attack_pct, "Savunma": defense_pct,
                 "Analiz": analysis_pct, "Sosyal": social_pct}
    
    best_role = None
    best_score = 0
    for role in career_roles:
        score = 0
        for skill, req in role['req'].items():
            score += min(req, skill_map[skill])
        if score > best_score:
            best_score = score
            best_role = role
    
    # Göster
    st.markdown("**📊 Yetenek Profilin:**")
    for skill_name, skill_pct in [("Saldırı", attack_pct), ("Savunma", defense_pct),
                                   ("Analiz", analysis_pct), ("Sosyal Mühendislik", social_pct)]:
        st.markdown(f"**{skill_name}:** %{skill_pct:.0f}")
        st.progress(skill_pct / 100)
    
    if best_role:
        st.markdown("---")
        st.markdown(f"### {best_role['icon']} ÖNERİLEN ROL")
        st.markdown(f"**{best_role['name']}**")
        st.markdown(f"💰 Maaş: {best_role['salary']}")
        st.markdown(f"📜 Sertifikalar: {', '.join(best_role['certs'])}")


# ============================================
# BÖLÜM 20: SERTİFİKA KONTROLÜ
# ============================================

def check_certificate_eligibility():
    """Tüm seviyeler tamamlandı mı kontrol eder, sertifika butonu gösterir"""
    gs = st.session_state.global_stats
    total_completed = len(gs['completed_scenarios'])
    
    if total_completed >= 65:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🏅 SERTİFİKA")
        
        if st.sidebar.button("🎓 Sertifika Oluştur", use_container_width=True):
            cert_data = {
                "name": "SiberKalkan Akademi - Master",
                "level": "Level 10 - Expert",
                "completed_scenarios": total_completed,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "certificate_id": hashlib.sha256(
                    f"{datetime.now().timestamp()}".encode()
                ).hexdigest()[:16].upper()
            }
            
            st.sidebar.success(f"✅ Sertifika ID: {cert_data['certificate_id']}")
            st.balloons()
    elif total_completed >= 30:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🏅 SERTİFİKA")
        st.sidebar.info(f"🔒 {65 - total_completed} senaryo daha tamamlayın!")

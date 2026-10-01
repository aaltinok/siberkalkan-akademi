"""
SiberKalkan Akademi - Etik Koruma Katmanı
==========================================

Bu modül, kullanıcı girdilerini ve içerikleri etik açıdan denetler.
Yasaklı içerik tespit edildiğinde uyarı verir ve engeller.

Görevleri:
    1. Etik sözleşme onayı alma
    2. Kullanıcı girdilerini denetleme
    3. AI çıktılarını denetleme
    4. Etik banner gösterme
    5. İhlal loglarını tutma

Kullanım:
    from utils.ethics_guard import EthicsGuard
    
    # Etik sözleşme kontrolü
    if not EthicsGuard.require_ethics_acceptance():
        st.stop()
    
    # Kullanıcı girdisi kontrolü
    is_safe, warning = EthicsGuard.check_user_input(user_text)
    if not is_safe:
        st.error(warning)
"""

import re
import streamlit as st
from datetime import datetime
from typing import Tuple, List, Dict


class EthicsGuard:
    """
    Etik koruma katmanı.
    
    Bu sınıf, tüm kullanıcı etkileşimlerini ve içerikleri etik açıdan
    denetler. Gerçek sistemlere zarar verebilecek bilgilerin platformda
    paylaşılmasını engeller.
    """
    
    # ============================================
    # YASAKLI PATTERN'LER
    # ============================================
    
    # Gerçek IP adresleri (private olmayan)
    # 10.x.x.x, 192.168.x.x, 172.16-31.x.x → İZİNLİ (private range)
    # Diğerleri → YASAKLI (gerçek IP olabilir)
    PRIVATE_IP_PATTERN = re.compile(
        r'^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|127\.|0\.0\.0\.0|255\.)'
    )
    
    # Gerçek domain pattern'leri
    REAL_DOMAIN_PATTERN = re.compile(
        r'\b(?!example\.com|test\.local|ornek\.com)'
        r'[a-z0-9-]+\.(com|net|org|gov|edu|io|co)\.?[a-z]{0,2}\b',
        re.IGNORECASE
    )
    
    # Yasaklı araç isimleri (gerçek saldırı araçları)
    FORBIDDEN_TOOLS = [
        'metasploit', 'msfconsole', 'msfvenom', 'empire', 'sliver',
        'cobalt strike', 'cobaltstrike', 'mimikatz', 'bloodhound',
        'crackmapexec', 'impacket', 'responder'
    ]
    
    # Yasaklı malware isimleri
    FORBIDDEN_MALWARE = [
        'mirai', 'emotet', 'trickbot', 'ryuk', 'conti', 'lockbit',
        'wannacry', 'notpetya', 'stuxnet', 'blackcat', 'revil'
    ]
    
    # Yasaklı CVE referansı (kullanım için)
    # Not: Eğitim amaçlı referans İZİNLİ, kullanım YASAKLI
    FORBIDDEN_CVE_USAGE = [
        r'CVE-\d{4}-\d{4,7}\s*exploit',
        r'exploit\s*CVE-\d{4}-\d{4,7}',
        r'CVE-\d{4}-\d{4,7}\s*kullan',
    ]
    
    # Yönlendirici ifadeler (AI çıktısında olmamalı)
    DANGEROUS_PHRASES = [
        'kopyala ve çalıştır',
        'bu komutu çalıştır',
        'şu kodu kullan',
        'copy and run',
        'exploit this',
        'hemen çalıştır',
        'gerçek sisteme uygula',
        'bu IP ye saldır',
    ]
    
    # ============================================
    # UYARI MESAJLARI
    # ============================================
    
    ETHICS_WARNINGS = {
        'real_ip': (
            "⚠️ **Gerçek IP adresi tespit edildi.**\n\n"
            "Lütfen simülasyon IP adresleri kullanın "
            "(örn: 10.0.0.1, 192.168.1.1).\n\n"
            "Gerçek IP adresleri platformda yasaktır."
        ),
        'real_domain': (
            "⚠️ **Gerçek domain tespit edildi.**\n\n"
            "Lütfen simülasyon domain'i kullanın "
            "(örn: example.com, test.local).\n\n"
            "Gerçek domain'ler platformda yasaktır."
        ),
        'real_tool': (
            "⚠️ **Gerçek saldırı aracı adı tespit edildi.**\n\n"
            "Bu platform kavramsal eğitim verir. "
            "Lütfen teknik terim kullanın (örn: 'SQL enjeksiyon aracı').\n\n"
            "Gerçek araç isimleri yasaktır."
        ),
        'real_malware': (
            "⚠️ **Gerçek zararlı yazılım adı tespit edildi.**\n\n"
            "Lütfen genel terim kullanın "
            "(örn: 'fidye yazılımı', 'solucan').\n\n"
            "Gerçek malware isimleri yasaktır."
        ),
        'cve_usage': (
            "⚠️ **CVE kullanımı tespit edildi.**\n\n"
            "CVE referansı yalnızca eğitim amaçlı gösterilebilir, "
            "kullanılamaz.\n\n"
            "Lütfen kavramsal açıklama yapın."
        ),
        'dangerous_phrase': (
            "⚠️ **Yönlendirici ifade tespit edildi.**\n\n"
            "Bu platform eğitim amaçlıdır. "
            "Doğrudan talimat veren ifadeler yasaktır."
        ),
    }
    
    # ============================================
    # SINIF DEĞİŞKENLERİ
    # ============================================
    
    _violation_log: List[Dict] = []
    
    # ============================================
    # METOT 1: KULLANICI GİRDİSİ KONTROLÜ
    # ============================================
    
    @classmethod
    def check_user_input(cls, text: str) -> Tuple[bool, str]:
        """
        Kullanıcı girdisini etik açıdan kontrol eder.
        
        Args:
            text: Kontrol edilecek metin
        
        Returns:
            (is_safe, warning_message):
                - is_safe: True ise güvenli, False ise yasaklı
                - warning_message: Yasaklı ise uyarı mesajı, değilse ""
        """
        if not text or not isinstance(text, str):
            return True, ""
        
        text_lower = text.lower()
        
        # 1. Gerçek IP kontrolü
        ip_matches = re.findall(
            r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 
            text
        )
        for ip in ip_matches:
            if not cls.PRIVATE_IP_PATTERN.match(ip):
                cls._log_violation('real_ip', ip)
                return False, cls.ETHICS_WARNINGS['real_ip']
        
        # 2. Gerçek domain kontrolü
        domain_matches = cls.REAL_DOMAIN_PATTERN.findall(text)
        if domain_matches:
            # example.com gibi güvenli olanları çıkar
            risky_domains = [
                d for d in domain_matches 
                if 'example' not in d.lower() 
                and 'test' not in d.lower()
                and 'ornek' not in d.lower()
            ]
            if risky_domains:
                cls._log_violation('real_domain', str(risky_domains))
                return False, cls.ETHICS_WARNINGS['real_domain']
        
        # 3. Yasaklı araç kontrolü
        for tool in cls.FORBIDDEN_TOOLS:
            if tool in text_lower:
                cls._log_violation('real_tool', tool)
                return False, cls.ETHICS_WARNINGS['real_tool']
        
        # 4. Yasaklı malware kontrolü
        for malware in cls.FORBIDDEN_MALWARE:
            if malware in text_lower:
                cls._log_violation('real_malware', malware)
                return False, cls.ETHICS_WARNINGS['real_malware']
        
        # 5. CVE kullanım kontrolü
        for pattern in cls.FORBIDDEN_CVE_USAGE:
            if re.search(pattern, text, re.IGNORECASE):
                cls._log_violation('cve_usage', text[:50])
                return False, cls.ETHICS_WARNINGS['cve_usage']
        
        # 6. Tehlikeli ifade kontrolü
        for phrase in cls.DANGEROUS_PHRASES:
            if phrase in text_lower:
                cls._log_violation('dangerous_phrase', phrase)
                return False, cls.ETHICS_WARNINGS['dangerous_phrase']
        
        # Tüm kontroller geçildi
        return True, ""
    
    # ============================================
    # METOT 2: AI ÇIKTISI KONTROLÜ
    # ============================================
    
    @classmethod
    def check_ai_output(cls, text: str) -> Tuple[bool, str]:
        """
        AI çıktısını etik açıdan kontrol eder.
        Kullanıcı girdisinden daha katı kurallar uygular.
        
        Args:
            text: AI yanıtı
        
        Returns:
            (is_safe, warning_message)
        """
        # Önce kullanıcı kontrolünü uygula
        is_safe, warning = cls.check_user_input(text)
        if not is_safe:
            return False, warning
        
        # AI-özel ek kontroller
        text_lower = text.lower()
        
        # Kod bloğu kontrolü (exploit kodu içermemeli)
        dangerous_code_patterns = [
            r'def\s+exploit\s*\(',
            r'payload\s*=\s*[\'"]',
            r'reverse_shell',
            r'nc\s+-e\s+/bin/(ba)?sh',
            r'bash\s+-i\s+>&\s+/dev/tcp',
            r'python\s+-c\s+[\'"]import\s+socket',
        ]
        
        for pattern in dangerous_code_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                cls._log_violation('exploit_code', pattern[:30])
                return False, "⚠️ AI çıktısında çalıştırılabilir saldırı kodu tespit edildi."
        
        # Adım adım talimat kontrolü
        instruction_patterns = [
            r'adım\s*1.*sisteme\s*bağlan',
            r'adım\s*1.*hedefe',
            r'şu\s*komutu\s*çalıştır',
            r'terminali\s*aç',
        ]
        
        for pattern in instruction_patterns:
            if re.search(pattern, text_lower):
                cls._log_violation('instructions', pattern[:30])
                return False, "⚠️ AI çıktısında yönlendirici talimat tespit edildi."
        
        return True, ""
    
    # ============================================
    # METOT 3: ETİK SÖZLEŞME ONAYI
    # ============================================
    
    @classmethod
    def require_ethics_acceptance(cls) -> bool:
        """
        İlk kullanımda etik sözleşme onayı alır.
        
        Returns:
            True: Sözleşme kabul edilmiş
            False: Sözleşme gösterildi (onay bekleniyor)
        """
        # Daha önce kabul edilmişse geç
        if st.session_state.get('ethics_accepted', False):
            return True
        
        # Sözleşme göster
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #0a1628 0%, #0d1a33 100%);
            border: 2px solid #00b4d8;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 8px 30px rgba(0, 180, 216, 0.2);
        ">
        """, unsafe_allow_html=True)
        
        st.markdown("# 📜 ETİK KULLANIM SÖZLEŞMESİ")
        
        st.markdown("""
        **SiberKalkan Akademi** platformunu kullanmadan önce 
        aşağıdaki maddeleri okuyup kabul etmelisiniz.
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ### ✅ Kabul Ediyorum
            
            1. Bu platformu **yalnızca eğitim amaçlı** kullanacağım.
            
            2. Öğrendiğim teknikleri **gerçek sistemlerde izinsiz** 
               kullanmayacağım.
            
            3. Platformdaki senaryolar **kavramsal simülasyonlardır**, 
               gerçek saldırı değildir.
            
            4. **TCK 243, 244, 245** maddelerini ihlal etmeyeceğim.
            
            5. Öğrendiklerimi **savunma amaçlı** kullanacağım.
            
            6. Platform verilerini **üçüncü şahıslarla** paylaşmayacağım.
            """)
        
        with col2:
            st.markdown("""
            ### 🎯 Amacım
            
            - Siber güvenlik alanında **savunma odaklı** bilgi edinmek
            
            - **Etik hacking** prensiplerine uygun hareket etmek
            
            - Kurumsal güvenliğe **katkı sağlamak**
            
            - Türkiye'nin siber güvenlik **iş gücüne katkı** sunmak
            
            - Gelecekte **siber savunmacı** olmak
            
            - **USOM** ile işbirliği yapmak
            """)
        
        st.markdown("---")
        
        st.error("""
        ⚠️ **YASAL UYARI**
        
        Bu platformdaki bilgileri kullanarak gerçek sistemlere izinsiz 
        erişim **TCK 243-245** kapsamında **suçtur**. 
        Yasadışı faaliyetlerden doğacak sorumluluk tamamen kullanıcıya aittir.
        """)
        
        st.markdown("---")
        
        # Onay butonları
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn2:
            accept = st.button(
                "✅ Kabul Ediyorum",
                type="primary",
                use_container_width=True,
                key="ethics_accept_btn"
            )
            reject = st.button(
                "❌ Reddediyorum",
                use_container_width=True,
                key="ethics_reject_btn"
            )
        
        if accept:
            st.session_state.ethics_accepted = True
            st.session_state.ethics_accepted_date = datetime.now().isoformat()
            st.success("✅ Sözleşme kabul edildi. Platforma yönlendiriliyorsunuz...")
            st.rerun()
        
        if reject:
            st.error("""
            ❌ Platformu kullanmak için sözleşmeyi kabul etmelisiniz.
            
            Anlayışınız için teşekkürler.
            """)
            st.stop()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        return False
    
    # ============================================
    # METOT 4: ETİK BANNER GÖSTER
    # ============================================
    
    @classmethod
    def display_ethics_banner(cls, scenario_id: str = ""):
        """
        Her senaryoda etik uyarı banner'ı gösterir.
        
        Args:
            scenario_id: Senaryo ID (örn: "7A")
        """
        # Senaryo-özel bilgi
        scenario_info = cls._get_scenario_ethics_info(scenario_id)
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1a3a5f 0%, #0d2a4a 100%);
            border-left: 5px solid #00b4d8;
            padding: 12px 18px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 0.85rem;
            color: #e0e0e0;
            line-height: 1.6;
        ">
            🛡️ <b>ETİK KULLANIM:</b> Bu senaryo <b>eğitim amaçlıdır</b>. 
            Sunulan teknikler yalnızca <b>izole simülasyon ortamında</b> geçerlidir. 
            Gerçek sistemlerde izinsiz kullanım <b>TCK 243-245</b> kapsamında suçtur.
            <br>
            🎓 <b>Öğrenme Hedefi:</b> {scenario_info['objective']}
            <br>
            📚 <b>Referans:</b> {scenario_info['reference']}
        </div>
        """, unsafe_allow_html=True)
    
    @classmethod
    def _get_scenario_ethics_info(cls, scenario_id: str) -> Dict[str, str]:
        """Senaryo için etik bilgileri döndürür"""
        default_info = {
            'objective': 'Bu senaryo sonunda savunma perspektifinden tehdidi tanıyabileceksiniz.',
            'reference': 'MITRE ATT&CK, OWASP Top 10, NIST'
        }
        
        # Seviye bazlı bilgiler
        if not scenario_id:
            return default_info
        
        level = scenario_id[0] if scenario_id[0].isdigit() else "1"
        
        level_info = {
            "1": {
                "objective": "Temel ağ kavramlarını ve güvenlik duvarı yönetimini öğrenmek.",
                "reference": "NIST SP 800-41 (Firewall Guidelines)"
            },
            "2": {
                "objective": "IDS/IPS sistemlerinin çalışma prensiplerini öğrenmek.",
                "reference": "NIST SP 800-94 (IDS/IPS Guide)"
            },
            "3": {
                "objective": "Kriptografik sistemlerin güvenliğini değerlendirmek.",
                "reference": "NIST SP 800-57 (Key Management)"
            },
            "4": {
                "objective": "DDoS saldırılarına karşı dayanıklılık geliştirmek.",
                "reference": "NIST SP 800-189 (DDoS Resilience)"
            },
            "5": {
                "objective": "Sızma testi metodolojilerini savunma bakışıyla anlamak.",
                "reference": "PTES (Penetration Testing Execution Standard)"
            },
            "6": {
                "objective": "APT saldırılarını tespit ve bertaraf etmek.",
                "reference": "MITRE ATT&CK Framework"
            },
            "7": {
                "objective": "Uygulama güvenliği açıklarını anlamak ve savunmak.",
                "reference": "OWASP Top 10 (2021)"
            },
            "8": {
                "objective": "Tersine mühendislik tekniklerini öğrenmek.",
                "reference": "SANS Reverse Engineering"
            },
            "9": {
                "objective": "Sosyal mühendislik saldırılarını tanımak ve önlemek.",
                "reference": "NIST SP 800-50 (Awareness Training)"
            },
            "10": {
                "objective": "Kapsamlı siber savunma stratejisi geliştirmek.",
                "reference": "NIST CSF 2.0"
            },
        }
        
        return level_info.get(level, default_info)
    
    # ============================================
    # METOT 5: İHLAL LOGLAMA
    # ============================================
    
    @classmethod
    def _log_violation(cls, violation_type: str, detail: str):
        """
        Etik ihlalleri loglar.
        
        Args:
            violation_type: İhlal türü (real_ip, real_domain, vb.)
            detail: İhlal detayı
        """
        cls._violation_log.append({
            'type': violation_type,
            'detail': detail,
            'timestamp': datetime.now().isoformat(),
        })
        
        # Session state'e de ekle
        if 'ethics_violations' not in st.session_state:
            st.session_state.ethics_violations = []
        st.session_state.ethics_violations.append({
            'type': violation_type,
            'detail': detail,
            'timestamp': datetime.now().strftime("%H:%M:%S"),
        })
    
    @classmethod
    def get_violation_log(cls) -> List[Dict]:
        """İhlal loglarını döndürür"""
        return cls._violation_log.copy()
    
    @classmethod
    def clear_violation_log(cls):
        """İhlal loglarını temizler"""
        cls._violation_log.clear()
        if 'ethics_violations' in st.session_state:
            st.session_state.ethics_violations = []
    
    # ============================================
    # METOT 6: SAVUNMA ÖNERİSİ GÖSTER
    # ============================================
    
    @classmethod
    def display_defense_recommendation(cls, scenario_id: str):
        """
        Her senaryo sonunda savunma önerileri gösterir.
        Jüri bunu çok sever!
        
        Args:
            scenario_id: Senaryo ID
        """
        recommendations = cls._get_defense_recommendations(scenario_id)
        
        if not recommendations:
            return
        
        with st.expander("🛡️ SAVUNMA ÖNERİLERİ (Bu senaryodan çıkarımlar)", expanded=False):
            st.markdown(f"### 📚 {recommendations['title']}")
            
            st.markdown("#### ✅ Yapılması Gerekenler:")
            for item in recommendations['dos']:
                st.markdown(f"- {item}")
            
            st.markdown("#### ❌ Kaçınılması Gerekenler:")
            for item in recommendations['donts']:
                st.markdown(f"- {item}")
            
            st.markdown("#### 📖 Referanslar:")
            for ref in recommendations['references']:
                st.markdown(f"- {ref}")
    
    @classmethod
    def _get_defense_recommendations(cls, scenario_id: str) -> Dict:
        """Senaryo için savunma önerileri"""
        recommendations = {
            "7A": {
                "title": "SQL Enjeksiyonundan Korunma",
                "dos": [
                    "✅ Parametreli sorgular (Prepared Statements) kullanın",
                    "✅ ORM (SQLAlchemy, Entity Framework) tercih edin",
                    "✅ Input validation + whitelist yaklaşımı uygulayın",
                    "✅ Veritabanı kullanıcısına minimum yetki verin",
                    "✅ WAF kuralı ile SQL anahtar kelimeleri filtreleyin",
                    "✅ Hata mesajlarında SQL detayı göstermeyin"
                ],
                "donts": [
                    "❌ String birleştirme ile sorgu yazmayın",
                    "❌ Kullanıcı girdisini doğrudan sorguya eklemeyin",
                    "❌ Aşırı yetkili DB kullanıcısı (root) kullanmayın",
                    "❌ Detaylı hata mesajlarını kullanıcıya gösterin"
                ],
                "references": [
                    "OWASP Top 10 A03:2021 - Injection",
                    "CWE-89: SQL Injection",
                    "MITRE ATT&CK T1190"
                ]
            },
            "9A": {
                "title": "Phishing Saldırılarından Korunma",
                "dos": [
                    "✅ E-posta filtreleme (SPF, DKIM, DMARC) yapılandırın",
                    "✅ Çalışanlara düzenli farkındalık eğitimi verin",
                    "✅ Şüpheli e-postaları raporlama sistemi kurun",
                    "✅ Çok faktörlü kimlik doğrulama (MFA) zorunlu kılın",
                    "✅ Simülasyon phishing testleri yapın"
                ],
                "donts": [
                    "❌ E-posta eklerini doğrulamadan açmayın",
                    "❌ Şüpheli bağlantılara tıklamayın",
                    "❌ Kimlik bilgilerinizi e-posta ile paylaşmayın"
                ],
                "references": [
                    "NIST SP 800-50 - Awareness Training",
                    "MITRE ATT&CK T1566 - Phishing"
                ]
            },
            # Diğer senaryolar için benzer yapı...
        }
        
        return recommendations.get(scenario_id, {})


# ============================================
# YARDIMCI FONKSİYONLAR
# ============================================

def check_and_warn(text: str, context: str = "input") -> str:
    """
    Metni kontrol eder ve güvenli değilse uyarı döndürür.
    
    Args:
        text: Kontrol edilecek metin
        context: "input" veya "output"
    
    Returns:
        Güvenli metin veya boş string
    """
    if context == "input":
        is_safe, warning = EthicsGuard.check_user_input(text)
    else:
        is_safe, warning = EthicsGuard.check_ai_output(text)
    
    if not is_safe:
        st.warning(warning)
        return ""
    
    return text


def display_ethics_status():
    """Sağ panelde etik durum göstergesi"""
    if 'ethics_violations' in st.session_state:
        violations = st.session_state.ethics_violations
        if violations:
            with st.expander(f"⚠️ Etik Uyarılar ({len(violations)})", expanded=False):
                for v in violations[-10:]:
                    st.caption(f"[{v['timestamp']}] {v['type']}: {v['detail'][:50]}")
        else:
            st.success("✅ Etik ihlal yok")
    else:
        st.success("✅ Etik ihlal yok")
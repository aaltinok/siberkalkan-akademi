"""
SiberKalkan Akademi - İçerik Güvenlik Filtresi
===============================================

Bu modül, AI çıktılarını ve içerikleri güvenlik açısından filtreler.
LLM entegrasyonu (opsiyonel) kullanıldığında devreye girer.

Görevleri:
    1. AI çıktılarını etik açıdan filtreleme
    2. Yasaklı içerikleri tespit etme ve değiştirme
    3. Eğitim bağlamı ekleme
    4. Referansları otomatik ekleme

Kullanım:
    from utils.safety_filter import AISafetyFilter
    
    # AI çıktısını filtrele
    filtered, warnings = AISafetyFilter.filter_output(ai_response)
    
    # Eğitim bağlamı ekle
    enriched = AISafetyFilter.add_educational_context(filtered, "7A")
"""

import re
import streamlit as st
from typing import Tuple, List, Dict, Optional
from datetime import datetime


class AISafetyFilter:
    """
    AI çıktı güvenlik filtresi.
    
    LLM'den gelen yanıtları etik ve teknik olarak denetler.
    Yasaklı içerikleri tespit eder, değiştirir ve kullanıcıya uyarı verir.
    """
    
    # ============================================
    # YASAKLI İÇERİK KATEGORİLERİ
    # ============================================
    
    BANNED_CONTENT: Dict[str, List[str]] = {
        # Çalıştırılabilir exploit kodu
        "exploit_code": [
            r"def\s+exploit\s*\(",
            r"payload\s*=\s*['\"]",
            r"reverse_shell",
            r"nc\s+-e\s+/bin/(ba)?sh",
            r"bash\s+-i\s+>&\s+/dev/tcp",
            r"python\s+-c\s+['\"]import\s+socket",
            r"msfvenom\s+-p",
            r"shellcode\s*=",
        ],
        
        # Adım adım saldırı talimatı
        "attack_instructions": [
            r"adım\s*1.*sisteme\s*bağlan",
            r"adım\s*1.*hedefe",
            r"şu\s*komutu\s*çalıştır",
            r"hemen\s*çalıştır",
            r"gerçek\s*sisteme\s*uygula",
            r"bu\s*IP\s*ye\s*saldır",
            r"exploit\s*et\s*ve",
            r"kopyala\s*ve\s*çalıştır",
        ],
        
        # Gerçek hedefler
        "real_targets": [
            r"\b(?!10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|127\.|0\.0\.0\.0)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
            r"\b(?!example|test|ornek)\w+\.(com|net|org|gov|edu)(?!\.(example|test))\b",
        ],
        
        # Zararlı yazılım isimleri
        "malware_names": [
            r"\b(mirai|emotet|trickbot|ryuk|conti|lockbit|wannacry|notpetya|stuxnet)\b",
        ],
        
        # Saldırı araçları
        "attack_tools": [
            r"\b(metasploit|msfconsole|msfvenom|empire|sliver|cobalt\s*strike|mimikatz|bloodhound)\b",
        ],
    }
    
    # ============================================
    # DEĞİŞTİRME METİNLERİ
    # ============================================
    
    REPLACEMENTS: Dict[str, str] = {
        "exploit_code": "// [Eğitim amaçlı kavramsal açıklama - kod filtrelendi]",
        "attack_instructions": "[Simülasyon talimatı - gerçek sistemlerde kullanılamaz]",
        "real_targets": "[örnek-hedef.local]",
        "malware_names": "[zararlı yazılım türü]",
        "attack_tools": "[saldırı aracı kategorisi]",
    }
    
    # ============================================
    # EĞİTİM REFERANSLARI (Senaryo bazlı)
    # ============================================
    
    SCENARIO_REFERENCES: Dict[str, Dict[str, str]] = {
        "1A": {
            "MITRE ATT&CK": "T1046 - Network Service Discovery",
            "NIST": "SP 800-41 - Firewall Guidelines",
            "Savunma": "Port tarama tespiti, IDS/IPS kuralları",
            "Gerçek Olay": "2016 Dyn DDoS (Mirai botnet)",
        },
        "1B": {
            "MITRE ATT&CK": "T1562.004 - Disable or Modify System Firewall",
            "NIST": "SP 800-41 - Firewall Guidelines",
            "Savunma": "Katmanlı güvenlik duvarı, kural yönetimi",
            "Gerçek Olay": "2015 Ukraine Power Grid",
        },
        "1C": {
            "MITRE ATT&CK": "T1592 - Gather Victim Host Information",
            "NIST": "SP 800-53 - Security Controls",
            "Savunma": "Honeypot, deception technology",
            "Gerçek Olay": "2017 NotPetya",
        },
        "1D": {
            "MITRE ATT&CK": "T1048 - Exfiltration Over Alternative Protocol",
            "NIST": "SP 800-53 - DLP Controls",
            "Savunma": "DLP, DNS monitoring, egress filtering",
            "Gerçek Olay": "2013 Target Breach",
        },
        "1E": {
            "MITRE ATT&CK": "T1557.002 - ARP Cache Poisoning",
            "NIST": "SP 800-153 - WLAN Security",
            "Savunma": "WPA3, 802.1X, kablosuz IDS",
            "Gerçek Olay": "2017 KRACK Attack",
        },
        "2A": {
            "MITRE ATT&CK": "T1595 - Active Scanning",
            "NIST": "SP 800-94 - IDS/IPS Guide",
            "Savunma": "Anomali tespiti, davranış analizi",
            "Gerçek Olay": "2014 Sony Pictures",
        },
        "2B": {
            "MITRE ATT&CK": "T1566 - Phishing",
            "NIST": "SP 800-61 - Incident Handling",
            "Savunma": "SIEM, SOAR, olay müdahale",
            "Gerçek Olay": "2013 Target Breach",
        },
        "2C": {
            "MITRE ATT&CK": "T1190 - Exploit Public-Facing Application",
            "OWASP": "A03:2021 - Injection",
            "Savunma": "WAF, kod güvenliği, input validation",
            "Gerçek Olay": "2017 Equifax Breach",
        },
        "2D": {
            "MITRE ATT&CK": "T1566.001 - Spearphishing Attachment",
            "NIST": "SP 800-50 - Awareness Training",
            "Savunma": "E-posta filtresi, farkındalık eğitimi",
            "Gerçek Olay": "2016 DNC Hack",
        },
        "2E": {
            "MITRE ATT&CK": "T1530 - Data from Cloud Storage",
            "NIST": "SP 800-144 - Cloud Security",
            "Savunma": "IAM, S3 bucket politikaları, CloudTrail",
            "Gerçek Olay": "2019 Capital One Breach",
        },
        "3A": {
            "MITRE ATT&CK": "T1600 - Weaken Encryption",
            "NIST": "SP 800-77 - IPsec VPN",
            "Savunma": "Güçlü kriptografi, PFS, anahtar yönetimi",
            "Gerçek Olay": "2014 Heartbleed",
        },
        "3B": {
            "MITRE ATT&CK": "T1486 - Data Encrypted for Impact",
            "NIST": "SP 800-184 - Ransomware Recovery",
            "Savunma": "Yedekleme, segmentasyon, EDR",
            "Gerçek Olay": "2017 WannaCry",
        },
        "3C": {
            "MITRE ATT&CK": "T1573 - Encrypted Channel",
            "NIST": "SP 800-57 - Key Management",
            "Savunma": "PGP/GPG, S/MIME, PKI",
            "Gerçek Olay": "2013 Snowden Revelations",
        },
        "3D": {
            "MITRE ATT&CK": "T1600 - Weaken Encryption",
            "NIST": "IR 8105 - Post-Quantum Crypto",
            "Savunma": "PQC algoritmaları, kripto çeviklik",
            "Gerçek Olay": "2022 NIST PQC Seçimi",
        },
        "3E": {
            "MITRE ATT&CK": "T1647 - Smart Contract Exploitation",
            "OWASP": "SC Top 10 - Reentrancy",
            "Savunma": "Kontrat denetimi, formal verification",
            "Gerçek Olay": "2016 The DAO Hack",
        },
        "4A": {
            "MITRE ATT&CK": "T1498 - Network Denial of Service",
            "NIST": "SP 800-189 - DDoS Resilience",
            "Savunma": "Anycast, scrubbing, rate limiting",
            "Gerçek Olay": "2016 Dyn DDoS",
        },
        "4B": {
            "MITRE ATT&CK": "T1498 - Network Denial of Service",
            "NIST": "SP 800-189 - DDoS Resilience",
            "Savunma": "CDN, WAF, auto-scaling, anycast",
            "Gerçek Olay": "2020 AWS DDoS (2.3 Tbps)",
        },
        "4C": {
            "MITRE ATT&CK": "T1498.002 - Reflection Amplification",
            "NIST": "SP 800-81 - DNS Security",
            "Savunma": "DNSSEC, RRL, açık resolver kapatma",
            "Gerçek Olay": "2018 GitHub 1.35 Tbps",
        },
        "4D": {
            "MITRE ATT&CK": "T1499 - Endpoint Denial of Service",
            "NIST": "SP 800-145 - Cloud Computing",
            "Savunma": "Load balancing, cache, CDN",
            "Gerçek Olay": "2021 Facebook Outage",
        },
        "4E": {
            "MITRE ATT&CK": "T1498 - Network Denial of Service",
            "NIST": "SP 800-145 - Cloud Computing",
            "Savunma": "CDN, edge computing, anycast",
            "Gerçek Olay": "2017 Amazon S3 Outage",
        },
        "5A": {
            "MITRE ATT&CK": "T1592 - Gather Victim Host Information",
            "NIST": "SP 800-53 - Reconnaissance",
            "Savunma": "OSINT minimization, OPSEC",
            "Gerçek Olay": "2013 Target Breach",
        },
        "5B": {
            "MITRE ATT&CK": "T1059.001 - PowerShell",
            "NIST": "SP 800-61 - Incident Handling",
            "Savunma": "SIEM, threat hunting, EDR",
            "Gerçek Olay": "2020 SolarWinds",
        },
        "5C": {
            "MITRE ATT&CK": "T1027 - Obfuscated Files",
            "NIST": "SP 800-83 - Malware Guide",
            "Savunma": "Sandbox, YARA, static analysis",
            "Gerçek Olay": "2010 Stuxnet",
        },
        "5D": {
            "MITRE ATT&CK": "T1068 - Exploitation for Privilege Escalation",
            "NIST": "SP 800-53 - Access Control",
            "Savunma": "Least privilege, EDR, patching",
            "Gerçek Olay": "2021 PrintNightmare",
        },
        "5E": {
            "MITRE ATT&CK": "T1070 - Indicator Removal",
            "NIST": "SP 800-86 - Forensics",
            "Savunma": "Log integrity, SIEM, immutable logs",
            "Gerçek Olay": "2013 Snowden",
        },
        "6A": {
            "MITRE ATT&CK": "T1190 - Exploit Public-Facing Application",
            "NIST": "SP 800-61 - Incident Handling",
            "Savunma": "Defense in depth, threat hunting",
            "Gerçek Olay": "2020 SolarWinds",
        },
        "6B": {
            "MITRE ATT&CK": "T1003 - OS Credential Dumping",
            "NIST": "SP 800-61 - Incident Handling",
            "Savunma": "EDR, NDR, SOAR, threat intel",
            "Gerçek Olay": "2021 Colonial Pipeline",
        },
        "6C": {
            "MITRE ATT&CK": "T1021 - Remote Services",
            "NIST": "SP 800-125B - Segmentation",
            "Savunma": "Microsegmentation, zero trust",
            "Gerçek Olay": "2017 NotPetya",
        },
        "6D": {
            "MITRE ATT&CK": "T1041 - Exfiltration Over C2",
            "NIST": "SP 800-53 - DLP Controls",
            "Savunma": "DLP, egress filtering, CASB",
            "Gerçek Olay": "2015 OPM Breach",
        },
        "6E": {
            "MITRE ATT&CK": "T1489 - Service Stop",
            "NIST": "SP 800-82 - ICS Security",
            "Savunma": "OT security, IT/OT segmentation",
            "Gerçek Olay": "2021 Colonial Pipeline",
        },
        "7A": {
            "MITRE ATT&CK": "T1190 - Exploit Public-Facing Application",
            "OWASP": "A03:2021 - Injection",
            "CWE": "CWE-89 - SQL Injection",
            "Savunma": "Parametreli sorgular, ORM, WAF",
            "Gerçek Olay": "2017 Equifax Breach",
        },
        "7B": {
            "MITRE ATT&CK": "T1562 - Impair Defenses",
            "OWASP": "Top 10 - All Categories",
            "Savunma": "WAF, virtual patching, SDLC",
            "Gerçek Olay": "2019 Capital One",
        },
        "7C": {
            "MITRE ATT&CK": "T1189 - Drive-by Compromise",
            "OWASP": "A03:2021 - XSS",
            "CWE": "CWE-79 - XSS",
            "Savunma": "CSP, output encoding, sanitization",
            "Gerçek Olay": "2005 MySpace Samy Worm",
        },
        "7D": {
            "MITRE ATT&CK": "T1059 - Command and Scripting Interpreter",
            "OWASP": "A03:2021 - Injection",
            "CWE": "CWE-78 - OS Command Injection",
            "Savunma": "Input validation, sandboxing",
            "Gerçek Olay": "2014 Shellshock",
        },
        "7E": {
            "MITRE ATT&CK": "T1558 - Steal or Forge Kerberos Tickets",
            "NIST": "SP 800-53 - Access Control",
            "Savunma": "AD hardening, tiered admin, LAPS",
            "Gerçek Olay": "2020 SolarWinds",
        },
        "8A": {
            "MITRE ATT&CK": "T1027 - Obfuscated Files",
            "NIST": "SP 800-83 - Malware Guide",
            "Savunma": "Anti-tamper, code signing",
            "Gerçek Olay": "2010 Stuxnet",
        },
        "8B": {
            "MITRE ATT&CK": "T1055 - Process Injection",
            "NIST": "SP 800-83 - Malware Guide",
            "Savunma": "EDR, YARA, sandbox",
            "Gerçek Olay": "2017 NotPetya",
        },
        "8C": {
            "MITRE ATT&CK": "T1027 - Obfuscated Files",
            "NIST": "SP 800-83 - Malware Guide",
            "Savunma": "Unpacking tools, memory forensics",
            "Gerçek Olay": "2014 Gameover Zeus",
        },
        "8D": {
            "MITRE ATT&CK": "T1542 - Pre-OS Boot",
            "NIST": "SP 800-147 - BIOS Protection",
            "Savunma": "Secure Boot, TPM, firmware signing",
            "Gerçek Olay": "2015 Hacking Team UEFI",
        },
        "8E": {
            "MITRE ATT&CK": "T1547 - Boot or Logon Autostart",
            "NIST": "SP 800-83 - Malware Guide",
            "Savunma": "Kernel integrity, memory forensics",
            "Gerçek Olay": "2010 Stuxnet",
        },
        "9A": {
            "MITRE ATT&CK": "T1566 - Phishing",
            "NIST": "SP 800-50 - Awareness Training",
            "Savunma": "DMARC, eğitim, MFA",
            "Gerçek Olay": "2016 DNC Hack",
        },
        "9B": {
            "MITRE ATT&CK": "T1566 - Phishing",
            "NIST": "SP 800-50 - Awareness Training",
            "Savunma": "Sürekli eğitim, simülasyon, kültür",
            "Gerçek Olay": "2017 Google/Facebook BEC",
        },
        "9C": {
            "MITRE ATT&CK": "T1592 - Gather Victim Host Information",
            "NIST": "SP 800-53 - Physical Security",
            "Savunma": "Erişim kontrolü, eğitim, izleme",
            "Gerçek Olay": "2013 Target Physical Breach",
        },
        "9D": {
            "MITRE ATT&CK": "T1598 - Phishing for Information",
            "NIST": "SP 800-50 - Awareness Training",
            "Savunma": "Telefon doğrulama, callback prosedürü",
            "Gerçek Olay": "2020 Twitter Hack",
        },
        "9E": {
            "MITRE ATT&CK": "T1589 - Gather Victim Identity Information",
            "NIST": "SP 800-50 - Awareness Training",
            "Savunma": "Zero trust, doğrulama, kültür",
            "Gerçek Olay": "2020 Twitter Hack",
        },
        "10A": {
            "MITRE ATT&CK": "Full Kill Chain",
            "NIST": "CSF 2.0 - All Functions",
            "Savunma": "Kapsamlı savunma stratejisi",
            "Gerçek Olay": "2020 SolarWinds",
        },
        "10B": {
            "MITRE ATT&CK": "Full Kill Chain",
            "NIST": "CSF 2.0 - All Functions",
            "Savunma": "SIEM, SOAR, EDR, NDR entegrasyonu",
            "Gerçek Olay": "2021 Colonial Pipeline",
        },
        "10C": {
            "MITRE ATT&CK": "Purple Teaming",
            "NIST": "CSF 2.0 - Continuous Improvement",
            "Savunma": "Detection engineering, tuning",
            "Gerçek Olay": "MITRE Engenuity Evaluations",
        },
        "10D": {
            "MITRE ATT&CK": "T1587 - Develop Capabilities",
            "NIST": "SP 800-40 - Patch Management",
            "Savunma": "Bug bounty, patch, mitigation",
            "Gerçek Olay": "2021 Log4Shell",
        },
        "10E": {
            "MITRE ATT&CK": "Full Kill Chain",
            "NIST": "CSF 2.0 - All Functions",
            "Savunma": "Ulusal siber savunma stratejisi",
            "Gerçek Olay": "2022 Ukraine Cyber Attacks",
        },
    }
    
    # ============================================
    # METOT 1: AI ÇIKTISI FİLTRELE
    # ============================================
    
    @classmethod
    def filter_output(cls, ai_response: str) -> Tuple[str, List[str]]:
        """
        AI çıktısını filtreler.
        
        Args:
            ai_response: AI'dan gelen ham yanıt
        
        Returns:
            (filtered_text, warnings_list):
                - filtered_text: Filtrelenmiş metin
                - warnings_list: Uyarı mesajları listesi
        """
        if not ai_response or not isinstance(ai_response, str):
            return "", []
        
        warnings: List[str] = []
        filtered = ai_response
        
        for category, patterns in cls.BANNED_CONTENT.items():
            for pattern in patterns:
                matches = re.findall(pattern, filtered, re.IGNORECASE)
                if matches:
                    warnings.append(
                        f"⚠️ {category}: {len(matches)} içerik filtrelendi"
                    )
                    filtered = re.sub(
                        pattern,
                        cls.REPLACEMENTS.get(category, "[filtrelendi]"),
                        filtered,
                        flags=re.IGNORECASE
                    )
        
        return filtered, warnings
    
    # ============================================
    # METOT 2: EĞİTİM BAĞLAMI EKLE
    # ============================================
    
    @classmethod
    def add_educational_context(cls, ai_response: str, scenario_id: str) -> str:
        """
        AI çıktısının sonuna eğitim bağlamı ve referans ekler.
        
        Args:
            ai_response: AI yanıtı
            scenario_id: Senaryo ID (örn: "7A")
        
        Returns:
            Zenginleştirilmiş metin
        """
        references = cls.SCENARIO_REFERENCES.get(scenario_id, {})
        
        if not references:
            return ai_response
        
        educational_note = "\n\n---\n\n"
        educational_note += "### 📚 Eğitim Notu ve Referanslar\n\n"
        
        for ref_type, ref_value in references.items():
            educational_note += f"- **{ref_type}:** {ref_value}\n"
        
        educational_note += "\n"
        educational_note += "> 🛡️ **Hatırlatma:** Bu bilgiler yalnızca savunma "
        educational_note += "amaçlı öğrenme içindir. Gerçek sistemlerde izinsiz "
        educational_note += "kullanım yasaktır (TCK 243-245).\n"
        
        return ai_response + educational_note
    
    # ============================================
    # METOT 3: GÜVENLİ MESAJ OLUŞTUR
    # ============================================
    
    @classmethod
    def create_safe_message(
        cls,
        ai_response: str,
        scenario_id: str,
        show_warnings: bool = True,
    ) -> str:
        """
        Filtrelenmiş ve eğitim bağlamı eklenmiş güvenli mesaj oluşturur.
        
        Args:
            ai_response: AI yanıtı
            scenario_id: Senaryo ID
            show_warnings: Uyarılar gösterilsin mi?
        
        Returns:
            Güvenli, zenginleştirilmiş mesaj
        """
        # 1. Filtrele
        filtered, warnings = cls.filter_output(ai_response)
        
        # 2. Eğitim bağlamı ekle
        enriched = cls.add_educational_context(filtered, scenario_id)
        
        # 3. Uyarıları göster (opsiyonel)
        if show_warnings and warnings:
            for warning in warnings:
                st.warning(warning)
        
        return enriched
    
    # ============================================
    # METOT 4: İÇERİK GÜVENLİ Mİ?
    # ============================================
    
    @classmethod
    def is_content_safe(cls, text: str) -> Tuple[bool, List[str]]:
        """
        İçeriğin güvenli olup olmadığını kontrol eder.
        
        Args:
            text: Kontrol edilecek metin
        
        Returns:
            (is_safe, issues_list)
        """
        issues = []
        
        for category, patterns in cls.BANNED_CONTENT.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    issues.append(f"{category}: {pattern[:30]}...")
        
        return len(issues) == 0, issues
    
    # ============================================
    # METOT 5: REFERANS AL
    # ============================================
    
    @classmethod
    def get_references(cls, scenario_id: str) -> Dict[str, str]:
        """
        Senaryo için referansları döndürür.
        
        Args:
            scenario_id: Senaryo ID
        
        Returns:
            Referans dict'i
        """
        return cls.SCENARIO_REFERENCES.get(scenario_id, {}).copy()
    
    # ============================================
    # METOT 6: HTML GÜVENLİ METİN
    # ============================================
    
    @classmethod
    def safe_html(cls, text: str) -> str:
        """
        Metni HTML'de güvenli şekilde göstermek için escape eder.
        
        Args:
            text: Ham metin
        
        Returns:
            HTML-güvenli metin
        """
        if not text:
            return ""
        
        # HTML özel karakterleri escape et
        replacements = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;",
        }
        
        safe = text
        for char, escaped in replacements.items():
            safe = safe.replace(char, escaped)
        
        return safe
    
    # ============================================
    # METOT 7: UYARI GÖSTER
    # ============================================
    
    @classmethod
    def display_warnings(cls, warnings: List[str]) -> None:
        """
        Uyarıları Streamlit'te gösterir.
        
        Args:
            warnings: Uyarı listesi
        """
        if not warnings:
            return
        
        with st.expander(f"⚠️ Güvenlik Uyarıları ({len(warnings)})", expanded=False):
            for warning in warnings:
                st.warning(warning)
    
    # ============================================
    # METOT 8: LLM PROMPT GÜVENLİĞİ
    # ============================================
    
    @classmethod
    def build_safe_prompt(cls, scenario_id: str, context: str = "") -> str:
        """
        LLM için güvenli prompt oluşturur.
        Prompt injection saldırılarına karşı korumalıdır.
        
        Args:
            scenario_id: Senaryo ID
            context: Ek bağlam
        
        Returns:
            Güvenli prompt
        """
        base_prompt = f"""
Sen SiberKalkan Akademi platformunda bir eğitim asistanısın.

GÖREVLERİN:
1. Öğrencilere siber güvenlik kavramlarını açıkla
2. Savunma perspektifinden bilgi ver
3. Etik hacking prensiplerini vurgula
4. Gerçek sistemlere zarar verebilecek bilgi verme

KURALLAR:
❌ Çalıştırılabilir exploit kodu verme
❌ Gerçek IP/domain hedefleme
❌ Saldırı araçlarının isimlerini verme
❌ Adım adım saldırı talimatı verme
❌ Gerçek zararlı yazılım isimleri kullanma

✅ Kavramsal açıklama yap
✅ Savunma yöntemlerini anlat
✅ MITRE ATT&CK / OWASP referansları ver
✅ Eğitim amaçlı olduğunu vurgula
✅ Etik ve yasal sınırları hatırlat

SENARYO: {scenario_id}

{context}

Yanıtını Türkçe ver. Kısa, teknik ve eğitici ol.
"""
        
        return base_prompt.strip()
    
    # ============================================
    # METOT 9: FİLTRE İSTATİSTİKLERİ
    # ============================================
    
    @classmethod
    def get_filter_stats(cls) -> Dict:
        """
        Filtre istatistiklerini döndürür.
        
        Returns:
            İstatistik dict'i
        """
        if 'ai_filter_stats' not in st.session_state:
            st.session_state.ai_filter_stats = {
                'total_filters': 0,
                'total_warnings': 0,
                'categories': {},
                'first_use': datetime.now().isoformat(),
            }
        
        return st.session_state.ai_filter_stats.copy()
    
    @classmethod
    def _update_stats(cls, warnings: List[str]) -> None:
        """İstatistikleri günceller"""
        if 'ai_filter_stats' not in st.session_state:
            st.session_state.ai_filter_stats = {
                'total_filters': 0,
                'total_warnings': 0,
                'categories': {},
                'first_use': datetime.now().isoformat(),
            }
        
        stats = st.session_state.ai_filter_stats
        stats['total_filters'] += 1
        stats['total_warnings'] += len(warnings)
        
        for warning in warnings:
            # Kategori çıkar
            for cat in cls.BANNED_CONTENT.keys():
                if cat in warning:
                    stats['categories'][cat] = stats['categories'].get(cat, 0) + 1


# ============================================
# YARDIMCI FONKSİYONLAR
# ============================================

def safe_display(text: str, scenario_id: str = "") -> str:
    """
    Metni güvenli şekilde gösterir ve eğitim bağlamı ekler.
    
    Args:
        text: Gösterilecek metin
        scenario_id: Senaryo ID
    
    Returns:
        Güvenli metin
    """
    filtered, warnings = AISafetyFilter.filter_output(text)
    
    if warnings:
        AISafetyFilter.display_warnings(warnings)
    
    if scenario_id:
        return AISafetyFilter.add_educational_context(filtered, scenario_id)
    
    return filtered


def display_references(scenario_id: str) -> None:
    """
    Sağ panelde senaryo referanslarını gösterir.
    
    Args:
        scenario_id: Senaryo ID
    """
    references = AISafetyFilter.get_references(scenario_id)
    
    if not references:
        st.info("Bu senaryo için referans bulunamadı.")
        return
    
    st.markdown("### 📚 Referanslar")
    
    for ref_type, ref_value in references.items():
        icon = {
            "MITRE ATT&CK": "🔴",
            "OWASP": "🟠",
            "CWE": "🟡",
            "NIST": "🔵",
            "Savunma": "🛡️",
            "Gerçek Olay": "🌍",
        }.get(ref_type, "📖")
        
        st.markdown(f"**{icon} {ref_type}:**")
        st.caption(ref_value)
        st.markdown("")


# ============================================
# MODÜL TESTİ
# ============================================

if __name__ == "__main__":
    print("✅ AISafetyFilter yüklendi")
    print(f"Toplam kategori: {len(AISafetyFilter.BANNED_CONTENT)}")
    print(f"Toplam senaryo referansı: {len(AISafetyFilter.SCENARIO_REFERENCES)}")
    
    # Basit test
    test_text = "SELECT * FROM users WHERE id = 1"
    is_safe, issues = AISafetyFilter.is_content_safe(test_text)
    print(f"Test metni güvenli mi? {is_safe}")
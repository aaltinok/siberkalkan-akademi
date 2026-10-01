"""
SiberKalkan Akademi - Senaryo Raporları Verisi
================================================

65 senaryo için öğrenme çıktıları, savunma önerileri ve referanslar.

Kullanım:
    from content.scenario_reports import SCENARIO_REPORTS
    report_data = SCENARIO_REPORTS.get("7A", {})
    learning = report_data.get('learning_outcomes', [])
"""

SCENARIO_REPORTS = {
    # ============================================
    # SEVİYE 1
    # ============================================
    "1A": {
        "achievements_map": {
            "attempts": "Deneme yapıldı",
            "hacked": "Hedef sunucu test edildi",
        },
        "learning_outcomes": [
            "Temel ağ keşif teknikleri",
            "Port tarama metodolojisi",
            "SSH/HTTP/MySQL servislerinin tanınması",
            "Basit exploit paketlerinin yapısı",
            "Güvenlik duvarı kurallarının çalışma prensibi",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Port tarama tespiti için IDS/IPS kuralları ekleyin",
                "✅ Kullanılmayan portları kapatın",
                "✅ SSH için anahtar tabanlı kimlik doğrulama kullanın",
                "✅ Rate limiting ile anormal erişimleri engelleyin",
                "✅ Honeypot kurarak tarama aktivitelerini izleyin",
            ],
            "donts": [
                "❌ Varsayılan portları açık bırakmayın",
                "❌ Zayıf şifreler kullanmayın",
                "❌ Detaylı hata mesajları göstermeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1046 - Network Service Discovery",
            "NIST": "SP 800-41 - Firewall Guidelines",
            "CIS": "CIS Control 4 - Controlled Use of Administrative Privileges",
            "Gerçek Olay": "2016 Dyn DDoS (Mirai botnet)",
        }
    },
    "1B": {
        "achievements_map": {
            "rules": "Kural eklendi",
            "ai_attacks": "AI test hamlesi yapıldı",
        },
        "learning_outcomes": [
            "Güvenlik duvarı kural yazma",
            "Katmanlı savunma stratejisi",
            "Yanlış pozitif yönetimi",
            "Anormal trafik tespiti",
            "Firewall performans izleme",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ En az 3 farklı kural katmanı oluşturun",
                "✅ SSH brute-force koruması ekleyin (fail2ban benzeri)",
                "✅ HTTP anomali filtrelemesi yapılandırın",
                "✅ ICMP flood koruması aktif edin",
                "✅ Kural loglarını düzenli analiz edin",
            ],
            "donts": [
                "❌ Tüm trafiği engelleyen aşırı katı kurallar koymayın",
                "❌ Kural güncellemelerini ihmal etmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1562.004 - Disable or Modify System Firewall",
            "NIST": "SP 800-41 - Firewall Guidelines",
            "Gerçek Olay": "2015 Ukraine Power Grid Attack",
        }
    },
    "1C": {
        "achievements_map": {
            "scans": "Tarama yapıldı",
            "hacked": "Doğru hedef tespit edildi",
            "detected": "Honeypot tespit edildi",
        },
        "learning_outcomes": [
            "Honeypot (bal küpü) kavramı",
            "Gerçek sunucu ile sahte sunucu ayrımı",
            "HTTP başlık analizi",
            "Aldatma teknolojileri",
            "Pasif keşif teknikleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Honeypot'ları gerçek sunuculardan farklı yapılandırın",
                "✅ Honeypot loglarını SIEM'e entegre edin",
                "✅ Sahte servis banner'ları kullanın",
                "✅ Honeypot trafiğini sürekli izleyin",
            ],
            "donts": [
                "❌ Honeypot'ları gerçek verilerle doldurmayın",
                "❌ Honeypot IP'lerini açık etmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1592 - Gather Victim Host Information",
            "NIST": "SP 800-53 - Deception Technology",
            "Gerçek Olay": "2017 NotPetya Honeypot Deployment",
        }
    },
    "1D": {
        "achievements_map": {
            "stopped_leaks": "Sızıntı durduruldu",
            "ai_leaks": "AI sızıntı yaptı",
        },
        "learning_outcomes": [
            "DNS tünelleme tekniği",
            "Veri kaybı önleme (DLP) sistemleri",
            "Anormal DNS sorgu tespiti",
            "Veri sızdırma metodolojileri",
            "Olay müdahale süreçleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ DNS sorgu uzunluğu limiti koyun",
                "✅ Bilinmeyen domain'lere sorguları engelleyin",
                "✅ DNS over HTTPS (DoH) kullanın",
                "✅ Ağ çıkış (egress) filtrelemesi yapın",
                "✅ DLP yazılımı kurun",
            ],
            "donts": [
                "❌ DNS trafiğini şifresiz bırakmayın",
                "❌ Uzun alan adı sorgularına izin vermeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1048 - Exfiltration Over Alternative Protocol",
            "NIST": "SP 800-53 - System and Communications Protection",
            "Gerçek Olay": "2013 Target Breach",
        }
    },
    "1E": {
        "achievements_map": {
            "captured_packets": "Paket yakalandı",
            "cookie_stolen": "Oturum çerezi çalındı",
            "detected": "Tespit edildi",
        },
        "learning_outcomes": [
            "Kablosuz ağ güvenliği prensipleri",
            "WEP/WPA2/WPA3 farkları",
            "Deauthentication saldırısı",
            "MAC adresi sahtekarlığı",
            "Kablosuz IDS (WIDS) sistemleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ WPA3 kullanın (yoksa WPA2-AES)",
                "✅ 802.1X kimlik doğrulama kurun",
                "✅ Guest ağı ile iç ağı ayırın",
                "✅ WIDS kurarak anormal trafiği izleyin",
                "✅ Management frame protection aktif edin",
            ],
            "donts": [
                "❌ WEP veya WPA-TKIP kullanmayın",
                "❌ WPS'i açık bırakmayın",
                "❌ Varsayılan SSID ve şifreleri değiştirmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1557.002 - ARP Cache Poisoning",
            "NIST": "SP 800-153 - WLAN Security",
            "Gerçek Olay": "2017 KRACK Attack",
        }
    },

    # ============================================
    # SEVİYE 2
    # ============================================
    "2A": {
        "achievements_map": {
            "normal_behavior": "Normal davranış sergilendi",
            "vuln_found": "Zafiyet bulundu",
            "exploited": "Test başarılı",
        },
        "learning_outcomes": [
            "IDS/IPS sistemlerinin çalışma prensibi",
            "İmza ve davranış analizi arasındaki fark",
            "Yavaş/gizli tarama teknikleri",
            "Anomali tespit mekanizmaları",
            "IDS atlatma metodolojileri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Hem imza hem davranış analizi kullanın",
                "✅ Baseline (normal davranış) öğrenmesi aktif edin",
                "✅ Yavaş tarama tespiti için uzun süreli analiz yapın",
                "✅ Anomali skorunu sürekli izleyin",
                "✅ IDS/IPS kurallarını düzenli güncelleyin",
            ],
            "donts": [
                "❌ Sadece imza tabanlı tespit yeterli değildir",
                "❌ Bilinen saldırı imzalarına güvenmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1595 - Active Scanning",
            "NIST": "SP 800-94 - IDS/IPS Guide",
            "Gerçek Olay": "2014 Sony Pictures Attack",
        }
    },
    "2B": {
        "achievements_map": {
            "resolved": "Olay çözüldü",
            "missed": "Olay kaçırıldı",
            "false_positives": "Yanlış pozitif",
        },
        "learning_outcomes": [
            "SIEM sistemlerinin çalışması",
            "Olay önceliklendirme",
            "Yanlış pozitif yönetimi",
            "SOC operasyonları",
            "Kriz anında karar verme",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ SIEM'de önceliklendirme kuralları tanımlayın",
                "✅ Kritik uyarılara öncelik verin",
                "✅ Yanlış pozitif oranını sürekli ölçün",
                "✅ SOAR ile otomasyon ekleyin",
                "✅ Analist eğitimlerini düzenli yapın",
            ],
            "donts": [
                "❌ Tüm uyarıları eşit görmeyin",
                "❌ Uyarıları görmezden gelmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1566 - Phishing",
            "NIST": "SP 800-61 - Incident Handling",
            "Gerçek Olay": "2013 Target Breach",
        }
    },
    "2C": {
        "achievements_map": {
            "bypass_found": "WAF atlatma bulundu",
            "waf_blocks": "WAF engelledi",
            "admin_accessed": "Admin panel erişildi",
        },
        "learning_outcomes": [
            "WAF (Web Application Firewall) yapısı",
            "SQL enjeksiyonu türleri",
            "WAF atlatma teknikleri",
            "Kodlama ve kaçış karakterleri",
            "Güvenli kod geliştirme prensipleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ WAF'ı katmanlı savunmanın bir parçası yapın",
                "✅ Kural setini güncel tutun (OWASP CRS)",
                "✅ Parametreli sorgular kullanın",
                "✅ Input validation yapın",
                "✅ WAF loglarını düzenli analiz edin",
            ],
            "donts": [
                "❌ WAF'ı tek savunma olarak görmeyin",
                "❌ Hata mesajlarında SQL detayı göstermeyin",
                "❌ String birleştirme ile sorgu yazmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1190 - Exploit Public-Facing Application",
            "OWASP": "A03:2021 - Injection",
            "Gerçek Olay": "2017 Equifax Breach",
        }
    },
    "2D": {
        "achievements_map": {
            "detected": "Oltalama tespit edildi",
            "missed": "Oltalama kaçırıldı",
            "false_positives": "Yanlış pozitif",
        },
        "learning_outcomes": [
            "Sosyal mühendislik saldırıları",
            "Phishing e-posta özellikleri",
            "E-posta başlık analizi",
            "URL ve ek dosya analizi",
            "Farkındalık eğitimi prensipleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ SPF, DKIM ve DMARC kayıtlarını yapılandırın",
                "✅ E-posta güvenlik ağ geçidi kullanın",
                "✅ Çalışanlara düzenli farkındalık eğitimi verin",
                "✅ Şüpheli e-postaları raporlama sistemi kurun",
                "✅ Simülasyon phishing testleri yapın",
            ],
            "donts": [
                "❌ E-posta eklerini doğrulamadan açmayın",
                "❌ Şüpheli bağlantılara tıklamayın",
                "❌ Kimlik bilgilerini e-posta ile paylaşmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1566.001 - Spearphishing Attachment",
            "NIST": "SP 800-50 - Awareness Training",
            "Gerçek Olay": "2016 DNC Hack",
        }
    },
    "2E": {
        "achievements_map": {
            "fixed": "Bucket düzeltildi",
            "leaked": "Veri sızdırıldı",
        },
        "learning_outcomes": [
            "Bulut güvenliği prensipleri",
            "AWS S3 bucket yapılandırması",
            "IAM rolleri ve politikaları",
            "CloudTrail ve Config kullanımı",
            "Paylaşılan sorumluluk modeli",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ S3 bucket'ları varsayılan olarak private yapın",
                "✅ IAM rollerini minimum yetki prensibiyle yapılandırın",
                "✅ CloudTrail'i tüm bölgelerde aktif edin",
                "✅ AWS Config kuralları ile uyumluluk izleyin",
                "✅ GuardDuty ile tehdit tespiti yapın",
            ],
            "donts": [
                "❌ S3 bucket'ları public yapmayın",
                "❌ Root hesabı günlük kullanmayın",
                "❌ API anahtarlarını kodda saklamayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1530 - Data from Cloud Storage",
            "NIST": "SP 800-144 - Cloud Security",
            "Gerçek Olay": "2019 Capital One Breach",
        }
    },

    # ============================================
    # SEVİYE 3
    # ============================================
    "3A": {
        "achievements_map": {
            "packets_captured": "Paket yakalandı",
            "key_broken": "Anahtar kırıldı",
            "data_stolen": "Veri çalındı",
        },
        "learning_outcomes": [
            "VPN şifreleme protokolleri",
            "Kriptografik algoritmalar",
            "Anahtar değişim mekanizmaları",
            "Kriptanaliz teknikleri",
            "Kripto zafiyetleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ AES-256 şifreleme kullanın",
                "✅ SHA-256/384 hash algoritmaları kullanın",
                "✅ Diffie-Hellman Group 14+ kullanın",
                "✅ Perfect Forward Secrecy aktif edin",
                "✅ Sertifika tabanlı kimlik doğrulama yapın",
            ],
            "donts": [
                "❌ DES, 3DES veya RC4 kullanmayın",
                "❌ MD5 veya SHA-1 kullanmayın",
                "❌ Zayıf DH grupları kullanmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1600 - Weaken Encryption",
            "NIST": "SP 800-77 - IPsec VPN",
            "Gerçek Olay": "2014 Heartbleed",
        }
    },
    "3B": {
        "achievements_map": {
            "isolated": "Sunucu izole edildi",
            "recovered": "Sistem kurtarıldı",
        },
        "learning_outcomes": [
            "Fidye yazılımı davranışı",
            "Olay müdahale süreçleri",
            "Yedekleme stratejileri",
            "Ağ segmentasyonu",
            "Kriz iletişimi",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ 3-2-1 yedekleme stratejisi uygulayın",
                "✅ Yedekleri çevrimdışı (offline) saklayın",
                "✅ Ağ segmentasyonu yapın",
                "✅ EDR çözümü kullanın",
                "✅ Düzenli fidye yazılımı tatbikatları yapın",
            ],
            "donts": [
                "❌ Fidye ödemeyin",
                "❌ Yedekleri ağa bağlı tutmayın",
                "❌ Segmentasyonu ihmal etmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1486 - Data Encrypted for Impact",
            "NIST": "SP 800-184 - Ransomware Recovery",
            "Gerçek Olay": "2017 WannaCry",
        }
    },
    "3C": {
        "achievements_map": {
            "keys_distributed": "Anahtar dağıtıldı",
            "encrypted_ratio": "Şifreli oran arttı",
            "mitm_success": "MITM saldırısı",
        },
        "learning_outcomes": [
            "PGP/GPG şifreleme",
            "Açık anahtar altyapısı (PKI)",
            "Anahtar yönetimi",
            "Ortadaki adam saldırısı",
            "Güven ağı",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ S/MIME veya PGP kullanın",
                "✅ Anahtar imzalama partileri düzenleyin",
                "✅ Sertifika iptal listelerini kontrol edin",
                "✅ Anahtar güven skorlarını izleyin",
                "✅ Uçtan uca şifreleme zorunlu kılın",
            ],
            "donts": [
                "❌ Şifresiz e-posta göndermeyin",
                "❌ Açık anahtarları doğrulamadan kullanmayın",
                "❌ Özel anahtarları güvensiz saklayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1573 - Encrypted Channel",
            "NIST": "SP 800-57 - Key Management",
            "Gerçek Olay": "2013 Snowden Revelations",
        }
    },
    "3D": {
        "achievements_map": {
            "legacy_found": "Zayıf sistem bulundu",
            "quantum_progress": "Kuantum analizi",
            "exploited": "Test başarılı",
        },
        "learning_outcomes": [
            "Kuantum bilişim tehdidi",
            "Post-quantum kriptografi (PQC)",
            "Kripto çeviklik kavramı",
            "Hibrit kripto sistemleri",
            "Geçiş dönemi riskleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Kuantum sonrası algoritmalara geçiş planı yapın",
                "✅ CRYSTALS-Kyber, Dilithium gibi PQC algoritmalarını test edin",
                "✅ Kripto çeviklik (crypto-agility) prensibi benimseyin",
                "✅ Hibrit kripto sistemler kullanın",
                "✅ Envanterdeki eski algoritmaları tespit edin",
            ],
            "donts": [
                "❌ SHA-1 ve MD5 kullanmayın",
                "❌ RSA-1024 veya altını kullanmayın",
                "❌ Kripto geçişini ertelemeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1600 - Weaken Encryption",
            "NIST": "IR 8105 - Post-Quantum Crypto",
            "Gerçek Olay": "2022 NIST PQC Seçimi",
        }
    },
    "3E": {
        "achievements_map": {
            "contract_analyzed": "Kontrat analiz edildi",
            "reentrancy_found": "Reentrancy bulundu",
            "funds_stolen": "Fon test edildi",
        },
        "learning_outcomes": [
            "Akıllı kontrat güvenliği",
            "Solidity programlama",
            "Reentrancy açığı",
            "Flash loan saldırıları",
            "Blockchain forensic",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Akıllı kontratları bağımsız denetleyin",
                "✅ Reentrancy guard kullanın",
                "✅ Formal verification yapın",
                "✅ Oracle fiyat manipülasyonuna karşı koruma",
                "✅ Gas limit ve timelock mekanizmaları",
            ],
            "donts": [
                "❌ Denetlenmemiş kontrat deploy etmeyin",
                "❌ Tek oracle'a güvenmeyin",
                "❌ Integer overflow kontrolü yapmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1647 - Smart Contract Exploitation",
            "OWASP": "SC Top 10 - Reentrancy",
            "Gerçek Olay": "2016 The DAO Hack",
        }
    },

    # ============================================
    # SEVİYE 4
    # ============================================
    "4A": {
        "achievements_map": {
            "ai_detection": "AI tespit seviyesi",
            "target_load": "Hedef yükü",
            "target_down": "Hedef çöktü",
        },
        "learning_outcomes": [
            "DDoS saldırı türleri",
            "Botnet yapısı ve yönetimi",
            "Trafik analizi",
            "Anti-DDoS sistemleri",
            "Dayanıklılık stratejileri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Anycast DNS kullanın",
                "✅ Scrubbing center hizmeti alın",
                "✅ CDN ile trafiği dağıtın",
                "✅ Auto-scaling yapılandırın",
                "✅ Rate limiting uygulayın",
            ],
            "donts": [
                "❌ Tek noktadan hizmet vermeyin",
                "❌ DDoS korumasını ihmal etmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1498 - Network Denial of Service",
            "NIST": "SP 800-189 - DDoS Resilience",
            "Gerçek Olay": "2016 Dyn DDoS",
        }
    },
    "4B": {
        "achievements_map": {
            "defenses": "Savunma katmanı",
            "downtime": "Kesinti süresi",
        },
        "learning_outcomes": [
            "Katmanlı DDoS savunması",
            "Yük dengeleme mimarileri",
            "Otomatik ölçeklendirme",
            "Maliyet optimizasyonu",
            "Hizmet sürekliliği",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ En az 4 savunma katmanı oluşturun",
                "✅ Rate limiting + CAPTCHA birlikte kullanın",
                "✅ CDN önbelleğini optimize edin",
                "✅ Otomatik ölçeklendirme politikaları tanımlayın",
                "✅ Hizmet sürekliliği planı hazırlayın",
            ],
            "donts": [
                "❌ Tek savunma katmanına güvenmeyin",
                "❌ Gereksiz ölçeklendirme yapmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1498 - Network Denial of Service",
            "NIST": "SP 800-189 - DDoS Resilience",
            "Gerçek Olay": "2020 AWS DDoS (2.3 Tbps)",
        }
    },
    "4C": {
        "achievements_map": {
            "resolvers": "Açık çözümleyici",
            "target_load": "Hedef yükü",
            "success": "Başarılı",
        },
        "learning_outcomes": [
            "DNS amplifikasyon saldırısı",
            "IP sahtekarlığı (spoofing)",
            "Açık resolver riskleri",
            "DNSSEC önemi",
            "DNS güvenlik en iyi uygulamaları",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Açık DNS çözümleyicileri kapatın",
                "✅ Response Rate Limiting (RRL) aktif edin",
                "✅ DNSSEC kullanın",
                "✅ Anti-spoofing (BCP38) uygulayın",
                "✅ DNS trafiğini izleyin",
            ],
            "donts": [
                "❌ ANY sorgularına izin vermeyin",
                "❌ Zone transfer'i herkese açık bırakmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1498.002 - Reflection Amplification",
            "NIST": "SP 800-81 - DNS Security",
            "Gerçek Olay": "2018 GitHub 1.35 Tbps",
        }
    },
    "4D": {
        "achievements_map": {
            "users": "Eş zamanlı kullanıcı",
            "response_time": "Yanıt süresi",
            "score": "Performans puanı",
        },
        "learning_outcomes": [
            "Kapasite planlaması",
            "Performans metrikleri",
            "Yatay vs dikey ölçeklendirme",
            "Darboğaz analizi",
            "Önbellek stratejileri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Yatay ölçeklendirme (horizontal) tercih edin",
                "✅ CDN kullanın",
                "✅ Cache stratejisi optimize edin",
                "✅ Veritabanı bağlantı havuzu yapılandırın",
                "✅ Düzenli yük testi yapın",
            ],
            "donts": [
                "❌ Dikey ölçeklendirmeye aşırı güvenmeyin",
                "❌ Önbelleği ihmal etmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1499 - Endpoint Denial of Service",
            "NIST": "SP 800-145 - Cloud Computing",
            "Gerçek Olay": "2021 Facebook Outage",
        }
    },
    "4E": {
        "achievements_map": {
            "pops": "PoP sayısı",
            "cache_hit": "Cache hit oranı",
            "latency": "Global gecikme",
        },
        "learning_outcomes": [
            "CDN mimarisi",
            "Edge computing",
            "Anycast yönlendirme",
            "Global trafik yönetimi",
            "Coğrafi yük dağıtımı",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Coğrafi olarak dağıtık PoP'lar kullanın",
                "✅ Cache hit oranını %80+ tutun",
                "✅ Anycast DNS kullanın",
                "✅ Edge sunucularını düzenli güncelleyin",
                "✅ Global monitoring kurun",
            ],
            "donts": [
                "❌ Tek bölgeye bağımlı olmayın",
                "❌ Cache süresini çok kısa tutmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1498 - Network Denial of Service",
            "NIST": "SP 800-145 - Cloud Computing",
            "Gerçek Olay": "2017 Amazon S3 Outage",
        }
    },

    # ============================================
    # SEVİYE 5
    # ============================================
    "5A": {
        "achievements_map": {
            "intel": "İstihbarat toplandı",
            "risk": "Risk seviyesi",
        },
        "learning_outcomes": [
            "OSINT (Açık Kaynak İstihbarat)",
            "Pasif keşif teknikleri",
            "Kurumsal ayak izi",
            "Sosyal medya istihbaratı",
            "OPSEC prensipleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Çalışanlara OPSEC eğitimi verin",
                "✅ Sosyal medya politikaları oluşturun",
                "✅ Kurumsal bilgi paylaşımını minimize edin",
                "✅ LinkedIn profillerini gözden geçirin",
                "✅ İş ilanlarında teknoloji detayı vermeyin",
            ],
            "donts": [
                "❌ Çalışan bilgilerini açık paylaşmayın",
                "❌ Altyapı detaylarını ifşa etmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1592 - Gather Victim Host Information",
            "NIST": "SP 800-53 - Reconnaissance",
            "Gerçek Olay": "2013 Target Breach",
        }
    },
    "5B": {
        "achievements_map": {
            "threats_found": "Tehdit bulundu",
            "false_positives": "Yanlış pozitif",
        },
        "learning_outcomes": [
            "Tehdit avı metodolojisi",
            "Olay korelasyonu",
            "PowerShell log analizi",
            "Anormal davranış tespiti",
            "Threat hunting araçları",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ PowerShell loglarını merkezi toplayın",
                "✅ Anormal saat aktivitelerini izleyin",
                "✅ SIEM'de korelasyon kuralları yazın",
                "✅ EDR ve NDR birlikte kullanın",
                "✅ Tehdit avı ekibi kurun",
            ],
            "donts": [
                "❌ Log toplamayı ihmal etmeyin",
                "❌ Kritik olayları görmezden gelmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1059.001 - PowerShell",
            "NIST": "SP 800-61 - Incident Handling",
            "Gerçek Olay": "2020 SolarWinds",
        }
    },
    "5C": {
        "achievements_map": {
            "iocs_found": "IoC bulundu",
            "c2_found": "C2 bulundu",
            "report_done": "Rapor oluşturuldu",
        },
        "learning_outcomes": [
            "Malware analizi metodolojisi",
            "Statik analiz teknikleri",
            "Dinamik analiz (sandbox)",
            "IoC (Indicators of Compromise)",
            "YARA kuralları",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Sandbox ortamı kurun",
                "✅ YARA kuralları yazın",
                "✅ EDR çözümü kullanın",
                "✅ IoC'leri tehdit istihbaratına ekleyin",
                "✅ Zararlı yazılım analiz ekibi kurun",
            ],
            "donts": [
                "❌ Şüpheli dosyaları gerçek sistemde çalıştırmayın",
                "❌ Analiz ortamını internete bağlamayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1027 - Obfuscated Files",
            "NIST": "SP 800-83 - Malware Guide",
            "Gerçek Olay": "2010 Stuxnet",
        }
    },
    "5D": {
        "achievements_map": {
            "access_level": "Yetki seviyesi",
            "root_obtained": "Root yetkisi",
            "edr_risk": "EDR riski",
        },
        "learning_outcomes": [
            "Yetki yükseltme teknikleri",
            "SUID binary analizi",
            "Servis yanlış yapılandırmaları",
            "Token manipülasyonu",
            "EDR atlatma",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Least privilege prensibi uygulayın",
                "✅ SUID binary'leri düzenli denetleyin",
                "✅ Kernel yamalarını güncel tutun",
                "✅ EDR çözümü kullanın",
                "✅ Servis hesaplarını minimum yetkiyle yapılandırın",
            ],
            "donts": [
                "❌ Gereksiz SUID binary bırakmayın",
                "❌ Sudo'yu şifresiz yapılandırmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1068 - Exploitation for Privilege Escalation",
            "NIST": "SP 800-53 - Access Control",
            "Gerçek Olay": "2021 PrintNightmare",
        }
    },
    "5E": {
        "achievements_map": {
            "logs_cleaned": "Log temizlendi",
            "forensic_risk": "Forensic riski",
        },
        "learning_outcomes": [
            "Anti-forensic teknikleri",
            "Log yönetimi",
            "Timestamp manipülasyonu",
            "Forensic bütünlük",
            "Zincir koruma (chain of custody)",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Logları merkezi ve değiştirilemez ortamda saklayın",
                "✅ Log bütünlüğünü hash ile doğrulayın",
                "✅ SIEM'e gerçek zamanlı gönderin",
                "✅ Değiştirilemez (immutable) storage kullanın",
                "✅ Yetkisiz log değişikliklerini izleyin",
            ],
            "donts": [
                "❌ Logları sadece yerel sistemde tutmayın",
                "❌ Log silme yetkisini herkese vermeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1070 - Indicator Removal",
            "NIST": "SP 800-86 - Forensics",
            "Gerçek Olay": "2013 Snowden",
        }
    },

    # ============================================
    # SEVİYE 6
    # ============================================
    "6A": {
        "achievements_map": {
            "phases_complete": "Aşama tamamlandı",
            "risk": "Risk seviyesi",
        },
        "learning_outcomes": [
            "MITRE ATT&CK kill chain",
            "APT operasyonel metodoloji",
            "Her aşamada farklı TTP",
            "Kalıcılık mekanizmaları",
            "C2 kanal yönetimi",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Kill chain'in her aşamasında savunma katmanı oluşturun",
                "✅ Behavioral analytics kullanın",
                "✅ Threat hunting ekibi kurun",
                "✅ EDR + NDR + SIEM entegrasyonu yapın",
                "✅ Tehdit istihbaratı beslemelerini kullanın",
            ],
            "donts": [
                "❌ Sadece perimeter savunmasına güvenmeyin",
                "❌ Bilinen IoC'lere bağımlı kalmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "Full Kill Chain",
            "NIST": "SP 800-61 - Incident Handling",
            "Gerçek Olay": "2020 SolarWinds",
        }
    },
    "6B": {
        "achievements_map": {
            "apt_phase": "APT aşaması",
            "contained": "İzole edildi",
            "detected_phases": "Tespit edilen aşama",
        },
        "learning_outcomes": [
            "APT tespit metodolojisi",
            "Threat hunting",
            "Olay müdahale süreci",
            "Forensic analiz",
            "Kriz yönetimi",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Sürekli tehdit avı yapın",
                "✅ İzolasyon prosedürleri hazırlayın",
                "✅ Forensic analiz yeteneği kurun",
                "✅ Kriz iletişim planı yapın",
                "✅ Üçüncü taraf uzmanlarla işbirliği",
            ],
            "donts": [
                "❌ Panik kararlar almayın",
                "❌ Saldırganı uyarmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1003 - OS Credential Dumping",
            "NIST": "SP 800-61 - Incident Handling",
            "Gerçek Olay": "2021 Colonial Pipeline",
        }
    },
    "6C": {
        "achievements_map": {
            "current_step": "Adım",
            "position": "Pozisyon",
            "risk": "Risk",
        },
        "learning_outcomes": [
            "Yanal hareket teknikleri",
            "Ağ segmentasyonu",
            "Pass-the-Hash",
            "Kerberos bilet manipülasyonu",
            "Lateral movement tespiti",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Mikro segmentasyon yapın",
                "✅ Tiered admin modeli uygulayın",
                "✅ LAPS (Local Admin Password Solution) kullanın",
                "✅ Yanal hareket tespiti için IDS/IPS",
                "✅ Privileged access management (PAM)",
            ],
            "donts": [
                "❌ Aynı şifreyi birden fazla sistemde kullanmayın",
                "❌ Domain admin hesaplarını normal işlerde kullanmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1021 - Remote Services",
            "NIST": "SP 800-125B - Segmentation",
            "Gerçek Olay": "2017 NotPetya",
        }
    },
    "6D": {
        "achievements_map": {
            "data_exfiltrated": "Veri sızdırıldı",
            "dlp_risk": "DLP riski",
        },
        "learning_outcomes": [
            "Veri sızdırma teknikleri",
            "DLP sistemlerinin çalışması",
            "Egress filtering",
            "Steganografi",
            "Kanal gizleme",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ DLP çözümü kurun",
                "✅ Egress trafiği filtreleyin",
                "✅ CASB (Cloud Access Security Broker) kullanın",
                "✅ Veri sınıflandırması yapın",
                "✅ Anormal çıkış trafiğini izleyin",
            ],
            "donts": [
                "❌ Tüm outbound trafiğe izin vermeyin",
                "❌ Hassas veriyi şifresiz transfer etmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1041 - Exfiltration Over C2",
            "NIST": "SP 800-53 - DLP Controls",
            "Gerçek Olay": "2015 OPM Breach",
        }
    },
    "6E": {
        "achievements_map": {
            "ot_security": "OT güvenliği",
            "it_security": "IT güvenliği",
            "process_stable": "Proses stabil",
        },
        "learning_outcomes": [
            "OT/ICS güvenliği",
            "IT-OT segmentasyonu",
            "PLC/DCS güvenliği",
            "Kritik altyapı koruması",
            "Endüstriyel protokoller",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ IT ve OT ağlarını ayırın",
                "✅ OT için özel IDS kullanın",
                "✅ PLC/DCS erişim kontrolü yapın",
                "✅ Fiziksel güvenlik güçlendirin",
                "✅ Acil durum prosedürleri hazırlayın",
            ],
            "donts": [
                "❌ OT ağını internete bağlamayın",
                "❌ Yamasız OT cihazı bırakmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1489 - Service Stop",
            "NIST": "SP 800-82 - ICS Security",
            "Gerçek Olay": "2021 Colonial Pipeline",
        }
    },

    # ============================================
    # SEVİYE 7
    # ============================================
    "7A": {
        "achievements_map": {
            "tables_found": "Tablo bulundu",
            "columns_found": "Kolon bulundu",
            "hash_cracked": "Hash kırıldı",
            "data_exported": "Veri sızdırıldı",
        },
        "learning_outcomes": [
            "SQL enjeksiyonu mekanizması",
            "UNION tabanlı sorgular",
            "Information schema kullanımı",
            "Hash tanıma ve kırma",
            "Veri sızdırma teknikleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Parametreli sorgular (Prepared Statements) kullanın",
                "✅ ORM (SQLAlchemy, Entity Framework) tercih edin",
                "✅ Input validation + whitelist yaklaşımı",
                "✅ Veritabanı kullanıcısına minimum yetki verin",
                "✅ WAF kuralı: SQL anahtar kelime filtreleme",
            ],
            "donts": [
                "❌ String birleştirme ile sorgu yazmayın",
                "❌ Detaylı hata mesajlarını kullanıcıya gösterin",
                "❌ Aşırı yetkili DB kullanıcısı (root) kullanmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1190 - Exploit Public-Facing Application",
            "OWASP": "A03:2021 - Injection",
            "CWE": "CWE-89 - SQL Injection",
            "Gerçek Olay": "2017 Equifax Breach",
        }
    },
    "7B": {
        "achievements_map": {
            "rules": "Kural eklendi",
            "attacks_blocked": "Saldırı engellendi",
            "false_positives": "Yanlış pozitif",
        },
        "learning_outcomes": [
            "WAF kural yazma",
            "Virtual patching",
            "OWASP Top 10",
            "Güvenli kod standartları",
            "WAF performansı",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ OWASP CRS (Core Rule Set) kullanın",
                "✅ Sanal yama (virtual patching) uygulayın",
                "✅ Kuralları uygulamaya özel uyarlayın",
                "✅ WAF loglarını analiz edin",
                "✅ Kural güncellemelerini takip edin",
            ],
            "donts": [
                "❌ Jenerik kurallarla yetinmeyin",
                "❌ WAF'ı tek savunma olarak görmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1562 - Impair Defenses",
            "OWASP": "Top 10 - All Categories",
            "Gerçek Olay": "2019 Capital One",
        }
    },
    "7C": {
        "achievements_map": {
            "csp_bypassed": "CSP atlatıldı",
            "cookie_stolen": "Cookie çalındı",
        },
        "learning_outcomes": [
            "XSS türleri",
            "Content Security Policy (CSP)",
            "Cookie güvenliği",
            "DOM manipülasyonu",
            "Client-side güvenlik",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Content Security Policy (CSP) uygulayın",
                "✅ Output encoding yapın",
                "✅ HttpOnly ve Secure cookie flag'leri kullanın",
                "✅ Input sanitization yapın",
                "✅ Framework'lerin otomatik escaping özelliklerini kullanın",
            ],
            "donts": [
                "❌ innerHTML kullanmayın",
                "❌ eval() fonksiyonunu kullanmayın",
                "❌ Cookie'leri HttpOnly olmadan kullanmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1189 - Drive-by Compromise",
            "OWASP": "A03:2021 - XSS",
            "CWE": "CWE-79 - XSS",
            "Gerçek Olay": "2005 MySpace Samy Worm",
        }
    },
    "7D": {
        "achievements_map": {
            "commands_run": "Komut çalıştırıldı",
            "shell_obtained": "Shell elde edildi",
        },
        "learning_outcomes": [
            "Komut enjeksiyonu mekanizması",
            "Shell metakarakterleri",
            "Reverse shell",
            "Blind injection",
            "Input validation",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Input validation ve whitelist kullanın",
                "✅ Sistem çağrılarını minimize edin",
                "✅ Sandbox ortamı kullanın",
                "✅ Least privilege prensibi",
                "✅ WAF kuralı: shell metakarakter filtreleme",
            ],
            "donts": [
                "❌ Kullanıcı girdisini doğrudan shell'e geçirmeyin",
                "❌ os.system() veya eval() kullanmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1059 - Command and Scripting Interpreter",
            "OWASP": "A03:2021 - Injection",
            "CWE": "CWE-78 - OS Command Injection",
            "Gerçek Olay": "2014 Shellshock",
        }
    },
    "7E": {
        "achievements_map": {
            "domain_mapped": "Domain haritalandı",
            "kerberoast_done": "Kerberoasting yapıldı",
            "dc_compromised": "DC ele geçirildi",
        },
        "learning_outcomes": [
            "LDAP protokolü",
            "Active Directory güvenliği",
            "Kerberoasting saldırısı",
            "DCSync",
            "Golden Ticket",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Tiered admin modeli uygulayın",
                "✅ Servis hesaplarını güçlü şifrelerle koruyun",
                "✅ Kerberos bilet sürelerini kısaltın",
                "✅ LAPS (Local Admin Password Solution) kullanın",
                "✅ AD denetim loglarını SIEM'e gönderin",
            ],
            "donts": [
                "❌ Servis hesaplarına zayıf şifre koymayın",
                "❌ Domain admin hesaplarını normal işlerde kullanmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1558 - Steal or Forge Kerberos Tickets",
            "NIST": "SP 800-53 - Access Control",
            "Gerçek Olay": "2020 SolarWinds",
        }
    },

    # ============================================
    # SEVİYE 8
    # ============================================
    "8A": {
        "achievements_map": {
            "static_done": "Statik analiz",
            "breakpoints_set": "Breakpoint",
            "algorithm_found": "Algoritma bulundu",
        },
        "learning_outcomes": [
            "Tersine mühendislik metodolojisi",
            "Assembly dili",
            "Debugger kullanımı",
            "Anti-debugging teknikleri",
            "Algoritma analizi",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Kod obfuscation kullanın",
                "✅ Anti-tamper mekanizmaları ekleyin",
                "✅ Code signing uygulayın",
                "✅ Anti-debugging teknikleri kullanın",
                "✅ Lisans doğrulama mekanizmaları ekleyin",
            ],
            "donts": [
                "❌ Hassas algoritmaları açıkça saklamayın",
                "❌ String olarak şifre saklamayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1027 - Obfuscated Files",
            "NIST": "SP 800-83 - Malware Guide",
            "Gerçek Olay": "2010 Stuxnet",
        }
    },
    "8B": {
        "achievements_map": {
            "iocs": "IoC bulundu",
            "c2_found": "C2 bulundu",
            "report_done": "Rapor oluşturuldu",
        },
        "learning_outcomes": [
            "Malware analizi metodolojisi",
            "PE header analizi",
            "Sandbox kullanımı",
            "C2 deşifre",
            "Threat report",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Sandbox ortamı kurun",
                "✅ YARA kuralları yazın",
                "✅ EDR çözümü kullanın",
                "✅ IoC'leri threat intel'e ekleyin",
                "✅ Zararlı yazılım analiz ekibi kurun",
            ],
            "donts": [
                "❌ Şüpheli dosyaları gerçek sistemde çalıştırmayın",
                "❌ Analiz ortamını internete bağlamayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1055 - Process Injection",
            "NIST": "SP 800-83 - Malware Guide",
            "Gerçek Olay": "2017 NotPetya",
        }
    },
    "8C": {
        "achievements_map": {
            "layers_unpacked": "Katman çözüldü",
            "unpacked": "Unpacking tamamlandı",
            "oep_found": "OEP bulundu",
        },
        "learning_outcomes": [
            "Packer teknolojileri",
            "Entropi analizi",
            "OEP (Original Entry Point)",
            "IAT rekonstrüksiyon",
            "Memory forensics",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Custom packer kullanın",
                "✅ Anti-unpacking teknikleri uygulayın",
                "✅ Multiple layer obfuscation",
                "✅ Runtime integrity check",
                "✅ Anti-dump koruması",
            ],
            "donts": [
                "❌ Standart packer'lar yeterli değildir",
                "❌ Tek katmanlı korumaya güvenmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1027 - Obfuscated Files",
            "NIST": "SP 800-83 - Malware Guide",
            "Gerçek Olay": "2014 Gameover Zeus",
        }
    },
    "8D": {
        "achievements_map": {
            "firmware_dumped": "Firmware dump",
            "rootkit_found": "Rootkit bulundu",
            "cleaned": "Temizlendi",
        },
        "learning_outcomes": [
            "Firmware güvenliği",
            "Secure Boot",
            "UEFI/BIOS güvenliği",
            "Firmware diffing",
            "Boot süreci güvenliği",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Secure Boot aktif edin",
                "✅ TPM (Trusted Platform Module) kullanın",
                "✅ Firmware imzalama uygulayın",
                "✅ Düzenli firmware güncellemesi",
                "✅ Firmware bütünlük kontrolü",
            ],
            "donts": [
                "❌ İmzasız firmware yüklemeyin",
                "❌ Fiziksel erişime izin vermeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1542 - Pre-OS Boot",
            "NIST": "SP 800-147 - BIOS Protection",
            "Gerçek Olay": "2015 Hacking Team UEFI",
        }
    },
    "8E": {
        "achievements_map": {
            "syscall_hooks": "Hook bulundu",
            "hidden_procs": "Gizli proses",
            "cleaned": "Rootkit kaldırıldı",
        },
        "learning_outcomes": [
            "Kernel modülü yapısı",
            "Syscall tablosu",
            "Hidden process detection",
            "Memory forensics",
            "Rootkit kaldırma",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Kernel modül imzalaması",
                "✅ Loadable kernel module (LKM) kısıtlaması",
                "✅ Secured Boot",
                "✅ Runtime kernel integrity check",
                "✅ Memory forensics araçları",
            ],
            "donts": [
                "❌ Gereksiz kernel modülüne izin vermeyin",
                "❌ Kernel debug arayüzünü açık bırakmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1547 - Boot or Logon Autostart",
            "NIST": "SP 800-83 - Malware Guide",
            "Gerçek Olay": "2010 Stuxnet",
        }
    },

    # ============================================
    # SEVİYE 9
    # ============================================
    "9A": {
        "achievements_map": {
            "emails_sent": "E-posta gönderildi",
            "credentials_stolen": "Kimlik bilgisi çalındı",
            "detected": "Tespit edildi",
        },
        "learning_outcomes": [
            "Phishing kampanya yapısı",
            "Psikolojik tetikleyiciler",
            "E-posta sosyal mühendisliği",
            "Landing page tasarımı",
            "Kampanya metrikleri",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ SPF, DKIM, DMARC uygulayın",
                "✅ E-posta güvenlik ağ geçidi kullanın",
                "✅ Çalışanlara düzenli eğitim",
                "✅ Şüpheli e-posta raporlama sistemi",
                "✅ Simülasyon testleri yapın",
                "✅ MFA zorunlu kılın",
            ],
            "donts": [
                "❌ E-posta eklerini doğrulamadan açmayın",
                "❌ Şüpheli linklere tıklamayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1566 - Phishing",
            "NIST": "SP 800-50 - Awareness Training",
            "Gerçek Olay": "2016 DNC Hack",
        }
    },
    "9B": {
        "achievements_map": {
            "training_done": "Eğitim verildi",
            "awareness_level": "Farkındalık seviyesi",
            "phishing_rate": "Phishing oranı",
        },
        "learning_outcomes": [
            "Farkındalık eğitimi tasarımı",
            "Yetişkin öğrenme prensipleri",
            "Davranış değişikliği psikolojisi",
            "Güvenlik kültürü oluşturma",
            "Metrik ölçümü",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Sürekli eğitim programı",
                "✅ Simülasyon testleri",
                "✅ Olumlu pekiştirme",
                "✅ Rol bazlı eğitim",
                "✅ Kültürel değişim liderliği",
            ],
            "donts": [
                "❌ Suçlayıcı yaklaşım sergilemeyin",
                "❌ Yıllık tek seferlik eğitimle yetinmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1566 - Phishing",
            "NIST": "SP 800-50 - Awareness Training",
            "Gerçek Olay": "2017 Google/Facebook BEC",
        }
    },
    "9C": {
        "achievements_map": {
            "areas_accessed": "Alan erişildi",
            "target_reached": "Hedefe ulaşıldı",
        },
        "learning_outcomes": [
            "Fiziksel güvenlik prensipleri",
            "Tailgating tekniği",
            "Pretexting",
            "Erişim kontrol sistemleri",
            "Bina güvenliği",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Erişim kontrol sistemleri (kart, biyometrik)",
                "✅ Güvenlik kamerası izleme",
                "✅ Personel eğitimi",
                "✅ Ziyaretçi prosedürleri",
                "✅ Fiziksel izleme turları",
            ],
            "donts": [
                "❌ Kapıyı açık bırakmayın",
                "❌ Kimlik kontrolü yapmadan içeri almayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1592 - Gather Victim Host Information",
            "NIST": "SP 800-53 - Physical Security",
            "Gerçek Olay": "2013 Target Physical Breach",
        }
    },
    "9D": {
        "achievements_map": {
            "calls_made": "Arama yapıldı",
            "info_obtained": "Bilgi alındı",
            "detected": "Tespit edildi",
        },
        "learning_outcomes": [
            "Vishing (telefon dolandırıcılığı)",
            "Ses tonu analizi",
            "Sosyal mühendislik",
            "Pretexting",
            "Kimlik doğrulama",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Geri arama prosedürleri",
                "✅ Çalışan eğitimi",
                "✅ Kimlik doğrulama süreçleri",
                "✅ Ses analizi sistemleri",
                "✅ Yetki matrisi",
            ],
            "donts": [
                "❌ Telefonda kişisel bilgi vermeyin",
                "❌ Şifre sıfırlama taleplerini doğrulamadan yapmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1598 - Phishing for Information",
            "NIST": "SP 800-50 - Awareness Training",
            "Gerçek Olay": "2020 Twitter Hack",
        }
    },
    "9E": {
        "achievements_map": {
            "completed": "Hedef tamamlandı",
            "risk": "Risk seviyesi",
        },
        "learning_outcomes": [
            "Pretexting metodolojisi",
            "Çoklu hedef yönetimi",
            "Tutarlılık analizi",
            "Farklı departmanlara yaklaşım",
            "İnsan davranışı tahmini",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Zero trust yaklaşımı",
                "✅ Departmanlar arası iletişim",
                "✅ Doğrulama kültürü",
                "✅ Şüpheli aktiviteleri bildirme",
                "✅ OPSEC eğitimi",
            ],
            "donts": [
                "❌ Otoriteye körü körüne güvenmeyin",
                "❌ Aciliyet baskısına kapılmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1589 - Gather Victim Identity Information",
            "NIST": "SP 800-50 - Awareness Training",
            "Gerçek Olay": "2020 Twitter Hack",
        }
    },

    # ============================================
    # SEVİYE 10
    # ============================================
    "10A": {
        "achievements_map": {
            "phases": "Aşama tamamlandı",
            "score": "Operasyon puanı",
        },
        "learning_outcomes": [
            "Full-scope kırmızı takım operasyonu",
            "Stratejik karar verme",
            "Adaptif savunmaya karşı yaratıcılık",
            "7 aşamalı kill chain",
            "Operasyonel güvenlik",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Kapsamlı savunma stratejisi",
                "✅ Sürekli tehdit avı",
                "✅ Kırmızı/mavi takım işbirliği",
                "✅ Sürekli iyileştirme",
                "✅ Üst yönetim desteği",
            ],
            "donts": [
                "❌ Sadece compliance odaklı olmayın",
                "❌ Statik savunma ile yetinmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "Full Kill Chain",
            "NIST": "CSF 2.0 - All Functions",
            "Gerçek Olay": "2020 SolarWinds",
        }
    },
    "10B": {
        "achievements_map": {
            "defenses": "Savunma katmanı",
            "contained": "İzole edildi",
            "apt_phase": "APT aşaması",
        },
        "learning_outcomes": [
            "Kapsamlı mavi takım savunması",
            "SIEM + SOAR + EDR entegrasyonu",
            "Kriz yönetimi",
            "Ekip koordinasyonu",
            "Bütüncül güvenlik",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ En az 5 savunma katmanı oluşturun",
                "✅ Otomasyon ile hız artırın",
                "✅ Olay müdahale playbook'ları",
                "✅ Kriz iletişim planı",
                "✅ Sürekli eğitim ve tatbikat",
            ],
            "donts": [
                "❌ Tek katmanlı savunmaya güvenmeyin",
                "❌ Kriz anında panik yapmayın",
            ]
        },
        "references": {
            "MITRE ATT&CK": "Full Kill Chain",
            "NIST": "CSF 2.0 - All Functions",
            "Gerçek Olay": "2021 Colonial Pipeline",
        }
    },
    "10C": {
        "achievements_map": {
            "maturity": "Olgunluk seviyesi",
            "improvements": "İyileştirme",
            "tests_run": "Test çalıştırıldı",
        },
        "learning_outcomes": [
            "Mor takım metodolojisi",
            "Detection engineering",
            "Güvenlik metrikleri",
            "Sürekli iyileştirme",
            "Güvenlik olgunluk modeli",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Detection kurallarını sürekli güncelleyin",
                "✅ Log retention süresini artırın",
                "✅ Alert tuning yapın",
                "✅ Playbook oluşturun",
                "✅ Otomasyon ekleyin",
            ],
            "donts": [
                "❌ Statik kurallarla yetinmeyin",
                "❌ Metrikleri ölçmeyi ihmal etmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "Purple Teaming",
            "NIST": "CSF 2.0 - Continuous Improvement",
            "Gerçek Olay": "MITRE Engenuity Evaluations",
        }
    },
    "10D": {
        "achievements_map": {
            "fuzzing_done": "Fuzzing yapıldı",
            "crash_analyzed": "Crash analiz edildi",
            "exploit_developed": "Exploit geliştirildi",
        },
        "learning_outcomes": [
            "Zero-day araştırma metodolojisi",
            "Fuzzing teknikleri",
            "Crash analizi",
            "Root cause analysis",
            "Exploit geliştirme",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Bug bounty programı kurun",
                "✅ Otomatik yama sistemi",
                "✅ Geçici önlemler (mitigation)",
                "✅ Yazılım güvenliği yaşam döngüsü (SSDLC)",
                "✅ Sürekli fuzzing testleri",
            ],
            "donts": [
                "❌ Zero-day'leri görmezden gelmeyin",
                "❌ Yama sürecini geciktirmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "T1587 - Develop Capabilities",
            "NIST": "SP 800-40 - Patch Management",
            "Gerçek Olay": "2021 Log4Shell",
        }
    },
    "10E": {
        "achievements_map": {
            "crisis_level": "Kriz seviyesi",
            "sectors": "Sektör durumu",
        },
        "learning_outcomes": [
            "Ulusal siber savunma",
            "Çok paydaşlı koordinasyon",
            "Kritik sektör koruması",
            "Kriz yönetimi",
            "Uluslararası işbirliği",
        ],
        "defense_recommendations": {
            "dos": [
                "✅ Ulusal CERT (USOM) ile işbirliği",
                "✅ Sektörel ISAC'ler kurun",
                "✅ Kamu-özel işbirliği",
                "✅ Uluslararası bilgi paylaşımı",
                "✅ Kriz tatbikatları",
            ],
            "donts": [
                "❌ Sektörler arası iletişimi kesmeyin",
                "❌ Uluslararası işbirliğini ihmal etmeyin",
            ]
        },
        "references": {
            "MITRE ATT&CK": "Full Kill Chain",
            "NIST": "CSF 2.0 - All Functions",
            "Gerçek Olay": "2022 Ukraine Cyber Attacks",
        }
    },
}

# ============================================
# MAVİ TAKIM İKİZLERİ İÇİN RAPOR VERİLERİ
# ============================================

_TWIN_MAPPING = {
    "1A-DEF": "1A", "1C-DEF": "1C", "1E-DEF": "1E",
    "2A-DEF": "2A", "2C-DEF": "2C",
    "3A-DEF": "3A", "3E-DEF": "3E",
    "4A-DEF": "4A", "4C-DEF": "4C",
    "5A-DEF": "5A", "5D-DEF": "5D",
    "6A-DEF": "6A", "7A-DEF": "7A",
    "9A-DEF": "9A", "10A-DEF": "10A",
}

_TWIN_TITLES = {
    "1A-DEF": "1A-DEF: Port Tarama Tespit Sistemi",
    "1C-DEF": "1C-DEF: Honeypot Yönetimi",
    "1E-DEF": "1E-DEF: Kablosuz Ağ Savunması",
    "2A-DEF": "2A-DEF: IDS Kural Yazma",
    "2C-DEF": "2C-DEF: WAF Yapılandırma",
    "3A-DEF": "3A-DEF: VPN Güçlendirme",
    "3E-DEF": "3E-DEF: Akıllı Kontrat Denetimi",
    "4A-DEF": "4A-DEF: DDoS Azaltma Stratejisi",
    "4C-DEF": "4C-DEF: DNS Sunucu Sertleştirme",
    "5A-DEF": "5A-DEF: Kurumsal Ayak İzi Yönetimi",
    "5D-DEF": "5D-DEF: Yetki Sertleştirme",
    "6A-DEF": "6A-DEF: APT Tespit ve Müdahale",
    "7A-DEF": "7A-DEF: SQLi Savunması - Kod Denetimi",
    "9A-DEF": "9A-DEF: Phishing Tespit ve Savunma",
    "10A-DEF": "10A-DEF: Kırmızı Takım Savunması",
}

# İkizler için özelleştirilmiş öğrenme çıktıları
_TWIN_LEARNING = {
    "1A-DEF": ["Port tarama tespiti", "IDS/IPS kural yazma", "Firewall yapılandırma", "Baseline davranış analizi"],
    "1C-DEF": ["Honeypot yönetimi", "Aldatma teknolojileri", "Tehdit istihbaratı toplama"],
    "1E-DEF": ["Kablosuz IDS (WIDS) yönetimi", "802.1X kimlik doğrulama", "Rogue AP tespiti"],
    "2A-DEF": ["IDS kural yazma", "İmza analizi", "Yanlış pozitif yönetimi"],
    "2C-DEF": ["WAF kural yönetimi", "Sanal yama (virtual patching)", "OWASP CRS"],
    "3A-DEF": ["VPN güçlendirme", "Kriptografik algoritma seçimi", "Sertifika yönetimi"],
    "3E-DEF": ["Akıllı kontrat denetimi", "Formal verification", "Gas optimizasyonu"],
    "4A-DEF": ["DDoS azaltma stratejisi", "Anycast yapılandırma", "Scrubbing center"],
    "4C-DEF": ["DNS sunucu sertleştirme", "DNSSEC yapılandırma", "Response Rate Limiting"],
    "5A-DEF": ["Kurumsal ayak izi yönetimi", "OSINT savunması", "OPSEC politikaları"],
    "5D-DEF": ["Sistem sertleştirme", "Least privilege uygulaması", "SUID binary denetimi"],
    "6A-DEF": ["APT tespit metodolojisi", "Kill chain savunması", "Threat hunting"],
    "7A-DEF": [
        "SQL enjeksiyonunu tespit etme",
        "Güvenli kod denetimi metodolojisi",
        "Parametreli sorgular ve ORM kullanımı",
        "Input validation teknikleri",
        "WAF kural yazma",
        "OWASP A03:2021 kapsamında korunma",
    ],
    "9A-DEF": [
        "Phishing e-postalarını tespit etme",
        "SPF, DKIM, DMARC yapılandırması",
        "Çalışan farkındalık eğitimi tasarımı",
        "Simülasyon testleri yapma",
        "Olay raporlama prosedürleri",
    ],
    "10A-DEF": ["Full-scope savunma stratejisi", "Kriz yönetimi", "Mavi takım koordinasyonu"],
}

# İkizleri kaynak verilerinden türet
for twin_id, source_id in _TWIN_MAPPING.items():
    if source_id in SCENARIO_REPORTS:
        import copy
        source = copy.deepcopy(SCENARIO_REPORTS[source_id])
        source['is_twin'] = True
        source['source_scenario'] = source_id
        source['twin_title'] = _TWIN_TITLES.get(twin_id, twin_id)
        if twin_id in _TWIN_LEARNING:
            source['learning_outcomes'] = _TWIN_LEARNING[twin_id]
        SCENARIO_REPORTS[twin_id] = source
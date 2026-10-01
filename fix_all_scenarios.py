"""
ALL_SCENARIOS Sözlüğüne 5A-10E Tanımlarını Ekle
================================================
Bu script, app.py'daki ALL_SCENARIOS sözlüğüne eksik olan
Seviye 5-10 senaryo tanımlarını otomatik ekler.
"""

import re
import shutil
from datetime import datetime

# ============================================
# 30 SENARYO TANIMI (5A - 10E)
# ============================================

NEW_SCENARIOS = '''

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

'''

# ============================================
# DÜZELTME İŞLEMİ
# ============================================

def fix_all_scenarios():
    """ALL_SCENARIOS sözlüğüne 5A-10E ekler."""
    
    app_file = 'app.py'
    
    print("=" * 70)
    print("ALL_SCENARIOS DÜZELTME ARACI")
    print("=" * 70)
    
    # 1. Yedek al
    backup_name = f"app.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy(app_file, backup_name)
    print(f"✅ Yedek alındı: {backup_name}")
    
    # 2. app.py oku
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📄 app.py okundu: {len(content)} karakter")
    
    # 3. Mevcut senaryoları say
    existing = re.findall(r'ALL_SCENARIOS\["(\d+[A-E])"\]\s*=', content)
    print(f"🔍 Mevcut senaryolar: {len(existing)}")
    
    # 4. Zaten ekli mi kontrol
    if 'ALL_SCENARIOS["5A"]' in content:
        print("⚠️  5A zaten mevcut, işlem atlanıyor.")
        return False
    
    # 5. ALL_SCENARIOS["4E"] tanımının sonunu bul
    # Pattern: ALL_SCENARIOS["4E"] = {...}
    pattern = r'(ALL_SCENARIOS\["4E"\]\s*=\s*\{.*?\n\})'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("❌ ALL_SCENARIOS[\"4E\"] tanımı bulunamadı!")
        return False
    
    print(f"🔍 ALL_SCENARIOS[\"4E\"] bulundu")
    
    # 6. Yeni senaryoları 4E'den sonra ekle
    insert_pos = match.end()
    new_content = content[:insert_pos] + NEW_SCENARIOS + content[insert_pos:]
    
    # 7. Kaydet
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ app.py güncellendi: {len(new_content)} karakter")
    
    # 8. Doğrulama
    with open(app_file, 'r', encoding='utf-8') as f:
        verify_content = f.read()
    
    new_scenarios = re.findall(r'ALL_SCENARIOS\["(\d+[A-E])"\]\s*=', verify_content)
    
    print()
    print("=" * 70)
    print("DOĞRULAMA")
    print("=" * 70)
    print(f"Toplam senaryo: {len(new_scenarios)}")
    print()
    
    for level in range(1, 11):
        level_scenarios = sorted([m for m in new_scenarios if m.startswith(str(level))])
        if len(level_scenarios) >= 5:
            print(f"✅ Seviye {level:2d}: {len(level_scenarios)} senaryo")
        elif level_scenarios:
            print(f"⚠️  Seviye {level:2d}: {len(level_scenarios)} senaryo (EKSİK)")
        else:
            print(f"❌ Seviye {level:2d}: YOK")
    
    print()
    if len(new_scenarios) >= 50:
        print("🎉 TAMAMLANDI! Tüm 50 senaryo hazır.")
        print()
        print("📌 Sonraki adımlar:")
        print("   1. Streamlit'i durdurun (Ctrl+C)")
        print("   2. Yeniden başlatın: streamlit run app.py --server.port 8502")
        print("   3. Tarayıcıda hard refresh: Ctrl+Shift+R")
        print("   4. Seviye 5-10 senaryoları test edin")
    else:
        print(f"⚠️  Toplam {len(new_scenarios)} senaryo var. 50 olmalı.")
    
    return True


if __name__ == "__main__":
    fix_all_scenarios()
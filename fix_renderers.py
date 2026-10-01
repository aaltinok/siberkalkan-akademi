"""
SiberKalkan Akademi - SCENARIO_RENDERERS Otomatik Düzeltme
============================================================
Bu script, app.py'daki SCENARIO_RENDERERS sözlüğünü
65 senaryonun tamamını içerecek şekilde düzeltir.
"""

import re
import shutil
from datetime import datetime

# ============================================
# DOĞRU SÖZLÜK (65 senaryo)
# ============================================

CORRECT_RENDERERS = '''SCENARIO_RENDERERS = {
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
}'''

# ============================================
# DÜZELTME İŞLEMİ
# ============================================

def fix_renderers():
    """SCENARIO_RENDERERS sözlüğünü düzeltir."""
    
    app_file = 'app.py'
    
    print("=" * 60)
    print("SCENARIO_RENDERERS DÜZELTME ARACI")
    print("=" * 60)
    
    # 1. Yedek al
    backup_name = f"app.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy(app_file, backup_name)
    print(f"✅ Yedek alındı: {backup_name}")
    
    # 2. app.py oku
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📄 app.py okundu ({len(content)} karakter)")
    
    # 3. SCENARIO_RENDERERS bloğunu bul
    # Pattern: SCENARIO_RENDERERS = { ... }
    pattern = r'SCENARIO_RENDERERS\s*=\s*\{[^{}]*?\n\}'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("❌ SCENARIO_RENDERERS bloğu bulunamadı!")
        print("   Lütfen app.py'da 'SCENARIO_RENDERERS = {' yazısının olduğundan emin olun.")
        return False
    
    old_block = match.group()
    old_lines = old_block.count('\n')
    print(f"🔍 Eski blok bulundu: {old_lines} satır")
    
    # 4. Yeni blok ile değiştir
    new_content = content[:match.start()] + CORRECT_RENDERERS + content[match.end():]
    
    # 5. Kaydet
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    new_lines = CORRECT_RENDERERS.count('\n')
    print(f"✅ Yeni blok yazıldı: {new_lines} satır")
    print(f"✅ app.py güncellendi ({len(new_content)} karakter)")
    
    # 6. Doğrulama
    with open(app_file, 'r', encoding='utf-8') as f:
        verify_content = f.read()
    
    checks = [
        ('"5A": render_5A', '5A'),
        ('"5B": render_5B', '5B'),
        ('"5C": render_5C', '5C'),
        ('"5D": render_5D', '5D'),
        ('"5E": render_5E', '5E'),
        ('"6A": render_6A', '6A'),
        ('"7A": render_7A', '7A'),
        ('"8A": render_8A', '8A'),
        ('"9A": render_9A', '9A'),
        ('"10A": render_10A', '10A'),
        ('"10E": render_10E', '10E'),
    ]
    
    print("\n" + "=" * 60)
    print("DOĞRULAMA")
    print("=" * 60)
    
    all_ok = True
    for pattern_check, name in checks:
        if pattern_check in verify_content:
            print(f"✅ {name}: Bulundu")
        else:
            print(f"❌ {name}: EKSİK!")
            all_ok = False
    
    if all_ok:
        print("\n🎉 TÜM SENARYOLAR EKLENDİ!")
        print("\n📌 Şimdi yapmanız gerekenler:")
        print("   1. Streamlit'i durdurun (Ctrl+C)")
        print("   2. Yeniden başlatın: streamlit run app.py --server.port 8502")
        print("   3. Tarayıcıda Ctrl+Shift+R (hard refresh)")
        print("   4. 5A senaryosunu test edin")
    else:
        print("\n⚠️ Bazı senaryolar eksik kaldı. Manuel kontrol gerekli.")
    
    return all_ok


if __name__ == "__main__":
    fix_renderers()
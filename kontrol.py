"""
ALL_SCENARIOS ve SCENARIO_RENDERERS Kontrol Aracı
"""
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 70)
print("SENARYO KONTROL ARACI")
print("=" * 70)
print()

# 1. ALL_SCENARIOS["XX"] tanımlarını bul
matches_scenarios = re.findall(r'ALL_SCENARIOS\["(\d+[A-E])"\]\s*=', content)

print("[1] ALL_SCENARIOS SÖZLÜĞÜ")
print("-" * 70)
print(f"    Toplam: {len(matches_scenarios)} senaryo tanımı")
print()

for level in range(1, 11):
    level_scenarios = sorted([m for m in matches_scenarios if m.startswith(str(level))])
    if level_scenarios:
        print(f"    ✅ Seviye {level:2d}: {len(level_scenarios)} senaryo -> {', '.join(level_scenarios)}")
    else:
        print(f"    ❌ Seviye {level:2d}: YOK")
print()

# 2. SCENARIO_RENDERERS içeriğini bul
match_block = re.search(r'SCENARIO_RENDERERS\s*=\s*\{(.*?)\n\}', content, re.DOTALL)

print("[2] SCENARIO_RENDERERS SÖZLÜĞÜ")
print("-" * 70)

if match_block:
    block = match_block.group(1)
    # Satır satır incele
    for line in block.split('\n'):
        line = line.strip()
        # "5A": render_5A veya "5A": None
        found = re.findall(r'"(\d+[A-E])":\s*(\S+?)[,}]', line)
        for key, value in found:
            if 'None' in value:
                print(f"    ❌ {key}: None (EKSİK!)")
            else:
                print(f"    ✅ {key}: {value}")
else:
    print("    ❌ SCENARIO_RENDERERS bulunamadı!")
print()

# 3. render_XX fonksiyon tanımları
print("[3] RENDER FONKSİYONLARI")
print("-" * 70)

for level in range(1, 11):
    level_funcs = []
    for letter in "ABCDE":
        func_name = f"render_{level}{letter}"
        if f"def {func_name}(" in content:
            level_funcs.append(func_name)
    if level_funcs:
        print(f"    ✅ Seviye {level:2d}: {len(level_funcs)} fonksiyon -> {', '.join(level_funcs)}")
    else:
        print(f"    ❌ Seviye {level:2d}: YOK")
print()

print("=" * 70)
print("RAPOR TAMAMLANDI")
print("=" * 70)
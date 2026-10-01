"""
SiberKalkan Akademi - Senaryo Rapor Motoru
===========================================

Bu modül, her senaryo tamamlandığında otomatik rapor oluşturur.

Kullanım:
    from utils.report_generator import ReportGenerator
    
    report = ReportGenerator.generate(scenario_id, state)
    ReportGenerator.display(report)
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List


class ReportGenerator:
    """Senaryo sonu rapor oluşturucu."""
    
    BADGES = {
        "gold": {"emoji": "🥇", "name": "Altın Analist", "min_score": 90, "color": "#ffd700"},
        "silver": {"emoji": "🥈", "name": "Gümüş Analist", "min_score": 70, "color": "#c0c0c0"},
        "bronze": {"emoji": "🥉", "name": "Bronz Analist", "min_score": 50, "color": "#cd7f32"},
        "participant": {"emoji": "🎖️", "name": "Katılımcı", "min_score": 0, "color": "#4f8bc9"}
    }
    
    @classmethod
    def generate(cls, scenario_id: str, state: Dict, scenario_info: Dict = None) -> Dict:
        """Senaryo state'inden rapor oluşturur."""
        try:
            from content.scenario_reports import SCENARIO_REPORTS
            report_data = SCENARIO_REPORTS.get(scenario_id, cls._default_report_data(scenario_id))
        except Exception:
            report_data = cls._default_report_data(scenario_id)
        
        start_time = state.get('_start_time', datetime.now())
        end_time = datetime.now()
        
        if isinstance(start_time, str):
            try:
                start_time = datetime.fromisoformat(start_time)
            except Exception:
                start_time = end_time
        
        try:
            duration = end_time - start_time
            duration_str = cls._format_duration(duration.total_seconds())
        except Exception:
            duration_str = "Bilinmiyor"
        
        success = cls._check_success(scenario_id, state)
        achievements = cls._extract_achievements(scenario_id, state, report_data)
        missing = cls._extract_missing(scenario_id, state, report_data)
        score = cls._calculate_score(scenario_id, state, success)
        badge = cls._get_badge(score)
        
        # Level hesapla
        try:
            base_id = scenario_id.split('-')[0]
            level = int(base_id[0]) if base_id and base_id[0].isdigit() else 1
        except Exception:
            level = 1
        
        report = {
            "scenario_id": scenario_id,
            "scenario_title": scenario_info.get('title', scenario_id) if scenario_info else scenario_id,
            "role": scenario_info.get('role_human', 'N/A') if scenario_info else 'N/A',
            "ai_role": scenario_info.get('role_ai', 'N/A') if scenario_info else 'N/A',
            "type": scenario_info.get('type', 'unknown') if scenario_info else 'unknown',
            "level": level,
            "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S') if hasattr(start_time, 'strftime') else str(start_time),
            "end_time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "duration": duration_str,
            "success": success,
            "score": score,
            "badge": badge,
            "achievements": achievements,
            "missing": missing,
            "learning_outcomes": report_data.get('learning_outcomes', []),
            "defense_recommendations": report_data.get('defense_recommendations', {}),
            "references": report_data.get('references', {}),
            "attempts": state.get('attempts', 0),
            "risk": state.get('risk', 0),
            "auto_pilot_used": cls._check_auto_pilot(scenario_id),
        }
        
        return report
    
    @classmethod
    def _check_success(cls, scenario_id: str, state: Dict) -> bool:
        """Senaryo başarılı mı kontrol eder."""
        success_keys = [
            'hacked', 'data_exported', 'shell_obtained', 'root_obtained',
            'success', 'target_down', 'target_reached', 'contained',
            'unpacked', 'cleaned', 'exploited', 'dc_compromised',
            'admin_accessed', 'hash_cracked', 'cookie_stolen',
            'report_done',
        ]
        
        for key in success_keys:
            if state.get(key) is True:
                return True
        
        if state.get('intel', 0) >= 80:
            return True
        if state.get('credentials_stolen', 0) >= 10:
            return True
        if state.get('data_exfiltrated', 0) >= state.get('data_total', 500):
            return True
        if state.get('funds_stolen', 0) >= 500:
            return True
        if state.get('maturity', 0) >= 90:
            return True
        if state.get('patched') and len(state.get('patched', [])) >= 4:
            return True
        
        return False
    
    @classmethod
    def _extract_achievements(cls, scenario_id: str, state: Dict, report_data: Dict) -> List[str]:
        """Başarılanları çıkarır."""
        achievements = []
        
        custom_achievements = report_data.get('achievements_map', {})
        for key, text in custom_achievements.items():
            value = state.get(key)
            if isinstance(value, bool):
                if value:
                    achievements.append(text)
            elif isinstance(value, (int, float)):
                if value > 0:
                    achievements.append(f"{text} ({value})")
            elif isinstance(value, list):
                if len(value) > 0:
                    achievements.append(f"{text} ({len(value)} adet)")
        
        if state.get('detected_scans', 0) > 0:
            achievements.append(f"Tespit edilen tarama: {state['detected_scans']}")
        if state.get('blocked', 0) > 0:
            achievements.append(f"Engellenen tehdit: {state['blocked']}")
        if state.get('detected', 0) > 0:
            achievements.append(f"Doğru tespit: {state['detected']}")
        if state.get('resolved', 0) > 0:
            achievements.append(f"Çözülen olay: {state['resolved']}")
        
        return achievements if achievements else ["Henüz tamamlanan hedef yok"]
    
    @classmethod
    def _extract_missing(cls, scenario_id: str, state: Dict, report_data: Dict) -> List[str]:
        """Eksikleri çıkarır."""
        missing = []
        
        risk = state.get('risk', 0)
        if risk > 70:
            missing.append(f"⚠️ Risk seviyesi %{risk} (ideal: %30)")
        elif risk > 40:
            missing.append(f"⚠️ Risk seviyesi %{risk} (ideal: %30)")
        
        attempts = state.get('attempts', 0)
        if attempts > 10:
            missing.append(f"⚠️ Çok sayıda deneme: {attempts}")
        
        if cls._check_auto_pilot(scenario_id):
            missing.append("⚠️ Otomatik pilot kullanıldı")
        
        if state.get('false_positives', 0) > 0:
            missing.append(f"❌ Yanlış pozitif: {state['false_positives']}")
        if state.get('missed', 0) > 0:
            missing.append(f"❌ Kaçırılan: {state['missed']}")
        if state.get('ai_success', 0) > 0:
            missing.append(f"❌ AI başarılı: {state['ai_success']}")
        
        return missing if missing else ["✅ Hiçbir eksik yok, mükemmel!"]
    
    @classmethod
    def _calculate_score(cls, scenario_id: str, state: Dict, success: bool) -> int:
        """Performans skoru hesaplar (0-100)."""
        score = 50
        
        if success:
            score += 25
        
        risk = state.get('risk', 0)
        if risk <= 20:
            score += 25
        elif risk <= 40:
            score += 15
        elif risk <= 60:
            score += 5
        elif risk <= 80:
            score -= 5
        else:
            score -= 15
        
        attempts = state.get('attempts', 0)
        if attempts == 0:
            pass
        elif attempts <= 5:
            score += 10
        elif attempts <= 10:
            score += 5
        elif attempts <= 20:
            score -= 5
        else:
            score -= 10
        
        score -= state.get('false_positives', 0) * 3
        score -= state.get('missed', 0) * 5
        score -= state.get('ai_success', 0) * 5
        
        if cls._check_auto_pilot(scenario_id):
            score -= 10
        
        return max(0, min(100, score))
    
    @classmethod
    def _get_badge(cls, score: int) -> Dict:
        """Skora göre rozet döndürür."""
        for badge_key in ["gold", "silver", "bronze", "participant"]:
            badge = cls.BADGES[badge_key]
            if score >= badge["min_score"]:
                return badge
        return cls.BADGES["participant"]
    
    @classmethod
    def _format_duration(cls, seconds: float) -> str:
        """Süreyi formatlar."""
        if seconds < 60:
            return f"{int(seconds)} saniye"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes} dakika {secs} saniye"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours} saat {minutes} dakika"
    
    @classmethod
    def _check_auto_pilot(cls, scenario_id: str) -> bool:
        """Otomatik pilot kullanıldı mı?"""
        pilot_key = f"auto_pilot_{scenario_id}"
        pilot_state = st.session_state.get(pilot_key, {})
        return pilot_state.get('completed', False)
    
    @classmethod
    def _default_report_data(cls, scenario_id: str) -> Dict:
        """Varsayılan rapor verisi."""
        return {
            'achievements_map': {},
            'learning_outcomes': [],
            'defense_recommendations': {'dos': [], 'donts': [], 'references': []},
            'references': {}
        }
    
    @classmethod
    def display(cls, report: Dict, expanded: bool = True) -> None:
        """Raporu Streamlit'te gösterir."""
        if report['success']:
            border_color = "#00ff41"
            status_icon = "✅"
            status_text = "BAŞARILI"
        else:
            border_color = "#ff4444"
            status_icon = "❌"
            status_text = "TAMAMLANMADI"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(26,35,50,0.95));
            border-left: 5px solid {border_color};
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        ">
            <h2 style="color:{border_color}; margin:0; font-size:1.4rem;">
                📊 SENARYO SONU RAPORU
            </h2>
            <p style="color:#888; margin:5px 0 0 0; font-size:0.85rem;">
                {status_icon} {status_text} • {report['end_time']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"""
            <div style="
                background: rgba(26,35,50,0.8);
                border-radius: 8px;
                padding: 15px;
                margin: 5px 0;
                border: 1px solid #2d4a6e;
            ">
                <h4 style="color:#5a9ed4; margin:0 0 10px 0; font-size:0.9rem;">
                    🎯 SENARYO BİLGİSİ
                </h4>
                <p style="margin:5px 0; font-size:0.85rem;">
                    <b>Senaryo:</b> {report['scenario_title'][:60]}
                </p>
                <p style="margin:5px 0; font-size:0.85rem;">
                    <b>Seviye:</b> {report['level']}/10
                </p>
                <p style="margin:5px 0; font-size:0.85rem;">
                    <b>Rolünüz:</b> {report['role']}
                </p>
                <p style="margin:5px 0; font-size:0.85rem;">
                    <b>Karşı Taraf:</b> {report['ai_role']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: rgba(26,35,50,0.8);
                border-radius: 8px;
                padding: 15px;
                margin: 5px 0;
                border: 1px solid #2d4a6e;
            ">
                <h4 style="color:#5a9ed4; margin:0 0 10px 0; font-size:0.9rem;">
                    ⏱️ PERFORMANS BİLGİSİ
                </h4>
                <p style="margin:5px 0; font-size:0.85rem;">
                    <b>Süre:</b> {report['duration']}
                </p>
                <p style="margin:5px 0; font-size:0.85rem;">
                    <b>Deneme:</b> {report['attempts']}
                </p>
                <p style="margin:5px 0; font-size:0.85rem;">
                    <b>Risk:</b> %{report['risk']}
                </p>
                <p style="margin:5px 0; font-size:0.85rem;">
                    <b>Otopilot:</b> {'✅ Kullanıldı' if report['auto_pilot_used'] else '❌ Kullanılmadı'}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### ✅ BAŞARILANLAR")
        for achievement in report['achievements']:
            st.markdown(f"- {achievement}")
        
        st.markdown("### ⚠️ EKSİKLER / BAŞARISIZLIKLAR")
        for item in report['missing']:
            st.markdown(f"- {item}")
        
        if report['learning_outcomes']:
            with st.expander("📚 ÖĞRENME ÇIKTILARI", expanded=False):
                for outcome in report['learning_outcomes']:
                    st.markdown(f"- ✅ {outcome}")
        
        if report['defense_recommendations'].get('dos'):
            with st.expander("🛡️ SAVUNMA ÖNERİLERİ", expanded=False):
                st.markdown("**✅ Yapılması Gerekenler:**")
                for item in report['defense_recommendations']['dos']:
                    st.markdown(f"- {item}")
                
                if report['defense_recommendations'].get('donts'):
                    st.markdown("**❌ Kaçınılması Gerekenler:**")
                    for item in report['defense_recommendations']['donts']:
                        st.markdown(f"- {item}")
        
        st.markdown("---")
        st.markdown("### 📊 PERFORMANS ANALİZİ")
        
        col_score1, col_score2, col_score3 = st.columns([2, 1, 1])
        with col_score1:
            st.markdown(f"### Skor: **{report['score']}/100**")
            st.progress(report['score'] / 100)
        with col_score2:
            badge = report['badge']
            st.markdown(f"""
            <div style="text-align:center; padding:10px;">
                <div style="font-size:2.5rem;">{badge['emoji']}</div>
                <div style="color:{badge['color']}; font-weight:bold; font-size:0.85rem;">
                    {badge['name']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_score3:
            if report['score'] >= 90:
                st.success("🏆 Mükemmel!")
            elif report['score'] >= 70:
                st.info("👍 İyi iş!")
            elif report['score'] >= 50:
                st.warning("⚠️ Geliştirilebilir")
            else:
                st.error("❌ Tekrar dene")
        
        if report['references']:
            with st.expander("📖 REFERANSLAR", expanded=False):
                for ref_type, ref_value in report['references'].items():
                    icon = {
                        "MITRE ATT&CK": "🔴",
                        "OWASP": "🟠",
                        "CWE": "🟡",
                        "NIST": "🔵",
                        "Savunma": "🛡️",
                        "Gerçek Olay": "🌍"
                    }.get(ref_type, "📖")
                    st.markdown(f"**{icon} {ref_type}:** {ref_value}")
        
        cls._render_download_button(report)
    
    @classmethod
    def _render_download_button(cls, report: Dict) -> None:
        """Markdown indirme butonu render eder."""
        try:
            md_content = cls.to_markdown(report)
            st.download_button(
                label="📥 Raporu İndir (.md)",
                data=md_content,
                file_name=f"rapor_{report['scenario_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
                key=f"download_{report['scenario_id']}"
            )
        except Exception:
            pass
    
    @classmethod
    def to_markdown(cls, report: Dict) -> str:
        """Raporu Markdown formatına çevirir."""
        badge = report['badge']
        status = "✅ BAŞARILI" if report['success'] else "❌ TAMAMLANMADI"
        
        md = f"""# 📊 SENARYO SONU RAPORU

## 🎯 Senaryo Bilgisi

- **Senaryo:** {report['scenario_title']}
- **Seviye:** {report['level']}/10
- **Rolünüz:** {report['role']}
- **Karşı Taraf:** {report['ai_role']}
- **Durum:** {status}

## ⏱️ Zaman Bilgisi

- **Başlangıç:** {report['start_time']}
- **Bitiş:** {report['end_time']}
- **Süre:** {report['duration']}

## ✅ Başarılanlar

"""
        for item in report['achievements']:
            md += f"- {item}\n"
        
        md += "\n## ⚠️ Eksikler / Başarısızlıklar\n\n"
        for item in report['missing']:
            md += f"- {item}\n"
        
        if report['learning_outcomes']:
            md += "\n## 📚 Öğrenme Çıktıları\n\n"
            for item in report['learning_outcomes']:
                md += f"- ✅ {item}\n"
        
        if report['defense_recommendations'].get('dos'):
            md += "\n## 🛡️ Savunma Önerileri\n\n### ✅ Yapılması Gerekenler\n\n"
            for item in report['defense_recommendations']['dos']:
                md += f"- {item}\n"
            
            if report['defense_recommendations'].get('donts'):
                md += "\n### ❌ Kaçınılması Gerekenler\n\n"
                for item in report['defense_recommendations']['donts']:
                    md += f"- {item}\n"
        
        md += f"""
## 📊 Performans Analizi

- **Skor:** {report['score']}/100
- **Rozet:** {badge['emoji']} {badge['name']}
- **Deneme Sayısı:** {report['attempts']}
- **Risk Seviyesi:** %{report['risk']}
- **Otomatik Pilot:** {'Kullanıldı' if report['auto_pilot_used'] else 'Kullanılmadı'}

## 📖 Referanslar

"""
        for ref_type, ref_value in report['references'].items():
            md += f"- **{ref_type}:** {ref_value}\n"
        
        md += f"""
---

*Bu rapor SiberKalkan Akademi tarafından otomatik oluşturulmuştur.*
*TÜBİTAK 2204-A Projesi | Ahmet ALTINOK 2026*
*Rapor Tarihi: {report['end_time']}*
"""
        return md
    
    @classmethod
    def render_report_button(cls, scenario_id: str, state: Dict, 
                              scenario_info: Dict = None) -> None:
        """
        Her senaryonun sonuna eklenecek 'Rapor Göster' butonu.
        Hem 's1A' hem 's1A-DEF' hem 's1A_DEF' formatlarını destekler.
        """
        # State boşsa alternatif anahtarları dene
        if not state:
            candidates = [
                f"s{scenario_id}",                          # s7A-DEF
                f"s{scenario_id.replace('-', '_')}",        # s7A_DEF
                scenario_id,                                 # 7A-DEF
                scenario_id.replace('-', '_'),              # 7A_DEF
            ]
            for alt_key in candidates:
                state = st.session_state.get(alt_key, {})
                if state:
                    break
        
        # State hala boşsa minimum state oluştur
        if not state:
            state = {'attempts': 0, 'risk': 0}
        
        st.markdown("---")
        
        try:
            success = cls._check_success(scenario_id, state)
        except Exception:
            success = False
        
        report_key = f"report_shown_{scenario_id}"
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button(
                "📊 Raporu Göster",
                use_container_width=True,
                key=f"show_report_{scenario_id}",
                type="primary" if success else "secondary"
            ):
                st.session_state[report_key] = True
                st.rerun()
        
        with col2:
            if success:
                st.success("✅ **Senaryo tamamlandı!** Raporu görüntüleyebilirsiniz.")
            else:
                st.info("ℹ️ **Senaryo devam ediyor.** İsterseniz raporu görüntüleyebilirsiniz.")
        
        if st.session_state.get(report_key, False):
            try:
                report = cls.generate(scenario_id, state, scenario_info)
                cls.display(report)
                
                if st.button("❌ Raporu Kapat", key=f"close_report_{scenario_id}"):
                    st.session_state[report_key] = False
                    st.rerun()
            except Exception as e:
                st.error(f"Rapor oluşturulamadı: {e}")


if __name__ == "__main__":
    print("✅ ReportGenerator yüklendi")
    print(f"Rozet sayısı: {len(ReportGenerator.BADGES)}")
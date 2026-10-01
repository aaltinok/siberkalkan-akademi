"""
SiberKalkan Akademi - İçerik Modülü
====================================

Bu paket, senaryo raporları ve içerik verilerini içerir.

Modüller:
    - scenario_reports: 65 senaryo için rapor verileri

Kullanım:
    from content import scenario_reports
"""

__version__ = "5.1.0"
__author__ = "Ahmet ALTINOK"
__license__ = "CC BY-NC-SA 4.0"

from . import scenario_reports

__all__ = ["scenario_reports"]
"""
SiberKalkan Akademi - Yardımcı Modüller
========================================

Bu paket, ana uygulamaya yardımcı olan modülleri içerir.

Modüller:
    - ethics_guard: Etik koruma katmanı
    - theme_manager: 10 tema sistemi
    - safety_filter: İçerik filtresi

Kullanım:
    from utils import ethics_guard, theme_manager, safety_filter
"""

__version__ = "5.0.0"
__author__ = "Ahmet ALTINOK"
__email__ = "[email]"
__license__ = "CC BY-NC-SA 4.0"

# Modül import'ları
from . import ethics_guard
from . import theme_manager
from . import safety_filter

__all__ = [
    "ethics_guard",
    "theme_manager",
    "safety_filter",
]
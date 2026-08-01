# -*- coding: utf-8 -*-
"""
IAM Screen Monitor - Monitoreo de pantalla
Responsabilidad única: capturar y analizar pantalla
"""

import os
import datetime
import tempfile
import threading
from pathlib import Path
from collections import deque
from typing import Optional, Dict, Any

from ..config.settings import settings

# Dependencias opcionales
try:
    import mss
    import mss.tools
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class ScreenMonitor:
    """
    Monitor de pantalla en segundo plano
    Capturas periódicas con OCR opcional
    """
    
    def __init__(self, max_captures: int = 5):
        self.max_captures = max_captures
        self.captures = deque(maxlen=max_captures)
        self.ocr_texts = deque(maxlen=max_captures)
        self.running = False
        self.thread = None
        self.interval = settings.SCREENSHOT_INTERVAL
        self.lock = threading.Lock()
        self.last_capture_path = None
    
    def capture_now(self) -> Optional[Dict[str, Any]]:
        """Capturar pantalla ahora mismo"""
        if not MSS_AVAILABLE:
            return None
        
        try:
            with mss.MSS() as sct:
                monitor = sct.monitors[0]
                img = sct.grab(monitor)
                timestamp = datetime.datetime.now().strftime("%H%M%S_%f")
                path = os.path.join(tempfile.gettempdir(), f"iam_now_{timestamp}.png")
                mss.tools.to_png(img.rgb, img.size, output=path)
                
                # OCR
                ocr_text = ""
                if OCR_AVAILABLE:
                    try:
                        pil_img = Image.open(path)
                        ocr_text = pytesseract.image_to_string(pil_img, lang='spa+eng')
                    except Exception:
                        ocr_text = ""
                
                return {"path": path, "time": datetime.datetime.now(), "ocr": ocr_text}
                
        except Exception as e:
            print(f"[!] Error al capturar: {e}")
            return None

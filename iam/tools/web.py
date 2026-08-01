# -*- coding: utf-8 -*-
"""
IAM Web - Herramientas web completas
HTTP requests, web scraping, API testing, etc.
"""

import subprocess
import json
from typing import Tuple, List, Dict, Any


class WebTools:
    """
    Herramientas web completas
    """
    
    # === HTTP REQUESTS ===
    
    def get(self, url: str, headers: Dict = None, timeout: int = 30) -> Tuple[bool, Any]:
        """GET request"""
        try:
            import requests
            response = requests.get(url, headers=headers, timeout=timeout)
            return True, {
                'status': response.status_code,
                'headers': dict(response.headers),
                'content': response.text[:5000],
                'length': len(response.content)
            }
        except ImportError:
            return False, "[ERROR] Instala requests: pip install requests"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def post(self, url: str, data: Any = None, json_data: Any = None,
             headers: Dict = None, timeout: int = 30) -> Tuple[bool, Any]:
        """POST request"""
        try:
            import requests
            response = requests.post(url, data=data, json=json_data,
                                    headers=headers, timeout=timeout)
            return True, {
                'status': response.status_code,
                'headers': dict(response.headers),
                'content': response.text[:5000]
            }
        except ImportError:
            return False, "[ERROR] Instala requests: pip install requests"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def put(self, url: str, data: Any = None, json_data: Any = None,
            headers: Dict = None, timeout: int = 30) -> Tuple[bool, Any]:
        """PUT request"""
        try:
            import requests
            response = requests.put(url, data=data, json=json_data,
                                   headers=headers, timeout=timeout)
            return True, {
                'status': response.status_code,
                'content': response.text[:5000]
            }
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def delete(self, url: str, headers: Dict = None, timeout: int = 30) -> Tuple[bool, Any]:
        """DELETE request"""
        try:
            import requests
            response = requests.delete(url, headers=headers, timeout=timeout)
            return True, {'status': response.status_code}
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def download(self, url: str, output_path: str) -> Tuple[bool, str]:
        """Descargar archivo"""
        try:
            import requests
            response = requests.get(url, stream=True, timeout=60)
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True, f"[OK] Descargado: {output_path}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === WEB SCRAPING ===
    
    def scrape_html(self, url: str) -> Tuple[bool, str]:
        """Obtener HTML de pagina"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remover scripts y styles
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text(separator='\n', strip=True)
            return True, text[:10000]
        except ImportError:
            return False, "[ERROR] Instala beautifulsoup4: pip install beautifulsoup4"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def scrape_links(self, url: str) -> Tuple[bool, List[str]]:
        """Obtener enlaces de pagina"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            links = []
            for link in soup.find_all('a', href=True):
                links.append(link['href'])
            
            return True, links
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def scrape_images(self, url: str) -> Tuple[bool, List[str]]:
        """Obtener imagenes de pagina"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            images = []
            for img in soup.find_all('img', src=True):
                images.append(img['src'])
            
            return True, images
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def scrape_table(self, url: str, table_index: int = 0) -> Tuple[bool, List[List[str]]]:
        """Obtener tabla HTML"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            tables = soup.find_all('table')
            if table_index < len(tables):
                table = tables[table_index]
                rows = []
                for tr in table.find_all('tr'):
                    cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                    rows.append(cells)
                return True, rows
            
            return False, "[ERROR] Tabla no encontrada"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === API TESTING ===
    
    def test_api(self, url: str, method: str = "GET", data: Any = None,
                 headers: Dict = None) -> Tuple[bool, Dict]:
        """Testear endpoint API"""
        try:
            import requests
            import time
            
            start_time = time.time()
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                return False, f"[ERROR] Metodo no soportado: {method}"
            
            elapsed = time.time() - start_time
            
            return True, {
                'status': response.status_code,
                'time_ms': round(elapsed * 1000, 2),
                'size': len(response.content),
                'headers': dict(response.headers),
                'content': response.text[:2000]
            }
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === URL UTILS ===
    
    def check_url(self, url: str) -> Tuple[bool, Dict]:
        """Verificar si URL esta activa"""
        try:
            import requests
            response = requests.head(url, timeout=10, allow_redirects=True)
            return True, {
                'active': response.status_code < 400,
                'status': response.status_code,
                'final_url': response.url
            }
        except Exception as e:
            return False, {'active': False, 'error': str(e)}
    
    def get_headers(self, url: str) -> Tuple[bool, Dict]:
        """Obtener headers HTTP"""
        try:
            import requests
            response = requests.head(url, timeout=10)
            return True, dict(response.headers)
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === CURL EQUIVALENT ===
    
    def curl(self, url: str, method: str = "GET", data: str = None,
             headers: List[str] = None) -> Tuple[bool, str]:
        """Ejecutar curl"""
        try:
            cmd = ['curl', '-s', '-X', method]
            
            if headers:
                for h in headers:
                    cmd.extend(['-H', h])
            
            if data:
                cmd.extend(['-d', data])
            
            cmd.append(url)
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return True, result.stdout
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === RSS ===
    
    def parse_rss(self, url: str) -> Tuple[bool, List[Dict]]:
        """Parsear feed RSS"""
        try:
            import requests
            import xml.etree.ElementTree as ET
            
            response = requests.get(url, timeout=30)
            root = ET.fromstring(response.content)
            
            items = []
            for item in root.findall('.//item'):
                title = item.find('title')
                link = item.find('link')
                desc = item.find('description')
                
                items.append({
                    'title': title.text if title is not None else '',
                    'link': link.text if link is not None else '',
                    'description': desc.text if desc is not None else ''
                })
            
            return True, items
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === SCREENSHOT WEB ===
    
    def web_screenshot(self, url: str, output: str, width: int = 1920, height: int = 1080) -> Tuple[bool, str]:
        """Tomar screenshot de pagina web"""
        try:
            # Usar Selenium si esta disponible
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            options = Options()
            options.add_argument('--headless')
            options.add_argument(f'--window-size={width},{height}')
            
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            driver.save_screenshot(output)
            driver.quit()
            
            return True, f"[OK] Screenshot guardado: {output}"
        except ImportError:
            return False, "[ERROR] Instala selenium: pip install selenium"
        except Exception as e:
            return False, f"[ERROR] {e}"


# Instancia global
web = WebTools()

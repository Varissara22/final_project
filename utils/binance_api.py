import requests
import time

def safe_api_call(url, params=None, retries=3, timeout=10): 
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"Timeout attempt {attempt + 1}/{retries}")
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error {e.response.status_code}")
            if 400 <= e.response.status_code < 500:
                return None
                
        except requests.exceptions.ConnectionError:
            print(f"Connection error attempt {attempt + 1}/{retries}")
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        
        if attempt < retries - 1:
            time.sleep(2 ** attempt)
    return None

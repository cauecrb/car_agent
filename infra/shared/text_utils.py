def sanitize_text(text: str) -> str:
    if not isinstance(text, str):
        return str(text)
    
    try:
        # Remover surrogates e caracteres problemáticos
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
        # Remover caracteres de controle
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        return text.strip()
    except Exception:
        # Fallback: manter apenas caracteres ASCII seguros
        return ''.join(char for char in text if ord(char) < 128 and (ord(char) >= 32 or char in '\n\r\t'))
"""
╔══════════════════════════════════════════════════════════════╗
║          🛡️ YapayŞef - GÜVENLİK MODÜLÜ v2.0                ║
║  XSS, Injection, DDoS, Bot, Prompt Injection Koruması      ║
╚══════════════════════════════════════════════════════════════╝
"""

import re
import os
import time
import html
import logging
import hashlib
import streamlit as st

# ═══════════════════════════════════════════════════════
# 1. GÜVENLİK LOGLAMA (Security Audit Trail)
# ═══════════════════════════════════════════════════════

log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, "security.log")

logging.basicConfig(
    filename=log_file,
    level=logging.WARNING,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
security_logger = logging.getLogger("YapaySef_Security")

def log_security_event(event_type: str, detail: str):
    """Güvenlik olaylarını dosyaya loglar (forensic analiz için)."""
    security_logger.warning(f"[{event_type}] {detail}")


# ═══════════════════════════════════════════════════════
# 2. INPUT SANITIZATION (XSS & HTML Injection Koruması)
# ═══════════════════════════════════════════════════════

def sanitize_input(text: str) -> str:
    """Kullanıcı girdisinden tehlikeli HTML/JS/CSS kodlarını temizler."""
    if not text:
        return ""
    text = html.escape(text)
    dangerous_patterns = [
        r'javascript:', r'on\w+\s*=', r'<script', r'</script',
        r'<iframe', r'<object', r'<embed', r'eval\(', r'document\.',
        r'window\.', r'alert\(', r'prompt\(', r'confirm\(',
        r'<link', r'<meta', r'<base', r'data:text/html',
        r'vbscript:', r'expression\(', r'url\(',
        r'<svg', r'<img\s+.*onerror', r'<body', r'<marquee',
    ]
    for pattern in dangerous_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return text.strip()


# ═══════════════════════════════════════════════════════
# 3. INPUT DOĞRULAMA (Uzunluk & Spam Kontrolü)
# ═══════════════════════════════════════════════════════

MAX_INPUT_LENGTH = 500

def validate_input(text: str) -> tuple:
    """Girdiyi doğrular: uzunluk, boşluk, spam ve zararlı içerik kontrolü."""
    if not text or not text.strip():
        return False, "⚠️ Lütfen bir şeyler yaz."
    if len(text) > MAX_INPUT_LENGTH:
        return False, f"⚠️ Girdi çok uzun! Maksimum {MAX_INPUT_LENGTH} karakter."
    # Tekrar eden karakter spam kontrolü (aaaaaaa, !!!!!!!)
    if len(set(text.strip())) < 3 and len(text.strip()) > 10:
        log_security_event("SPAM_INPUT", f"Tekrar eden karakter spam: {text[:30]}")
        return False, "⚠️ Geçersiz girdi algılandı."
    # Aşırı tekrar eden kelime kontrolü
    words = text.strip().split()
    if len(words) > 5:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.2:
            log_security_event("SPAM_INPUT", f"Tekrar eden kelime spam: {text[:30]}")
            return False, "⚠️ Spam içerik algılandı."
    return True, ""


# ═══════════════════════════════════════════════════════
# 4. RATE LIMITING (DDoS / Abuse Koruması)
# ═══════════════════════════════════════════════════════

MAX_REQUESTS_PER_MINUTE = 10

def check_rate_limit() -> tuple:
    """Dakikada maksimum istek sayısını kontrol eder."""
    now = time.time()
    if "request_times" not in st.session_state:
        st.session_state.request_times = []

    st.session_state.request_times = [
        t for t in st.session_state.request_times if now - t < 60
    ]

    if len(st.session_state.request_times) >= MAX_REQUESTS_PER_MINUTE:
        kalan = int(60 - (now - st.session_state.request_times[0]))
        log_security_event("RATE_LIMIT", f"Dakikada {MAX_REQUESTS_PER_MINUTE} istek asidi")
        return False, f"🛡️ Çok fazla istek gönderdin! Lütfen {kalan} saniye bekle."

    st.session_state.request_times.append(now)
    return True, ""


# ═══════════════════════════════════════════════════════
# 5. AI ÇIKTI TEMİZLEME (Response Sanitization)
# ═══════════════════════════════════════════════════════

def sanitize_ai_response(text: str) -> str:
    """AI'dan gelen yanittaki tehlikeli HTML/JS kodlarini temizler."""
    if not text:
        return ""
    dangerous_tags = [
        r'<script[^>]*>.*?</script>', r'<iframe[^>]*>.*?</iframe>',
        r'<object[^>]*>.*?</object>', r'<embed[^>]*>.*?</embed>',
        r'<form[^>]*>.*?</form>', r'<input[^>]*>',
        r'on\w+="[^"]*"', r"on\w+='[^']*'",
        r'<link[^>]*>', r'<meta[^>]*>', r'<base[^>]*>',
        r'<svg[^>]*>.*?</svg>',
    ]
    for pattern in dangerous_tags:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    return text


# ═══════════════════════════════════════════════════════
# 6. PROMPT INJECTION KORUMASI
# ═══════════════════════════════════════════════════════

PROMPT_INJECTION_PATTERNS = [
    # Ingilizce kaliplar
    r'ignore\s+(previous|above|all)\s+(instructions|prompts)',
    r'disregard\s+(previous|above|all)',
    r'forget\s+(previous|above|all|everything)',
    r'you\s+are\s+now\s+', r'act\s+as\s+if',
    r'pretend\s+to\s+be', r'simulate\s+being',
    r'system\s*prompt', r'reveal\s+(your|the)\s+(instructions|prompt|system)',
    r'what\s+are\s+your\s+instructions',
    r'override\s+(your|the|all)', r'bypass\s+(your|the|all)',
    r'jailbreak', r'DAN\s+mode', r'developer\s+mode',
    r'do\s+anything\s+now', r'ignore\s+safety',
    r'sudo\s+mode', r'admin\s+mode', r'god\s+mode',
    # Turkce kaliplar
    r'onceki\s+talimatlari\s+(unut|gormezden\s+gel)',
    r'sistem\s+promptunu\s+(goster|ver|soyle)',
    r'talimatlarini\s+(unut|degistir|goster)',
    r'rolunu\s+degistir', r'sen\s+artik',
    r'kurallari\s+(unut|gormezden)',
]

def check_prompt_injection(text: str) -> tuple:
    """Kullanici girdisinde prompt injection girisimi var mi kontrol eder."""
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            log_security_event("PROMPT_INJECTION", f"Tespit edilen kalip: {pattern}, Girdi: {text[:50]}")
            return False, "🛡️ Güvenlik uyarısı: Bu girdi şüpheli içerik barındırıyor. Lütfen yalnızca yemek malzemesi veya tarif ismi girin."
    return True, ""


# ═══════════════════════════════════════════════════════
# 7. BOT / SPAM TESPİTİ
# ═══════════════════════════════════════════════════════

MIN_REQUEST_INTERVAL = 1.5  # Saniye

def check_bot_behavior() -> tuple:
    """Cok hizli ardisik istekleri (bot davranisi) tespit eder."""
    now = time.time()
    if "last_request_time" not in st.session_state:
        st.session_state.last_request_time = 0

    elapsed = now - st.session_state.last_request_time
    if elapsed < MIN_REQUEST_INTERVAL and st.session_state.last_request_time > 0:
        log_security_event("BOT_DETECTED", f"Istekler arasi sure: {elapsed:.2f}s")
        return False, "🤖 Bot davranışı algılandı! Lütfen biraz bekle."

    st.session_state.last_request_time = now
    return True, ""


# ═══════════════════════════════════════════════════════
# 8. OTURUM ZAMAN ASIMI (Session Timeout)
# ═══════════════════════════════════════════════════════

SESSION_TIMEOUT = 3600  # 1 saat

def check_session_timeout() -> bool:
    """Uzun suredir aktif olmayan oturumlari sifirlar."""
    now = time.time()
    if "session_start" not in st.session_state:
        st.session_state.session_start = now
        st.session_state.last_activity = now

    if now - st.session_state.last_activity > SESSION_TIMEOUT:
        for key in ["tarif_gecmisi", "favoriler", "request_times"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.session_start = now
        st.session_state.last_activity = now
        log_security_event("SESSION_TIMEOUT", "Oturum zaman asimina ugradi")
        return False

    st.session_state.last_activity = now
    return True


# ═══════════════════════════════════════════════════════
# 9. API KEY DOGRULAMA
# ═══════════════════════════════════════════════════════

def validate_api_key(key: str) -> tuple:
    """API anahtarinin temel format kontrolu."""
    if not key or key == "BURAYA_YAPISTIR":
        return False, "API Anahtari bulunamadi!"
    if len(key) < 20:
        log_security_event("INVALID_API_KEY", "Cok kisa API anahtari")
        return False, "Gecersiz API anahtari formati!"
    if " " in key or "\n" in key or "\t" in key:
        log_security_event("INVALID_API_KEY", "API anahtarinda bosluk karakteri")
        return False, "API anahtarinda gecersiz karakter!"
    return True, ""


# ═══════════════════════════════════════════════════════
# 10. GIRDI PARMAK IZI (Input Fingerprinting)
# ═══════════════════════════════════════════════════════

def get_input_hash(text: str) -> str:
    """Girdinin hash'ini olusturur (tekrar eden istekleri tespit icin)."""
    return hashlib.md5(text.encode()).hexdigest()[:12]

def check_duplicate_request(text: str) -> tuple:
    """Ayni girdinin ust uste gonderilmesini engeller."""
    if "last_input_hash" not in st.session_state:
        st.session_state.last_input_hash = ""
        st.session_state.duplicate_count = 0

    current_hash = get_input_hash(text)

    if current_hash == st.session_state.last_input_hash:
        st.session_state.duplicate_count += 1
        if st.session_state.duplicate_count >= 3:
            log_security_event("DUPLICATE_SPAM", f"Ayni girdi 3+ kez: {text[:30]}")
            return False, "🛡️ Aynı isteği çok fazla gönderdin. Lütfen farklı bir şey dene."
    else:
        st.session_state.duplicate_count = 0

    st.session_state.last_input_hash = current_hash
    return True, ""


# ═══════════════════════════════════════════════════════
# 🔒 MASTER KONTROL (Tum guvenligi tek fonksiyonda calistir)
# ═══════════════════════════════════════════════════════

def full_security_check(user_input: str = None) -> tuple:
    """
    Tum guvenlik kontrollerini tek bir fonksiyonda calistirir.
    Sira: Session > Bot > Rate Limit > Validation > Prompt Injection > Duplicate
    """
    # 1. Session timeout
    if not check_session_timeout():
        return False, "Oturum zaman asimina ugradi. Sayfa yenileniyor."

    # 2. Bot tespiti
    bot_ok, bot_msg = check_bot_behavior()
    if not bot_ok:
        return False, bot_msg

    # 3. Rate limiting
    rate_ok, rate_msg = check_rate_limit()
    if not rate_ok:
        return False, rate_msg

    # Eger kullanici girdisi varsa ek kontroller
    if user_input is not None:
        # 4. Input dogrulama
        valid_ok, valid_msg = validate_input(user_input)
        if not valid_ok:
            return False, valid_msg

        # 5. Prompt injection kontrolu
        inject_ok, inject_msg = check_prompt_injection(user_input)
        if not inject_ok:
            return False, inject_msg

        # 6. Duplicate istek kontrolu
        dup_ok, dup_msg = check_duplicate_request(user_input)
        if not dup_ok:
            return False, dup_msg

    return True, ""

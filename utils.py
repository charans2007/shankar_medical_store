import urllib.parse
from datetime import datetime
import re

def clean_phone_for_tel(phone_number):
    """Format phone number for tel: links (e.g. tel:+919876543210)."""
    if not phone_number:
        return ""
    cleaned = re.sub(r'[^0-9+]', '', phone_number)
    return f"tel:{cleaned}"

def clean_whatsapp_number(whatsapp_number):
    """Format WhatsApp number (digits only with country code, no +, spaces, or dashes)."""
    if not whatsapp_number:
        return ""
    return re.sub(r'[^0-9]', '', whatsapp_number)

def generate_whatsapp_link(whatsapp_number, product_name=None, shop_name=None, message_type='general'):
    """
    Generate pre-filled WhatsApp click-to-chat URL.
    Ensures message is URL-encoded and complies with non-ecommerce enquiry rules.
    """
    number = clean_whatsapp_number(whatsapp_number)
    shop_title = shop_name or "your medical store"
    
    if message_type == 'availability' and product_name:
        msg = f"Hello, I would like to enquire about the availability of '{product_name}' at {shop_title}. Is it currently in stock at your physical store?"
    elif message_type == 'location':
        msg = f"Hello {shop_title}, I would like directions / assistance in visiting your physical medical shop today."
    else:
        msg = f"Hello {shop_title}, I would like to enquire about healthcare products and services at your physical medical store."
        
    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/{number}?text={encoded_msg}"

def get_store_status(shop):
    """
    Calculate dynamic store status:
    - is_open: True / False
    - status_text: 'OPEN NOW' / 'CLOSED'
    - today_hours_text: e.g. 'Today: 10:00 AM – 8:00 PM'
    - sub_text: e.g. 'Opens today at 10:00 AM' or 'Open until 8:00 PM today'
    - reopen_time_text: e.g. 'Today at 10:00 AM' or 'Tomorrow at 10:00 AM' or 'Monday at 10:00 AM'
    """
    now = datetime.now()
    day_of_week = now.weekday() # 0 = Monday, 6 = Sunday
    current_time_str = now.strftime('%H:%M')
    
    is_sunday = (day_of_week == 6)
    is_saturday = (day_of_week == 5)
    
    weekday_open = (getattr(shop, 'weekday_open_time', '10:00') if shop else '10:00') or '10:00'
    weekday_close = (getattr(shop, 'weekday_close_time', '20:00') if shop else '20:00') or '20:00'
    formatted_weekday_open = format_time_12h(weekday_open)
    formatted_weekday_close = format_time_12h(weekday_close)
    weekday_hours_text = f"Monday – Saturday: {formatted_weekday_open} – {formatted_weekday_close}"
    
    is_sun_closed = (getattr(shop, 'is_sunday_closed', True) if shop else True)
    if shop and shop.weekly_closure and 'sunday' in shop.weekly_closure.lower():
        is_sun_closed = True
        
    sunday_open = (getattr(shop, 'sunday_open_time', '00:00') if shop else '00:00') or '00:00'
    sunday_close = (getattr(shop, 'sunday_close_time', '00:00') if shop else '00:00') or '00:00'
    sunday_hours_text = "Sunday: Closed (Weekly Holiday)" if is_sun_closed else f"Sunday: {format_time_12h(sunday_open)} – {format_time_12h(sunday_close)}"
    
    if is_sunday:
        if is_sun_closed:
            return {
                'is_open': False,
                'status_text': 'CLOSED',
                'status_class': 'status-closed',
                'badge_color': '#ef4444',
                'today_hours_text': 'Today: Closed (Weekly Holiday)',
                'sub_text': f"Opens Monday at {formatted_weekday_open}",
                'reopen_time_text': f"Monday at {formatted_weekday_open}",
                'open_time': weekday_open,
                'close_time': weekday_close,
                'open_time_12h': formatted_weekday_open,
                'close_time_12h': formatted_weekday_close,
                'weekday_hours_text': weekday_hours_text,
                'sunday_hours_text': sunday_hours_text
            }
        open_time = sunday_open
        close_time = sunday_close
    else:
        open_time = weekday_open
        close_time = weekday_close
        
    is_open = (open_time <= current_time_str < close_time)
    formatted_open = format_time_12h(open_time)
    formatted_close = format_time_12h(close_time)
    today_hours_text = f"Today: {formatted_open} – {formatted_close}"
    
    if is_open:
        status_text = 'OPEN NOW'
        status_class = 'status-open'
        badge_color = '#10b981'
        sub_text = f"Open until {formatted_close} today"
        reopen_time_text = ""
    else:
        status_text = 'CLOSED'
        status_class = 'status-closed'
        badge_color = '#ef4444'
        if current_time_str < open_time:
            sub_text = f"Opens today at {formatted_open}"
            reopen_time_text = f"Today at {formatted_open}"
        else:
            if is_saturday and is_sun_closed:
                sub_text = f"Closed for the weekend. Reopens Monday at {formatted_weekday_open}."
                reopen_time_text = f"Monday at {formatted_weekday_open}"
            else:
                sub_text = f"Closed for the day. Reopens tomorrow at {formatted_weekday_open}."
                reopen_time_text = f"Tomorrow at {formatted_weekday_open}"

    return {
        'is_open': is_open,
        'status_text': status_text,
        'status_class': status_class,
        'badge_color': badge_color,
        'today_hours_text': today_hours_text,
        'sub_text': sub_text,
        'reopen_time_text': reopen_time_text,
        'open_time': open_time,
        'close_time': close_time,
        'open_time_12h': formatted_open,
        'close_time_12h': formatted_close,
        'weekday_hours_text': weekday_hours_text,
        'sunday_hours_text': sunday_hours_text
    }

def format_time_12h(time_str):
    """Convert 24h '08:00' or '22:00' to '8:00 AM' or '10:00 PM'."""
    try:
        dt = datetime.strptime(time_str.strip(), '%H:%M')
        return dt.strftime('%I:%M %p').lstrip('0')
    except Exception:
        return time_str

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
import threading

logger = logging.getLogger(__name__)

def send_problem_notification_email(name, phone, problem_type, message, shop_name="Shankar Homoeo Stores"):
    """
    Sends an email notification to the official store email (shankarhomeostores@gmail.com)
    when a customer raises a problem/complaint.
    Supports environment SMTP variables (SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD).
    If SMTP credentials are not yet configured in environment, safely logs the full email payload.
    """
    to_email = os.environ.get('EMAIL', 'shankarhomeostores@gmail.com')
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USERNAME', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')

    subject = f"⚠️ [Customer Problem Raised] {problem_type} - {name}"
    
    body = f"""Hello Shankar Homoeo Stores Management,

A new customer problem/issue has been raised on the website:

--------------------------------------------------
Customer Name: {name}
Contact Phone / WhatsApp: {phone}
Problem Category: {problem_type}
Timestamp: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
Official Store Target Email: {to_email}
--------------------------------------------------

Details of the Problem:
{message}

--------------------------------------------------
Please review and follow up with the customer directly at {phone}.
"""
    
    if smtp_user and smtp_password:
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [to_email], msg.as_string())
            server.quit()
            logger.info(f"Problem notification successfully emailed to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to deliver email via SMTP: {e}")
            return False
    else:
        logger.info(f"[Email Notification Dispatch] Target: {to_email} | Subject: {subject}\n{body}")
        return True

def async_send_problem_notification(name, phone, problem_type, message, shop_name="Shankar Homoeo Stores"):
    """Dispatch email notification in a background thread to prevent blocking HTTP response."""
    thread = threading.Thread(
        target=send_problem_notification_email,
        args=(name, phone, problem_type, message, shop_name)
    )
    thread.daemon = True
    thread.start()

# ----------------- HIGH-CONCURRENCY IN-MEMORY CACHE -----------------
_CACHE_LOCK = threading.Lock()
_CACHE = {}

def get_cached_value(key, ttl_seconds, fetcher_fn):
    """
    Thread-safe TTL in-memory cache for high-concurrency read operations.
    Avoids redundant database queries across hundreds of simultaneous requests.
    """
    import time
    now = time.time()
    with _CACHE_LOCK:
        if key in _CACHE:
            val, expiry = _CACHE[key]
            if now < expiry:
                return val
    
    # Compute fresh value outside critical section
    fresh_val = fetcher_fn()
    
    with _CACHE_LOCK:
        _CACHE[key] = (fresh_val, now + ttl_seconds)
    return fresh_val

def clear_cache(key_prefix=None):
    """Invalidate cached entries when admin makes updates."""
    with _CACHE_LOCK:
        if key_prefix:
            keys_to_del = [k for k in _CACHE if k.startswith(key_prefix)]
            for k in keys_to_del:
                _CACHE.pop(k, None)
        else:
            _CACHE.clear()


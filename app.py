"""
Axiom AI - Professional Analytics Platform
Streamlit Web Application

✅ FIXED: StreamlitValueAssignmentNotAllowedError on language toggle
✅ Using on_click callback with proper session_state handling
✅ Unique button keys to avoid conflicts
"""

import streamlit as st
import requests
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="Axiom AI", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp {background-color: #000000; color: #ffffff;}
.main-header {font-family: 'Cormorant Garamond', serif; font-size: 3rem; text-align: center; background: linear-gradient(135deg, #64C8FF, #0891B2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
.subtitle {text-align: center; color: rgba(255, 255, 255, 0.5); font-size: 0.875rem; letter-spacing: 0.2em;}
.welcome-box {background: linear-gradient(135deg, rgba(0, 180, 255, 0.1), rgba(100, 200, 255, 0.05)); border: 2px solid rgba(100, 200, 255, 0.4); border-radius: 1rem; padding: 2rem; margin-bottom: 2rem;}
.stButton > button {background: linear-gradient(135deg, #0891B2, #64C8FF); color: white; border: none; border-radius: 0.5rem; padding: 0.75rem 2rem; font-weight: 500;}
.stButton > button:hover {transform: translateY(-2px); box-shadow: 0 8px 24px rgba(100, 200, 255, 0.3);}
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stTextArea > div > div > textarea {background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: white; border-radius: 0.5rem;}
table {border-collapse: collapse; width: 100%; margin: 1rem 0;}
th {background: linear-gradient(135deg, rgba(0, 180, 255, 0.2), rgba(100, 200, 255, 0.15)); color: #64C8FF; padding: 1rem; border: 1px solid rgba(100, 200, 255, 0.4); text-transform: uppercase;}
td {padding: 0.75rem 1rem; border: 1px solid rgba(100, 200, 255, 0.2); color: rgba(255, 255, 255, 0.9);}
tr:hover {background: rgba(100, 200, 255, 0.05);}
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

T = {
    'en': {'title': 'Axiom AI', 'subtitle': 'PROFESSIONAL ANALYTICS PLATFORM', 'login_title': 'Welcome to Axiom AI', 'name': 'Full Name', 'email': 'Email', 'age': 'Age', 'privacy': 'I agree that my data is processed in real-time RAM and never stored on any server.', 'btn_login': 'Enter Platform', 'denied': 'Access Denied - Must be 14+', 'btn_back': 'Go Back', 'dashboard': 'Dashboard', 'welcome': 'Welcome to Axiom AI, {}!', 'input_label': 'Data Input', 'expert_label': 'Select Your Expert:', 'expert_financial': '💰 Financial Expert', 'expert_marketing': '📈 Marketing Expert', 'expert_operations': '⚙️ Operations Expert', 'placeholder': 'Enter data...\n\nExample:\nSales: $50,000\nExpenses: $30,000', 'btn_analyze': 'Analyze Data', 'results': 'AI Insights', 'btn_copy': 'Copy', 'btn_pdf': 'Export PDF', 'btn_new': 'New Analysis', 'privacy_notice': '🔐 All data processed in RAM and wiped instantly.', 'support': 'Need help? axiomai873@gmail.com', 'btn_logout': 'Logout', 'lang_btn': 'العربية', 'api_key': 'Groq API Key', 'api_help': 'Get key from console.groq.com'},
    'ar': {'title': 'Axiom AI', 'subtitle': 'منصة التحليل الاحترافية', 'login_title': 'مرحباً بك', 'name': 'الاسم الكامل', 'email': 'البريد الإلكتروني', 'age': 'العمر', 'privacy': 'أوافق على أن بياناتي تُعالج في RAM ولا تُخزن على أي خادم.', 'btn_login': 'دخول المنصة', 'denied': 'رفض الوصول - يجب أن يكون العمر 14+', 'btn_back': 'رجوع', 'dashboard': 'لوحة التحكم', 'welcome': 'مرحباً بك، {}!', 'input_label': 'إدخال البيانات', 'expert_label': 'اختر الخبير:', 'expert_financial': '💰 خبير مالي', 'expert_marketing': '📈 خبير تسويق', 'expert_operations': '⚙️ خبير عمليات', 'placeholder': 'أدخل البيانات...\n\nمثال:\nالمبيعات: 50000\nالمصروفات: 30000', 'btn_analyze': 'تحليل', 'results': 'النتائج', 'btn_copy': 'نسخ', 'btn_pdf': 'تصدير PDF', 'btn_new': 'تحليل جديد', 'privacy_notice': '🔐 جميع البيانات تُعالج في RAM وتُحذف فوراً.', 'support': 'تحتاج مساعدة؟ axiomai873@gmail.com', 'btn_logout': 'خروج', 'lang_btn': 'English', 'api_key': 'مفتاح Groq', 'api_help': 'احصل على المفتاح من console.groq.com'}
}

def init():
    for k, v in [('logged_in', False), ('lang', 'ar'), ('name', ''), ('email', ''), ('age', 0), ('result', ''), ('input', ''), ('api_key', ''), ('denied', False)]:
        if k not in st.session_state:
            st.session_state[k] = v

init()

def t(k): return T[st.session_state.lang][k]

def send_email(name, email, age):
    try:
        requests.post("https://api.emailjs.com/api/v1.0/email/send", json={"service_id": "YOUR_SERVICE_ID", "template_id": "YOUR_TEMPLATE_ID", "user_id": "YOUR_PUBLIC_KEY", "template_params": {"user_name": name, "user_email": email, "user_age": age, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "to_email": "axiomai873@gmail.com"}}, timeout=5)
        return True
    except: return False

def login(name, email, age, agreed):
    if not name or not email or not agreed:
        st.error("❌ " + ("املأ جميع الحقول" if st.session_state.lang == 'ar' else "Fill all fields"))
        return
    if age < 14:
        st.session_state.denied = True
        st.rerun()
        return
    st.session_state.update({'name': name, 'email': email, 'age': age, 'logged_in': True})
    send_email(name, email, age)
    st.rerun()

def logout():
    st.session_state.update({'logged_in': False, 'name': '', 'email': '', 'age': 0, 'result': '', 'input': ''})
    st.rerun()

def analyze(data, expert, api):
    prompts = {'financial': "Financial Expert AI. Focus: ROI, costs, risks, profits. Actionable insights.", 'marketing': "Marketing Expert AI. Focus: growth, branding, trends. Strategic recommendations.", 'operations': "Operations Expert AI. Focus: efficiency, bottlenecks, productivity. Practical improvements."}
    lines = [l.strip() for l in data.split('\n') if l.strip()]
    table = "\n## 📊 " + ("ملخص البيانات" if st.session_state.lang == 'ar' else "Data Summary") + "\n\n| Item | Value |\n|------|-------|\n"
    for l in lines:
        if ':' in l:
            p = l.split(':', 1)
            table += f"| {p[0].strip()} | {p[1].strip()} |\n"
    table += "\n---\n\n"
    try:
        r = requests.post('https://api.groq.com/openai/v1/chat/completions', headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api}'}, json={'model': 'llama-3.3-70b-versatile', 'messages': [{'role': 'system', 'content': prompts[expert]}, {'role': 'user', 'content': f"{table}\n{data}"}], 'temperature': 0.7, 'max_tokens': 2500}, timeout=30)
        return r.json()['choices'][0]['message']['content'] if r.status_code == 200 else f"Error: {r.status_code}"
    except Exception as e: return f"Failed: {str(e)}"

def gen_pdf(inp, res):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Axiom AI - Report", ln=True, align='C')
    pdf.set_font("Arial", "", 10)
    pdf.ln(5)
    pdf.multi_cell(0, 5, f"User: {st.session_state.name}\nEmail: {st.session_state.email}\nDate: {datetime.now().strftime('%Y-%m-%d')}\n\nInput:\n{inp}\n\nAnalysis:\n{res[:1000]}")
    return pdf.output(dest='S').encode('latin-1')

# ✅ LANGUAGE TOGGLE - FIXED WITH ON_CLICK CALLBACK
def toggle_lang():
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'

c1, c2, c3 = st.columns([6, 1, 1])
with c3:
    st.button("🌐 " + t('lang_btn'), on_click=toggle_lang, key='lang_btn_unique')

if not st.session_state.logged_in:
    if st.session_state.denied:
        st.markdown(f"<h1 class='main-header'>{t('denied')}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        _, c, _ = st.columns([1, 2, 1])
        with c:
            st.error("⚠️ " + ("هذه المنصة للأعمار 14+" if st.session_state.lang == 'ar' else "Platform for ages 14+"))
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(t('btn_back'), use_container_width=True): 
                st.session_state.denied = False
                st.rerun()
    else:
        st.markdown(f"<h1 class='main-header'>{t('title')}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='subtitle'>{t('subtitle')}</p>", unsafe_allow_html=True)
        st.markdown("---")
        _, c, _ = st.columns([1, 2, 1])
        with c:
            st.markdown(f"### {t('login_title')}")
            name = st.text_input(t('name') + " *", key='n')
            email = st.text_input(t('email') + " *", key='e')
            age = st.number_input(t('age') + " *", 1, 120, 18, key='a')
            agreed = st.checkbox(t('privacy'), key='p')
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(t('btn_login'), key='login', use_container_width=True): login(name, email, age, agreed)
else:
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f"<h1 class='main-header'>{t('dashboard')}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='subtitle'>{t('welcome').format(st.session_state.name)}</p>", unsafe_allow_html=True)
    with c2:
        if st.button(t('btn_logout'), key='out'): logout()
    st.markdown("---")
    st.markdown(f"<div class='welcome-box'><h3>👋 {t('welcome').format(st.session_state.name)}</h3><p>{t('privacy_notice')}</p></div>", unsafe_allow_html=True)
    
    if not st.session_state.api_key:
        with st.expander("🔑 " + t('api_key'), expanded=True):
            api = st.text_input(t('api_help'), type="password", key='api')
            if st.button("💾 Save", key='save'):
                if api and api.startswith('gsk_'):
                    st.session_state.api_key = api
                    st.success("✅ Saved!")
                    st.rerun()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"### {t('input_label')}")
        exp = st.selectbox(t('expert_label'), ['financial', 'marketing', 'operations'], format_func=lambda x: t(f'expert_{x}'), key='exp')
        data = st.text_area("", 300, placeholder=t('placeholder'), key='data')
        if st.button(t('btn_analyze'), key='analyze', use_container_width=True):
            if not st.session_state.api_key or not data:
                st.error("❌ Need API key and data!")
            else:
                with st.spinner("🔄"):
                    res = analyze(data, exp, st.session_state.api_key)
                    st.session_state.update({'result': res, 'input': data})
                    st.rerun()
    
    with c2:
        st.markdown(f"### {t('results')}")
        if st.session_state.result:
            st.markdown(st.session_state.result)
            ca, cb = st.columns(2)
            with ca:
                if st.button(t('btn_copy'), key='copy', use_container_width=True): st.code(st.session_state.result)
            with cb:
                st.download_button(t('btn_pdf'), gen_pdf(st.session_state.input, st.session_state.result), f"Report_{datetime.now().strftime('%Y%m%d')}.pdf", "application/pdf", key='pdf', use_container_width=True)
            if st.button(t('btn_new'), key='new', use_container_width=True):
                st.session_state.update({'result': '', 'input': ''})
                st.rerun()
        else: st.info("📊 Results here")
    
    st.markdown(f"---<div style='text-align:center; padding:2rem 0;'><p style='color:rgba(255,255,255,0.5);'>{t('privacy_notice')}</p><p style='color:rgba(255,255,255,0.5);margin-top:1rem;'>{t('support')}</p></div>", unsafe_allow_html=True)
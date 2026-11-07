import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\artifacts_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

OLD_MD = '    st.markdown(html, unsafe_allow_html=True)'
NEW_MD = '''    clean_html = "\\n".join([line.strip() for line in html.split("\\n") if line.strip()])
    st.markdown(clean_html, unsafe_allow_html=True)'''

if OLD_MD in content:
    content = content.replace(OLD_MD, NEW_MD)
    with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\artifacts_helper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("artifacts_helper.py successfully patched with clean_html!")
else:
    print("Target not found in artifacts_helper.py")

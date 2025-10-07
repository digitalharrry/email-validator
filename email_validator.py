import streamlit as st
import requests

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Email Validator", page_icon="📧", layout="centered")

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,700;1,300&family=Poppins:wght@300;400;500;600&display=swap');

* { font-family: 'Poppins', sans-serif; }

.nav {
    display: flex;
    justify-content: space-between;
    background-color: black;
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}

.nav a { color: white; text-decoration: none; padding: 0 10px; }
.nav a:hover { color: rgb(192, 189, 205); }

.container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    border-radius: 12px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
}

input, button {
    font-size: 16px;
    padding: 8px 10px;
    margin-top: 10px;
}

button {
    background-color: black;
    color: white;
    border-radius: 6px;
    cursor: pointer;
}

.result-box {
    background-color: #fff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #ccc;
    margin-top: 15px;
    word-break: break-word;
}

footer {
    font-size: 12px;
    background-color: black;
    color: white;
    padding: 12px;
    text-align: center;
    border-radius: 8px;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# ----------------- NAVBAR -----------------
st.markdown("""
<div class="nav">
    <div class="logo"><b>Email Validator</b></div>
    <div><a href="#">Home</a></div>
</div>
""", unsafe_allow_html=True)

# ----------------- MAIN CONTAINER -----------------
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown("### Enter your email:")

email = st.text_input(" ", placeholder="example@email.com")

if st.button("Validate"):
    if not email:
        st.warning("⚠️ Please enter an email address.")
    else:
        with st.spinner("🔍 Validating email..."):
            try:
                # ----------------- API CALL -----------------
                api_key = 'API_KEY'  # <-- Put your API key here
                url = f'https://api.mails.so/v1/validate?email={email}'
                headers = {'x-mails-api-key': api_key}

                response = requests.get(url, headers=headers)
                
                if response.status_code != 200:
                    st.error(f"❌ API returned status code {response.status_code}")
                else:
                    result = response.json()
                    if result:
                        # ----------------- INTERPRET RESULTS -----------------
                        is_valid = result.get("isv_format", False) and \
                                   result.get("isv_domain", False) and \
                                   result.get("isv_mx", False)

                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown(f"**Email:** {email}")

                        if is_valid:
                            st.success("✅ This email is valid and can receive emails!")
                        else:
                            st.error("❌ This email failed the validation test or cannot receive emails.")

                        # Optional: Show additional info
                        st.markdown(f"**Provider:** {result.get('provider', 'Unknown')}")
                        st.markdown(f"**MX Record:** {result.get('mx_record', 'N/A')}")
                        st.markdown(f"**Score:** {result.get('score', 'N/A')}%")
                        st.markdown(f"**Reason (if invalid):** {result.get('reason', 'N/A')}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("❌ API returned empty response.")

            except Exception as e:
                st.error(f"⚠️ Error connecting to API: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ----------------- FOOTER -----------------
st.markdown("""
<footer>
    &copy; 2025 Email Validator App
</footer>
""", unsafe_allow_html=True)


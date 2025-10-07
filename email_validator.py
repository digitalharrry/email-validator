import streamlit as st
import requests

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Email Validator", page_icon="📧", layout="centered")

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
* { font-family: 'Poppins', sans-serif; }

.nav {
    display: flex; justify-content: space-between;
    background-color: black; color: white;
    padding: 12px 20px; border-radius: 8px; margin-bottom: 20px;
}
.nav a { color: white; text-decoration: none; padding: 0 10px; }
.nav a:hover { color: rgb(192, 189, 205); }

.container { max-width: 600px; margin: auto; padding: 20px; border-radius: 12px; background-color: #f9f9f9; border: 1px solid #ddd; }
input, button { font-size: 16px; padding: 8px 10px; margin-top: 10px; }
button { background-color: black; color: white; border-radius: 6px; cursor: pointer; }

.result-box { background-color: #fff; padding: 15px; border-radius: 10px; border: 1px solid #ccc; margin-top: 15px; word-break: break-word; }
footer { font-size: 12px; background-color: black; color: white; padding: 12px; text-align: center; border-radius: 8px; margin-top: 25px; }
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
                api_key = '38f0fe1b-4f35-48ef-bfbc-d50bc51ea0c2'  # <-- Put your API key here
                url = f'https://api.mails.so/v1/validate?email={email}'
                headers = {'x-mails-api-key': api_key}

                response = requests.get(url, headers=headers)
                
                if response.status_code != 200:
                    st.error(f"❌ API returned status code {response.status_code}")
                else:
                    result = response.json()
                    if result:
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown(f"**Email:** {email}")

                        # ----------------- VALIDATION LOGIC -----------------
                        format_ok = result.get("isv_format", False)
                        domain_ok = result.get("isv_domain", False)
                        smtp_ok = result.get("isv_mx", False)

                        # ----------------- FRIENDLY MESSAGE -----------------
                        if format_ok and domain_ok and smtp_ok:
                            st.success("✅ This email is valid and can receive emails!")
                        elif format_ok and domain_ok:
                            st.warning("⚠️ Email format and domain are correct, but deliverability could not be verified from this server.")
                        else:
                            st.error("❌ This email failed the validation test or is invalid.")

                        # ----------------- OPTIONAL DETAILS -----------------
                        details = {
                            "Provider": result.get("provider"),
                            "MX Record": result.get("mx_record"),
                            "Score": f"{result.get('score')}%" if result.get("score") is not None else None,
                            "Reason": result.get("reason")
                        }

                        for key, value in details.items():
                            if value and value != "Unknown" and value != "N/A":
                                st.markdown(f"**{key}:** {value}")

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

import os
import streamlit as st

# Dependency handling
try:
    from groq import Groq
    GROQ_INSTALLED = True
except ImportError:
    GROQ_INSTALLED = False

st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags for any platform.")

if not GROQ_INSTALLED:
    st.error("⚠️ **Missing Required Library: `groq`**")
    st.info("Ensure `requirements.txt` contains `streamlit` and `groq` on separate lines.")
    st.stop()

# Secret Key detection logic
secret_key = st.secrets.get("GROQ_API_KEY", "") if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY", "")

with st.sidebar:
    st.header("Configuration")
    
    # Always display status or text input
    if secret_key:
        st.success("🔑 API Key Status: **Connected**")
        st.caption("Key loaded automatically from Streamlit Secrets.")
        groq_api_key = secret_key
    else:
        groq_api_key = st.text_input(
            "Enter Groq API Key", 
            type="password", 
            help="Get a free key at https://console.groq.com"
        )
    
    st.markdown("---")
    st.markdown("**Model Settings**")
    st.info("⚡ Powered by `llama-3.3-70b-versatile` (Free)")

# Input controls
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Blog/Newsletter"])
    content_type = st.selectbox("Content Type", ["Educational Post", "Promotional / Sales", "Personal Story", "Industry Insight", "Product Launch"])
    tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Energetic & Bold", "Informative", "Humorous"])

with col2:
    audience = st.text_input("Target Audience", placeholder="e.g. Software Developers, Small Business Owners")
    topic = st.text_input("Topic / Main Idea", placeholder="e.g. Benefits of microservices architecture")

# Submit button
if st.button("Generate Content", type="primary"):
    if not groq_api_key:
        st.error("Please provide a valid Groq API Key.")
    elif not topic or not audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=groq_api_key.strip())

            prompt = f"""
            You are an expert social media content strategist. Generate a complete, publish-ready post based on the following details:
            - Platform: {platform}
            - Content Type: {content_type}
            - Tone: {tone}
            - Target Audience: {audience}
            - Topic: {topic}

            Format your response clearly with:
            1. Post Content (engaging, formatted appropriately for {platform} with emojis and line breaks)
            2. Caption / Short Summary (if applicable)
            3. 5-10 Relevant Hashtags
            """

            with st.spinner("Generating content..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                generated_text = response.choices[0].message.content

            st.success("Content generated successfully!")
            st.markdown("---")
            st.markdown(generated_text)
            
            st.download_button(
                label="📥 Download Output as Text File",
                data=generated_text,
                file_name=f"{platform.lower().replace(' ', '_')}_post.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred while generating content: {e}")

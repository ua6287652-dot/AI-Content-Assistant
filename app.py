import os
import streamlit as st

# Fallback error handling for missing dependencies
try:
    from groq import Groq
    GROQ_INSTALLED = True
except ImportError:
    GROQ_INSTALLED = False

# Page layout configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags for any platform.")

# Display friendly error if groq package is missing
if not GROQ_INSTALLED:
    st.error("⚠️ **Missing Required Library: `groq`**")
    st.info(
        """
        **How to fix this issue:**
        1. **Locally:** Run `pip install groq` in your terminal.
        2. **Streamlit Cloud:** Ensure you have a file named `requirements.txt` in the main folder of your GitHub repository containing:
           ```text
           streamlit
           groq
           ```
        3. Reboot your app from **Manage app** $\rightarrow$ **Reboot**.
        """
    )
    st.stop()  # Stop execution until dependency issue is resolved

# Sidebar for API Key configuration
with st.sidebar:
    st.header("Configuration")
    groq_api_key = os.getenv("GROQ_API_KEY") or st.text_input(
        "Groq API Key", type="password", help="Get a free key at https://console.groq.com"
    )

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
        st.error("Please provide a valid Groq API Key in the sidebar.")
    elif not topic or not audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=groq_api_key)

            # Construct structured prompt
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
                # Call free Groq model
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                generated_text = response.choices[0].message.content

            st.success("Content generated successfully!")
            st.markdown("---")
            st.markdown(generated_text)
            
            # Download button for the generated output
            st.download_button(
                label="📥 Download Output as Text File",
                data=generated_text,
                file_name=f"{platform.lower().replace(' ', '_')}_post.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred while generating content: {e}")

%%writefile app.py


import os

import streamlit as st
from groq import Groq


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="ContentPilot AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Professional styling
# -----------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: #f7f8fc;
        }

        [data-testid="stSidebar"] {
            background: #111827;
            border-right: 1px solid #1f2937;
        }

        [data-testid="stSidebar"] * {
            color: #f9fafb;
        }

        .hero {
            padding: 2rem 2.2rem;
            border-radius: 22px;
            background: linear-gradient(135deg, #111827 0%, #243b6b 55%, #4f46e5 100%);
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 12px 30px rgba(31, 41, 55, 0.12);
        }

        .hero h1 {
            margin: 0;
            font-size: 2.6rem;
            font-weight: 800;
        }

        .hero p {
            margin: 0.6rem 0 0;
            color: #e5e7eb;
            font-size: 1.05rem;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 750;
            color: #111827;
            margin: 1rem 0 0.8rem;
        }

        .result-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
        }

        .metric-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 1rem;
            text-align: center;
        }

        .small-muted {
            color: #6b7280;
            font-size: 0.9rem;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## ✦ ContentPilot AI")
    st.caption("AI Content Assistant")
    st.divider()

    st.markdown("### Content settings")

    content_type = st.selectbox(
        "Content type",
        [
            "Social media post",
            "LinkedIn post",
            "Instagram caption",
            "Facebook post",
            "X post",
            "Blog introduction",
            "Marketing copy",
        ],
    )

    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Instagram", "Facebook", "X", "General"],
    )

    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Friendly",
            "Persuasive",
            "Educational",
            "Inspirational",
            "Casual",
            "Bold",
        ],
    )

    target = st.text_input(
        "Target audience",
        placeholder="e.g. university students, developers, small businesses",
    )

    st.divider()
    st.caption("Built with Python + Streamlit + Groq")


# -----------------------------
# Main header
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>✦ ContentPilot AI</h1>
        <p>Generate polished posts, captions, and relevant hashtags in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Create your content</div>', unsafe_allow_html=True)

topic = st.text_area(
    "Topic",
    placeholder="What do you want to write about?",
    height=100,
)

guidance = st.text_area(
    "Guidance / key points",
    placeholder="Add important points, CTA, product details, keywords, or anything the AI should include.",
    height=120,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="metric-card"><b>1</b><br><span class="small-muted">Choose settings</span></div>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        '<div class="metric-card"><b>2</b><br><span class="small-muted">Describe your topic</span></div>',
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        '<div class="metric-card"><b>3</b><br><span class="small-muted">Generate & publish</span></div>',
        unsafe_allow_html=True,
    )

st.write("")

generate = st.button(
    "✦ Generate Content",
    type="primary",
    use_container_width=True,
)


# -----------------------------
# AI generation
# -----------------------------
def generate_content():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error(
            "GROQ_API_KEY is missing. Add it to your local environment or "
            "Streamlit Cloud Secrets."
        )
        return

    if not topic.strip():
        st.warning("Please enter a topic first.")
        return

    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert social media content strategist and copywriter.

Create a high-quality, ready-to-publish piece of content using these requirements:

Content type: {content_type}
Platform: {platform}
Topic: {topic}
Target audience: {target or "General audience"}
Tone: {tone}
Additional guidance: {guidance or "None"}

Return the answer in exactly these three sections:

POST:
Write the complete ready-to-publish post/caption. Make it engaging, natural,
clear, and suitable for the selected platform. Do not add unnecessary labels
inside the post.

CAPTION:
Write a concise supporting caption or alternative caption. If the main post
already functions as a caption, create a useful shorter version.

HASHTAGS:
Provide 8-12 relevant hashtags. Avoid spammy or unrelated hashtags.

Do not mention that you are an AI. Do not explain your process.
"""

    with st.spinner("Creating your content..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional content strategist.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1200,
        )

    return response.choices[0].message.content


if generate:
    result = generate_content()

    if result:
        st.session_state["content_result"] = result


# -----------------------------
# Display result
# -----------------------------
if "content_result" in st.session_state:
    st.markdown('<div class="section-title">Your generated content</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="result-card">',
        unsafe_allow_html=True,
    )
    st.markdown(st.session_state["content_result"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.download_button(
        "⬇ Download content",
        data=st.session_state["content_result"],
        file_name="contentpilot_post.txt",
        mime="text/plain",
        use_container_width=True,
    )

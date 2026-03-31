import streamlit as st
import nltk
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from utils.extractor import extract_text
from utils.summarizer import summarize_text
from utils.keywords import extract_keywords
from utils.sentiment import analyze_sentiment
from utils.translator import translate_to_tamil
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #00ADB5;
}
.stButton>button {
    background-color: #00ADB5;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.stTextArea textarea {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.title("📰 AI News Summarizer")
st.markdown("### Summarize • Analyze • Visualize News Instantly")

# ------------------ SIDEBAR ------------------
st.sidebar.title("⚙️ Settings")

input_type = st.sidebar.radio("Choose Input Type", ["Text", "URL"])
sent_count = st.sidebar.slider("Summary Length", 2, 10, 5)

st.sidebar.markdown("---")
st.sidebar.info("Paste news text or URL and click Analyze 🚀")

# ------------------ INPUT ------------------
text = ""

if input_type == "Text":
    text = st.text_area("📝 Enter News Article", height=250)

elif input_type == "URL":
    url = st.text_input("🌐 Enter News URL")
    if url:
        text = extract_text(url)
        if text:
            st.success("✅ Article extracted successfully!")
            with st.expander("Preview Article"):
                st.write(text[:500] + "...")
        else:
            st.error("❌ Failed to extract article")

# ------------------ BUTTON ------------------
if st.button("🚀 Analyze News"):

    if text:

        # Tabs
        tabs = st.tabs(["📄 Summary", "😊 Sentiment", "🏷️ Keywords", "📊 Chart", "🌐 Tamil"])

        # -------- SUMMARY --------
        with tabs[0]:
            st.subheader("✂️ Summary")
            summary = summarize_text(text, sent_count)

            st.info(summary)

            st.download_button("💾 Download Summary", summary)

        # -------- SENTIMENT --------
        with tabs[1]:
            sentiment, score = analyze_sentiment(text)

            st.subheader("😊 Sentiment Result")

            if "Positive" in sentiment:
                st.success(sentiment)
            elif "Negative" in sentiment:
                st.error(sentiment)
            else:
                st.warning(sentiment)

            st.write(f"📊 Polarity Score: {score:.2f}")

        # -------- KEYWORDS --------
        with tabs[2]:
            st.subheader("🏷️ Top Keywords")

            keywords = extract_keywords(text)

            for word, freq in keywords:
                st.markdown(f"🔹 **{word}** ({freq})")

        # -------- CHART --------
        with tabs[3]:
            st.subheader("📊 Word Frequency")

            keywords = extract_keywords(text)
            labels = [w[0] for w in keywords]
            values = [w[1] for w in keywords]

            fig, ax = plt.subplots()
            ax.bar(labels, values)
            plt.xticks(rotation=45)

            st.pyplot(fig)
        
        # -------- TAMIL TRANSLATION --------
        with tabs[4]:
            st.subheader("🌐 Tamil Translation")

            summary = summarize_text(text, sent_count)
            tamil_text = translate_to_tamil(summary)

            st.info(tamil_text)

            st.download_button("💾 Download Tamil Text", tamil_text)

    else:
        st.warning("⚠️ Please enter text or URL")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("✨ Developed as an NLP Project")
# main.py
import streamlit as st
import difflib
from recommend import df, recommend_songs

# --- Page Config ---
st.set_page_config(
    page_title="Music Recommender 🎵",
    page_icon="🎧",
    layout="centered"
)

# --- Styles ---
st.markdown("""
    <style>
    /* Full screen gradient background */
    .stApp {
        background-image: linear-gradient(to bottom, #e0f7fa, #80deea); /* Light bluish gradient */
        background-size: cover;
        background-position: center;
        min-height: 100vh;
        padding: 0 !important;
    }
    /* Main container with no background and padding */
    .main {
        background-color: transparent !important; /* No background */
        padding: 2rem;
        border-radius: 12px;
        box-shadow: none; /* Remove any box-shadow */
    }
    /* Title section */
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: #1DB954;
        text-align: center;
        margin-bottom: 1em;
    }
    /* Style for dropdown, text input, and buttons */
    .stSelectbox, .stTextInput, .stButton, .stSlider, .stTextArea {
        background-color: transparent !important; /* Transparent background */
        color: #003366;  /* Deep blue color for text */
        border: none !important; /* Remove border */
        border-radius: 8px !important;
    }
    /* Style for 'recommendation' text */
    .recommend-text {
        color: black;
        font-size: 1.2em;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5em;
    }
    /* Style for the 'did you mean' text */
    .did-mean {
        color: black;
        font-weight: 600;
    }
    /* Footer section */
    .footer {
        font-size: 0.8em;
        text-align: center;
        color: #888;
        margin-top: 3em;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Body ---
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="title">🎶 Instant Music Recommender</div>', unsafe_allow_html=True)

song_list = sorted(df['song'].dropna().unique())

# Dropdown
st.markdown('<p style="font-weight: bold; color: #003366;">🎵 Choose from list:</p>', unsafe_allow_html=True)
selected_song = st.selectbox("", song_list)

# Text input with fuzzy matching
st.markdown('<p style="font-weight: bold; color: #003366;">🔍 Or type a song name:</p>', unsafe_allow_html=True)
typed_song = st.text_input("")
matched_song = None

if typed_song:
    matches = difflib.get_close_matches(typed_song, song_list, n=1, cutoff=0.6)
    if matches:
        matched_song = matches[0]
        st.markdown(f'<p class="did-mean">🎯 Did you mean: **{matched_song}**?</p>', unsafe_allow_html=True)
    else:
        st.warning("😕 Couldn't find a close match.")

# Final song to recommend from
final_song = matched_song or selected_song

# Recommend button
# Recommend button
if st.button("🚀 Recommend Similar Songs"):
    with st.spinner("Finding similar songs..."):
        recommendations = recommend_songs(final_song)
        if recommendations is None:
            st.warning("Sorry, song not found.")
        else:
            st.markdown('<p class="recommend-text">✅ Here are your recommended tracks:</p>', unsafe_allow_html=True)
            recommendations = recommendations.reset_index(drop=True)
            recommendations.index += 1  # Start index from 1
            st.dataframe(recommendations)


# Footer
st.markdown("""
    <div class="footer">
        By Jenia ❤️ 2025 · Explore more at <a href="https://open.spotify.com/" target="_blank">Spotify</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

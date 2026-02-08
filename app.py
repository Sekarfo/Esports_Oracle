import streamlit as st
from src.gemini_agent import analyze_matchup_with_image

st.set_page_config(page_title="Gemini 3 Dota Oracle", page_icon="👁️", layout="wide")

st.title(" Dota 2 --- Esports Oracle ")


col1, col2 = st.columns(2)
with col1:
    team_1 = st.text_input("Team 1 (Radiant)", "Team Spirit")
with col2:
    team_2 = st.text_input("Team 2 (Dire)", "Tundra Esports")

# Загрузка
uploaded_file = st.file_uploader("📸 Upload Draft Screenshot", type=["jpg", "png", "jpeg"])

if st.button("ANALYZE MATCH"):
    if not team_1 or not team_2:
        st.warning("Enter team names.")
    else:
        # --- ИСПРАВЛЕНИЕ ПРЕДУПРЕЖДЕНИЯ ---
        if uploaded_file:
            # Было: use_container_width=True
            # Стало: width="stretch" (как просило предупреждение)
            st.image(uploaded_file, caption="Draft Preview", width="stretch") 
        
        with st.spinner(" Gemini 3 is analyzing the Matrix..."):
            # Если файла нет, передаем None
            result = analyze_matchup_with_image(team_1, team_2, uploaded_file)
            
            st.success("Analysis Complete!")
            st.markdown(result)
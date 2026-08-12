import streamlit as st
from langchain_community.llms import Ollama


# Not: Eğer vektör veritabanını ve yükleme kısımlarını ragpycharm.py içinde
# fonksiyon haline getirdiysen onları da buraya import edebilirsin.

st.title("Şevval's ChatBot")
# Hafıza Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Önceki mesajları ekranda göster
for mesaj in st.session_state.messages:
    with st.chat_message(mesaj["role"]):
        st.markdown(mesaj["content"])

# Sohbet Girişi
if prompt := st.chat_input("🌸 🌺 🌼 Buraya yazabilirsin... app.py:19🌼 🌺 🌸"):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Asistanın Cevap Verme Kısmı
    with st.chat_message("assistant"):
        try:
            # Doğru model ismi ve sınıfı buraya yazıldı:
            llm = Ollama(model="qwen2.5:1.5b", temperature=0.3)

            # Şimdilik direkt modelden cevap alıyoruz (RAG zincirini buraya bağlayabilirsin)
            cevap = llm.invoke(prompt)

            # Balonları uçur 🎈
            st.balloons()

            # Cevabı ekrana bas
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})

        except Exception as e:
            st.error(f"Bir hata oluştu kanka: {e}")
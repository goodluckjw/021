import streamlit as st
from processing.law_processor import process_laws

st.set_page_config(page_title="부칙 개정 도우미")
st.title("📘 부칙 개정 도우미")
st.markdown("법률명 없어도, 찾을 단어와 바꿀 단어만 입력하면 자동으로 법령을 찾아 부칙 개정 문장을 생성해주는 AI 도우미입니다.")

if "button_clicked" not in st.session_state:
    st.session_state["button_clicked"] = False

search_word = st.text_input("🔍 찾을 단어", placeholder="예: 지방법원")
replace_word = st.text_input("📝 바꿀 단어", placeholder="예: 지역법원")

if st.button("🚀 시작하기"):
    st.session_state["button_clicked"] = True

if search_word and replace_word and st.session_state["button_clicked"]:
    try:
        with st.spinner("법령을 검색하고 개정 문장을 생성 중입니다..."):
            result = process_laws(search_word, replace_word)

        if result is None:
            st.error("공공데이터 응답이 올바르지 않습니다.")
        elif not result:
            st.warning("⚠️ 일치하는 법령이 없습니다.")
        else:
            st.success("✅ 개정 문장이 성공적으로 생성되었습니다!")
            all_lines = []
            for i, (law, sentences) in enumerate(result.items(), 1):
                st.markdown(f"### {law}")
                for sentence in sentences:
                    line = f"{i:02d}. {law} {sentence}"
                    st.markdown(f"- {line}")
                    all_lines.append(f"{chr(9311+i)} {law} {sentence}")
            with open("result.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(all_lines))
            with open("result.txt", "r", encoding="utf-8") as f:
                st.download_button("📄 결과 TXT 다운로드", f.read(), file_name="result.txt")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")

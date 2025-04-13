import streamlit as st
import requests
import xml.etree.ElementTree as ET
import time
import urllib.parse

API_KEY = st.secrets["api_key"]
OC = st.secrets["oc"]

def get_law_list():
    url = f"http://www.law.go.kr/DRF/lawSearch.do?OC={OC}&target=law&type=XML&key={urllib.parse.quote(API_KEY)}"
    try:
        res = requests.get(url, timeout=10)
        root = ET.fromstring(res.content)
        laws = []
        for law in root.findall(".//law"):
            law_id = law.findtext("lawId")
            law_name = law.findtext("lawNm")
            if law_id and law_name:
                laws.append({"id": law_id, "name": law_name})
        return laws
    except:
        return None

def search_law_text(law_id, search_word):
    url = f"http://www.law.go.kr/DRF/lawService.do?OC={OC}&target=elaw&type=XML&key={urllib.parse.quote(API_KEY)}&lawId={law_id}"
    try:
        res = requests.get(url, timeout=10)
        root = ET.fromstring(res.content)
        hits = []
        for article in root.findall(".//ARTICLE"):
            article_no = article.findtext("ArticleNo", default="").strip()
            article_title = article.findtext("ArticleTitle", default="").strip()
            article_text = article.findtext("ArticleContent", default="").strip()
            if search_word in article_text:
                hits.append({"article_no": article_no, "title": article_title})
        return hits
    except:
        return None

def process_laws(search_word, replace_word):
    laws = get_law_list()
    if not laws:
        return None
    result = {}
    for law in laws:
        time.sleep(0.3)
        matches = search_law_text(law["id"], search_word)
        if matches:
            result[law["name"]] = []
            for m in matches:
                art = m["article_no"]
                title = m["title"]
                sentence = f"제{art}조의 제목 중 “{search_word}”를 “{replace_word}”로 한다." if title else f"제{art}조 중 “{search_word}”를 “{replace_word}”로 한다."
                result[law["name"]].append(sentence)
    return result

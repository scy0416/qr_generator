import io
from datetime import datetime
import streamlit as st
import qrcode
from qrcode.constants import ERROR_CORRECT_L

@st.fragment
def make_qr():
    if st.session_state["data"] == "":
        st.info("정보를 입력하세요!")
        return
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(st.session_state["data"])
    qr.make(fit=True)

    img = qr.make_image(fill_color=st.session_state["fill"], back_color=st.session_state["back"]).get_image()
    st.image(img)

    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG")
    buf.seek(0)

    st.download_button(
        label="QR코드 다운로드",
        data=buf,
        file_name=f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        mime="image/png",
        use_container_width=True,
        key="download_qr_btn"
    )

st.set_page_config(layout="wide")
st.header("경민이를 위한 QR코드 생성기")
st.divider()

st.subheader("변환하고자 하는 정보")
st.text_input(label="문자열 또는 링크", key="data")

st.subheader("QR코드 색상 선택")
col1, col2 = st.columns(2, border=True)
with col1:
    st.color_picker("셀 색상 선택", key="fill")
with col2:
    st.color_picker("배경 색상 선택", "#ffffff", key="back")

st.subheader("생성된 QR코드")
make_qr()
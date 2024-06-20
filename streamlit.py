import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
from modules.predict import predict_digit

def load_image(image_file):
	img = Image.open(image_file)
	return img

choice = "Image"

LABELS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}
if choice == "Image":

    st.subheader("Dự đoán chữ hoa viết tay")
    st.caption('Trang web này giúp bạn dự đoán chữ hoa viết tay với độ chính xác tương đối :)))')
    st.caption('Bạn hãy vẽ một bức ảnh có chứa một số bằng paint hoặc bất kì app nào khác, đừng vẽ thêm những thứ khác')
    st.caption('Sau đó lưu lại và upload vào đây nhé!!!')
    st.caption('Cảm ơn bạn đã tin dùng, website created by Than Thien')
    image_file = st.file_uploader("Upload Images",
                                  type=["png", "jpg", "jpeg"])

    if image_file is not None:
        # TO See details
        file_details = {"filename": image_file.name, "filetype": image_file.type,
                        "filesize": image_file.size}
        st.write(file_details)
        st.image(load_image(image_file), width=250)

        # Saving upload
        with open(os.path.join("fileDir", image_file.name), "wb") as f:
            f.write((image_file).getbuffer())

        st.success("File Saved")
        num = predict_digit(os.path.join("fileDir", image_file.name))

        st.write("Chữ cái bạn đã vẽ là: ", ", ".join([LABELS[i[0]] for i in num]))
        st.write("Độ chính xác tương ứng là: ", ", ".join([ str(round(i[1]*100.0, 2)) for i in num]))


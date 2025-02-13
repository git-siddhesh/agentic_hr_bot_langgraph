





import streamlit as st
from pathlib import Path
# image = '.\\images\\user_input\\DSC_0108_BS.jpeg'
# st.image(image)

def process_file():
    save_folder = './'
    save_path = Path(save_folder, st.session_state['uploaded_image'].name)
    with open(save_path, mode='wb') as w:
        w.write(st.session_state['uploaded_image'].getvalue())

    if save_path.exists() and save_path.is_file():
        st.toast(f"Invoice has been uploaded.")


with st.container():
    invoice_image = st.file_uploader(label="Upload Invoice",
                                     key='uploaded_image',
                                     type=['png', 'jpg', 'jpeg', 'pdf'],
                                     accept_multiple_files=False,
                                     on_change=process_file)




# import streamlit as st



# st.header('Scrolling Columns')


# # col1, col2 = st.columns([1, 5])

# # with col1:
# #     with st.container():
# #         btn1 = st.button('Button 1')
# #         btn2 = st.button('Button 2')
# #         btn3 = st.button('Button 3')

# # with col2:
# #     with st.container(border=True, height=200):
# #         # scrollable 

# #         st.write('This is another container')
# #         st.write('You can put any content here')
# #         st.write('Like text, images, or charts')

# # text = st.chat_input("Ask me anything...")




# import streamlit as st
# from time import sleep

# if "image_uploader_key" not in st.session_state:
#     st.session_state["image_uploader_key"] = 1
# if "audio_uploader_key" not in st.session_state:
#     st.session_state["audio_uploader_key"] = 1

# uploaded_file = st.file_uploader("Please upload an image",type=["jpg", "jpeg", "png"],key=st.session_state["image_uploader_key"],)
# audio_file = st.audio_input("Record a voice message", key="audio_file")

# if uploaded_file is not None:
#     with st.spinner("Processing"):
#         sleep(3)

#     # Clear the file uploader
#     st.session_state["image_uploader_key"] += 1
#     st.rerun()

# if audio_file is not None:
#     with st.spinner("Processing"):
#         sleep(3)

#     # Clear the file uploader
#     st.session_state["audio_uploader_key"] += 1
#     st.rerun()
    


# # cols = st.columns(3)
# # with st.container():
# #     cols[0].write('A short column')
# # with st.container():
# #     cols[1].write('Meow' + ' meow'*1000)
# # with st.container():
# #     cols[2].write('Another short column')

# # css='''
# # <style>
# #     section.main>div {
# #         padding-bottom: 1rem;
# #     }
# #     [data-testid="column"]>div>div>div>div>div {
# #         overflow: auto;
# #         height: 70vh;
# #     }
# # </style>
# # '''

# # st.markdown(css, unsafe_allow_html=True)

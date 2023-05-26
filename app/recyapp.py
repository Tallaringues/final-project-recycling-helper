import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

from functions_prediction import predict_class, load_lottieurl, load_data, update_csv

from PIL import Image
import matplotlib as plt
import time
import numpy as np
import plotly.express as px
import cv2


# More emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
	page_title = "Recyclapp",
    page_icon=":recycling_symbol:",
    layout="wide")


# LOAD ASSETS
lottie_recycle = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_VRpTUvkfkU.json")
lottie_contact = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_in4cufsz.json")
lottie_resources = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_1a8dx7zj.json")

#with st.sidebar:
selected = option_menu(
	menu_title = None,
	options = ["Home", "Trash classifier", "Resources", "Contact", "About me"],
	icons = ['house', "recycle","book", "envelope", "person lines fill"],
	menu_icon = "flower1",
	orientation = "horizontal",
	styles={
    "container": {"padding": "0!important", "background-color": "#fafafa"},
    "icon": {"color": "orange", "font-size": "25px"}, 
    "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "green"},
})

if selected == "About me":
    col1, col2 = st.columns( [0.7, 0.3])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)
        with st.container():
            st.write("Allow me to introduce myself: I'm Marta Alirangues-Núñez, the creator behind the Recyclapp :recycle:")
            st.subheader("I'm an Ecologist... :sunflower:")
            st.write("###")
            st.write(
                """
                My passion for plants started at an early age. As a kid, you could find me following my grandpa around the garden, or gathering cuttlings with my mother.
                That passion and knowledge grew even further thanks to my experience in the scouts (yes, we do more than selling cookies).
                I decided to study a bachelor in Environmental Sciences, followed by a Master in Restoration Ecology that took me to The Netherlands Institute of Ecology 
                [(NIOO)](https://nioo.knaw.nl/en) and to get my first work experience in the research world.
                Currently, I'm finishing my PhD thesis in Aquatic Ecology in [IGB (Berlin)](https://www.igb-berlin.de/en)
                """)
        with st.container():
            st.subheader("...and also a Data Scientist :computer:")
            st.write("Recently, I decided to go for a career change (or, if you thing about it, expansion) and took part in a (extremely) instensive Data Analytics Bootcamp by [Ironhack](https://www.ironhack.com/de/en/data-analytics/remote).")
            st.write(
                """
                Among the topics that we learned, I am passionate about:
                - Image Classification with Convolutional Neural Networks
                - Build, Evaluate and Deploy Machine Learning Models
                - Data analysis using Python and MySQL
                """
			)
    with col2:
        my_photo = Image.open("images/3N9A1253.jpg")
        st.image(my_photo)
    with st.container():
        st.write("---")
        st.subheader("Get in touch :email:")
        col1, col2 =  st.columns([0.3,0.7])
        with col1:
            st_lottie(lottie_contact, height=150, key="contact")
        with col2:
            st.write(
                """
                - :bird: [Twitter]()
                - :computer: [GitHub]()
                - :printer: [LinkedIn]()
                """
                     )
    with st.container():
        st.write("---")
        st.write("“The more clearly we can focus our attention on the wonders and realities of the universe about us, the less taste we shall have for destruction.” ― Rachel Carson")
        
        
elif selected == "Trash classifier":
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Where should I throw this away?</p>', unsafe_allow_html=True)
        #st.write("###")
        st.write(":camera: Upload a photo, click on \"Classify\" and wait just a few seconds")
        st.write("The answer will appear right under the photo")
        uploaded_image = st.file_uploader("Upload your image here :camera:", type=["png","jpg","jpeg"],label_visibility="collapsed")
        class_btn = st.button("Classify")
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption='Uploaded image')
        if class_btn:
            if uploaded_image is None:
                st.write("Invalid file, please try again :blush:")
            else:
                with st.spinner('Model working....'):
                    result = predict_class(image)
                    time.sleep(1)
                    st.success('Classified')
                    st.write('This waste should go to', result)
                    if result is not None:
                        update_csv('counter_vertical.csv', result)                        
    with col2:
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Recycled so far...</p>', unsafe_allow_html=True)
        st.write("Everytime you use the classifier, the app records the answer so you can keep track of your queries")
        rec_count = load_data()
        fig = px.pie(rec_count, values='values', names='classes', color_discrete_sequence=px.colors.sequential.Sunset_r)
        fig.update_layout(font = dict(size=18), legend = dict(xanchor="left", x=-0.1, yanchor='bottom', y=-0.2,orientation='h', font = dict(size=16)))
        st.write(fig)

elif selected == "Resources":
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Some interesting resources</p>', unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns([0.7,0.3])
        with col1:
            st.subheader("What about some interesting books? :book:")
            st.write(
            """
            - Silent Spring by Rachel Carson - Read a review in [Goodreads](https://www.goodreads.com/book/show/27333.Silent_Spring)
            - How to blow a Pipeline by Andreas Malm - Read an interview in [The Guardian](https://www.theguardian.com/environment/2023/apr/21/climate-diplomacy-is-hopeless-says-author-of-how-to-blow-up-a-pipeline-andreas-malm)
            - Cómo dinamitar un oleoducto por Andreas Malm - (Spanish version) - Puedes leer acerca del libro y comprarlo [aquí](https://tienda.elsaltodiario.com/producto/como-dinamitar-un-oleoducto/)

            """
        )
        
        with col2:
            st_lottie(lottie_resources, height=300, key="resources", loop=False)
    with st.container():
        st.subheader("Be more sustainable in your day to day life :seedling:")
        #st.write("###")
        st.write(
            """
            - Think twice before shopping.
            - Make sure your big purchases have big environmental benefits.
            - Go #PlasticFree.
            - Boycott products that endanger wildlife.
            - Pay attention to labels.
            - Be water wise.
            - Drive less, drive green.
            - Green your home.
            - Choose Wild Energy.
            - Take Extinction Off Your Plate.
            - Use your voice and your vote.
            """
		)
        st.write("[More information >](https://www.biologicaldiversity.org/programs/population_and_sustainability/sustainability/live_more_sustainably.html)")

elif selected == "Home":
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Welcome to Recyclapp</p>', unsafe_allow_html=True)
    with st.container():
        col1, col2 =  st.columns([0.6, 0.4])
        with col1:
            st.subheader("I am here to help")
            st.write("###")
            st. write (
                """
                Whether you are a master of recycling or you struggle with finding out where to dispose each item, 
                this app is here to help you understand where to throw away your trash.
                """)
            st.write("###")
            st.write(
                """
                :recycle: Recyclapp will help you to:
                - Correctly classify your waste
                - Keep track of the different types of waste classified
                - Achieve a more sustainable life
                """
			)
            st.write("###")
            st.write(
                """
                :warning: Remember
                - The last "exit" for your waste is recycling
                - There are other steps to consider first, even before buying: refuse, reduce, repair, remake...
                
                You can find more information and ideas in the "Resources" section.
                """
			)
        with col2:
            st_lottie(lottie_recycle, height=400, key="recycle")
    with st.container():
        st.write("---")
        st.write("###")
        st.write("“Every individual matters. Every individual has a role to play. Every individual makes a difference.” ― Jane Goodall")
            
elif selected == "Contact":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
        #st.write('Please help us improve!')
        Name=st.text_input(label='Please Enter Your Name') #Collect user feedback
        Email=st.text_input(label='Please Enter Email') #Collect user feedback
        Message=st.text_input(label='Please Enter Your Message') #Collect user feedback
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.write('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')

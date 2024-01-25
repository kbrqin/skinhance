from bs4 import BeautifulSoup
import streamlit as st
import pickle
import requests

skincare_data = pickle.load(open("skincare_list.pkl", 'rb'))
skincare_list = skincare_data['product_name'].values
similarities = pickle.load(open("similarities.pkl", 'rb'))
ingredients_similarities = pickle.load(open("ingredients_similarities.pkl",'rb'))

st.header("Skinhance - KBeauty Skincare Recommendation System")

desc_expander = st.expander("App Description + How to Use")

app_desc = '''
Welcome to Skinhance! This app helps you find similar skincare products to a product that you are currently using or looking into.

**How to use:**
- Choose a product from the dropdown list. You can search by product, brand, or keyword.
- You will find a list of **Product Recommendations** and **Similar Ingredients**.
- The **Product Recommendations** list recommends products with similar benefits to the chosen product.
- The **Similar Ingredients** list recommends products with similar ingredients to the chosen product.
- The two lists are ordered from most similar to least similar, so the first few products are the most similar, but the further down the list you go, the less related to the chosen product they will be.
- The two lists can be very similar, but this would make sense, since products with similar ingredients will have similar benefits!
'''

desc_expander.write(app_desc)

select_value = st.selectbox("Search product by brand, name, or keyword", skincare_list)
recs_num = st.number_input("How many recommendations would you like?", value=5, step=1, min_value = 1, max_value=343)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0", "Accept-Encoding": "gzip, deflate, br","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "DNT":"1","Connection":"close","Upgrade-Insecure-Requests": "1"}

def recommend(product, n):
    index = skincare_data[skincare_data['product_name']==product].index[0]
    distances = sorted(list(enumerate(similarities[index])), reverse=True, key = lambda vector:vector[1])
    recommended_skincare = []
    recommended_images = []
    if n + 1 < 344:
        n += 1
    else:
        n = 343
    for i in distances[1:n]:
        print(skincare_data.iloc[i[0]].product_name)
        print(skincare_data.iloc[i[0]].url)
        recommended_skincare.append(skincare_data.iloc[i[0]].product_name)
        recommended_images.append(skincare_data.iloc[i[0]].img_link)
    return recommended_skincare, recommended_images

def find_similar_ingredients(product, n):
    index = skincare_data[skincare_data['product_name']==product].index[0]
    distances = sorted(list(enumerate(ingredients_similarities[index])), reverse=True, key = lambda vector:vector[1])
    similar_ingredients_skincare = []
    similar_ingredients_images = []
    if n + 1 < 344:
        n += 1
    else:
        n = 343
    for i in distances[1:n]:
        print(skincare_data.iloc[i[0]].product_name)
        print(skincare_data.iloc[i[0]].url)
        similar_ingredients_skincare.append(skincare_data.iloc[i[0]].product_name)
        similar_ingredients_images.append(skincare_data.iloc[i[0]].img_link)
    return similar_ingredients_skincare, similar_ingredients_images

if st.button("Show Recommendations"):
    skincare_g_names, skincare_g_images = recommend(select_value, recs_num) 
    skincare_si_names, skincare_si_images = find_similar_ingredients(select_value, recs_num) 
    recs_header = st.subheader("Product Recommendations:")
    c1 = st.container()

    for i in range(0, len(skincare_g_names), 5):
        imgsc = c1.container()
        col6, col7, col8, col9, col10 = imgsc.columns(5)
        with col6:
            st.image(skincare_g_images[i])
        with col7:
            if i + 1 < len(skincare_g_names):
                st.image(skincare_g_images[i+1])
        with col8:
            if i + 2 < len(skincare_g_names):
                st.image(skincare_g_images[i+2])
        with col9:
            if i + 3 < len(skincare_g_names):
                st.image(skincare_g_images[i+3])
        with col10:
            if i + 4 < len(skincare_g_names):
                st.image(skincare_g_images[i+4])

        namesc = c1.container()
        col1, col2, col3, col4, col5 = namesc.columns(5)
        with col1:
            st.markdown(skincare_g_names[i])
        with col2:
            if i + 1 < len(skincare_g_names):
                st.markdown(skincare_g_names[i+1])
        with col3:
            if i + 2 < len(skincare_g_names):
                st.markdown(skincare_g_names[i+2])
        with col4:
            if i + 3 < len(skincare_g_names):
                st.markdown(skincare_g_names[i+3])
        with col5:
            if i + 4 < len(skincare_g_names):
                st.markdown(skincare_g_names[i+4])
    
    similar_ingredients_header = st.subheader("Similar Ingredients:")

    c2 = st.container()

    for i in range(0, len(skincare_si_names), 5):
        imgsc = c2.container()
        col6, col7, col8, col9, col10 = imgsc.columns(5)
        with col6:
            st.image(skincare_si_images[i])
        with col7:
            if i + 1 < len(skincare_g_names):
                st.image(skincare_si_images[i+1])
        with col8:
            if i + 2 < len(skincare_g_names):
                st.image(skincare_si_images[i+2])
        with col9:
            if i + 3 < len(skincare_g_names):
                st.image(skincare_si_images[i+3])
        with col10:
            if i + 4 < len(skincare_g_names):
                st.image(skincare_si_images[i+4])

        namesc = c2.container()
        col1, col2, col3, col4, col5 = namesc.columns(5)
        with col1:
            st.markdown(skincare_si_names[i])
        with col2:
            if i + 1 < len(skincare_si_names):
                st.markdown(skincare_si_names[i+1])
        with col3:
            if i + 2 < len(skincare_si_names):
                st.markdown(skincare_si_names[i+2])
        with col4:
            if i + 3 < len(skincare_si_names):
                st.markdown(skincare_si_names[i+3])
        with col5:
            if i + 4 < len(skincare_si_names):
                st.markdown(skincare_si_names[i+4])

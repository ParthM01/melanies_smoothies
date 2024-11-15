# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie",)
st.write("The name on your smoothie Will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df =my_dataframe.to_pandas()

ingredients_select = st.multiselect(
    "Choose upto 5 ingredient",
     my_dataframe
     , max_selections=5
)

if ingredients_select:
    # st.write(ingredients_select)
    # st.text(ingredients_select)
    ingredients_string = ''
    for fruit_chosen in ingredients_select:
        ingredients_string +=  fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information ')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)    
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button("Submit order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# # st.text(smoothiefroot_response.json())
# sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)



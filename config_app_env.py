# Import libraries
from libs_and_modules import *

# ---------------------------------------#
# Function: set_st_bg                    #
# Goal:Set the Background of streamlit   #
# Input: Image file used for backgrouns  #
# Return: None ( VOID )                  #
#----------------------------------------#
def set_st_bg(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
#-----------End of Function "set_st_bg"-----------#

# ------------------------------------------------#
# Function: config_st_page                        #
# Goal: Configure the format of streamlit's page  #
# Input: None                                     #
# Return: None ( VOID )                           #
#-------------------------------------------------#
def config_st_page():
    st.set_page_config(
        page_title="MyCountry - The World In Your Hands",
        page_icon=" ",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.markdown("""
    <style>
        /* Styles for the text inside the input box, making it left-aligned */
        .stTextInput > div > div > input {
            color: black;
            font-weight: bold;
            text-align: left;
        }

        /* Styles for the overall st.text_input container to align its content (label and input field) to the left */
        [data-testid="stTextInput"] {
            width: 100%; /* Ensure it takes full available width within its column */
            display: flex; /* Use flexbox for its children */
            flex-direction: column; /* Stack label and input vertically */
            align-items: flex-start; /* This aligns the children (label, input) to the start (left) */
        }

        /* Styles for the label of the text input, making it left-aligned */
        [data-testid="stTextInput"] label {
            color: white;
            font-weight: bold;
            text-align: left;
            width: 100%; /* Ensure label takes full width for text-align to work within its flex container */
        }

        /* Styles for general st.write output, making it left-aligned */
        [data-testid="stText"] {
            color: white;
            font-weight: bold;
            text-align: left;
        }

        /* Note: The `.main > div` rule has been removed for more targeted styling. */
        /* The `layout="centered"` in st.set_page_config() will center the entire Streamlit app column. */

    </style>
    """, unsafe_allow_html=True)

#-----------End of Function "config_st_page"-----------#

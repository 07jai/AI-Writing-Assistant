
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import requests
from urllib.parse import quote

# LOAD API KEYS
load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
POLLINATIONS_KEY = os.getenv("POLLINATIONS_API_KEY")


# PAGE SETTINGS
st.set_page_config(
    page_title="AI Writing Assistant",
    page_icon="✍️",
    layout="wide"
)


# SESSION STATE
defaults = {
    "history": [],
    "generated_output": "",
    "theme": "Light Mode",
    "last_format": "Markdown",
    "generated_image": None,
    "generated_task": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# GROQ CLIENT
@st.cache_resource
def get_client(api_key):
    if api_key:
        return Groq(api_key=api_key)
    return None


client = get_client(GROQ_KEY)


# IMAGE GENERATION FUNCTION
def generate_image(prompt):

    if not POLLINATIONS_KEY:
        raise Exception(
            "Pollinations API key not found. "
            "Add POLLINATIONS_API_KEY to your .env file."
        )

    encoded_prompt = quote(prompt, safe="")

    url = (
        "https://gen.pollinations.ai/image/"
        + encoded_prompt
    )

    headers = {
        "Authorization": f"Bearer {POLLINATIONS_KEY}"
    }

    params = {
        "model": "black-forest-labs/flux.1-schnell",
        "width": 1024,
        "height": 1024
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=240
    )

    response.raise_for_status()

    content_type = response.headers.get(
        "Content-Type", ""
    )

    if not content_type.startswith("image/"):
        raise Exception(
            "Image service did not return a valid image."
        )

    return response.content


# PROFESSIONAL THEME
with st.sidebar:

    st.title("✍️ AI Assistant")
    st.caption("Intelligent Content Creation Platform")
    st.divider()

    theme = st.radio(
        "🎨 Appearance",
        ["Light Mode", "Dark Mode"],
        key="theme"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        ["Create Content", "History", "About Project"]
    )

    st.divider()

    st.caption("Powered by AI Technology")


# THEME CSS
if theme == "Dark Mode":

    st.markdown("""
    <style>

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #111827 !important;
        color: #f9fafb !important;
    }

    [data-testid="stHeader"] {
        background-color: #111827 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #1f2937 !important;
    }

    [data-testid="stSidebar"] * {
        color: #f9fafb !important;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp [data-testid="stWidgetLabel"],
    .stApp [data-testid="stCaptionContainer"] {
        color: #f9fafb !important;
    }

    .stTextArea textarea,
    .stTextInput input {
        background-color: #374151 !important;
        color: #ffffff !important;
        border: 1px solid #6b7280 !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #d1d5db !important;
    }

    [data-baseweb="select"] > div {
        background-color: #374151 !important;
        border-color: #6b7280 !important;
    }

    [data-baseweb="select"] * {
        color: #ffffff !important;
    }

    [role="listbox"],
    [role="option"] {
        background-color: #374151 !important;
        color: #ffffff !important;
    }

    .stButton button,
    .stDownloadButton button {
        color: #ffffff !important;
    }

    [data-testid="stSlider"] *,
    [data-testid="stRadio"] label {
        color: #f9fafb !important;
    }

    [data-testid="stExpander"] {
        background-color: #1f2937 !important;
        border: 1px solid #4b5563 !important;
    }

    [data-testid="stAlert"] {
        background-color: #374151 !important;
        color: #ffffff !important;
    }

    .stCodeBlock,
    [data-testid="stCodeBlock"] {
        background-color: #1f2937 !important;
    }

    .stCodeBlock code {
        color: #f9fafb !important;
    }

    hr {
        border-color: #4b5563 !important;
    }

    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #f5f7fb !important;
        color: #243b65 !important;
    }

    [data-testid="stHeader"] {
        background-color: #f5f7fb !important;
    }

    [data-testid="stSidebar"] {
        background-color: #e9eef8 !important;
    }

    [data-testid="stSidebar"] * {
        color: #243b65 !important;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp [data-testid="stWidgetLabel"],
    .stApp [data-testid="stCaptionContainer"] {
        color: #243b65 !important;
    }

    .stTextArea textarea,
    .stTextInput input {
        background-color: #ffffff !important;
        color: #243b65 !important;
        border: 1px solid #cbd5e1 !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #64748b !important;
    }

    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
    }

    [data-baseweb="select"] * {
        color: #243b65 !important;
    }

    [role="listbox"],
    [role="option"] {
        background-color: #ffffff !important;
        color: #243b65 !important;
    }

    .stButton button,
    .stDownloadButton button {
        color: #243b65 !important;
    }

    .stButton button[kind="primary"] {
        color: #ffffff !important;
    }

    [data-testid="stSlider"] *,
    [data-testid="stRadio"] label {
        color: #243b65 !important;
    }

    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
    }

    [data-testid="stAlert"] {
        background-color: #e9eef8 !important;
        color: #243b65 !important;
    }

    .stCodeBlock,
    [data-testid="stCodeBlock"] {
        background-color: #ffffff !important;
    }

    .stCodeBlock code {
        color: #243b65 !important;
    }

    hr {
        border-color: #cbd5e1 !important;
    }

    </style>
    """, unsafe_allow_html=True)


# CREATE CONTENT
if page == "Create Content":

    st.title("✍️ AI Writing Assistant")

    st.caption(
        "Create professional content and social media posters with Artificial Intelligence."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        task = st.selectbox(
            "Choose Your Task",
            [
                "Blog Writing",
                "Email Drafting",
                "Code Explanation",
                "Social Media Post"
            ]
        )

    with col2:

        output_format = st.selectbox(
            "Choose Output Format",
            ["Markdown", "Plain Text", "Bullet Points"]
        )

    # REQUIREMENTS
    if task == "Social Media Post":

        details = st.text_area(
            "Enter Your Post Topic",
            placeholder="Example: Create a post about Artificial Intelligence",
            height=130
        )

        st.info(
            "Enter your topic. AI will automatically create a social media poster image."
        )

    else:

        details = st.text_area(
            "Enter Your Requirements",
            placeholder="Example: Write a blog about Artificial Intelligence...",
            height=160
        )

    # CREATIVITY
    creativity = st.slider(
        "Creativity Level",
        0.0, 1.0, 0.7, 0.1
    )

    if creativity < 0.3:
        style = "Use a simple and factual style."
    elif creativity < 0.7:
        style = "Use a balanced and informative style."
    else:
        style = "Use a creative and engaging style."

    st.write("")

    # GENERATE BUTTON
    if st.button(
        "✨ Generate Content",
        type="primary",
        use_container_width=True
    ):

        if not details.strip():

            st.warning("Please enter your requirements.")

        # SOCIAL MEDIA IMAGE GENERATION
        elif task == "Social Media Post":

            try:

                st.session_state.generated_output = ""
                st.session_state.generated_image = None
                st.session_state.generated_task = task

                image_prompt = f"""
                Create a professional and attractive square social media poster
                about: {details}.

                Design requirements:
                - Modern professional graphic design
                - Eye-catching visual composition
                - Relevant illustrations and creative elements
                - Attractive background and balanced layout
                - High quality social media poster
                - Suitable typography and readable text
                - Square 1:1 Instagram-style poster
                - Make the poster visually meaningful for the given topic
                """

                with st.spinner(
                    "AI is creating your social media poster..."
                ):

                    image_bytes = generate_image(image_prompt)

                st.session_state.generated_image = image_bytes

                st.session_state.history.insert(0, {
                    "task": task,
                    "input": details,
                    "output": "AI Social Media Poster generated successfully.",
                    "format": "Image"
                })

                st.success("Your social media poster is ready!")

            except requests.exceptions.HTTPError as e:

                st.error("Image generation request failed.")
                st.code(str(e))

            except requests.exceptions.RequestException as e:

                st.error("Unable to connect to image service.")
                st.code(str(e))

            except Exception as e:

                st.error("Image generation failed.")
                st.code(str(e))

        # OTHER TEXT GENERATION TASKS
        elif client is None:

            st.error(
                "Groq API key not found. Check your .env file."
            )

        else:

            templates = {

                "Blog Writing":
                    "Write a professional blog with title, introduction, headings and conclusion.",

                "Email Drafting":
                    "Write a professional email with subject, greeting, body and closing.",

                "Code Explanation":
                    "Explain the given code in simple English, including purpose, working and output."
            }

            prompt = f"""
            {templates[task]}

            User Requirements: {details}

            Writing Style: {style}

            Output Format: {output_format}

            Give a complete and useful response in simple English.
            """

            try:

                with st.spinner("AI is creating your content..."):

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a helpful AI writing assistant."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=max(creativity, 0.01),
                        max_completion_tokens=2048
                    )

                    result = response.choices[0].message.content

                if result and result.strip():

                    st.session_state.generated_output = result
                    st.session_state.last_format = output_format
                    st.session_state.generated_task = task
                    st.session_state.generated_image = None

                    st.session_state.history.insert(0, {
                        "task": task,
                        "input": details,
                        "output": result,
                        "format": output_format
                    })

                    st.success("Content generated successfully!")

                else:

                    st.warning("AI returned an empty response.")

            except Exception as e:

                error = str(e)
                error_lower = error.lower()

                if "429" in error or "rate_limit" in error_lower:

                    st.error("Groq API rate limit reached.")
                    st.info("Please wait and try again later.")

                elif "401" in error or "authentication" in error_lower:

                    st.error("Invalid API key. Check your GROQ_API_KEY.")

                elif "403" in error:

                    st.error("API access is restricted.")

                else:

                    st.error("Unable to generate content.")
                    st.code(error)


    # SHOW GENERATED IMAGE
    if st.session_state.generated_image:

        st.divider()
        st.subheader("🎨 Your AI Social Media Poster")

        st.image(
            st.session_state.generated_image,
            use_container_width=True
        )

        st.download_button(
            "⬇️ Download Social Media Poster",
            data=st.session_state.generated_image,
            file_name="AI_Social_Media_Poster.jpg",
            mime="image/jpeg",
            use_container_width=True
        )


    # SHOW GENERATED TEXT
    if st.session_state.generated_output:

        st.divider()
        st.subheader("✨ AI Generated Output")

        output = st.session_state.generated_output

        if st.session_state.last_format == "Plain Text":
            st.text(output)
        else:
            st.markdown(output)

        st.subheader("📋 Copy Output")

        st.code(output, language="text")

        st.caption(
            "Use the copy icon in the code block to copy the content."
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.download_button(
                "⬇️ Download TXT",
                data=output,
                file_name="AI_Writing_Output.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col2:

            st.download_button(
                "⬇️ Download MD",
                data=output,
                file_name="AI_Writing_Output.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col3:

            if st.button(
                "🗑️ Clear Output",
                use_container_width=True
            ):

                st.session_state.generated_output = ""
                st.session_state.generated_image = None
                st.session_state.last_format = "Markdown"
                st.rerun()


# HISTORY
elif page == "History":

    st.title("📚 Generation History")
    st.caption("View your previously generated content.")
    st.divider()

    if st.session_state.history:

        for index, item in enumerate(st.session_state.history):

            with st.expander(
                f"{index + 1}. {item['task']}"
            ):

                st.write("Your Input:")
                st.write(item["input"])

                st.write("Generated Output:")

                st.write(item["output"])

                st.download_button(
                    "⬇️ Download This Content",
                    data=item["output"],
                    file_name=f"history_{index + 1}.txt",
                    key=f"download_{index}"
                )

        if st.button("🗑️ Clear History"):

            st.session_state.history = []
            st.session_state.generated_output = ""
            st.session_state.generated_image = None
            st.rerun()

    else:

        st.info(
            "No history available. Generate content first!"
        )


# ABOUT PROJECT
elif page == "About Project":

    st.title("ℹ️ About AI Writing Assistant")
    st.divider()

    st.subheader("Project Overview")

    st.write("""
    AI Writing Assistant is an intelligent content creation platform
    developed using Python and Artificial Intelligence.

    It helps users generate professional blogs, draft emails,
    understand programming code and create social media poster images
    through a simple and user-friendly interface.
    """)

    st.subheader("Key Features")

    st.markdown("""
    - AI-Powered Blog Writing
    - Professional Email Drafting
    - Programming Code Explanation
    - AI Social Media Poster Generation
    - Automatic Image Creation from User Topic
    - Image Preview and Download
    - Adjustable Creativity Level
    - Multiple Output Formats
    - Generation History
    - Download Generated Content
    - Copy and Clear Output
    - Light Mode and Dark Mode
    """)

    st.subheader("Technologies Used")

    st.markdown("""
    - Python
    - Streamlit
    - Groq API
    - Pollinations Image API
    - Requests Library
    - Visual Studio Code
    """)

    st.success(
        "AI Writing Assistant | Intelligent Content Creation Platform"
    )


# FOOTER
st.divider()

st.caption(
    "AI Writing Assistant | Intelligent Content Creation Platform"
)

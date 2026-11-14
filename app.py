
import streamlit as st

import os
from dotenv import load_dotenv
from tavily import TavilyClient
from datetime import date, timedelta
from email.utils import parsedate_to_datetime
from openai import OpenAI
import re
import html
import time

# Page configuration
st.set_page_config(
    page_title="AI Meeting Research Assistant",
    page_icon="🔍"
)



st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eaf0ff, #f5f7ff);
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #10234f;
}

label {
    color: #263653 !important;
    font-weight: 600 !important;
}

/* Company, job role, date and time input boxes */
.stTextInput [data-baseweb="input"] > div,
.stDateInput [data-baseweb="input"] > div,
.stTimeInput [data-baseweb="input"] > div {
    background-color: white !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* Input text */
.stTextInput input,
.stDateInput input,
.stTimeInput input {
    background-color: transparent !important;
    color: #1e293b !important;
    border: none !important;
    border-radius: 8px !important;
}

/* Dropdown */
.stSelectbox [data-baseweb="select"] > div {
    background-color: white !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* Generate button */
.stButton > button {
    background: linear-gradient(90deg, #315ceb, #7045d8) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    opacity: 0.9;
}
/* Date box */
div[data-testid="stDateInput"] [data-baseweb="input"] {
    background: white !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 8px !important;
    min-height: 42px !important;
}

/* Time box */
div[data-testid="stTimeInput"] [data-baseweb="input"] {
    background: white !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 8px !important;
    min-height: 42px !important;
}

/* Meeting purpose box */
div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: white !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 8px !important;
    min-height: 42px !important;
}

/* Text colour */
div[data-testid="stDateInput"] input,
div[data-testid="stTimeInput"] input,
div[data-testid="stSelectbox"] span {
    color: #1e293b !important;
}

/* Dropdown text */
div[data-testid="stSelectbox"] span {
    color: #1e293b !important;
}
/* Inner date and time input boxes */
div[data-testid="stDateInput"] input,
div[data-testid="stTimeInput"] input {
    background-color: white !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    min-height: 40px !important;
}

/* Inner meeting purpose dropdown */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: white !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    min-height: 40px !important;
}
/* 1. More prominent heading */
h1 {
    font-size: 2.7rem !important;
    font-weight: 800 !important;
    color: #10234f !important;
}

/* 2. Visible focus effect on input boxes */
.stTextInput [data-baseweb="input"]:focus-within,
.stDateInput [data-baseweb="input"]:focus-within,
.stTimeInput [data-baseweb="input"]:focus-within {
    border: 2px solid #315ceb !important;
    box-shadow: 0 0 0 3px rgba(49, 92, 235, 0.18) !important;
}

/* 3. More visible outer container shadows */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    box-shadow: 0 4px 15px rgba(30, 50, 90, 0.13) !important;
}

/* 4. Button shadow */
.stButton > button {
    box-shadow: 0 5px 15px rgba(49, 92, 235, 0.3) !important;
    transition: all 0.2s ease;
}

/* 5. Button hover */
.stButton > button:hover {
    transform: translateY(-2px);
    opacity: 0.9;
}
/* Prevent table text from overlapping */
div[data-testid="stMarkdownContainer"] table {
    width: 100% !important;
    table-layout: fixed !important;
    border-collapse: collapse;
}

div[data-testid="stMarkdownContainer"] th,
div[data-testid="stMarkdownContainer"] td {
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
    vertical-align: top;
}

</style>
""", unsafe_allow_html=True)





# Connect to Tavily
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
BIFROST_API_KEY = os.getenv("BIFROST_API_KEY")
if not BIFROST_API_KEY:
    st.error("Bifrost API key not found. Check your .env file.")
    st.stop()
BIFROST_BASE_URL = "http://localhost:8080/v1"
ai_client = OpenAI(
    api_key=BIFROST_API_KEY,
    base_url=BIFROST_BASE_URL
)

if TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
else:
    tavily_client = None

# Application heading

st.markdown("""
<div class="hero">
<h1>AI Meeting Research Assistant</h1>
<p>
Get up-to-date, source-backed research and a focused
meeting briefing for your important meetings.
</p>
<div class="features">
<span>⚡ Real-time Research</span>
<span>📚 Source-backed Insights</span>
<span>🎯 Focused Briefing</span>
<span>📍 AI-powered</span>
</div>
</div>
""", unsafe_allow_html=True)



# Company details
with st.container(border=True):
    company = st.text_input("Enter Company Name *")

with st.container(border=True):
    role = st.text_input("Enter Your Job Role *")





# Meeting date and time

with st.container(border=True):
    meeting_date = st.date_input(
        "Select Meeting Date",
        key="meeting_date"
    )

with st.container(border=True):
    meeting_time = st.time_input(
        "Select Meeting Time",
        key="meeting_time"
    )


# Meeting purpose

meeting_purpose_options = [
    "Job Interview",
    "Sales Meeting",
    "Investor Meeting",
    "Partnership Meeting",
    "Client Meeting",
    "Vendor Meeting",
    "Networking Meeting",
    "Project Discussion",
    "Team Meeting",
    "Business Development Meeting",
    "Performance Review",
    "General Meeting",
    "Other"
]

with st.container(border=True):
    meeting_purpose_choice = st.selectbox(
        "Select Meeting Purpose",
        meeting_purpose_options
    )


# Custom meeting purpose

if meeting_purpose_choice == "Other":
    meeting_purpose = st.text_input(
        "Enter Your Meeting Purpose"
    )
else:
    meeting_purpose = meeting_purpose_choice


# Generate briefing button
if st.button("Generate Briefing"):

    if company.strip() and role.strip() and meeting_purpose.strip():

        st.success("Meeting details submitted successfully!")
        if tavily_client:

            st.subheader("Company Research")

            with st.spinner("Searching the web using Tavily..."):

                try:
                    today = date.today()
                    start_date = (today - timedelta(days=30)).isoformat()
                    end_date = today.isoformat()
                    search_response = tavily_client.search(
                        query=f"{company} company latest announcements products business updates",
                    
                        topic="news",
                        start_date=start_date,
                        end_date=end_date,
                        max_results=5
                    )

                    all_results = search_response.get("results", [])
                    research_text=""

                    results = []

                    for result in all_results:
                        published_date = result.get("published_date")

                        if published_date:
                            try:
                                article_date = parsedate_to_datetime(published_date).date()

                                if start_date <= article_date.isoformat() <= end_date:
                                    results.append(result)

                            except (ValueError, TypeError):
                                continue


                    for result in results:
                        st.write("Title:", result.get("title"))
                        st.write("Published Date:", result.get("published_date", "Date not available"))
                        content = html.unescape(result.get("content", ""))
                        # Remove omitted-text markers such as [...]
                        content = re.sub(r'\[\s*(?:\.{3}|…)\s*\]', '', content)

                        # Remove leftover Markdown heading symbols
                        content = re.sub(r'#{1,6}\s*', '', content)

                        # Remove common website navigation text
                        content = re.sub(
                            r'(?i)\b(Read More|Add ET Logo as a Reliable and Trusted News Source)\b',
                            '',
                            content
                        )

                        # Remove standalone website and social-media labels
                        content = re.sub(
                            r'(?im)^\s*(tweet|share|facebook|advertisement|subscribe)\s*$',
                            '',
                            content
                        )

                        # Remove unwanted special symbols
                        content = re.sub(r'[\uE000-\uF8FF\uFFFD]', '', content)

                        # Clean extra spaces and line breaks
                        content = re.sub(r'\s+', ' ', content).strip()
                        research_text += f"""
                        Title: {result.get('title')}
                        Published Date: {result.get('published_date')}
                        Information: {content}
                        Source: {result.get('url')}
                        """

                        st.write("Information:", content)


                        st.write("Source:", result.get("url"))
                        st.divider()

                    # Ask NVIDIA Nemotron to prepare the meeting briefing
                    st.subheader("Preparing your AI meeting briefing...")
                    nvidia_start = time.perf_counter()

                    response = ai_client.chat.completions.create(
                        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                        messages=[
                            {
                                "role": "system",
                                "content": """
                    You are a professional meeting research assistant.

                    Create a concise and accurate meeting research report.
                    Use only the research provided by Tavily.
                    Never invent facts or unsupported information.
                    Clearly identify uncertain or missing information.
                    Include original source links.
                    Use simple language.
                    """
                            },
                            {
                                "role": "user",
                                "content": f"""
                    Prepare a meeting research report about {company}.

                    Meeting purpose: {meeting_purpose}
                    Job role: {role}
                    IMPORTANT:
Customize the briefing according to the selected meeting purpose and job role.

Do not give a generic briefing.

MEETING PERSONALIZATION:

The selected meeting purpose can be any type of meeting,
including standard options or a custom purpose entered by the user.

Always use the exact meeting purpose provided:
{meeting_purpose}

Adapt the briefing to the actual purpose of the meeting.

Do not restrict the briefing to predefined meeting types.




Also consider the selected job role:
{role}

Make the discussion points and suggested questions
specific to BOTH the meeting purpose and job role.



                    Research collected by Tavily:
                    {research_text}
                    
IMPORTANT MEETING PERSONALIZATION:

Use the exact meeting purpose and job role provided by the user.

Do not produce a generic meeting briefing.

For the AI MEETING BRIEFING section:
- Give at least 5 useful, specific discussion points.
- Give at least 5 relevant questions the user can ask.
- Explain why the research matters for this particular meeting.
- Adapt every discussion point and question to BOTH the meeting purpose and job role.
- For Investor Meetings, focus on financial performance, revenue, growth, risks, and investment opportunities.
- For Job Interviews, focus on role-specific skills, responsibilities, technical knowledge, and interview questions.
- For Networking Meetings, focus on professional introductions, shared interests, industry trends, and possible connections.
- For Partnership Meetings, focus on collaboration, mutual benefits, and possible joint opportunities.
- For other meeting purposes, interpret the user's exact purpose and customize the briefing accordingly.

SOURCE ACCURACY:
- Use only facts supported by the Tavily research.
- Attach the actual source URL to relevant factual claims.
- Never invent a source, URL, date, or statistic.
- If information is missing or uncertain, clearly say so.

OUTPUT:
- Always return all three sections.
- Use these exact headings:
1. COMPANY RESEARCH
2. AI MEETING BRIEFING
3. KEY TAKEAWAYS
- Include at least 5 key takeaways.
- Do not leave empty headings, empty table cells, or unfinished bullet points.
- Use clean Markdown formatting.


                    Organize your answer into three separate sections:

                    1. COMPANY RESEARCH
                    - Company overview
                    - Main products and services
                    - Important recent developments
                    - Industry information

                    2. AI MEETING BRIEFING
                    - Important points before the meeting
                    - Meeting-related discussion topics
                    - Useful questions to ask

                    3. KEY TAKEAWAYS
                    - Five important points to remember
                    - Opportunities and concerns
                    - Information requiring verification

                    Include original source links.
                    Formatting rules:
- Do not use HTML tags such as <br>.
- Use properly formatted Markdown headings and bullet points.
- Do not display raw formatting symbols.
- Keep the output clean and readable.
IMPORTANT: Use these exact headings in your response.
Do not rename, remove, or combine them.

1. COMPANY RESEARCH
2. AI MEETING BRIEFING
3. KEY TAKEAWAYS

Under COMPANY RESEARCH include:
- Company overview
- Main products and services
- Important recent developments
- Industry information

Under AI MEETING BRIEFING include:
- Important points before the meeting
- Meeting-related discussion topics
- Useful questions to ask

Under KEY TAKEAWAYS include:
- Five important points to remember
- Opportunities and concerns
- Information requiring verification
Use these exact headings in the final output:
1. COMPANY RESEARCH
2. AI MEETING BRIEFING
3. KEY TAKEAWAYS
                    """
                            }
                        ],
                        max_tokens=3000,
                        stream=True
                    )

                   # response = ai_client.chat.completions.create(
                    # model="YOUR_EXISTING_MODEL_NAME",
                    # messages=messages,
                    # max_tokens=900,
                    # stream=True
                    #  )























                    st.subheader("Your AI-Generated Meeting Briefing")


                    def generate_response():
                        for chunk in response:
                            content = chunk.choices[0].delta.content
                            if content:
                                yield content


                    briefing = "".join(generate_response())
                    # Clean unwanted HTML and citation artifacts
                    briefing = re.sub(r'<br\s*/?>', '\n', briefing, flags=re.IGNORECASE)
                    briefing = re.sub(r'</?(?:p|div)>', '\n', briefing, flags=re.IGNORECASE)
                    briefing = re.sub(
                        r'\[\d+\s*[†‡]\s*source\]',
                        '',
                        briefing,
                        flags=re.IGNORECASE
                    )
                    briefing = re.sub(r'\s*\[\s*\d+\s*\]', '', briefing)
                    briefing = re.sub(r'\n{3,}', '\n\n', briefing).strip()
                    company_text, sep1, remaining = briefing.partition("2. AI MEETING BRIEFING")

                    meeting_text, sep2, takeaway_text = remaining.partition("3. KEY TAKEAWAYS")

                    if sep1 and sep2:
                        company_section, meeting_section, takeaway_section = st.columns(3)

                        with company_section:
                            st.markdown(company_text)

                        with meeting_section:
                            st.markdown("## 2. AI MEETING BRIEFING\n" + meeting_text)

                        with takeaway_section:
                            st.markdown("## 3. KEY TAKEAWAYS\n" + takeaway_text)

                    else:
                        st.markdown(briefing)

                    nvidia_end = time.perf_counter()
                    st.write(f"AI response time: {nvidia_end - nvidia_start:.2f} seconds")



                except Exception as e:

                    st.error(f"Tavily search failed: {e}")

        else:
            st.error("Tavily API key not found. Please check your .env file.")

        st.write("Company:", company)

        st.write("Meeting Purpose:", meeting_purpose)

        st.write("Job Role:", role)

        st.write("Meeting Date:", meeting_date)

        st.write("Meeting Time:", meeting_time)

    else:

        st.warning("Please enter the company name, job role, and meeting purpose.")

# AI Meeting Research Assistant

An AI-powered meeting research assistant that gathers real-time company information using Tavily and generates personalized meeting briefings using NVIDIA Nemotron through Bifrost.

## 1. Project Overview

The AI Meeting Research Assistant helps professionals prepare for meetings with people from other companies or organizations.

Before a meeting, users can enter a company name, job role and meeting purpose. The application researches relevant company information and generates a structured briefing to help users understand the organization and prepare meaningful discussion points.

## 2. Key Features

- **Company Research:** Collects relevant and up-to-date company information using Tavily.
- **AI Meeting Briefing:** Generates personalized meeting briefings based on the selected company, job role and meeting purpose.
- **Role-Based Research:** Adapts research and briefing content according to the user's job role.
- **Meeting Purpose Analysis:** Provides relevant information based on the objective of the meeting.
- **Key Takeaways:** Highlights important points that users should understand before attending the meeting.
- **Source References:** Uses research sources to support the generated information.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | Web application interface |
| Tavily API | Real-time web research |
| Bifrost | AI gateway and model routing |
| NVIDIA Nemotron | AI-powered briefing generation |
| OpenAI Python SDK | API communication with Bifrost |
| python-dotenv | Environment variable management |

## 4. Project Architecture

The application follows this workflow:

1. User enters company name, job role and meeting purpose.
2. Streamlit collects the input.
3. Tavily searches the web and gathers relevant company information.
4. Research results are passed to the AI model through Bifrost.
5. NVIDIA Nemotron processes the research and generates a personalized meeting briefing.
6. The application displays company research, AI meeting briefing and key takeaways.

## 5. Project Structure

```text
AI-Meeting-Research-Assistant/
│
├── app.py
├── requirements.txt
├── .gitignore
└── .env
```

**Note:** The `.env` file contains private API credentials and should never be uploaded to GitHub.

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- PyCharm or another Python IDE
- Tavily API key
- Bifrost API key and configured AI model

### Step 1: Clone the Repository

```bash
git clone https://github.com/jawahar042007-collab/AI-Meeting-Research-Assistant.git
```

### Step 2: Navigate to the Project

```bash
cd AI-Meeting-Research-Assistant
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project directory.

Add the following configuration:

```env
TAVILY_API_KEY=your_tavily_api_key
BIFROST_API_KEY=your_bifrost_virtual_key
BIFROST_BASE_URL=http://localhost:8080/v1
```

Replace the placeholder values with your own API credentials.

### Step 5: Start Bifrost

Install and launch Bifrost using:

```bash
npx -y @maximhq/bifrost
```

Open the Bifrost dashboard:

```text
http://localhost:8080
```

Configure the AI provider, model and virtual key in the Bifrost dashboard.

### Step 6: Run the Application

Open a terminal in the project directory and execute:

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 7. Implementation

The project is implemented using the following components:

**Frontend – Streamlit**

Provides the user interface for entering company information, selecting job roles and specifying meeting purposes. It displays research results and generated meeting briefings.

**Research Engine – Tavily**

Uses Tavily Search API to gather relevant information from online sources about the selected company.

**AI Processing – NVIDIA Nemotron**

Processes the collected research and generates meeting-related insights, personalized briefings and key takeaways.

**AI Gateway – Bifrost**

Connects the application to the configured AI model through an API-compatible interface and manages model access and routing.

**Backend – Python**

Coordinates user inputs, research collection, AI processing and output generation.

## 8. Expected Output

The application generates three main sections:

1. **Company Research:** Relevant company information and recent developments.
2. **AI Meeting Briefing:** Personalized information based on the company, job role and meeting purpose.
3. **Key Takeaways:** Important discussion points and insights to consider before the meeting.

## 9. Security

- Store API credentials in environment variables.
- Never upload `.env` files to public repositories.
- Keep API keys private.
- Use `.gitignore` to exclude sensitive files.

## 10. Future Enhancements

- Meeting agenda generation.
- Exportable meeting briefing reports.
- Additional AI model integrations.
- Improved source verification and citation handling.
- Support for more meeting types and industries.

## 11. Project Information

**Project Name:** AI Meeting Research Assistant

**Category:** AI Agents & Intelligent Systems

**Problem Statement:** Tavily Research Agent

**Developer:** Jawahar M.S.

---

*AI Meeting Research Assistant – Research smarter. Prepare better. Meet with confidence.*

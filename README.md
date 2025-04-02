# InfoBite - Ai Summarizer

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python 3.10"/>
  <img src="https://img.shields.io/badge/Flask-2.0+-green.svg" alt="Flask 2.0+"/>
  <img src="https://img.shields.io/badge/Google%20Generative%20AI-Gemini-purple.svg" alt="Google Gemini"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/>
</div>

## Overview

**InfoBite** is a web application designed for Mumbai University engineering students to quickly extract key information from educational content. It uses Google's Gemini AI to generate structured, comprehensive summaries from YouTube videos and documents (PDF/PPT), formatted specifically for exam preparation.

![Application Screenshot](https://github.com/KaleKaran/InfoBite/blob/d27e3ebb23d87ad6fceab599b2a523ee9a203266/static/images/Homepage.png)

## Features

- **YouTube Video Summarization**
  - Process YouTube video transcripts using powerful AI
  - Multiple summary formats:
    - Detailed MU-Style Notes with sections for definitions, classifications, diagrams, explanations, and applications
    - Concise 5-10 key points format
    - Custom prompt options for tailored summaries

- **Document Summarization**
  - Extract and summarize content from:
    - PDF files
    - PowerPoint presentations (PPT/PPTX)
  - Structured format with chapter overview, topics breakdown, simplified explanations, and key points

- **AI-Powered Q&A**
  - Interactive chat interface to ask questions about the summarized content
  - Context-aware responses using the full document or video content

- **Smart Diagram Recognition**
  - Automatic identification of diagram needs in educational content
  - Retrieval of relevant images to complement the summary

- **Screenshot Functionality**
  - Take screenshots of summaries for easy sharing and offline reference
  - Clean, formatted output with proper styling and included diagrams

## Tech Stack

- **Backend**: Flask (Python)
- **AI**: Google Generative AI (Gemini 1.5 Flash)
- **Content Processing**:
  - YouTube Transcript API for video transcripts
  - PyPDF2 for PDF processing
  - python-pptx for PowerPoint files
  - Selenium for screenshot capabilities
- **Image Search**: DuckDuckGo Search API
- **Frontend**: HTML, CSS, JavaScript
- **UI Theme**: Dark Purple (#3E2A47)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/infobite.git
   cd infobite
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory with:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   
   > **Note**: You need to obtain a Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   
   Open your browser and go to: `http://localhost:5000`

3. **Using the application**

   - **For YouTube videos**:
     - Paste a YouTube URL
     - Select a prompt option (Default, Concise, or Custom)
     - Click "Get MU-Style Notes"
   
   - **For documents**:
     - Upload a PDF or PPT file
     - Click "Get MU-Style Notes"
   
   - **For both**:
     - After generating notes, use the screenshot button to save a clean copy
     - Use the Q&A chat feature to ask questions about the content

## Project Structure

```
infobite/
│
├── app/                    # Application package
│   ├── __init__.py         # Application factory
│   ├── config/             # Configuration settings
│   │   ├── __init__.py
│   │   └── config.py       # Prompts and API settings
│   │
│   ├── models/             # Data models
│   │   └── __init__.py
│   │
│   ├── routes/             # Route handlers
│   │   ├── __init__.py
│   │   ├── main.py         # Main routes (home, about)
│   │   ├── video.py        # Video processing routes
│   │   └── document.py     # Document processing routes
│   │
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── document.py     # Document processing utilities
│       ├── filters.py      # Template filters
│       ├── images.py       # Image handling utilities
│       ├── screenshot.py   # Screenshot generation utilities
│       ├── summary.py      # Summary generation utilities
│       └── transcript.py   # Transcript extraction utilities
│
├── static/                 # Static assets
│   ├── css/
│   ├── js/
│   ├── images/
│   └── screenshots/        # Storage for generated screenshots
│
├── templates/              # HTML templates
│   ├── index.html
│   ├── result.html
│   ├── document_result.html
│   └── about.html
│
├── temp_images/            # Temporary storage for images
├── uploads/                # Temporary storage for uploaded files
├── app.py                  # Application entry point
└── requirements.txt        # Package dependencies
```

## Use Cases

- **Exam Preparation**: Quickly extract key points from lengthy lecture videos
- **Research Assistance**: Summarize research papers and presentations
- **Study Groups**: Share concise summaries of course materials with screenshots
- **Quick Reviews**: Refresh your understanding of complex topics before exams
- **Day to Day Use**: Reading the Top 10 headlines on Today
  
## Contributors

- [Karan Kale](https://github.com/KaleKaran) -> [LinkedIn](https://www.linkedin.com/in/karan-b-kale-ai-ml-dl/)
- [Gandharava Khedekar](https://github.com/GandharvaChamp) -> [LinkedIn](https://www.linkedin.com/in/gandharva-khedekar/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [Google Generative AI](https://ai.google.dev/) for the powerful AI capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Selenium](https://www.selenium.dev/) for screenshot capabilities
- Mumbai University Engineering Department for inspiration

---

<div align="center">
  <p>If you found this project helpful, please consider giving it a star!</p>
  <p>© 2025 InfoBite. All rights reserved.</p>
</div> 

# AI Summarizer

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/Flask-2.0+-green.svg" alt="Flask 2.0+"/>
  <img src="https://img.shields.io/badge/Google%20Generative%20AI-Gemini-purple.svg" alt="Google Gemini"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/>
</div>

## Overview

**AI Summarizer** is a web application designed for Mumbai University engineering students to quickly extract key information from educational content. It uses Google's Gemini AI to generate structured, comprehensive summaries from YouTube videos and documents (PDF/PPT), formatted specifically for exam preparation.

![Application Screenshot](https://via.placeholder.com/800x400?text=AI+Summarizer+Screenshot) <!-- Replace with your actual screenshot -->

## Features

- **YouTube Video Summarization**
  - Process YouTube video transcripts using powerful AI
  - Multiple summary formats:
    - Detailed notes with sections for definitions, classifications, explanations, and applications
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

- **Beautiful UI**
  - Modern, responsive interface with purple theme
  - Intuitive navigation and user experience

## Tech Stack

- **Backend**: Flask (Python)
- **AI**: Google Generative AI (Gemini 1.5 Flash)
- **Content Processing**:
  - YouTube Transcript API for video transcripts
  - PyPDF2 for PDF processing
  - python-pptx for PowerPoint files
- **Image Search**: DuckDuckGo Search API
- **Frontend**: HTML, CSS, JavaScript

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-summarizer.git
   cd ai-summarizer
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
     - Click "Generate Summary"
   
   - **For documents**:
     - Upload a PDF or PPT file
     - Click "Generate Summary"

## Project Structure

```
ai-summarizer/
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
│       ├── summary.py      # Summary generation utilities
│       └── transcript.py   # Transcript extraction utilities
│
├── static/                 # Static assets
│   ├── css/
│   ├── js/
│   └── images/
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
- **Study Groups**: Share concise summaries of course materials
- **Quick Reviews**: Refresh your understanding of complex topics before exams

## Contributors

- [Karan Kale](https://github.com/KaleKaran) - [LinkedIn](https://www.linkedin.com/in/karan-b-kale-ai-ml-dl/)
- [Gandharav Akhedekar](mailto:gandharavakhedekar236@nhitm.ac.in)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [Google Generative AI](https://ai.google.dev/) for the powerful AI capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework
- Mumbai University Engineering Department for inspiration

---

<div align="center">
  <p>If you found this project helpful, please consider giving it a star!</p>
  <p>© 2025 AI Summarizer. All rights reserved.</p>
</div> 
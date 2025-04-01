from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from app.utils.transcript import extract_transcript
from app.utils.summary import generate_summary
from app.utils.images import determine_diagram_query, download_relevant_images
from app.config.config import PROMPT, CONCISE_PROMPT
import google.generativeai as genai
import os

video_bp = Blueprint('video', __name__)

@video_bp.route('/process_video')
def process_video():
    """
    Process YouTube video and generate summary.
    """
    youtube_link = session.get('youtube_link')
    prompt_option = session.get('prompt_option')
    custom_prompt = session.get('custom_prompt', '')

    if not youtube_link:
        return "Error: No YouTube link provided."

    video_id = youtube_link.split("v=")[-1].split("&")[0]
    thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"

    transcript = extract_transcript(video_id)

    if "Error" in transcript:
        return render_template('result.html',
                               thumbnail_url=thumbnail_url,
                               summary=transcript,
                               images=[],
                               transcript="")

    if prompt_option == "concise":
        summary = generate_summary(transcript, CONCISE_PROMPT)
        images = []
    elif prompt_option == "custom":
        summary = generate_summary(transcript, custom_prompt)
        images = []
    else:
        summary = generate_summary(transcript, PROMPT)
        diagram_query = determine_diagram_query(summary)
        images = download_relevant_images(diagram_query)
        if isinstance(images, str):
            images = []

    if "Error" in summary:
        return render_template('result.html',
                               thumbnail_url=thumbnail_url,
                               summary=summary,
                               images=[],
                               transcript="")

    session['summary'] = summary
    session['images'] = images
    session['current_image_index'] = 0

    return render_template('result.html',
                           thumbnail_url=thumbnail_url,
                           summary=summary,
                           images=images,
                           transcript=transcript,
                           youtube_link=youtube_link)

@video_bp.route('/static/temp_images/<path:filename>')
def serve_image(filename):
    """
    Serve image files from temp directory.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    temp_images_dir = os.path.join(base_dir, 'temp_images')
    return send_from_directory(temp_images_dir, filename)

@video_bp.route('/process_youtube', methods=['POST'])
def process_youtube():
    """
    Process YouTube link from form submission.
    """
    youtube_link = request.form.get('youtube_link')
    prompt_option = request.form.get('prompt_option')
    custom_prompt = request.form.get('custom_prompt', '')

    if youtube_link:
        session['youtube_link'] = youtube_link
        session['prompt_option'] = prompt_option
        session['custom_prompt'] = custom_prompt
        return redirect(url_for('video.process_video'))
    return redirect(url_for('main.home'))

@video_bp.route('/ask_question', methods=['POST'])
def ask_question():
    """
    Answer questions based on document content.
    """
    try:
        data = request.json
        question = data.get('question')
        context = data.get('context')
        summary = data.get('summary')

        if not question or not context:
            return jsonify({
                'error': 'Missing question or context'
            }), 400

        prompt = f"""
        Based on the following document content and its summary, please answer the question.
        If the answer cannot be found in the content, say so.

        Document Summary:
        {summary}

        Full Document Content:
        {context}

        Question: {question}

        Please provide a clear and concise answer, using information from the document.
        If the information is not in the document, respond with "I cannot find information about this in the document."
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if not response.text:
            return jsonify({
                'error': 'No response generated'
            }), 500

        return jsonify({
            'answer': response.text
        })

    except Exception as e:
        print(f"Error in ask_question: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500 
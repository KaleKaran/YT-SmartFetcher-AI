from flask import Blueprint, render_template, request, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    """
    Home page route that handles form submissions.
    """
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link')
        prompt_option = request.form.get('prompt_option')
        custom_prompt = request.form.get('custom_prompt', '')

        if youtube_link:
            session['youtube_link'] = youtube_link
            session['prompt_option'] = prompt_option
            session['custom_prompt'] = custom_prompt
            return redirect(url_for('video.process_video'))
    return render_template('index.html')


@main_bp.route('/about')
def about():
    """
    About page route.
    """
    return render_template('about.html') 
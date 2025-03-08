import markdown

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.youtube_utils import extract_video_id, get_youtube_transcript, get_youtube_thumbnail
from app.utils.summarization import summarize_transcript

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        video_id = extract_video_id(url)
        if not video_id:
            flash('Invalid YouTube URL', 'error')
            return redirect(url_for('main.index'))

        transcript = get_youtube_transcript(url)
        if isinstance(transcript, str) and transcript.startswith("Error"):
            flash(transcript, 'error')
            return redirect(url_for('main.index'))

        summary = summarize_transcript(transcript)
        thumbnail_url = get_youtube_thumbnail(video_id)
        summary_html = markdown.markdown(summary)

        return render_template('summary.html', summary=summary_html, thumbnail_url=thumbnail_url, url=url)

    return render_template('index.html')
from flask import redirect, url_for, current_app

from . import main


@main.route('/jekyll/', methods=['GET'])
def list_all_repositories():
    if not current_app.debug:
        return redirect(url_for('static', filename='welcome.html'))

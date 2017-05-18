from flask import flash, redirect, url_for


def flash_and_redirect_to_index(message, category):
    flash(message, category)
    return redirect(url_for('jekyll.welcome'))

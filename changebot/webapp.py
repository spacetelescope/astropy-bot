import os

from flask import Flask

from werkzeug.contrib.fixers import ProxyFix

from changebot.blueprints.stale_issues import stale_issues
from changebot.blueprints.stale_pull_requests import stale_pull_requests
from changebot.blueprints.pull_request_checker import pull_request_checker

app = Flask('stsci-bot')

app.wsgi_app = ProxyFix(app.wsgi_app)

app.integration_id = int(os.environ['GITHUB_APP_INTEGRATION_ID'])
app.private_key = os.environ['GITHUB_APP_PRIVATE_KEY']
app.cron_token = os.environ.get('CRON_TOKEN', None)
app.stale_issue_close = os.environ.get('STALE_ISSUE_CLOSE', 'FALSE').lower() == 'true'
app.stale_issue_close_seconds = float(os.environ.get('STALE_ISSUE_CLOSE_SECONDS', 'inf'))
app.stale_issue_warn_seconds = float(os.environ.get('STALE_ISSUE_WARN_SECONDS', 'inf'))
app.stale_pull_requests_close = os.environ.get('STALE_PULL_REQUEST_CLOSE', 'FALSE').lower() == 'true'
app.stale_pull_requests_close_seconds = float(os.environ.get('STALE_PULL_REQUEST_CLOSE_SECONDS', 'inf'))
app.stale_pull_requests_warn_seconds = float(os.environ.get('STALE_PULL_REQUEST_WARN_SECONDS', 'inf'))

app.register_blueprint(pull_request_checker)
app.register_blueprint(stale_issues)
app.register_blueprint(stale_pull_requests)


@app.route("/")
def index():
    return '{"message": "Nothing to see here"}'


@app.route("/installation_authorized")
def installation_authorized():
    return '{"message": "Installation authorized"}'

from flask import request, jsonify, render_template, url_for, redirect
from requests.exceptions import HTTPError, ConnectionError, Timeout
from .client import send_write_request, send_retrieve_request

def register_routes(app):

    #################
    #   Home page   #
    #################
    @app.route("/")
    def home():
        return render_template("home.html", title="Welcome to the Poolside Project!")
    
    #################
    #   Write page  #
    #################
    @app.route("/write")
    def write():
        return render_template("write.html", title="Write your string!")
    
    #####################
    #   Retrieve page   #
    #####################
    @app.route("/retrieve")
    def retrieve():
        return render_template("retrieve.html", title="Retrieve your string!")
 
    #####################
    #   Write String    #
    #####################
    @app.route("/write/submit", methods=["POST"])
    def submit():
        skey = request.form.get('skey')
        svalue = request.form.get('svalue')
 
        if not skey or not svalue:
            return jsonify({"error": "A key and value are required"}), 400
 
        try:
            result = send_write_request(key=skey, value=svalue)
        except HTTPError as e:
            return jsonify({"error": f"DB API error: {e.response.text}"}), e.response.status_code
        except (ConnectionError, Timeout):
            return jsonify({"error": "Could not reach the database API"}), 503
 
        return redirect(url_for("write") + "?success=true")
 
    #######################
    #   Retrieve String   #
    #######################
    @app.route("/retrieve/submit", methods=["POST"])
    def fetch():
        skey = request.form.get('skey')
        
        try:
            result = send_retrieve_request(key=skey)
        except HTTPError as e:
            return jsonify({"error": f"DB API error: {e.response.text}"}), e.response.status_code
        except (ConnectionError, Timeout):
            return jsonify({"error": "Could not reach the database API"}), 503
 
        return redirect(url_for("retrieve") + f"?key={result['key']}&value={result['value']}")

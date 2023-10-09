from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os
from werkzeug.utils import secure_filename


def create_app():

    # Create a Flask web application
    app = Flask(__name__)
    app.secret_key = 'h20h20h2igul7ogu0h20123'

    # Define a route to display "Hello, Flask!"
    @app.route('/')
    def hello():
        return render_template("home.html",name='Muneeb', codes = session.keys())

    @app.route('/your_url', methods=['GET', 'POST'])
    def your_url():

        if request.method == 'POST':   
            urls = {}

            if os.path.exists('urls.json'):
                with open('urls.json') as urls_file:
                    urls = json.load(urls_file)

            if request.form['code'] in urls.keys():
                flash("This short name has already been taken. Please choose another one.")

                return redirect(url_for('hello'))

            if 'url' in request.form.keys():

                urls[request.form['code']] = {'url': request.form['url']}

            else:
                f = request.files['file']
                full_name = request.form['code'] + secure_filename(f.filename)
                
                f.save("D:/Flask Practice/url_shortener/static/user_files/" + full_name)
                urls[request.form['code']] = {'file': full_name}

            with open('urls.json', 'w') as url_file:
                json.dump(urls, url_file)
                session[request.form['code']] = True

            return render_template('your_url.html', code=request.form['code'])
        
        else:
            return redirect(url_for('hello'))

    @app.route('/<string:code>')

    def redirect_to_url(code):

        if os.path.exists('urls.json'):

            with open("urls.json") as file:

                urls = json.load(file)

                if code in urls.keys():

                    if 'url' in urls[code].keys():

                        return redirect(urls[code]['url'])
                    
                    else:
                        return redirect(url_for('static', filename = 'user_files/' + urls[code]['file']))

        return abort(404)

    @app.errorhandler(404)
    def page_not_found(error):

        return render_template('page_not_found.html'), 404

    @app.route('/api')
    def session_api():
        return jsonify(list(session.keys()))
    

    return app



if __name__ == '__main__':
    # Run the Flask app
    app = create_app()
    app.run(debug=True)
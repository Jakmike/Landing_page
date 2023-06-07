#!python3

from flask import Flask, render_template, jsonify, request
import random
import requests
r = requests.get('https://www.python.org')

app = Flask(__name__)

# Array of quotes
quotes = (
    "The only way to do great work is to love what you do.",
    "Innovation distinguishes between a leader and a follower.",
    "Life is 10% what happens to us and 90% how we react to it.",
    "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.",
    "Instead of worrying about what you cannot control, shift your energy to what you can create.",
    "I have no special talents. I am only passionately curious.",
    "Be the reason someone smiles. Be the reason someone feels loved and believes in the goodness in people.",
    "Accept yourself, love yourself, and keep moving forward. If you want to fly, you have to give up what weighs you down.",
    "Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine.",
    "You cannot control the behavior of others, but you can always choose how you respond to it.",
    "Success is not how high you have climbed, but how you make a positive difference to the world.",
    "Pursue what catches your heart, not what catches your eyes.",
    "Make improvements, not excuses. Seek respect, not attention.",
    "Start each day with a positive thought and a grateful heart.",
    "Life is about accepting the challenges along the way, choosing to keep moving forward, and savoring the journey.",
    "Never lose hope. Storms make people stronger and never last forever.",
    "Do not fear failure but rather fear not trying.",
    "Do not let the memories of your past limit the potential of your future. There are no limits to what you can achieve on your journey through life, except in your mind.",
    "Stop comparing yourself to other people, just choose to be happy and live your own life.",
    "When you arise in the morning think of what a privilege it is to be alive, to think, to enjoy, to love.",
    "I close my eyes in order to see."
)

# Route to render the index.html template
@app.route('/')
def rootpage():
    return render_template("index.html")


# Route to generate a random quote
@app.route("/random-quote", methods=['GET', 'POST'])
def random_quote():
    quote = random.choice(quotes)
    return jsonify(quote)

# Route to generate quote of the day via search icon
@app.route('/search', methods=['POST'])
def search():
    search_word = request.form.get('search_word')

    if search_word.lower() == 'quote of the day':
        # Make a request to the They Said So Quotes API for the quote of the day
        url = "https://quotes.rest/qod"
        headers = {"X-TheySaidSo-Api-Secret": "bQfClzm6lbrqUKEDB6GZkwsJrLr2r9k1sewSWWr2"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            quote_data = data.get('contents', {}).get('quotes', [])[0]
            quote = quote_data.get('quote')
            author = quote_data.get('author')

            return render_template('result.html', quote=quote, author=author)
        else:
            message = 'Failed to fetch the quote of the day. Please try again.'
            return render_template('error.html', message=message)

    else:
        # Make a request to the They Said So Quotes API with the search word
        url = f"https://quotes.rest/quote/search?category={search_word}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            quotes = data.get('contents', {}).get('quotes', [])

            if quotes:
                # Randomly select a quote from the retrieved quotes
                random_quote = random.choice(quotes)
                quote = random_quote.get('quote')
                author = random_quote.get('author')

                return render_template('result.html', quote=quote, author=author)
            else:
                message = 'No quotes found for the search word.'
        else:
            message = 'Failed to fetch quotes. Please try again.'

        return render_template('error.html', message=message)



# Route to landing page
@app.route('/Home', methods=['GET'])
def landing_page():
    return render_template('landing.html')

# Run the Flask application
if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, sent_tokenize

import nltk

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def summarize_text():
    if request.method == 'POST':
        # Get the input text from the form
        text = request.form['text']

        # Get the number of sentences for the summary from the form
        num_sentences = int(request.form['num_sentences'])

        # Tokenize the text into sentences
        sentences = sent_tokenize(text)

        # Tokenize the text into words
        words = word_tokenize(text)

        # Remove stopwords
        stop_words = set(stopwords.words("english"))
        words = [word for word in words if word.casefold() not in stop_words]

        # Calculate the frequency of each word
        word_frequencies = FreqDist(words)

        # Assign scores to each sentence based on the frequency of words it contains
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            for word in word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    if len(sentence.split()) < 30:
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = word_frequencies[word]
                        else:
                            sentence_scores[sentence] += word_frequencies[word]

        # Sort the sentences in descending order of scores
        sorted_sentences = sorted(
            sentence_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Get the top n sentences
        top_sentences = sorted_sentences[:num_sentences]

        # Combine the top sentences to generate the summary
        summary = " ".join([sentence for sentence, _ in top_sentences])

        return render_template('index.html', summary=summary)

    return render_template('index.html', summary=None)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask_cors import CORS, cross_origin
from collections import Counter
import sys
    #note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
    #from vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

@app.route("/getText", methods=['POST','GET'])
def getText():

    if request.method == 'POST':
        userRequired = {
            'type': '',
            'sentiment': '',
            'positiveNegetiveCount': '',
            'status': ''
        }
        jsonData = request.get_json(force=True)
        textDescription = jsonData['textDescription']
        positiveNegetiveCount=positive_negetive_count(textDescription)

        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(textDescription)
        #print("{:-<65} {}".format(textDescription, str(vs)))

        userRequired = {
            'type': 'sentiment',
            'sentiment':str(vs),
			'positiveNegetiveCount':positiveNegetiveCount,
            'status': 1
        }
        print(userRequired)
        #sys.exit()
        #return jsonify(userValidation)
        #sys.exit()


def positive_negetive_count(paragraph):

    f = open('positive.txt')
    positive = [line.rstrip() for line in f.readlines()]
    f2 = open('negetive.txt')
    negative = [line.rstrip() for line in f2.readlines()]
    polarity = ''
    textSet = ''
    count = Counter(paragraph.split())
    pos = 0
    neg = 0
    positive_negetive_arr=[]
    for key, val in count.items():
        key = key.rstrip('.,?!\n')  # removing possible punctuation signs
        if key in positive:
            pos += val
        if key in negative:
            neg += val


    positive_negetive_arr.append({'pos':pos,'neg':neg})
    return positive_negetive_arr

if __name__=='__main__':
    app.debug = True
    app.run(host="192.168.43.31",port=5000)
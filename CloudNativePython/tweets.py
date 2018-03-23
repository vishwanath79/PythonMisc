from flask import Flask, jsonify,make_response
import json
import sqlite3
app = Flask(__name__)

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

def list_tweets():
    conn = sqlite3.connect('vish.db')
    print('Opened database sucessfully')
    api_list=[]
    cursor = conn.execute("select username, body, tweet_time,id from tweets")
    data = cursor.fetchall()
    if data!= 0:
        for row in cursor:
            tweets = {}
            tweets['tweet by'] = row[0]
            tweets['Body'] = row[1]
            tweets['Timestamp'] = row[2]

            tweets['id'] = row[3]
            api_list.append(tweets)
        else:
            return api_list
    conn.close()
    return jsonify({'tweets_list': api_list})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
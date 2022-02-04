import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from auth import are_same
 
# create a flask app
app = Flask(__name__)
# enable CORS
CORS(app)
# TODO: this program needs "login" and "users" folders and a score.txt file in order to execute correctly


@app.route('/signup/<user_id>', methods=['POST'])
def user(user_id):
    if request.method == 'POST':
        # if recording exists return error
        if os.path.exists(f"users/{user_id}.wav"):
            return jsonify({"error": "user already exists"})
        # extract audio data
        res = request.data.decode("utf-8")
        res = res.replace("data:audio/wav;base64,", "")
        res = str.encode(res)
        # turn base64 into a audio file
        decode_string = base64.b64decode(res)
        with open(f"users/{user_id}.wav", 'wb') as f:
            f.write(decode_string)
        # append a default lowest possible score with the username
        with open(f"score.txt", 'a') as f:
            f.write(f"{user_id} 0\n")
            print(user_id)
            return jsonify({"res": user_id})
    else:
        return jsonify({"error": "error"})


@app.route('/login/<user_id>', methods=['POST'])
def user1(user_id):
    if request.method == 'POST':
        # if user does not exist return error
        if not os.path.exists(f"users/{user_id}.wav"):
            return jsonify({"error": "no such user"})
        res = request.data.decode("utf-8")
        res = res.replace("data:audio/wav;base64,", "")
        res = str.encode(res)
        # extract audio data and store it temporarily to a file
        decode_string = base64.b64decode(res)
        with open(f"login/{user_id}.wav", 'wb') as f:
            f.write(decode_string)
        try:
            # compare voices
            ans = are_same(user_id)
            # remove file from directory
            os.remove(f"login/{user_id}.wav")
            print("Are same", ans)
            # check if the voices are alike enough to be considered the same
            if ans < 0.75:
                return jsonify({"error": "not the same"})
            else:
                return jsonify({"res": user_id})
        except:
            return jsonify({"error": "could not compare"})
    else:
        return jsonify({"error": "error"})


@app.route('/score', methods=['POST', 'GET'])
def user2():
    if request.method == 'POST':
        # POST request for updating a score
        res = request.json
        user_id = res["user_id"]
        score = res["score"]
        # checks if a user exists
        if not os.path.exists(f"users/{user_id}.wav"):
            return jsonify({"error": "no such user"})
        # get the results string
        with open(f"score.txt", 'r') as f:
            lines = f.read().split("\n")
        # write to the results file
        # check if the score is better for the given user and update if it is
        with open(f"score.txt", 'w') as g:
            for i in range(len(lines)):
                if user_id in lines[i]:
                    old_score = int(lines[i].split(" ")[1])
                    print(lines[i])
                    if old_score < score:
                        lines[i] = f"{user_id} {score}"
                    break
            new_str = "\n".join(lines)
            g.write(new_str)
        return jsonify({"res": "res"})
    elif request.method == 'GET':
        # GET request which gives all the results
        res = []
        with open(f"score.txt", 'r') as f:
            for i in f.read().split("\n"):
                if len(i) > 0:
                    line = i.split(" ")
                    res.append({"user_id": line[0], "score": line[1]})
        return jsonify({"res": res})
    else:
        return jsonify({"error": "error"})


# running the server
if __name__ == "__main__":
    app.run(debug=True)


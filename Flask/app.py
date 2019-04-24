import bot
from flask import Flask, request, make_response, render_template

pyBot = bot.Bot()
slack = pyBot.client

app = Flask(__name__)

def _event_handler(event_type, slack_event):
   
    team_id = slack_event["team_id"]

    if event_type == "team_join":
        user_id = slack_event["event"]["user"]["id"]

        pyBot.onboarding_message(team_id, user_id)
        return make_response("Welcome Message Sent", 200,)

    elif event_type == "message" and slack_event["event"].get("attachments"):
        user_id = slack_event["event"].get("user")
        
        if slack_event["event"]["attachments"][0].get("is_share"):
            pyBot.update_share(team_id, user_id)
            
            return make_response("Welcome message updates with shared message",
                                 200,)

    elif event_type == "reaction_added":
        user_id = slack_event["event"]["user"]
        pyBot.update_emoji(team_id, user_id)
        
        return make_response("Welcome message updates with reactji", 200,)

    elif event_type == "pin_added":
        user_id = slack_event["event"]["user"]
        pyBot.update_pin(team_id, user_id)
        
        return make_response("Welcome message updates with pin", 200,)

    message = "You have not added an event handler for the %s" % event_type
    
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/install", methods=["GET"])
def pre_install():
   
    client_id = pyBot.oauth["client_id"]
    scope = pyBot.oauth["scope"]
   
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    
    code_arg = request.args.get('code')
    pyBot.auth(code_arg)
    return render_template("thanks.html")


@app.route("/listening", methods=["GET", "POST"])
def hears():

    slack_event = request.get_json()

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if pyBot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (slack_event["token"], pyBot.verification)
        
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]

        return _event_handler(event_type, slack_event)

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True)
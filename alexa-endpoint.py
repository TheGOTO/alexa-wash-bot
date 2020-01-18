
from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter

import subprocess
import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)


@app.before_request
def log_request():
    app.logger.debug("New Request")
    return None


def read_wm_status():


    query= "sqlite3 /home/pi/devel/wash-bot-alexa-skill/wash-bot.sqlite 'select value from waschmaschine where key=\"is_running\";'"

    p = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    is_running="False"
    for r in p.stdout.readlines():
        is_running=r.decode("utf-8")[:-1]#cut \n
    return is_running

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("Skill Launched by user_id: "+ handler_input.request_envelope.session.user.user_id)

        speak_output = "Guten Tag, hier ist die freundliche Waschmaschine"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



class MessageHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("Messaging.MessageReceived")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("new message")
        speak_output = "New Message"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
class StatusIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StatusIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
		
        is_running=read_wm_status()
		
        print("WM_running:"+is_running)
		
        if is_running ==  "True":
            speak_output = "Die Waschmaschine läuft gerade"
        else:
            speak_output = "Die Waschmaschine läuft gerade nicht"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.



sb = SkillBuilder()
# Register all handlers, interceptors etc.
# For eg : sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StatusIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(MessageHandler())


sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())


handler = sb.lambda_handler()

skill_response = SkillAdapter(skill=sb.create(), skill_id="amzn1.ask.skill.153a3e93-50d5-4821-b7f8-246b4dd0906b", app=app)

skill_response.register(app=app, route="/")


if __name__ == '__main__':

    read_wm_status()
#    app.run(host= '0.0.0.0',ssl_context=('cert.pem', 'privkey.pem'))
    app.run(host= '0.0.0.0',ssl_context=('/home/pi/devel/wash-bot-alexa-skill/self-signed_cert/certificate.pem', '/home/pi/devel/wash-bot-alexa-skill/self-signed_cert/private-key.pem'))
#    app.run()




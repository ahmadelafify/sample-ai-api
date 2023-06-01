from flask import request, make_response
from flask import request, make_response, Blueprint
from pydantic import ValidationError

from api.schemas.prompt_responses import PromptResponse
from api.utils.auth import requires_auth
from api.models.responses import AskAIPayload
from api.utils.openai import get_openai_response


ai_bp = Blueprint('ai', __name__, template_folder='../templates', static_folder="../static")


@ai_bp.route('/history', methods=["GET"])
@requires_auth
def get_openai_history():
    email = request.args.get("email", None)
    if email is None:
        return make_response(f"Invalid email query parameter provided", 400)

    history_query: list[PromptResponse] = PromptResponse.get_all(email=email)
    history = [{"prompt": h.prompt, "response": h.openai_response} for h in history_query]
    return make_response({"results": history}, 200)


@ai_bp.route('/ask', methods=["POST"])
@requires_auth
def ask_open_ai():
    body = request.get_json()
    try:
        payload = AskAIPayload(**body)
    except ValidationError as e:
        return make_response(f"Validation errors with fields: {', '.join([f.get('loc')[0] for f in e.errors()])}", 400)

    openai_response = get_openai_response(prompt=payload.prompt)

    db_entry = PromptResponse(email=payload.email, prompt=payload.prompt,
                              openai_response=openai_response)
    db_entry.persist()

    return make_response({"prompt": payload.prompt, "response": openai_response}, 200)


@ai_bp.route('/clear_history', methods=["DELETE"])
@requires_auth
def clear_ai_history():
    email = request.args.get("email", None)
    if email is None:
        return make_response(f"Invalid email query parameter provided", 400)

    history_query: list[PromptResponse] = PromptResponse.get_all(email=email)
    for prompt in history_query:
        prompt.delete()
    return make_response("Prompt history cleared", 200)

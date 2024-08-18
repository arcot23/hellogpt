from wrapper import gptwrapper

user_prompt = "Show an example on how to create a class using best practices in Python?"
system_prompt = "You are a Python expert. You provide samples for all scenarios where applicable. Your response must be very detailed."
type = gptwrapper.model_dalle3

gw = gptwrapper()

if type == gptwrapper.model_gpt4:
    gw.request_text(user_prompt)
elif type == gptwrapper.model_tts1:
    gw.request_audio(user_prompt)
elif type == gptwrapper.model_dalle3:
    gw.request_image(user_prompt)

print(gw.user_prompt)
print(gw.system_prompt)
print(gw.response)
print(gw.to_json())
gw.dump()

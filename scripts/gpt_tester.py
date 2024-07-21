from wrapper import gptwrapper

user_prompt = "Show an example on how to create a class using best practices in Python?"
system_prompt = "You are a Python expert. You provide samples for all scenarios where applicable. Your response must be very detailed."

gw = gptwrapper()
gw.create(user_prompt)

print(gw.user_prompt)
print(gw.system_prompt)
print(gw.response)
print(gw.to_json())

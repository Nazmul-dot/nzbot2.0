from app.chatbot import ask

print("Professional Chatbot")
print("Type 'exit' to quit.")

while True:

    question = input("\nYou : ")

    if question.lower() == "exit":
        break

    answer = ask(question)

    print("\nBot :", answer)
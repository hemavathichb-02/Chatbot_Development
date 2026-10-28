
import ollama
import csv
import os
from datetime import datetime

history = []
folder = "dataset"

os.makedirs(folder, exist_ok=True)

file = os.path.join(folder, "chat_history.csv")

if not os.path.exists(file):
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "User", "Question", "Response"])

print("Education AI Chatbot")
print("Type 'exit' to stop.\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    history.append({
        "role": "user",
        "content": question
    })

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are an Education AI Chatbot. "
                "Explain academic topics in simple language "
                "with examples. Give clear and helpful answers."
            }
        ] + history
    )

    answer = response["message"]["content"]

    print("Chatbot:", answer, "\n")

    history.append({
        "role": "assistant",
        "content": answer
    })

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, "User", question, answer])

    with open("dataset/chatbot_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\nYou: {question}\n")
        f.write(f"Chatbot: {answer}\n\n")

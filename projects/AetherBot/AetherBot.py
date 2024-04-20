import json, pyjokes, webbrowser, wikipedia, warnings
from difflib import get_close_matches
warnings.filterwarnings("ignore")

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as f:
        data: dict = json.load(f)
    return data

def save_knowledge_base(file_path: str, data: dict) -> None:
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        
def tell_joke() -> str:
    return pyjokes.get_joke(category="all")

def open_site() -> str:
    webbrowser.open("voidigo.github.io")
    return ""

def wiki() -> str:
    wikipedia.set_lang("en")
    query = input("Type a query for wikipedia: ")
    sentences = input("Enter the amount of sentences you wan't the summary to be: ")
    result = wikipedia.summary(query, sentences=sentences)
    return result

def mainloop() -> None:
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")

    print("""AetherBot [Version 1.0]
(c) Voidigo. All rights reserved.
""")

    while True:
        user_input: str = input("You: ")

        if user_input == "quit":
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            for q in knowledge_base["questions"]:
                if q["question"] == best_match:
                    answer: str = q["answer"]
                    function_name: str = q["function"]
                    if function_name:
                        function = globals().get(function_name)
                        if function:
                            answer = function()
                    print(f"AetherBot: {answer}")
                    break
        else:
            print("AetherBot: I don't know the answer. Can you teach me?")
            new_answer: str = input("Type the answer or \"skip\" to skip: ")

            if new_answer.lower() != "skip":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer, "function": ""})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print("AetherBot: Thank you! I learned a new response!")

if __name__ == "__main__":
    mainloop()

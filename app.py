from flask import Flask, render_template, request, jsonify
import pandas as pd
from duckduckgo_search import DDGS
from fuzzywuzzy import fuzz
import wikipedia
import os
import logging
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATASET_FILE = "qa_dataset.csv"


# ---------------- DATASET ---------------- #

def init_dataset():
    if not os.path.exists(DATASET_FILE):
        df = pd.DataFrame(columns=["question","answer","timestamp","source"])
        df.to_csv(DATASET_FILE,index=False)


def load_dataset():
    try:
        return pd.read_csv(DATASET_FILE)
    except:
        return pd.DataFrame(columns=["question","answer","timestamp","source"])


def save_to_dataset(question,answer,source):
    df = load_dataset()

    new_row = pd.DataFrame({
        "question":[question],
        "answer":[answer],
        "timestamp":[datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "source":[source]
    })

    df = pd.concat([df,new_row],ignore_index=True)
    df.to_csv(DATASET_FILE,index=False)


# ---------------- CACHE SEARCH ---------------- #

def find_cached_answer(question,threshold=85):

    df = load_dataset()

    if df.empty:
        return None,0

    best_answer=None
    best_score=0

    for _,row in df.iterrows():

        score = fuzz.ratio(question.lower(),str(row["question"]).lower())

        if score>threshold and score>best_score:
            best_score=score
            best_answer=row["answer"]

    return best_answer,best_score


# ---------------- INTERNET SEARCH ---------------- #

def duckduckgo_search(question):

    try:
        with DDGS() as ddgs:
            results=list(ddgs.text(question,max_results=5))

        if not results:
            return None

        answer=""

        for r in results:
            title=r.get("title","")
            body=r.get("body","")
            link=r.get("href","")

            answer += f"{title}\n{body}\n{link}\n\n"

        return answer[:2000]

    except Exception as e:
        logger.error(e)
        return None


def wikipedia_search(question):

    try:
        summary=wikipedia.summary(question,sentences=3)
        return summary

    except:
        return None


# ---------------- MAIN ANSWER SYSTEM ---------------- #

def get_answer(question):

    cached,similarity=find_cached_answer(question)

    if cached:
        return cached,"cache"

    # DuckDuckGo search
    answer=duckduckgo_search(question)

    if answer:
        save_to_dataset(question,answer,"duckduckgo")
        return answer,"duckduckgo"

    # Wikipedia fallback
    answer=wikipedia_search(question)

    if answer:
        save_to_dataset(question,answer,"wikipedia")
        return answer,"wikipedia"

    return "Sorry, I couldn't find an answer on the internet.","none"


# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask",methods=["POST"])
def ask():

    data=request.json
    question=data.get("question","").strip()

    if question=="":
        return jsonify({"answer":"Please enter a question."})

    answer,source=get_answer(question)

    return jsonify({
        "answer":answer,
        "source":source
    })


@app.route("/stats")
def stats():

    df=load_dataset()

    return jsonify({
        "total_questions":len(df),
        "unique_questions":df["question"].nunique()
    })


# ---------------- RUN ---------------- #

if __name__=="__main__":

    init_dataset()

    app.run(debug=True,port=5000)
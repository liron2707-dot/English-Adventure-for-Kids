import random

# הגדרות בסיסיות: 99 שלבים, 8 שאלות לשלבים
LEVELS = 99
QUESTIONS_PER_LEVEL = 8

# דוגמאות מלאי מילים לפי קבוצת גיל (יש להרחיב)
VOCAB = {
    "7-9": ["apple","cat","dog","ball","book","sun","hat","milk","fish","car"],
    "10-12": ["planet","adventure","museum","science","battery","camera","forest","island","mountain","ocean"],
    "13-15": ["economy","environment","technology","philosophy","biography","hypothesis","strategy","evidence","analysis","perspective"]
}

GRAMMAR_TEMPLATES = [
    {"type":"fill_blank","template":"I ____ to school yesterday.","answer":"went"},
    {"type":"choose_correct","template":"Choose the correct past form of 'go'","options":["goed","went","goes"],"answer":"went"},
    {"type":"sentence_order","template":"Order: 'to / like / I / swim'","answer":"I like to swim"}
]

READING_PROMPTS = [
    {"text":"Sara has a red kite. She plays at the park every Sunday.","question":"What color is Sara's kite?","answer":"red"}
]

VIDEO_PROMPTS = [
    {"title":"Short clip about animals","question":"Which animal can fly?","options":["Cat","Bird","Dog"],"answer":"Bird"}
]

def generate_question(age_group, difficulty=None):
    qtype = random.choice(["vocab","grammar","reading","mini_game","video"])
    if qtype == "vocab":
        word = random.choice(VOCAB[age_group])
        choices = random.sample(VOCAB[age_group], k=3)
        if word not in choices:
            choices[0] = word
        random.shuffle(choices)
        return {"type":"vocab","prompt":f"Which word matches the picture?", "word":word, "choices":choices, "answer":word}
    if qtype == "grammar":
        gm = random.choice(GRAMMAR_TEMPLATES)
        return {"type":"grammar","prompt":gm["template"], "answer":gm["answer"], "options": gm.get("options", None)}
    if qtype == "reading":
        rp = random.choice(READING_PROMPTS)
        return {"type":"reading","prompt":rp["text"], "question":rp["question"], "answer":rp["answer"]}
    if qtype == "video":
        vp = random.choice(VIDEO_PROMPTS)
        return {"type":"video","prompt":vp["title"], "question":vp["question"], "choices":vp["options"], "answer":vp["answer"]}
    # mini_game placeholder
    return {"type":"mini_game","prompt":"Match the pairs quickly!", "answer":None}

def get_stage_questions(age_group, stage):
    # מבוסס על random seed כדי להחזיר אותו באופן יציב אם רוצים
    random.seed(f"{age_group}-{stage}")
    qs = [generate_question(age_group) for _ in range(QUESTIONS_PER_LEVEL)]
    return qs

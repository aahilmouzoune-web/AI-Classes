# ---------------------------------------------------------------
# Step 1: The sentiment lexicon (word -> points) and helper words
# ---------------------------------------------------------------
LEXICON = {
    "good": 2, "great": 3, "amazing": 3, "love": 3, "fast": 1, "worth": 2,
    "awesome": 3, "excellent": 3, "nice": 2, "perfect": 3,
    "bad": -2, "terrible": -3, "slow": -1, "broke": -2, "disappointed": -2,
    "awful": -3, "hate": -3, "poor": -2, "useless": -3,
}
NEGATIONS = {"not", "no", "never", "hardly"}
INTENSIFIERS = {"very": 2, "really": 2, "so": 2, "extremely": 3}
USE_BUT_RULE = False          # "Break it" fix 1: words after "but" count double
USE_NEGATION_WINDOW = False   # "Break it" fix 2: "not" only reaches the next few words
NEGATION_WINDOW = 3
PUNCTUATION = ".,!?:;\"'()"
# ---------------------------------------------------------------
# Step 2: Clean a word and spot negations (not, never, don't...)
# ---------------------------------------------------------------
def clean_word(word):
    return word.lower().strip(PUNCTUATION)
def is_negation(word):
    # endswith catches don't, isn't, wasn't...
    return word in NEGATIONS or word.endswith("n't")
# ---------------------------------------------------------------
# Step 3: Walk through the review and give every word its points
# ---------------------------------------------------------------
def analyse(review):
    """Return a list of (original_word, points) pairs."""
    pairs = []
    negate_for = 0     # how many more words the last negation still covers
    boost = 1          # multiplier set by an intensifier like "very"
    but_weight = 1     # becomes 2 after "but" when USE_BUT_RULE is on
    for original in review.split():
        word = clean_word(original)
        points = 0
        if is_negation(word):
            negate_for = NEGATION_WINDOW if USE_NEGATION_WINDOW else 999
            pairs.append((original, 0))
            continue
        if word == "but" and USE_BUT_RULE:
            but_weight = 2
        elif word in INTENSIFIERS:
            boost = INTENSIFIERS[word]
        elif word in LEXICON:
            points = LEXICON[word] * boost * but_weight
            if negate_for > 0:
                points = -points
            negate_for, boost = 0, 1
        negate_for = max(0, negate_for - 1)
        pairs.append((original, points))
    return pairs
# ---------------------------------------------------------------
# Step 4: Total score and final mood
# ---------------------------------------------------------------
def mood_score(review):
    return sum(points for _, points in analyse(review))
def classify(review):
    score = mood_score(review)
    if score >= 1:
        return "POSITIVE"
    if score <= -1:
        return "NEGATIVE"
    return "NEUTRAL"
# ---------------------------------------------------------------
# Step 5: Test on reviews where we already know the right answer
# ---------------------------------------------------------------
TEST_REVIEWS = [
    ("Amazing phone, I love the camera", "POSITIVE"),
    ("Terrible battery and very slow charging", "NEGATIVE"),
    ("The delivery was fast and the packing was good", "POSITIVE"),
    ("This is not good at all", "NEGATIVE"),
    ("Not bad for the price", "POSITIVE"),
    ("It arrived on Tuesday in a blue box", "NEUTRAL"),
    ("The screen is great but the battery life is terrible", "NEGATIVE"),
    ("Great, it broke on day one", "NEGATIVE"),
    ("I never thought it would be this good, totally worth it", "POSITIVE"),
    ("Really disappointed, the strap broke in a week", "NEGATIVE"),
]
def run_tests():
    correct = 0
    for review, expected in TEST_REVIEWS:
        result = classify(review)
        mark = "OK" if result == expected else "XX"
        correct += result == expected
        print(f"{mark}  {result:<8}  score={mood_score(review):>3}  {review}")
    print(f"\nAccuracy: {correct}/{len(TEST_REVIEWS)}")
# ---------------------------------------------------------------
# Step 6: Check any review live
# ---------------------------------------------------------------
if __name__ == "__main__":
    run_tests()
    print("\nType a review to check it, or 'quit' to stop.")
    while True:
        review = input("\n> ")
        if review.strip().lower() == "quit":
            break
        scored = [(w, p) for w, p in analyse(review) if p != 0]
        print(f"{classify(review)} | score: {mood_score(review)} | words: {scored}")
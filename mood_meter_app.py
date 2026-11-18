"""
Review Mood Meter web page (Gradio). Step 8 of the activity.
Keep this file in the same folder as mood_meter.py.
Run:  python mood_meter_app.py   then open http://127.0.0.1:7860
Do not use launch(share=True): it makes a public link to your computer.
"""
import gradio as gr
from mood_meter import analyse, classify, mood_score
# The colour of each kind of word. Try changing "lightgreen" or "salmon" (step 8).
COLORS = {"positive": "lightgreen", "negative": "salmon"}
def check(review):
    # Gradio calls this function every time someone presses Submit.
    # It returns one value for each output box below, in the same order.
    pieces = []
    for word, points in analyse(review):
        if points > 0:
            label = "positive"
        elif points < 0:
            label = "negative"
        else:
            label = None
        pieces.append((word + " ", label))
    return classify(review), mood_score(review), pieces
demo = gr.Interface(
    fn=check,
    inputs=gr.Textbox(lines=3, label="Paste a review"),
    outputs=[
        gr.Textbox(label="Mood"),
        gr.Number(label="Mood score"),
        gr.HighlightedText(label="Which words decided it?", color_map=COLORS),
    ],
    title="Review Mood Meter",
    description="Green words add points and red words take points away. Total 1 or more is POSITIVE, -1 or less is NEGATIVE.",
    examples=[
        ["Amazing phone, I love the camera"],
        ["This is not good at all"],
        ["The screen is great but the battery life is terrible"],
    ],
)
if __name__ == "__main__":
    demo.launch()

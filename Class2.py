import importlib

try:
    if importlib.util.find_spec("colorama") is None:
        raise ImportError
    colorama = importlib.import_module("colorama")
    Fore = colorama.Fore
    Style = colorama.Style
    colorama.init()
except Exception:
    class _DummyFore:
        CYAN = MAGENTA = YELLOW = GREEN = RED = BLUE = ""

    class _DummyStyle:
        RESET_ALL = ""

    Fore = _DummyFore()
    Style = _DummyStyle()

try:
    if importlib.util.find_spec("textblob") is None:
        raise ImportError
    TextBlob = importlib.import_module("textblob").TextBlob
except Exception:
    # Fallback simple sentiment analyzer if textblob is not installed
    class _Sentiment:
        def __init__(self, polarity: float):
            self.polarity = polarity

    class TextBlob:
        def __init__(self, text: str):
            self._text = text or ""

        @property
        def sentiment(self):
            # Very small heuristic: count positive/negative words
            pos_words = {"good", "great", "happy", "love", "excellent", "awesome", "nice", "pleasant", "fantastic"}
            neg_words = {"bad", "sad", "terrible", "hate", "awful", "worst", "horrible", "angry", "poor"}
            words = [w.strip(".,!?;:\"'()[]") for w in self._text.lower().split() if w.strip()]
            if not words:
                return _Sentiment(0.0)
            pos = sum(1 for w in words if w in pos_words)
            neg = sum(1 for w in words if w in neg_words)
            polarity = (pos - neg) / len(words)
            # clamp to [-1,1]
            if polarity > 1:
                polarity = 1.0
            if polarity < -1:
                polarity = -1.0
            return _Sentiment(polarity)
print(f"{Fore.CYAN}Welcome to Sentiment Spy!{Style.RESET_ALL}")
user_name=input(f"{Fore.MAGENTA}Please Enter Your Name:{Style.RESET_ALL}").strip()
if not user_name:
    user_name="Mystery Agent"
conversation_history=[]
print(f"\n{Fore.CYAN}Hello,Agent {user_name}!")
print(f"Type a Sentence and I will analyze yor sentence with textblob and  show you the sentiment of your sentiment")
print(f"Type {Fore.YELLOW}reset{Fore.CYAN},{Fore.YELLOW}History{Fore.CYAN},"f"or {Fore.YELLOW}exit{Fore.CYAN} to quit{Style.RESET_ALL}\n")
while True:
    user_input=input(f"{Fore.Green}>>{Style.RESET_ALL}").strip()
    if not user_input:
        print(f"{Fore.RED}Please enter a valid command.{Style.RESET_ALL}")
        continue
    if user_input.lower()=="exit":
        print(f"\n{Fore.BLUE}Exiting Sentiment Spy. Farewell, Agent {user_name}!{Style.RESET_ALL}")
        break
    elif user_input.lower()=="reset":
        conversation_history.clear()
        print(f"{Fore.CYAN}All conversation his tory cleared!{Style.RESET_ALL}")
        continue
    elif user_input.lower()=="history":
        if not conversation_history:
            print(f"{Fore.YELLOW}No conversation history available.{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}Conversation History:{Style.RESET_ALL}")
            for idx,(text,polarity,sentiment_type)in enumerate(conversation_history,start=1):
                if sentiment_type=="positive":
                    sentiment_color=Fore.GREEN
                    emoji="😊"
                elif sentiment_type=="negative":
                    sentiment_color=Fore.RED
                    emoji="😞"
                else:
                    sentiment_color=Fore.YELLOW
                    emoji="😐"
                print(f"{idx}.{sentiment_color}{emoji} {text}"f" - Polarity: {polarity:.2f}, Sentiment: {sentiment_type}{Style.RESET_ALL}")
        continue
    else:
        polarity=TextBlob(user_input).sentiment.polarity
        if polarity>0.25:
            sentiment_type="positive"
            color=Fore.GREEN
            emoji="😊"
        elif polarity<-0.25:
            sentiment_type="negative"
            color=Fore.RED
            emoji="😞"
        else:
            sentiment_type="neutral"
            color=Fore.YELLOW
            emoji="😐"
        conversation_history.append((user_input,polarity,sentiment_type))
        print(f"{color}{emoji} {sentiment_type} sentiment detected - Polarity Score: {polarity:.2f}{Style.RESET_ALL}")
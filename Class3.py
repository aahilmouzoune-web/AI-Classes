import re,random
from colorama import Fore,init
init(autoreset=True)
destination ={
    "Beaches":["Bali","Maldives","Phuket"],
    "Mountains":["Swiss Alps","Rocky Mountains","Himalayas"],
    "Cities":["New York","Tokyo","Paris"],
}
jokes =["Why don't programmers like nature? It has too many bugs!",
        "Why did the computer go to the doctor? Because it caught a virus!",
        "Why do travelers always feel warm? Because of all their hot spots!"]
def normalize_input(text):
    return re.sub(r"\s+","", text.strip().lower())
def recomend():
    print(Fore.CYAN + "TravelBot: Beaches,Mountains,Cities")
    preference = input(Fore.Yellow + "You:")
    preference = normalize_input(preference)
    if preference in destination:
        suggestion =random.choice(destination[preference])
        print(Fore.GREEN + f"TravelBot: How about {suggestion}?")
        print(Fore.CYAN + "TravelBot:Do you like it? (yes/no)")
        answer=input(Fore.YELLOW + "You:").lower()
        if answer=="yes":
            print(Fore.GREEN + f"TravelBot: Awesome! Enjoy {suggestion}!")
        elif answer=="no":
            print(Fore.RED + f"TravelBot:Let's try another")
            recomend()
        else:
            print(Fore.RED + "TravelBot: I'll suggest again")
            recomend()
    else:
        print(Fore.RED + "TravelBot: Sorry, I don't have that type of destination.")
        recomend()
def packing_tips():
    print(Fore.CYAN + "TravelBot: Where to? ")
    location=normalize_input(input(Fore.YELLOW + "You:"))
    print(Fore.CYAN + "TravelBot: How many days?")
    days=input(Fore.YELLOW + "You:")
    print(Fore.GREEN + f"TravelBot: Packing tips for {location} for {days} days: ")
    print(Fore.GREEN +"- Pack versatile clothing")
    print(Fore.GREEN +"- Don't forget chargers and adapters")
    print(Fore.GREEN +"-Check the weather forecast")
def tell_joke():
    print(Fore.YELLOW +"TravelBot:"
    "{random.choice(jokes)}")
def show_help():
    print(Fore.MAGENTA + "TravelBot:\nI Can:")
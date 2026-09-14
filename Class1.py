print("Hello! I am a AI Bot. What is your name? :")
#Get user Input
name=input()
#Respond to the user's name
print(f"Nice to meet you,{name}!")
#Ask a Question
print("How are you feeling today?(Good/Bad):")
mood=input().lower()
#Use coditional Statement To Respond Based On Input
if mood=="good":
    print("I am glad to hear that!")
elif mood=="Bad":
    print("I am sorry tohear that.Hope things get better soon.")
else:
    print("I see somtimes it's hard to put fellings into words")
    
print(f"It was nice chatting with you {name}.Goodbye")
comments = open("total_comments.log", "r")
infections = open("total_infections.dedupe4.log", "r")

act_comments = [cmt.strip().split("\t") for cmt in comments.readlines()]
print(len(act_comments), "comments loaded")

act_infections = [inf.strip().split("\t") for inf in infections.readlines()]
print(len(act_infections), "infections loaded")

user = None

while True:
    new_user = input("User {}: ".format("" if not user else f"({user})"))
    if new_user == "":
        new_user = user
    for inf in act_infections:
        if inf[1] == new_user:
            print(inf[3], inf)
            user = inf[3]

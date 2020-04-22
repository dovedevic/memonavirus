comments = open("total_comments.log", "r")

act_comments = [cmt.strip().split("\t") for cmt in comments.readlines()]
print(len(act_comments), "comments loaded")

while True:
    search_for = input("User : ")
    for com in act_comments:
        if com[1] == search_for:
            print(com)

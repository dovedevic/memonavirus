import json, datetime

comments = open("../total_comments.log", "r")
infections = open("../total_infections.dedupe3.log", "r")


act_comments = [cmt.strip().split("\t") for cmt in comments.readlines()]
print(len(act_comments), "comments loaded")

act_infections = [inf.strip().split("\t") for inf in infections.readlines()]
print(len(act_infections), "infections loaded")


with open("../manual_fixes.json", "r") as fp:
    users = json.load(fp)


def find_infection_for(usr):
    for inf in act_infections:
        if inf[1] == usr:
            return inf
    return None

records = []
for user in users:
    u_cmts = users[user]
    u_cmts.reverse()
    found = False
    for cmt in u_cmts:
        result = find_infection_for(f"u/{cmt[2]}")
        # If not found, parent wasnt infected. If was, check times
        if result and cmt[0] < result[0].split(".")[0] and cmt[3] == "C":
            new_record = [
                cmt[0] + ".000000",
                user,
                cmt[1],
                result[1],
                result[2],
                "C"
            ]
            print("\t".join(new_record))
            records.append(new_record)
            found = True
            break
    if not found:
        print("No fix found for", user)

for record in records:
    act_infections.append(record)

input()

print("Sorting...")
act_infections = sorted(act_infections, key=lambda x: x[0])
print("Saving...")
with open("../total_infections.dedupe4.log", "w") as fp:
    for com in act_infections:
        fp.write("\t".join(com) + "\n")

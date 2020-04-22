comments = open("../total_comments.log", "r")
valid_infections = open("../total_infections.dedupe.log", "r")

act_comments = [cmt.strip().split("\t") for cmt in comments.readlines()]
print(len(act_comments), "comments loaded")

act_infections = [inf.strip().split("\t") for inf in valid_infections.readlines()]
print(len(act_infections), "infections loaded")


def verify_in_stream(i_log, last_idx):
    offset = 0
    for c_log in act_comments[last_idx:]:
        offset += 1
        if i_log[1] == c_log[1] and i_log[2] == c_log[2]:
            return True, last_idx + offset
    return False, last_idx


current_infection = set()
current_infection.add("u/woodendoors7")
# Ignore woodendoors7
last_index = 0
inf_stat = 0
for infection in act_infections[1:]:
    inf_stat += 1
    verified, last_index = verify_in_stream(infection, last_index)
    if not verified:
        print("\t".join(infection), "has no log in the comments")
    if inf_stat % 10000 == 0:
        print("processed", inf_stat, "infections")

print("Done.")

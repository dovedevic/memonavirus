comments = open("../total_comments.log", "r")
valid_infections = open("../total_infections.dedupe5.log", "r")

act_comments = [cmt.strip().split("\t") for cmt in comments.readlines()]
print(len(act_comments), "comments loaded")

act_infections = [inf.strip().split("\t") for inf in valid_infections.readlines()]
print(len(act_infections), "infections loaded")


current_infection = set()
current_infection.add("u/woodendoors7")

not_logged_infections = []
not_logged_infectors = set()
# Ignore woodendoors7
for infection in act_infections[1:]:
    try:
        if infection[3] not in current_infection and infection[3] not in not_logged_infectors:
            not_logged_infections.append(infection)
            not_logged_infectors.add(infection[3])
            print("\t".join(infection), "infected by someone not already infected")
    except:
        print(infection)
        raise Exception
    current_infection.add(infection[1])

input()
act_comments.reverse()
fixes = {}
no_fixes = []
for nli in not_logged_infections:
    # Search Comments for a potential fix
    found = False
    for cmt in act_comments:
        # skip to timestamp minimum
        if cmt[0] > nli[0]:
            continue
        if nli[3] == cmt[1] and nli[3] != cmt[3] and cmt[6] == "I" and cmt[5] == "C":
            # Found a potential fix
            if nli[3] in fixes:
                if cmt[0] < fixes[nli[3]][0]:
                    print("UPDATED FIX FOR nli=", "\t".join(nli), "FIX=", "\t".join([cmt[0], cmt[1], cmt[2], cmt[3], cmt[4], cmt[5]]))
                    fixes[nli[3]] = [cmt[0], cmt[1], cmt[2], cmt[3], cmt[4], cmt[5]]
            else:
                print("FIX FOR nli=", "\t".join(nli), "FIX=", "\t".join([cmt[0], cmt[1], cmt[2], cmt[3], cmt[4], cmt[5]]))
                fixes[nli[3]] = [cmt[0], cmt[1], cmt[2], cmt[3], cmt[4], cmt[5]]
            found = True
            break
    if not found:
        print("NO FIX FOR nli=", "\t".join(nli))

input()

for fix in fixes:
    print("\t".join(fixes[fix]))

input()

for fix in fixes:
    act_infections.append(fixes[fix])

print("Sorting...")
act_infections = sorted(act_infections, key=lambda x: x[0])
print("Saving...")
with open("../total_infections.dedupe4.log", "w") as fp:
    for inf in act_infections:
        fp.write("\t".join(inf) + "\n")

for nf in no_fixes:
    print("\t".join(nf))

print("Done.")

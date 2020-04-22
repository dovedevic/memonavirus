import os

comments = open("../total_comments.log", "r")
infections = open("../total_infections.dedupe4.log", "r")
enum_infections = [inf.strip().split("\t") for inf in infections.readlines()]

valid_infections = open("../total_infections.dedupe5.log", "w")
deduped_infections = set()
infectors = set()

deduped_infections.add("u/woodendoors7")
valid_infections.write("\t".join(enum_infections[0]) + "\n")

line = 2
dupes = 0
for inf in enum_infections[1:]:
    if inf[1] in deduped_infections or inf[1] == inf[3]:
        print(f"Duped at line \t{line}\t: " + "\t".join(inf))
        dupes += 1
    elif inf[1] in infectors:
        print(f"Found infection past prior infect at line \t{line}\t: " + "\t".join(inf))
        dupes += 1
    else:
        valid_infections.write("\t".join(inf) + "\n")
        deduped_infections.add(inf[1])
        infectors.add((inf[3]))
    line += 1

print(f"Found {dupes} dupes!")

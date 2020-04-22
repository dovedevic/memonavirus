import os

past_infection_files = ["../../data/" + f for f in os.listdir("../../data") if f.startswith("memes_infections") and f.endswith(".log")]
past_comment_files = ["../../data/" + f for f in os.listdir("../../data") if f.startswith("memes_comments") and f.endswith(".log")]

total_infection_file = []
total_comment_file = []

print("Gathering infections...")
for pif in past_infection_files:
    with open(pif, "r") as fp:
        for line in fp.readlines():
            total_infection_file.append(line.strip().split('\t'))

print("Sorting...")
total_infection_file = sorted(total_infection_file, key=lambda x: x[0])
print("Saving...")
with open("total_infections.log", "w") as fp:
    for inf in total_infection_file:
        fp.write("\t".join(inf) + "\n")

print("Gathering comments...")
for pcf in past_comment_files:
    with open(pcf, "r") as fp:
        for line in fp.readlines():
            total_comment_file.append(line.strip().split('\t'))

print("Sorting...")
total_comment_file = sorted(total_comment_file, key=lambda x: x[0])
print("Saving...")
with open("total_comments.log", "w") as fp:
    for com in total_comment_file:
        fp.write("\t".join(com) + "\n")

print("Done.")

import datetime

comments = open("../clean_up/total_comments.log", "r")
infections = open("../../data/clean/total_infections.log", "r")

act_comments = [cmt.strip().split("\t") for cmt in comments.readlines()]
print(len(act_comments), "comments loaded")

act_infections = [inf.strip().split("\t") for inf in infections.readlines()]
print(len(act_infections), "infections loaded")

infected_users = set()
for ai in act_infections:
    infected_users.add(ai[1])

print()
print()

# Infection analysis
infs = dict()
infs_time = dict()
infs['u/woodendoors7'] = 0
infs_time['u/woodendoors7'] = '2020-03-20 19:59:59.0'
sub_infs = 0
for inf in act_infections[1:]:
    if inf[3] not in infs:
        infs[inf[3]] = 0
    if inf[1] not in infs_time:
        infs_time[inf[1]] = inf[0]
    infs[inf[3]] += 1
    if inf[5] == "S":
        sub_infs += 1
infs = {k: v for k, v in sorted(infs.items(), key=lambda item: item[1], reverse=True)}

# Comment analysis
coms = dict()
users = set()
risk_taker = dict()
uninf_commenter = dict()
active = set()
inf_noninf = [0, 0]
infsubs_noninfsubs = [0, 0]
first_comm = dict()
for com in act_comments:
    if com[1] not in coms:
        coms[com[1]] = 0
    coms[com[1]] += 1
    if coms[com[1]] == 5:
        active.add(com[1])
    if com[5] == "S" and com[6] == "I" and com[1] not in infected_users:
        if com[1] not in risk_taker:
            risk_taker[com[1]] = 0
        risk_taker[com[1]] += 1
    elif com[1] in infected_users and com[1] in risk_taker:
        del risk_taker[com[1]]
    if com[1] not in infected_users:
        if com[1] not in uninf_commenter:
            uninf_commenter[com[1]] = 0
        uninf_commenter[com[1]] += 1
    elif com[1] in infected_users and com[1] in uninf_commenter:
        del uninf_commenter[com[1]]
    inf_noninf[0 if com[6] == "I" else 1] += 1
    if com[5] == "S":
        infsubs_noninfsubs[0 if com[6] == "I" else 1] += 1
    if com[1] not in first_comm:
        first_comm[com[1]] = com[0]
    users.add(com[1])
coms = {k: v for k, v in sorted(coms.items(), key=lambda item: item[1], reverse=True)}
risk_taker = {k: v for k, v in sorted(risk_taker.items(), key=lambda item: item[1], reverse=True)}
uninf_commenter = {k: v for k, v in sorted(uninf_commenter.items(), key=lambda item: item[1], reverse=True)}

time = 0
for inf in infs_time:
    if inf in first_comm:
        first = datetime.datetime.strptime(first_comm[inf], '%Y-%m-%d %H:%M:%S.%f')
        last = datetime.datetime.strptime(infs_time[inf], '%Y-%m-%d %H:%M:%S.%f')
        time += (last - first).total_seconds()
time = time / len(infs_time.keys())

print("Top 10 infectors are:")
stop = 10
for k in infs:
    print('\t', k, '\t', infs[k])
    stop -= 1
    if stop <= 0:
        break

print("Top 10 commentors are:")
stop = 10
for k in coms:
    print('\t', k, '\t', coms[k])
    stop -= 1
    if stop <= 0:
        break

print("Top 10 risk takers are:")
stop = 10
for k in risk_taker:
    print('\t', k, '\t', risk_taker[k])
    stop -= 1
    if stop <= 0:
        break

print("Top 10 uninf commentors are:")
stop = 10
for k in uninf_commenter:
    print('\t', k, '\t', uninf_commenter[k])
    stop -= 1
    if stop <= 0:
        break

print("Total infections", len(act_infections))
print("Total comments", len(act_comments))
print("Infection %", 100 * len(act_infections) / len(act_comments))
print("Active People", len(active))
print("Active Infected", len([a for a in active if a in infected_users]))
print("Active UnInfected", len([a for a in active if a not in infected_users]))
print("Total users", len(users))
print("Sub Infections", sub_infs)
print("Total Risk Takers", sum(risk_taker.values()))
print("Infected Comments vs NonInfected", inf_noninf)
print("Submission Infected Comments vs NonInfected", infsubs_noninfsubs)
print("Infs avg time =", time)

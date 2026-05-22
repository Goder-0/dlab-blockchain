choices = ["지민", "서준", "하린"]

# TODO 1) 아래 표를 바꿔보세요.
votes = [
    ("민수", "지민"),
    ("민수", "서준"),
    ("서연", "유나"),
    ("지우", "하린"),
]

voted_names = []
accepted = []
rejected = []
count = {"지민": 0, "서준": 0, "하린": 0}

for voter, choice in votes:
    if voter == "":
        rejected.append((voter, choice, "이름이 비어 있음"))
    elif choice not in choices:
        rejected.append((voter, choice, "없는 후보"))
    elif voter in voted_names:
        rejected.append((voter, choice, "중복 투표"))
    else:
        accepted.append((voter, choice))
        voted_names.append(voter)
        count[choice] = count[choice] + 1

print("[채택된 표]")
for item in accepted:
    print(item)

print()
print("[거절된 표]")
for item in rejected:
    print(item)

print()
print("[현재 집계]")
print(count)

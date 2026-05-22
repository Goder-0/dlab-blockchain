import hashlib


def make_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# TODO 1) choice2를 다른 선택지로 바꿔보세요.
voter = "민수"
choice1 = "지민"
choice2 = "서준"

vote1 = voter + ":" + choice1
vote2 = voter + ":" + choice2

print("[1] 같은 기록은 같은 해시가 나옵니다.")
print(make_hash(vote1))
print(make_hash(vote1))
print()

print("[2] 선택지를 바꾸면 해시가 달라집니다.")
print("vote1 =", vote1)
print("hash1 =", make_hash(vote1))
print()
print("vote2 =", vote2)
print("hash2 =", make_hash(vote2))

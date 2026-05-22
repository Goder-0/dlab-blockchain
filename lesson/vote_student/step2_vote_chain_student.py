import hashlib


def make_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


vote1 = "민수:지민"
hash1 = make_hash(vote1)

vote2 = "서연:서준"
hash2 = make_hash(vote2 + "|" + hash1)

print("[1] 첫 번째 기록")
print("vote1 =", vote1)
print("hash1 =", hash1)
print()

print("[2] 두 번째 기록은 첫 번째 해시도 함께 사용합니다.")
print("vote2 =", vote2)
print("hash2 =", hash2)
print()

# TODO 1) changed_vote1 값을 바꿔보세요.
changed_vote1 = "민수:하린"
changed_hash1 = make_hash(changed_vote1)
changed_hash2 = make_hash(vote2 + "|" + changed_hash1)

print("[3] 첫 번째 기록을 바꾸면 뒤의 해시도 달라집니다.")
print("changed_vote1 =", changed_vote1)
print("changed_hash1 =", changed_hash1)
print("changed_hash2 =", changed_hash2)

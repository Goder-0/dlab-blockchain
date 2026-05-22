def simple_hash(text):
    return len(text)


# TODO 1) 아래 두 문자열을 바꿔보세요.
text1 = "민수:지민"
text2 = "민수:서준"

print("[1] 내가 만든 아주 단순한 해시 함수")
print("text1 =", text1)
print("hash1 =", simple_hash(text1))
print()
print("text2 =", text2)
print("hash2 =", simple_hash(text2))
print()

print("[2] 다른 문자열인데 같은 값이 나올 수도 있습니다.")
a = "ab"
b = "cd"
print("a =", a, "->", simple_hash(a))
print("b =", b, "->", simple_hash(b))
print()

print("[3] 지금 함수는 글자 수만 세기 때문에 너무 단순합니다.")
print("그래서 실제 시스템은 더 복잡한 해시 함수를 씁니다.")

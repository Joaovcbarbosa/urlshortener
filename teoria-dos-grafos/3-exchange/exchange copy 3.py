# Python3 program to print all combinations of size
# k of elements in set 1..n
ans = []
tmp = []

def makeCombiUtil(n, left, k):
  # Pushing this vector to a vector of vector
  if (k == 0):
    ans.append(tmp)
    for i in range(len(tmp)):
      print(tmp[i], end = " ")
    print()
    return

  # i iterates from left to n. First time
  # left will be 1
  for i in range(left, n + 1):
    tmp.append(i)
    makeCombiUtil(n, i + 1, k - 1)

    # Popping out last inserted element
    # from the vector
    tmp.pop()

# Prints all combinations of size k of numbers
# from 1 to n.
def makeCombi(n, k):
  makeCombiUtil(n, 1, k)
  return ans

# given number
n = 3
k = 3
ans = makeCombi(n, k)

# This code is contributed by divyeshrabadiya07.

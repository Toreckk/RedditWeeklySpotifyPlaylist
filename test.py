import re

text = "Juan Atkins - Beat Track [Electronic][Hip Hop][Hip House][House][Techno] (1987)"
data = re.split(r"^([^:(]+?)(\s*[[(])", text)
print(data[1])
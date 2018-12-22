
def remove_parentheses(html):
  paren_count = 0
  bracket_count = 0
  result = ""
  for char in html:
    if char == '<':
      bracket_count += 1
    elif char == '>':
      bracket_count -= 1
    elif char == '(' and bracket_count == 0:
      paren_count += 1
    elif char == ')' and bracket_count == 0:
      paren_count -= 1
      continue
    if paren_count == 0:
      result += char
  return result

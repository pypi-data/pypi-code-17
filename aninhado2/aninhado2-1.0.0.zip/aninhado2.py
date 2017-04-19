def print_lol(uma_lista):
  for cada_item in uma_lista:
    if isinstance(cada_item,list):
      print_lol(cada_item)
    else:
      print(cada_item)

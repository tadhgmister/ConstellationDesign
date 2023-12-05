import markdown
text = """
<html>
 <head>
  <meta name="color-scheme" content="light dark">
 </head>
<body>
{}
</body>
</html>
"""
with open("README.md", "r") as f:
    print(text.format(markdown.markdown(f.read())))

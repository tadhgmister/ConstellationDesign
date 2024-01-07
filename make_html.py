import markdown
text = """
<html>
 <head>
  <meta name="color-scheme" content="light dark">
  
  {mathconfig}
 </head>
<body>
{}
</body>
</html>
"""
# config for mathjax as described by https://pypi.org/project/python-markdown-math/
mathconfig_for_mdx_math_extension = """
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js">
</script>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  config: ["MMLorHTML.js"],
  jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
  extensions: ["MathMenu.js", "MathZoom.js"]
});
</script>
"""
mathconfig_mathjax_3 = """
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
  <script id="MathJax-script" async
          src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
  </script>
"""
mathconfig = mathconfig_mathjax_3
md = markdown.Markdown()#extensions=["mdx_math"])
with open("README.md", "r") as f:
    print(text.format(md.convert(f.read()), mathconfig=mathconfig))

    

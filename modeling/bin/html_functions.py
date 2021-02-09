from IPython.display import display, HTML #improve visuals

def ez_display(html_text):
    if isinstance(html_text,list):
        for t in html_text:
            try: 
                display(HTML(t))
            except:
                display(HTML(str(t)))
    else:
        display(HTML(html_text))
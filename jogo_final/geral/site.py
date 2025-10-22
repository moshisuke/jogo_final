num=0
def abrir_site():
    global num
    if not num>0:
        import webbrowser

        # Caminho para o arquivo HTML
        html_file_path = 'D:\python\jogo_final\geral\site_empresa\index.html'

        # Abre o arquivo HTML no navegador padrão
        webbrowser.open('file://' + html_file_path)
        num+=1

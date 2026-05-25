import PyPDF2
import sys
import os
from pathlib import Path


def converter_pdf_para_txt(caminho_pdf, caminho_saida=None):
    """
    Converte um arquivo PDF para TXT.
    
    Args:
        caminho_pdf (str): Caminho para o arquivo PDF de entrada
        caminho_saida (str): Caminho para o arquivo TXT de saída (opcional)
    
    Returns:
        bool: True se a conversão foi bem-sucedida, False caso contrário
    """
    try:
        # Verificar se o arquivo PDF existe
        if not os.path.exists(caminho_pdf):
            print(f"Erro: O arquivo '{caminho_pdf}' não foi encontrado.")
            return False
        
        # Se o caminho de saída não foi fornecido, usar o mesmo nome com extensão .txt
        if caminho_saida is None:
            caminho_saida = os.path.splitext(caminho_pdf)[0] + '.txt'
        
        # Abrir o arquivo PDF
        with open(caminho_pdf, 'rb') as arquivo_pdf:
            leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
            numero_paginas = len(leitor_pdf.pages)
            
            print(f"Convertendo '{caminho_pdf}' ({numero_paginas} páginas)...")
            
            # Extrair texto de todas as páginas
            texto_completo = ""
            for numero_pagina in range(numero_paginas):
                pagina = leitor_pdf.pages[numero_pagina]
                texto = pagina.extract_text()
                texto_completo += f"\n--- Página {numero_pagina + 1} ---\n"
                texto_completo += texto
        
        # Salvar o texto em um arquivo TXT
        with open(caminho_saida, 'w', encoding='utf-8') as arquivo_txt:
            arquivo_txt.write(texto_completo)
        
        print(f"✓ Conversão concluída com sucesso!")
        print(f"✓ Arquivo salvo em: '{caminho_saida}'")
        return True
        
    except Exception as erro:
        print(f"Erro durante a conversão: {erro}")
        return False


def processar_multiplos_pdfs(diretorio):
    """
    Processa todos os arquivos PDF em um diretório.
    
    Args:
        diretorio (str): Caminho do diretório contendo os PDFs
    """
    try:
        caminho = Path(diretorio)
        
        if not caminho.exists():
            print(f"Erro: O diretório '{diretorio}' não existe.")
            return
        
        # Encontrar todos os arquivos PDF
        arquivos_pdf = list(caminho.glob('*.pdf'))
        
        if not arquivos_pdf:
            print(f"Nenhum arquivo PDF encontrado em '{diretorio}'")
            return
        
        print(f"Encontrados {len(arquivos_pdf)} arquivo(s) PDF(s)\n")
        
        # Processar cada PDF
        for arquivo_pdf in arquivos_pdf:
            converter_pdf_para_txt(str(arquivo_pdf))
            print()
    
    except Exception as erro:
        print(f"Erro ao processar diretório: {erro}")


def main():
    """
    Função principal que processa argumentos da linha de comando.
    """
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_pdf> [arquivo_saida.txt]")
        print("     python main.py --dir <diretório>")
        print("\nExemplos:")
        print("  python main.py documento.pdf")
        print("  python main.py documento.pdf saida.txt")
        print("  python main.py --dir ./pdfs/")
        return
    
    if sys.argv[1] == '--dir':
        # Processar todos os PDFs em um diretório
        if len(sys.argv) < 3:
            print("Erro: Especifique o diretório após '--dir'")
            print("Uso: python main.py --dir <diretório>")
            return
        processar_multiplos_pdfs(sys.argv[2])
    else:
        # Processar um único PDF
        arquivo_pdf = sys.argv[1]
        arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else None
        converter_pdf_para_txt(arquivo_pdf, arquivo_saida)


if __name__ == '__main__':
    main()

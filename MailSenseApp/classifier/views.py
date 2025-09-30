import json
from django.shortcuts import render
from django.conf import settings
# Importações do App local:
from .forms import EmailForm
from .utils import pre_process_text, extract_text_from_file
from google import genai 


SYSTEM_INSTRUCTION = """
Você é um assistente de classificação e resposta de emails para uma grande empresa do setor financeiro. 
Sua tarefa é estritamente analisar um email e classificá-lo em uma das duas categorias: 
'Produtivo' (requer ação específica, como solicitação de status, dúvida ou suporte, emails corporativos) 
ou 'Improdutivo' (não requer ação, como agradecimento, felicitação, spam ou mensagens informais).
Mensagens automáticas, como confirmações de leitura ou respostas automáticas, também são 'Improdutivas'.

Após a classificação, você deve gerar uma 'resposta_sugerida' em português, apropriada para a categoria identificada.

A saída deve ser APENAS um objeto JSON válido, sem qualquer texto adicional ou explicação.

O formato JSON obrigatório é:
{
    "categoria": "CLASSIFICAÇÃO", 
    "resposta_sugerida": "TEXTO DA RESPOSTA EM PORTUGUÊS APROPRIADA"
}
"""

def classify_email(request):
    form = EmailForm()
    results = None
    
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        
        if form.is_valid():
            email_content = form.cleaned_data.get('email_text')
            email_file = form.cleaned_data.get('email_file')

            if email_file:
                # 1. Leitura do Conteúdo do Arquivo
                email_content = extract_text_from_file(email_file)

            if email_content:
                
                # 2. PRÉ-PROCESSAMENTO OBRIGATÓRIO (Requisito de NLP)
                processed_content = pre_process_text(email_content)
                
                # 3. Chamada à API de IA usando o texto processado
                try:
                    # Inicializa o cliente com a chave de settings
                    client = genai.Client(api_key=settings.GEMINI_API_KEY)
                    
                    # O prompt foca apenas no conteúdo que a IA deve analisar.
                    # As regras de classificação já estão na SYSTEM_INSTRUCTION.
                    prompt = f"Analise o seguinte texto limpo e pré-processado:\n---\n{processed_content}\n---"
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config={
                            # CORREÇÃO: Usa a variável local SYSTEM_INSTRUCTION
                            "system_instruction": SYSTEM_INSTRUCTION, 
                            "response_mime_type": "application/json"
                        }
                    )
                    
                    # 4. Processar a Resposta JSON
                    results = json.loads(response.text.strip())
                    
                    # Opcional: Adicionar o conteúdo original e processado aos resultados
                    results['original_email'] = email_content 
                    results['processed_text'] = processed_content 
                    
                except Exception as e:
                    # Trata erros de API, autenticação ou parsing de JSON
                    results = {"error": f"Erro na API de IA. Detalhe: {e}"}
            
    context = {
        'form': form,
        'results': results
    }
    return render(request, 'classification_form.html', context)
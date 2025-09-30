import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
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
    
    # Inicializa o histórico na sessão se não existir
    if 'classification_history' not in request.session:
        request.session['classification_history'] = []
    
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
                            "system_instruction": SYSTEM_INSTRUCTION, 
                            "response_mime_type": "application/json"
                        }
                    )
                    
                    # 4. Processar a Resposta JSON
                    results = json.loads(response.text.strip())

                    # Adicionar informações extras aos resultados
                    results['original_email'] = email_content 
                    results['processed_text'] = processed_content
                    results['timestamp'] = timezone.now().isoformat()
                    results['preview'] = email_content[:100] + '...' if len(email_content) > 100 else email_content

                    # Normaliza categoria
                    categoria_norm = results.get('categoria', '').strip().lower()
                    is_produtivo = (categoria_norm == 'produtivo')
                    is_improdutivo = (categoria_norm == 'improdutivo')

                    # Adiciona ao histórico na sessão (mantém apenas os últimos 10)
                    history = request.session['classification_history']
                    history.insert(0, {
                        'categoria': results.get('categoria', 'Desconhecida'),
                        'preview': results['preview'],
                        'timestamp': results['timestamp'],
                        'resposta_sugerida': results.get('resposta_sugerida', ''),
                        'processed_text': results.get('processed_text', '')
                    })

                    # Mantém apenas os últimos 10 itens no histórico
                    if len(history) > 10:
                        history = history[:10]

                    request.session['classification_history'] = history
                    request.session.modified = True
                    
                except Exception as e:
                    # Trata erros de API, autenticação ou parsing de JSON
                    results = {"error": f"Erro na API de IA. Detalhe: {e}"}

            return redirect('classify')
    
    # Obtém o histórico da sessão para o template
    classification_history = request.session.get('classification_history', [])
    
    context = {
        'form': form,
        'results': results,
        'classification_history': classification_history,
        'is_produtivo': is_produtivo if results else False,
        'is_improdutivo': is_improdutivo if results else False,
    }
    return render(request, 'classification_form.html', context)

def clear_history(request):
    if 'classification_history' in request.session:
        request.session['classification_history'] = []
        request.session.modified = True
    return redirect('classify')
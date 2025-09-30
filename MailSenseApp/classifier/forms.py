from django import forms

class EmailForm(forms.Form):
    """
    Define o formulário web para receber o conteúdo do email, 
    permitindo input via texto ou upload de arquivo.
    """
    
    # Campo 1: Para colar o texto do email diretamente
    email_text = forms.CharField(
        # Define o campo como uma área de texto grande (Textarea)
        widget=forms.Textarea(attrs={
            'rows': 10, 
            'placeholder': 'Cole o conteúdo do e-mail aqui (Assunto + Corpo)...',
            'class': 'form-control' # Classe para estilização (Bootstrap, etc.)
        }),
        required=False, # Não é obrigatório se o arquivo for enviado
        label="1. Inserir Conteúdo do E-mail"
    )
    
    # Campo 2: Para upload de arquivo
    email_file = forms.FileField(
        required=False, # Não é obrigatório se o texto for colado
        label="2. Ou fazer upload de arquivo (.txt ou .pdf)"
    )

    # --- Lógica de Validação Customizada ---
    
    def clean(self):
        """
        Garante que pelo menos um dos campos (texto ou arquivo) foi preenchido.
        """
        # Chama a validação padrão do Django
        cleaned_data = super().clean()
        
        email_text = cleaned_data.get('email_text')
        email_file = cleaned_data.get('email_file')

        # Verifica se ambos os campos estão vazios
        if not email_text and not email_file:
            # Se nenhum dado foi fornecido, levanta um erro de validação
            raise forms.ValidationError(
                "Por favor, cole o texto do e-mail *ou* faça o upload de um arquivo.",
                code='no_input_provided'
            )
        
        # Opcional: Validação de tipo de arquivo
        if email_file:
            filename = email_file.name.lower()
            if not filename.endswith(('.txt', '.pdf')):
                 raise forms.ValidationError(
                    "Formato de arquivo não suportado. Use .txt ou .pdf.",
                    code='invalid_file_type'
                )

        return cleaned_data
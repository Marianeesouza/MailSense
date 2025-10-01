function copyResponse() {
            const responseText = document.getElementById('suggested-response-text').innerText;
            navigator.clipboard.writeText(responseText).then(() => {
                const btn = document.querySelector('.suggested-response .copy-btn');
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Copiado!';
                btn.style.backgroundColor = '#28a745';
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.backgroundColor = '';
                }, 2000);
            }).catch(err => {
                console.error('Falha ao copiar:', err);
                alert("Erro ao copiar o texto. Tente novamente.");
            });
        }

        function copySidebarResponse(responseText, button) {
            navigator.clipboard.writeText(responseText).then(() => {
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-check"></i> Copiado!';
                button.style.backgroundColor = '#28a745';
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.backgroundColor = '';
                }, 2000);
            }).catch(err => {
                console.error('Falha ao copiar:', err);
                alert("Erro ao copiar o texto. Tente novamente.");
            });
        }

        document.addEventListener('DOMContentLoaded', function() {
            const fileInput = document.querySelector('input[type="file"]');
            const fileButton = document.querySelector('.file-input-button');
            
            if (fileInput && fileButton) {
                fileInput.addEventListener('change', function() {
                    if (this.files && this.files[0]) {
                        fileButton.innerHTML = `<i class="fas fa-file"></i> ${this.files[0].name}`;
                        fileButton.style.borderColor = '#4361ee';
                        fileButton.style.color = '#4361ee';
                    } else {
                        fileButton.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> Clique para selecionar um arquivo de e-mail';
                        fileButton.style.borderColor = '';
                        fileButton.style.color = '';
                    }
                });
            }
        });

        const modal = document.getElementById('responseModal');
        const closeModal = document.querySelector('.close-modal');
        const modalResponseSection = document.getElementById('modalResponseSection');

        function openModal(category, fullResponse, emailContent) {
            console.log('Abrindo modal com categoria:', category);
            console.log('Resposta completa:', fullResponse);
            console.log('Conteúdo do e-mail:', emailContent);

            const modalCategory = document.getElementById('modalCategory');
            const modalEmailContent = document.getElementById('modalEmailContent');
            const modalFullResponse = document.getElementById('modalFullResponse');
            const modalResponseSection = document.getElementById('modalResponseSection');
            
            // Define a classe baseada na categoria
            modalCategory.className = 'result-box';
            const categoryLower = category.toLowerCase().trim();
            
            if (categoryLower === 'produtivo') {
                modalCategory.classList.add('produtivo');
                modalCategory.innerHTML = `
                    <h3 class="result-header"><i class="fas fa-check-circle"></i> Classificação: ${category.toUpperCase()}</h3>
                    <p><strong>Ação Necessária:</strong> Requer atenção e ação específica da equipe.</p>
                `;
                // Mostra a seção de resposta
                modalResponseSection.style.display = 'block';
                modalFullResponse.textContent = fullResponse;
            } else if (categoryLower === 'improdutivo') {
                modalCategory.classList.add('improdutivo');
                modalCategory.innerHTML = `
                    <h3 class="result-header"><i class="fas fa-info-circle"></i> Classificação: ${category.toUpperCase()}</h3>
                    <p><strong>Ação Necessária:</strong> Não requer ação imediata. Mensagem de cortesia/informativa.</p>
                `;
                // Esconde a seção de resposta para improdutivo
                modalResponseSection.style.display = 'none';
            } else {
                modalCategory.classList.add('error');
                modalCategory.innerHTML = `
                    <h3 class="result-header"><i class="fas fa-question-circle"></i> Classificação: ${category.toUpperCase()}</h3>
                    <p><strong>Ação Necessária:</strong> Categoria não reconhecida.</p>
                `;
                modalResponseSection.style.display = 'block';
                modalFullResponse.textContent = fullResponse;
            }
            
            modalEmailContent.textContent = emailContent;
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }

        function closeModalFunc() {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }

        function copyModalResponse() {
            const responseText = document.getElementById('modalFullResponse').innerText;
            navigator.clipboard.writeText(responseText).then(() => {
                const btn = document.querySelector('.modal-body .copy-btn');
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Copiado!';
                btn.style.backgroundColor = '#28a745';
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.backgroundColor = '';
                }, 2000);
            });
        }

        closeModal.addEventListener('click', closeModalFunc);
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModalFunc();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.style.display === 'block') {
                closeModalFunc();
            }
        });


        // Modo Escuro
        const themeToggle = document.getElementById('themeToggle');
        const currentTheme = localStorage.getItem('theme') || 'light';

        // Aplicar tema salvo
        if (currentTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i><span>Modo Claro</span>';
        }

        // Toggle do tema
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            
            if (currentTheme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                themeToggle.innerHTML = '<i class="fas fa-moon"></i><span>Modo Escuro</span>';
                localStorage.setItem('theme', 'light');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                themeToggle.innerHTML = '<i class="fas fa-sun"></i><span>Modo Claro</span>';
                localStorage.setItem('theme', 'dark');
            }
        });
# 🌆Urban Tech

Projeto desenvolvido como solução de software para problemas urbanos, utilizando o framework Flask (Python). A aplicação tem como objetivo oferecer uma interface web para cadastro, visualização e gestão de dados relacionados a questões urbanas.


Funcionalidades
- Sistema de rotas com Flask
- Interface web responsiva com HTML/CSS
- Organização MVC (Model-View-Controller)
- Estrutura modular com controllers, models, views e utils

Tecnologias
- Python 3
- Flask
- HTML5, CSS3
- JavaScript
- Jinja2

Estrutura do Projeto
```
urbantech/
├── app.py              # Arquivo principal da aplicação Flask
├── controllers/        # Lógica de controle (rotas, requisições)
├── models/             # Estrutura de dados e objetos da aplicação
├── views/              # Templates HTML
├── static/             # Arquivos estáticos (CSS, JS, imagens)
└── utils/              # Funções auxiliares
```

Como executar

- Clone o repositório:
```
git clone https://github.com/maricastroo/Urban-Tech.git
cd Urban-Tech/urbantech
```

- Crie um ambiente virtual:
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

- Instale as dependências:
```
pip install flask
```

- Execute
```
python app.py
```

- Acesse no navegador
```
http://localhost:5000
```

Desenvolvido por:
- Alex Menegatti Secco
- Mariana de Castro
- Tarso Bertolini Rodrigues

Como parte de um projeto acadêmico para a disciplina de Experiência Criativa

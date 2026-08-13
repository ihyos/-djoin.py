
# 🤖 AUTO !DJOIN - Discord Automation

Uma ferramenta em **Python com interface via CMD** desenvolvida para automatizar o fluxo de execução periódica do comando `!djoin` em um servidor específico do Discord.

O projeto foi criado para eliminar a necessidade de digitar manualmente o mesmo comando após cada período de cooldown.

---

## 📌 Como funciona

O servidor utilizado pelo projeto é:

> **Discord:** [Acessar servidor](https://discord.gg/VxFQG5Gmy8?utm_source=chatgpt.com)

Dentro dele existe um bot que aceita comandos no seguinte formato:

```text
!djoin ID_DO_SEU_SERVIDOR
```

Exemplo:

```text
!djoin 123456789012345678
```

O comando solicita ao bot o envio de membros para o servidor correspondente ao ID informado.

Entretanto, existe um **cooldown entre as solicitações**. É justamente nesse ponto que o `djoin.py` entra.

---

## ⚙️ O que o `djoin.py` faz?

O script automatiza a interação com o Discord utilizando `PyAutoGUI`.

Após informar o ID do servidor, o programa monta automaticamente:

```text
!djoin SEU_SERVER_ID
```

Essa montagem automática está implementada diretamente na configuração do programa.

Depois de iniciado, o sistema:

1. Abre/localiza o canal configurado.
2. Digita automaticamente o comando `!djoin`.
3. Envia o comando.
4. Aguarda o cooldown configurado.
5. Tenta executar novamente.
6. Mantém o processo em **loop** até ser interrompido.

O loop principal aguarda o cooldown antes de iniciar o próximo ciclo.

---

## ⏱️ Sistema de Cooldown + Retry

Por padrão, o projeto utiliza:

```text
Cooldown: 185 segundos
Retry:       5 segundos
```

Esses valores podem ser alterados durante a configuração.

Caso uma tentativa ainda encontre o cooldown ativo, o programa pode realizar uma nova tentativa após o intervalo de `retry` configurado.

Isso permite deixar a automação funcionando sem precisar acompanhar manualmente o momento em que o próximo comando poderá ser executado.

---

## 🖥️ Menu CMD

O projeto possui um menu interativo diretamente no terminal:

```text
[1] Configurar automação
[2] Iniciar automação
[3] Ver configuração atual
[4] Obter coordenadas do mouse
[5] Sair
```

O próprio script também exibe informações como servidor alvo, canal configurado e cooldown atual.

---

## 🔧 Configuração

Ao selecionar:

```text
[1] Configurar automação
```

basta informar o **ID do servidor**.

O programa valida o ID e gera automaticamente o comando correspondente:

```text
!djoin ID_DO_SERVIDOR
```

Também é possível configurar:

- nome do canal;
- coordenadas X/Y do canal;
- duração do cooldown;
- intervalo entre novas tentativas.

As configurações são persistidas em:

```text
djoin_config.json
```

---

## 📍 Localização do canal

O AUTO !DJOIN suporta duas formas de localizar o canal.

### Pelo nome

O programa utiliza a navegação do Discord e pesquisa o nome configurado do canal.

### Por coordenadas

Também é possível informar as coordenadas `X` e `Y` da posição do canal na tela.

O próprio programa possui:

```text
[4] Obter coordenadas do mouse
```

Após alguns segundos, ele captura a posição atual do cursor para auxiliar nessa configuração.

---

## 📦 Requisitos

O projeto utiliza Python e automação de interface gráfica.

Entre as dependências declaradas estão:

```text
pyautogui>=0.9.54
pygetwindow>=0.0.9
```



O `djoin.py` também importa `pyperclip` para trabalhar com a área de transferência.

Instalação:

```bash
pip install pyautogui pyperclip pygetwindow
```

---

## 🚀 Executando

Com as dependências instaladas:

```bash
python djoin.py
```

Depois:

```text
1. Abra o Discord.
2. Entre no servidor correto.
3. Execute o djoin.py.
4. Escolha [1] Configurar.
5. Informe o ID do seu servidor.
6. Configure o canal e o cooldown.
7. Volte ao menu.
8. Escolha [2] Iniciar automação.
```

O script possui uma espera inicial de **10 segundos** antes de começar a automação, permitindo colocar o Discord em foco.

---

## 🛑 Como interromper

O `PyAutoGUI FAILSAFE` está habilitado.

Para interromper rapidamente a automação, mova o mouse para o:

```text
CANTO SUPERIOR ESQUERDO
```

Também é possível utilizar:

```text
Ctrl + C
```

O tratamento dessas formas de interrupção está presente no loop principal.

---

## ⚠️ Aviso

Este projeto apenas **automatiza ações de teclado e mouse realizadas pelo usuário**. Ele não modifica o Discord, o bot do servidor ou o funcionamento do comando `!djoin`.

O funcionamento depende do servidor e do bot externo continuarem disponibilizando esse comando.

Utilize a automação respeitando as regras do servidor, os limites estabelecidos pelo bot e os Termos de Serviço do Discord.

---

## 🛠️ Tecnologias

```text
Python
PyAutoGUI
Pyperclip
JSON
CMD / Terminal
```

---

## ⭐ Objetivo

O objetivo do **AUTO !DJOIN** é transformar um processo repetitivo:

```text
Enviar comando
      ↓
Esperar cooldown
      ↓
Enviar novamente
      ↓
Esperar cooldown
```

em:

```text
Configurar uma vez
      ↓
Iniciar AUTO !DJOIN
      ↓
Automação executando o ciclo
      ↓
Cooldown → Retry → Próxima execução
```

**Menos ações repetitivas. Mais automação.**



import json
import os
import sys
import time

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("Faltam dependências. Instale com:  pip install pyautogui pyperclip")
    sys.exit(1)

# Habilita cores ANSI e UTF-8 no terminal do Windows
os.system("")
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"


def ciano(t):    return f"{CYAN}{t}{RESET}"
def verde(t):    return f"{GREEN}{t}{RESET}"
def vermelho(t): return f"{RED}{t}{RESET}"
def amarelo(t):  return f"{YELLOW}{t}{RESET}"


# ===================== BANNER ASCII =====================
LETRAS = {
    "R": ["RRRRR  ", "R    R ", "R    R ", "RRRRR  ", "R R    ", "R  R   ", "R   R  "],
    "L": ["L      ", "L      ", "L      ", "L      ", "L      ", "L      ", "LLLLLL "],
    "K": ["K   K  ", "K  K   ", "K K    ", "KK     ", "K K    ", "K  K   ", "K   K  "],
    "M": ["M     M", "MM   MM", "M M M M", "M  M  M", "M     M", "M     M", "M     M"],
    "G": [" GGGG  ", "G    G ", "G      ", "G GGG  ", "G    G ", "G    G ", " GGGG  "],
    "C": [" CCCCC ", "C      ", "C      ", "C      ", "C      ", "C      ", " CCCCC "],
    "3": ["33333  ", "    3  ", "    3  ", "33333  ", "    3  ", "    3  ", "33333  "],
    " ": ["       ", "       ", "       ", "       ", "       ", "       ", "       "],
}


def ascii_banner(texto):
    linhas = [""] * 7
    for ch in texto.upper():
        if ch not in LETRAS:
            ch = " "
        for i in range(7):
            linhas[i] += LETRAS[ch][i] + " "
    return "\n".join(linhas)


def print_banner():
    for linha in ascii_banner("RLK MGC 33").splitlines():
        print(CYAN + BOLD + linha + RESET)
    print(YELLOW + "=" * 88)
    print(CYAN + BOLD + "  AUTO !DJOIN  |  AUTOMAÇÃO DISCORD  |  v2.0  |  RLK MGC 33" + RESET)
    print(YELLOW + "=" * 88)


# ===================== CONFIGURAÇÃO =====================
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "djoin_config.json")

DEFAULT = {
    "server_id": "",
    "comando": "",
    "channel_name": "farm-here",
    "channel_x": -1,
    "channel_y": -1,
    "cooldown_seg": 185,
    "retry_seg": 5,          # CORRIGIDO: re-tenta a cada 5 s (antes era 30 s)
}


def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for k, v in DEFAULT.items():
            cfg.setdefault(k, v)
        return cfg
    except Exception:
        return dict(DEFAULT)


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def show_config(cfg):
    print(ciano("\n  --- CONFIGURAÇÃO ATUAL ---"))
    print(f"  Servidor alvo : {amarelo(cfg['server_id'] or '(vazio)')}")
    print(f"  Comando       : {amarelo(cfg['comando'] or '(auto-montado)')}")
    linha_canal = f"  Canal         : {amarelo(cfg['channel_name'])}"
    if cfg["channel_x"] >= 0:
        linha_canal += f"  (coordenadas X={cfg['channel_x']} Y={cfg['channel_y']})"
    print(linha_canal)
    print(f"  Cooldown      : {amarelo(str(cfg['cooldown_seg']))} s")
    print(f"  Retry         : a cada {amarelo(str(cfg['retry_seg']))} s")


def setup():
    print(ciano("=" * 70))
    print(ciano("  CONFIGURAÇÃO DA AUTOMAÇÃO"))
    print(ciano("=" * 70))
    cfg = load_config()

    server_id = input("\n  Cole o ID do servidor que você quer divulgar (ex: 1299365844178047068): ").strip()
    while not (server_id.isdigit() and 10 <= len(server_id) <= 25):
        server_id = input("  ID inválido (só números). Cole novamente: ").strip()
    cfg["server_id"] = server_id
    cfg["comando"] = f"!djoin {server_id}"          # comando montado sozinho

    canal = input("  Nome do canal onde o comando roda (Enter = farm-here): ").strip()
    cfg["channel_name"] = canal or "farm-here"

    resp = input("  Usar coordenadas de tela em vez do nome do canal? (S/N): ").strip().upper()
    if resp == "S":
        try:
            x = int(input("  Coordenada X: ").strip())
            y = int(input("  Coordenada Y: ").strip())
            cfg["channel_x"], cfg["channel_y"] = x, y
        except ValueError:
            print(vermelho("  Coordenadas inválidas. Voltando pro modo nome do canal."))
            cfg["channel_x"] = cfg["channel_y"] = -1
    else:
        cfg["channel_x"] = cfg["channel_y"] = -1

    cool = input("  Cooldown em segundos (Enter = 185): ").strip()
    cfg["cooldown_seg"] = int(cool) if cool.isdigit() and int(cool) > 0 else 185

    retry = input("  Re-tentar a cada X segundos se o envio falhar (Enter = 5): ").strip()
    cfg["retry_seg"] = max(2, int(retry)) if retry.isdigit() else 5

    save_config(cfg)
    print(verde("\n  Configuração salva em djoin_config.json"))
    show_config(cfg)
    input(amarelo("\n  Pressione Enter para voltar ao menu..."))


# ===================== AUTOMAÇÃO =====================
SENTINELA = "###VERIFICA_ENVIO###"


def abrir_canal(cfg):
    if cfg["channel_x"] >= 0 and cfg["channel_y"] >= 0:
        pyautogui.click(cfg["channel_x"], cfg["channel_y"])
    else:
        pyautogui.hotkey('ctrl', 'k')
        time.sleep(2.5)
        pyautogui.write(cfg["channel_name"], interval=0.03)
        time.sleep(1.5)
        pyautogui.press('enter')
    time.sleep(2.0)


def enviar_comando(cfg):
    """Insiste até o envio ser confirmado.

    CORRIGIDO: re-tenta a cada retry_seg (5 s por padrão) em vez de 30 s.
    Assim, se o primeiro envio bater no cooldown com poucos segundos
    restantes, o próximo cai exatamente na hora do fim do cooldown.
    """
    comando = cfg["comando"]
    retry = max(2, int(cfg["retry_seg"]))
    tentativa = 0
    while True:
        tentativa += 1

        try:
            pyperclip.copy(SENTINELA)
        except Exception as e:
            print(amarelo(f"[!] Sem acesso à área de transferência ({e}). Assumindo envio OK."))
            return

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.write(comando, interval=0.02)
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(2.5)

        # Se a caixa ainda tem o comando, o envio NÃO foi aceito (cooldown ativo)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.3)

        try:
            conteudo = pyperclip.paste()
        except Exception as e:
            print(amarelo(f"[!] Erro ao ler a área de transferência ({e}). Assumindo envio OK."))
            return

        if conteudo != comando:
            print(verde(f"[OK] Enviado na tentativa {tentativa}."))
            return

        print(vermelho(f"[!] Cooldown ainda ativo (tentativa {tentativa}) — re-tentando em {retry} s..."))
        time.sleep(retry)


def iniciar(cfg):
    if not cfg["comando"]:
        print(vermelho("\n[!] Nenhuma configuração encontrada. Configure primeiro (opção 1)."))
        input(amarelo("Pressione Enter..."))
        return

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3

    print(ciano("=" * 70))
    print(ciano("  INICIANDO AUTOMAÇÃO"))
    print(ciano("=" * 70))
    print(f"  Comando : {amarelo(cfg['comando'])}")
    print(f"  Canal   : {amarelo(cfg['channel_name'])}")
    print(f"  Cooldown: {amarelo(str(cfg['cooldown_seg']))} s  |  Retry: {amarelo(str(cfg['retry_seg']))} s")
    print("\n  Abra o Discord, maximize a janela do servidor e dê foco nele.")
    print("  Começando em 10 segundos... (Ctrl+C cancela)")

    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print(amarelo("\n  Cancelado."))
        return

    n = 0
    print(vermelho("\n  RODANDO — mova o mouse ao CANTO SUPERIOR ESQUERDO a qualquer momento para ABORTAR.\n"))
    while True:
        n += 1
        print(ciano(f"[{n}] Abrindo canal e enviando {cfg['comando']}..."))
        try:
            abrir_canal(cfg)
            enviar_comando(cfg)
            print(verde(f"[{n}] OK! Próximo envio em {cfg['cooldown_seg']} s."))
        except pyautogui.FailSafeException:
            print(vermelho("\n[!] Failsafe ativado (mouse no canto). Encerrando."))
            break
        except KeyboardInterrupt:
            print(amarelo("\n[!] Interrompido pelo usuário."))
            break
        try:
            time.sleep(int(cfg["cooldown_seg"]))
        except KeyboardInterrupt:
            print(amarelo("\n[!] Interrompido pelo usuário."))
            break
    input(amarelo("\nPressione Enter para voltar ao menu..."))


def obter_coordenadas():
    print(ciano("=" * 70))
    print(ciano("  OBTENDO COORDENADAS DO MOUSE"))
    print(ciano("=" * 70))
    print("  Mova o mouse sobre o canal desejado (barra lateral do Discord).")
    print("  Capturando posição em 5 segundos...")
    time.sleep(5)
    x, y = pyautogui.position()
    print(verde(f"  Posição capturada: X = {x}  Y = {y}"))
    print(amarelo("  Use esses valores na configuração (pergunta de coordenadas)."))
    input("\n  Pressione Enter para voltar ao menu...")


# ===================== MENU =====================
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def menu():
    while True:
        clear()
        print_banner()
        cfg = load_config()
        if cfg["comando"]:
            print(f"  STATUS: {verde('CONFIGURADO')}  |  Alvo: {amarelo(cfg['comando'])}  |  "
                  f"Canal: {amarelo(cfg['channel_name'])}  |  Cooldown: {amarelo(str(cfg['cooldown_seg']))} s")
        else:
            print(f"  STATUS: {vermelho('NÃO CONFIGURADO')}  |  use a opção 1 para configurar")
        print()
        print("  [1] Configurar automação (cole o ID do servidor)")
        print("  [2] Iniciar automação")
        print("  [3] Ver configuração atual")
        
        print("  [4] Obter coordenadas do mouse")
        print("  [5] Sair")

        op = input("\n  Escolha uma opção: ").strip()
        if op == "1":
            setup()
        elif op == "2":
            iniciar(load_config())
        elif op == "3":
            show_config(load_config())
            input(amarelo("\n  Pressione Enter para voltar ao menu..."))
        elif op == "4":
            obter_coordenadas()
        elif op == "5":
            print(verde("\n  Até mais! RLK MGC 33."))
            break
        else:
            print(vermelho("\n  Opção inválida."))
            time.sleep(1)


def main():
    clear()
    print_banner()
    print(ciano("  Bem-vindo ao sistema RLK MGC 33."))
    print("  Qualquer usuário pode configurar: cole o ID do servidor")
    print("  que o comando !djoin é montado automaticamente.\n")
    input(amarelo("  Pressione Enter para continuar..."))
    menu()


if __name__ == "__main__":
    main()

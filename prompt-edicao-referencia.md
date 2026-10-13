# Prompt de edição — referência: vlog de oficina (estilo "Lucas Fontana")

> Cole este bloco no prompt que você já usa para o Claude editar seus vídeos.
> Base: análise do vídeo de referência (22 min, 16:9, 296 cortes, ~4,5 s por corte em média).

---

## REFERÊNCIA DE ESTILO (siga isto ao editar)

Edite meu vídeo no estilo de um **vlog brasileiro de bastidores de oficina/projeto**: câmera na mão, energia alta, várias pessoas conversando enquanto trabalham, e mostrando o processo de perto. O vídeo tem que parecer **real e ao vivo**, não comercial. O ritmo é rápido, mas a fala nunca é cortada no meio.

### 1. Ritmo e cortes
- **Jump cuts o tempo todo**: tire todo silêncio, respiração longa, "éé…" e repetição. A referência quase não tem pausa (só 3 silêncios em 22 minutos).
- **Duração dos planos**: mediana de **3 s**. Nos primeiros 15 minutos, um corte a cada **3,5 s**. No bloco final (conversa ou fechamento), os planos ficam mais longos: **~9 s**.
- Intercale **fala → close do detalhe → reação**: alguém explica, corta para a mão ou a peça em super close, volta para o rosto rindo.
- Pode cortar no meio do movimento da câmera. Não precisa esperar estabilizar.
- **Gancho nos primeiros 3 s**: pessoa olhando para a câmera fazendo "joinha" ou falando direto com quem assiste. Nada de vinheta longa no começo.

### 2. Transições
- **90% são cortes secos.** Transição é tempero, não regra.
- **Whip / spin transition** (por volta de 0:59): a câmera gira ou é "jogada", com **motion blur forte** por 0,3–0,5 s, e cai na cena seguinte. Use para mudar de assunto ou de ambiente.
- **Quadro inclinado com borda preta** (zoom-out + rotação de ~5–10°, fundo preto): a imagem vira uma "tela dentro da tela" e entra um **picture-in-picture** pequeno (meme, reação ou foto) no canto. Use para piada ou comentário.
- Speed ramp leve (acelerar trechos repetitivos de trabalho manual, tipo lixar, soldar ou desmontar) em 2x–4x.

### 3. Câmera / enquadramento (para orientar a escolha de takes)
- **Grande-angular / action cam (GoPro)** com distorção nas bordas, na altura do peito ou em selfie.
- Muito **POV e super close** de mãos, ferramentas, peças, solda (faísca), parafusos e texturas.
- Selfie de perto com o rosto ocupando 1/3 do quadro, o fundo da oficina inteiro aparecendo e luz de teto tubular.
- Tremido natural é OK, desde que não estrague a leitura. Estabilize só o que estiver ilegível.

### 4. Color grading — cores da LataVéias
- Base nas cores da logo: **azul-marinho/azul elétrico** `#04183D` → `#2961B3`, **vermelho** `#B12327` e **aço escovado** `#B8BBC2` / `#F5F6F6`.
- Altas luzes neutras e limpas (cor de aço, nada amarelado), sombras levemente puxadas para o azul-marinho. **Azul e vermelho saltam**, o resto fica um pouco dessaturado. Contraste médio-alto, sem grão e sem vinheta pesada.
- Filtro testado: `eq=contrast=1.15:gamma=0.96:saturation=0.9,colorbalance=bs=0.05:bm=0.03:rh=-0.03,huesaturation=saturation=0.45:colors=b+c+m,huesaturation=saturation=0.4:colors=r,unsharp=5:5:0.5`

### 5. Elementos gráficos / overlays
- **Card LataVéias** (`intro/card-lataveias.png`): avatar LV redondo com anel azul/vermelho, a logo LataVéias e o botão vermelho INSCREVA-SE. Fica no canto inferior esquerdo com ~26% da altura e aparece nos primeiros 10 s, depois a cada ~3 min por ~8 s e no final.
- **Sem QR code e sem patrocinador.**
- Legendas: **não** use legenda corrida estilo TikTok no vídeo horizontal. Texto na tela só para nome ou piada pontual, em fonte bold itálica branca. Para destaques, use caixa vermelha `#B12327`.
- Fonte: sans-serif bold itálica (FreeSans Bold Oblique / Montserrat ExtraBold Italic).

### 6. Áudio
- A fala é a protagonista: voz alta e clara, **loudness final ~ -14 a -15 LUFS** (a referência mede -15,4 LUFS).
- Som ambiente da oficina **fica** (ferramenta, solda, risada) e ajuda a dar a sensação de "real".
- Trilha de fundo baixa (−20 a −25 dB sob a voz) e sobe só nas transições whip e nos trechos acelerados.
- SFX de **whoosh** em cada whip transition e um "pop" quando entra um overlay ou tag.

### 7. Estrutura
1. **Gancho (0–5 s)**: alguém falando com a câmera e prometendo o que vai acontecer.
2. **Processo (miolo)**: blocos de trabalho, cada um com explicação, close e reação, separados por whip.
3. **Interações**: entram outras pessoas ou convidados, numa conversa descontraída com zoeira.
4. **Fechamento**: plano mais aberto e estável, com o resultado do dia, o pedido de inscrição e o card LataVéias na tela.
5. **Encerramento** rápido, sem tela final longa.

### 8. O que NÃO fazer
- Não deixe silêncio, nem plano parado por mais de ~6 s (fora do fechamento).
- Não use transições de template (cubo, página virando, dissolve longo).
- Não deixe o grading quente ou amarelado e não lave as cores.
- Não cubra o rosto ou a peça principal com overlay.

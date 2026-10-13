# Prompt de edição — referência: vlog de oficina (estilo "Lucas Fontana")

> Cole este bloco no prompt que você já usa para o Claude editar seus vídeos.
> Base: análise do vídeo de referência (22 min, 16:9, 296 cortes, ~4,5 s por corte em média).

---

## REFERÊNCIA DE ESTILO (siga isto ao editar)

Edite meu vídeo no estilo de um **vlog brasileiro de bastidores de oficina/projeto**: câmera na mão, energia alta, várias pessoas conversando enquanto trabalham, e mostrando o processo de perto. O vídeo tem que parecer **real e ao vivo**, não comercial. O ritmo é rápido, mas a fala nunca é cortada no meio.

### 1. Ritmo e cortes
- **Jump cuts o tempo todo**: tire todo silêncio, respiração longa, "éé…" e repetição. A referência quase não tem pausa (só 3 silêncios em 22 minutos).
- **Duração dos planos**: mediana de **3 s**. Nos primeiros 15 minutos, um corte a cada **3,5 s**. No bloco final (conversa ou publi), os planos ficam mais longos: **~9 s**.
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

### 4. Color grading
- **Look "oficina limpa / fria"**: brancos limpos, levemente **frios (azulados)**, sombras quase pretas, **contraste médio-alto** e **saturação alta só nas cores fortes** (o roxo do carro, o vermelho e o azul dos bonés, o amarelo da fita).
- Paleta de referência: `#14191D` (sombras) · `#505961` · `#8A959A` · `#A4B5B4` · `#C4D6D5` (altas luzes frias) + acentos saturados roxo/azul/vermelho.
- Sem look de cinema, sem grão, sem vinheta pesada. Fica entre o "nítido de YouTube" e o "punchy".
- Sugestão ffmpeg: `eq=contrast=1.12:saturation=1.25:gamma=0.97,colortemperature=temperature=5800,unsharp=5:5:0.6` (ajuste à luz do seu material).

### 5. Elementos gráficos / overlays
- **Card do criador fixo no canto inferior esquerdo**: foto redonda + NOME em caixa alta, itálico e negrito branco, com um botão de inscrever pequeno. Depois de um tempo ele **alterna para um QR code** com o nome embaixo. Ocupa ~10% da altura e fica no vídeo quase todo.
- **Tag de patrocinador no rodapé central**: retângulo branco pequeno de canto arredondado com o logo da marca em preto. Aparece **quando o produto entra em cena** e some depois de ~3 s. Também há uma tag "PATROCINADORES" sobre o close do produto.
- Legendas: **não** use legenda corrida estilo TikTok (a referência é horizontal e não tem). Texto na tela só para nome, patrocinador ou piada pontual.
- Fonte: sans-serif bold condensada e itálica (tipo Montserrat ExtraBold Italic / Bebas).

### 6. Áudio
- A fala é a protagonista: voz alta e clara, **loudness final ~ -14 a -15 LUFS** (a referência mede -15,4 LUFS).
- Som ambiente da oficina **fica** (ferramenta, solda, risada) e ajuda a dar a sensação de "real".
- Trilha de fundo baixa (−20 a −25 dB sob a voz) e sobe só nas transições whip e nos trechos acelerados.
- SFX de **whoosh** em cada whip transition e um "pop" quando entra um overlay ou tag.

### 7. Estrutura
1. **Gancho (0–5 s)**: alguém falando com a câmera e prometendo o que vai acontecer.
2. **Processo (miolo)**: blocos de trabalho, cada um com explicação, close e reação, separados por whip.
3. **Interações**: entram outras pessoas ou convidados, numa conversa descontraída com zoeira.
4. **Bloco de publi no final**: plano mais aberto e estável, a pessoa segurando o produto na frente da câmera, card do criador e QR code visíveis.
5. **Encerramento** rápido, sem tela final longa.

### 8. O que NÃO fazer
- Não deixe silêncio, nem plano parado por mais de ~6 s (fora da publi).
- Não use transições de template (cubo, página virando, dissolve longo).
- Não deixe o grading quente ou amarelado e não lave as cores.
- Não cubra o rosto ou a peça principal com overlay.

# Kahoot Ranking

Este repositório tem como objetivo gerar o ranking geral de vários Kahoots a partir dos relatórios gerados pela plataforma do próprio Kahoot.

## Como funciona a construção do ranking?
- Nome (utilizado como identificação de cada jogador ao longo dos Kahoots)
- Sistema de pontuação por pódio
  - 🥇 1 lugar : 3 pontos
  - 🥈 2 lugar : 2 pontos
  - 🥉 3 lugar : 1 ponto
- Pontuação total acumulada

1. É realizada a limpeza dos nomes dos jogadores, para identificá-los corretamente
    - Remove espaços, números, acentos e letras maiúsculas
    - Aliases podem ser inseridos manualmente (a limpeza dos nomes não visa ser sofisticada para este projeto)
    - (ex.: "julio" == "Julio", "maria eduardà" == "mariaeduarda")
2. É contabilizado os pontos pela pontuação por pódio
3. É realizado o desempate pela pontuação total obtida nos Kahoots

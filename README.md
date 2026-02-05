# Projet de Fin de Cours - MSBNS3IN03 Intelligence Artificielle Generative (2025-2026)

Bienvenue sur le depot officiel pour la soumission du projet de fin de cours sur l'IA Generative.

## Instructions de Soumission

1. **Forkez ce depot :** Chaque groupe doit creer un "fork" de ce depot pour y travailler.
2. **Creez un dossier pour votre groupe :** A la racine de votre fork, creez un dossier unique pour votre groupe (ex: `groupe-alpha`, `projet-rag-chatbot`, etc.).
3. **Placez vos livrables :** Tous vos livrables (code, `README.md` de votre projet, slides, etc.) doivent etre places a l'interieur de ce dossier.
4. **Soumettez via une Pull Request :** Une fois votre projet termine, creez une Pull Request depuis votre fork vers le depot principal. La PR doit etre soumise au plus tard **le 25 fevrier 2026** (avant-veille de la soutenance).

## Date de Soutenance

**27 fevrier 2026**

---

# Catalogue des Sujets de Projet

Les sujets sont organises en categories thematiques. Chaque sujet inclut :
- Une description detaillee des objectifs
- Les references aux **notebooks du cours** ([CoursIA](https://github.com/jsboige/CoursIA))
- Des **references externes** (articles, documentation, projets SOTA)
- Le niveau de difficulte estime

> **Note :** Vous etes encourages a proposer vos propres sujets ou a combiner plusieurs idees !

---

## Index des Sujets

### Categorie A : Agents Conversationnels & RAG
| # | Sujet | Difficulte |
|---|-------|------------|
| [A1](#a1---agent-rag-pour-documentation-difficulte-25) | Agent RAG pour Documentation | 2/5 |
| [A2](#a2---assistant-personnel-intelligent-difficulte-35) | Assistant Personnel Intelligent | 3/5 |
| [A3](#a3---agent-de-recherche-web-difficulte-25) | Agent de Recherche Web | 2/5 |
| [A4](#a4---chatbot-multi-personnalites-difficulte-25) | Chatbot Multi-Personnalites | 2/5 |

### Categorie B : Jeux de Role & Narration Interactive
| # | Sujet | Difficulte |
|---|-------|------------|
| [B1](#b1---escape-game-textuel-multi-agents-difficulte-35) | Escape Game Textuel Multi-Agents | 3/5 |
| [B2](#b2---maitre-de-jeu-ia-pour-jdr-difficulte-35) | Maitre de Jeu IA pour JDR | 3/5 |
| [B3](#b3---visual-novel-generatif-difficulte-35) | Visual Novel Generatif | 3/5 |
| [B4](#b4---conte-musical-interactif-difficulte-45) | Conte Musical Interactif | 4/5 |
| [B5](#b5---simulation-de-proces-difficulte-35) | Simulation de Proces | 3/5 |

### Categorie C : Creation Multimedia & Arts Generatifs
| # | Sujet | Difficulte |
|---|-------|------------|
| [C1](#c1---generateur-de-bandes-dessinees-difficulte-35) | Generateur de Bandes Dessinees | 3/5 |
| [C2](#c2---compositeur-musical-ia-difficulte-35) | Compositeur Musical IA | 3/5 |
| [C3](#c3---createur-de-posts-reseaux-sociaux-difficulte-25) | Createur de Posts Reseaux Sociaux | 2/5 |
| [C4](#c4---studio-de-doublage-virtuel-difficulte-35) | Studio de Doublage Virtuel | 3/5 |
| [C5](#c5---generateur-de-pochettes-dalbum-difficulte-25) | Generateur de Pochettes d'Album | 2/5 |
| [C6](#c6---avatar-anime-interactif-difficulte-45) | Avatar Anime Interactif | 4/5 |

### Categorie D : Applications Metier & Professionnelles
| # | Sujet | Difficulte |
|---|-------|------------|
| [D1](#d1---agent-de-recrutement-difficulte-35) | Agent de Recrutement | 3/5 |
| [D2](#d2---generateur-de-contrats-difficulte-25) | Generateur de Contrats | 2/5 |
| [D3](#d3---veille-concurrentielle-difficulte-35) | Veille Concurrentielle | 3/5 |
| [D4](#d4---assistant-juridique-difficulte-35) | Assistant Juridique | 3/5 |
| [D5](#d5---redacteur-de-rapports-difficulte-25) | Redacteur de Rapports | 2/5 |
| [D6](#d6---traducteur-localisateur-difficulte-25) | Traducteur-Localisateur | 2/5 |

### Categorie E : Outils pour Developpeurs
| # | Sujet | Difficulte |
|---|-------|------------|
| [E1](#e1---generateur-de-tests-unitaires-difficulte-35) | Generateur de Tests Unitaires | 3/5 |
| [E2](#e2---documenteur-de-code-difficulte-25) | Documenteur de Code | 2/5 |
| [E3](#e3---revieweur-de-code-ia-difficulte-35) | Revieweur de Code IA | 3/5 |
| [E4](#e4---convertisseur-de-langage-difficulte-35) | Convertisseur de Langage | 3/5 |
| [E5](#e5---generateur-dapi-mock-difficulte-25) | Generateur d'API Mock | 2/5 |

### Categorie F : Education & Formation
| # | Sujet | Difficulte |
|---|-------|------------|
| [F1](#f1---generateur-de-quiz-difficulte-25) | Generateur de Quiz | 2/5 |
| [F2](#f2---tuteur-de-code-adaptatif-difficulte-35) | Tuteur de Code Adaptatif | 3/5 |
| [F3](#f3---correcteur-de-copies-intelligent-difficulte-35) | Correcteur de Copies Intelligent | 3/5 |
| [F4](#f4---simulateur-dentretien-difficulte-25) | Simulateur d'Entretien | 2/5 |
| [F5](#f5---generateur-de-flashcards-difficulte-25) | Generateur de Flashcards | 2/5 |
| [F6](#f6---professeur-de-langues-difficulte-35) | Professeur de Langues | 3/5 |

### Categorie G : Jeux & Divertissement
| # | Sujet | Difficulte |
|---|-------|------------|
| [G1](#g1---bot-de-jeu-de-societe-difficulte-35) | Bot de Jeu de Societe | 3/5 |
| [G2](#g2---generateur-de-puzzles-difficulte-25) | Generateur de Puzzles | 2/5 |
| [G3](#g3---commentateur-sportif-ia-difficulte-35) | Commentateur Sportif IA | 3/5 |
| [G4](#g4---createur-de-niveaux-de-jeu-difficulte-35) | Createur de Niveaux de Jeu | 3/5 |
| [G5](#g5---arbitre-de-debat-difficulte-35) | Arbitre de Debat | 3/5 |

### Categorie H : Analyse & Intelligence
| # | Sujet | Difficulte |
|---|-------|------------|
| [H1](#h1---analyseur-de-sentiments-difficulte-25) | Analyseur de Sentiments | 2/5 |
| [H2](#h2---detecteur-de-fake-news-difficulte-35) | Detecteur de Fake News | 3/5 |
| [H3](#h3---resumeur-de-reunions-difficulte-25) | Resumeur de Reunions | 2/5 |
| [H4](#h4---analyseur-de-tendances-difficulte-35) | Analyseur de Tendances | 3/5 |
| [H5](#h5---extracteur-de-donnees-structurees-difficulte-25) | Extracteur de Donnees Structurees | 2/5 |

### Categorie X : IA Hybride & Projets Avances (Bonus)
| # | Sujet | Difficulte |
|---|-------|------------|
| [X1](#x1---agent-dargumentation-logique-difficulte-45) | Agent d'Argumentation Logique | 4/5 |
| [X2](#x2---assistant-de-preuve-mathematique-difficulte-45) | Assistant de Preuve Mathematique | 4/5 |
| [X3](#x3---systeme-de-recommandation-bayesien-difficulte-45) | Systeme de Recommandation Bayesien | 4/5 |
| [X4](#x4---negociateur-multi-agents-difficulte-45) | Negociateur Multi-Agents | 4/5 |
| [X5](#x5---planificateur-sous-contraintes-difficulte-35) | Planificateur sous Contraintes | 3/5 |
| [X6](#x6---diagnostic-medical-probabiliste-difficulte-45) | Diagnostic Medical Probabiliste | 4/5 |
| [X7](#x7---agent-de-trading-algorithmique-difficulte-45) | Agent de Trading Algorithmique | 4/5 |
| [X8](#x8---systeme-de-revision-de-croyances-difficulte-45) | Systeme de Revision de Croyances | 4/5 |

---

## Categorie A : Agents Conversationnels & RAG

Ces projets explorent les fondamentaux de l'IA generative : chatbots, recherche augmentee, et agents autonomes.

### A1 - Agent RAG pour Documentation (Difficulte: 2/5)

**Description :** Developper un chatbot capable de repondre aux questions sur un corpus de documents (cours, wiki d'entreprise, FAQ) en utilisant la technique RAG (Retrieval-Augmented Generation).

**Objectifs :**
- Implementer un systeme d'indexation vectorielle de documents
- Creer un pipeline de recuperation contextuelle
- Integrer un LLM pour la generation de reponses sourcees
- Fournir des citations et references dans les reponses

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/5_RAG_Modern.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/5_RAG_Modern.ipynb) | Architecture RAG moderne avec embeddings |
| [`GenAI/Texte/1_OpenAI_Intro.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/1_OpenAI_Intro.ipynb) | Introduction a l'API OpenAI |
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Generation de sorties structurees |

**References externes :**
- [LangChain RAG Documentation](https://python.langchain.com/docs/tutorials/rag/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [FAISS - Facebook AI Similarity Search](https://github.com/facebookresearch/faiss)
- [Chroma Vector Database](https://www.trychroma.com/)

---

### A2 - Assistant Personnel Intelligent (Difficulte: 3/5)

**Description :** Creer un majordome virtuel inspire de Jarvis, integrant la gestion d'agenda, emails, meteo et rappels via des APIs externes.

**Objectifs :**
- Orchestrer plusieurs outils/APIs via Function Calling
- Implementer un systeme de dialogue naturel multi-turn
- Gerer le contexte utilisateur et les preferences
- Creer une interface utilisateur intuitive (web ou CLI)

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/4_Function_Calling.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/4_Function_Calling.ipynb) | Appel de fonctions et tools |
| [`GenAI/SemanticKernel/01-SemanticKernel-Intro.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/SemanticKernel/01-SemanticKernel-Intro.ipynb) | Introduction a Semantic Kernel |
| [`GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb) | Orchestration multi-agents |

**References externes :**
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Google Calendar API](https://developers.google.com/calendar/api)
- [Gmail API](https://developers.google.com/gmail/api)
- [OpenWeather API](https://openweathermap.org/api)

---

### A3 - Agent de Recherche Web (Difficulte: 2/5)

**Description :** Developper un agent autonome capable de rechercher, synthetiser et citer des sources web sur un sujet donne.

**Objectifs :**
- Implementer la recherche web via API (Tavily, SerpAPI, etc.)
- Extraire et analyser le contenu des pages web
- Synthetiser les informations de multiples sources
- Generer des rapports avec citations et sources verifiables

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/4_Function_Calling.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/4_Function_Calling.ipynb) | Integration d'outils externes |
| [`GenAI/Texte/2_PromptEngineering.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/2_PromptEngineering.ipynb) | Techniques de prompt engineering |

**References externes :**
- [Tavily AI Search API](https://tavily.com/)
- [Perplexity AI](https://www.perplexity.ai/) - Exemple de systeme de recherche IA
- [LangChain Web Research](https://python.langchain.com/docs/tutorials/web_scraping/)

---

### A4 - Chatbot Multi-Personnalites (Difficulte: 2/5)

**Description :** Creer un chatbot capable d'adopter differents styles et personnalites selon le contexte (formel, humoristique, technique, empathique).

**Objectifs :**
- Definir des profils de personnalite avec des prompts systeme distincts
- Implementer la detection automatique du contexte approprie
- Maintenir la coherence du personnage au fil de la conversation
- Permettre le changement dynamique de personnalite

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/2_PromptEngineering.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/2_PromptEngineering.ipynb) | System prompts et personas |
| [`GenAI/Texte/1_OpenAI_Intro.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/1_OpenAI_Intro.ipynb) | Gestion des messages et roles |

**References externes :**
- [Character.AI](https://character.ai/) - Plateforme de personnages IA
- [OpenAI System Messages Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

---

## Categorie B : Jeux de Role & Narration Interactive

Exploitez l'IA pour creer des experiences narratives immersives et interactives.

### B1 - Escape Game Textuel Multi-Agents (Difficulte: 3/5)

**Description :** Creer une simulation d'escape game ou plusieurs agents IA (gardien, donneur d'indices, mecanismes de pieges) interagissent avec le joueur dans un scenario d'evasion.

**Objectifs :**
- Concevoir plusieurs agents avec des roles et comportements distincts
- Implementer un systeme de progression et d'enigmes
- Gerer les interactions entre agents et avec le joueur
- Creer une narration dynamique et immersive

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb) | Systemes multi-agents |
| [`GenAI/Texte/2_PromptEngineering.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/2_PromptEngineering.ipynb) | Creation de personnages via prompts |

**References externes :**
- [AI Dungeon](https://aidungeon.com/) - Jeu narratif IA de reference
- [AutoGen Multi-Agent](https://microsoft.github.io/autogen/) - Framework Microsoft pour agents conversationnels

---

### B2 - Maitre de Jeu IA pour JDR (Difficulte: 3/5)

**Description :** Developper un agent qui joue le role de Game Master pour des parties de jeu de role (style D&D), gerant l'histoire, les PNJ et les combats.

**Objectifs :**
- Generer des scenarios narratifs coherents et adaptatifs
- Gerer les personnages non-joueurs (PNJ) avec personnalites distinctes
- Implementer un systeme de regles (combat, competences, jets de des)
- Maintenir la coherence de l'univers et de l'histoire

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb) | Orchestration d'agents |
| [`GenAI/Texte/4_Function_Calling.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/4_Function_Calling.ipynb) | Integration de mecaniques de jeu |

**References externes :**
- [D&D 5e SRD](https://www.dndbeyond.com/sources/basic-rules) - Regles de reference
- [LLM as Game Master (Paper)](https://arxiv.org/abs/2402.01030) - Recherche academique
- [Storyteller AI](https://www.aitdm.com/) - Exemples d'IA narratives

---

### B3 - Visual Novel Generatif (Difficulte: 3/5)

**Description :** Creer une histoire interactive illustree ou le texte est genere par LLM et les images par un modele de generation (DALL-E, Stable Diffusion, FLUX).

**Objectifs :**
- Generer une narration coherente avec des embranchements
- Creer des illustrations correspondant aux scenes narratives
- Maintenir la coherence visuelle des personnages et decors
- Implementer un systeme de choix influencant l'histoire

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/2_PromptEngineering.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/2_PromptEngineering.ipynb) | Generation narrative |
| [`GenAI/Images/01-1-OpenAI-DALL-E-3.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Images/01-1-OpenAI-DALL-E-3.ipynb) | API DALL-E 3 |
| [`GenAI/Images/02-2-FLUX-1-Advanced-Generation.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Images/02-2-FLUX-1-Advanced-Generation.ipynb) | FLUX.1 pour illustrations coherentes |
| [`GenAI/Images/01-4-Forge-SD-XL-Turbo.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Images/01-4-Forge-SD-XL-Turbo.ipynb) | Stable Diffusion local |

**References externes :**
- [NovelAI](https://novelai.net/) - Generation narrative et image
- [DALL-E 3 Documentation](https://platform.openai.com/docs/guides/images)
- [Replicate FLUX Models](https://replicate.com/black-forest-labs)

---

### B4 - Conte Musical Interactif (Difficulte: 4/5)

**Description :** Creer une experience narrative ou chaque chapitre genere texte + illustration + ambiance musicale via des modeles de generation audio (Suno, Udio, Stable Audio).

**Objectifs :**
- Orchestrer la generation multimodale (texte, image, audio)
- Creer des ambiances musicales coherentes avec la narration
- Synchroniser les differents medias dans une experience fluide
- Permettre l'interaction utilisateur influencant tous les medias

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Images/01-1-OpenAI-DALL-E-3.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Images/01-1-OpenAI-DALL-E-3.ipynb) | Generation d'illustrations |
| [`GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb) | Orchestration multi-agents |

**References externes :**
- [Suno AI](https://suno.com/) - Generation musicale SOTA (v4)
- [Udio](https://www.udio.com/) - Alternative pour generation musicale
- [Stable Audio](https://stability.ai/stable-audio) - Generation audio par Stability AI
- [ElevenLabs](https://elevenlabs.io/) - Generation de voix pour narration

---

### B5 - Simulation de Proces (Difficulte: 3/5)

**Description :** Creer un jeu de role juridique avec des agents jouant les roles d'avocat, procureur, juge et temoins debattant d'une affaire.

**Objectifs :**
- Modeliser des agents avec expertise juridique
- Implementer les mecanismes proceduraux d'un proces
- Gerer les interactions contradictoires entre agents
- Produire un verdict argumente base sur les debats

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/SemanticKernel/03-SemanticKernel-Agents.ipynb) | Debat multi-agents |
| [`SymbolicAI/Tweety/Tweety-5-Abstract-Argumentation.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-5-Abstract-Argumentation.ipynb) | Frameworks d'argumentation formelle |

**References externes :**
- [LegalBench](https://hazyresearch.stanford.edu/legalbench/) - Benchmark LLM juridique
- [Case Law Access Project](https://case.law/) - Corpus de jurisprudence

---

## Categorie C : Creation Multimedia & Arts Generatifs

Projets axes sur la generation de contenu visuel, audio ou artistique.

### C1 - Generateur de Bandes Dessinees (Difficulte: 3/5)

**Description :** A partir d'un synopsis, generer une BD complete avec cases, dialogues et illustrations coherentes.

**Objectifs :**
- Decouper un synopsis en scenes et dialogues
- Generer des illustrations coherentes (personnages, decors)
- Creer une mise en page BD automatique
- Maintenir la coherence visuelle du style

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Images/02-2-FLUX-1-Advanced-Generation.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Images/02-2-FLUX-1-Advanced-Generation.ipynb) | Generation d'images coherentes |
| [`GenAI/Images/03-1-Orchestration.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Images/03-1-Orchestration.ipynb) | Pipeline de generation multi-images |

**References externes :**
- [ComicGen (Paper)](https://arxiv.org/abs/2312.15131) - Recherche sur la generation de BD
- [Midjourney](https://www.midjourney.com/) - Style coherent pour personnages

---

### C2 - Compositeur Musical IA (Difficulte: 3/5)

**Description :** Developper un agent qui compose des melodies ou accompagnements musicaux selon un style ou une emotion donnee.

**Objectifs :**
- Generer de la musique a partir de descriptions textuelles
- Permettre le controle du style, tempo, instruments
- Creer des variations et arrangements
- Exporter en formats audio standard

**References externes :**
- [Suno AI v4](https://suno.com/) - Generation musicale SOTA
- [Udio](https://www.udio.com/) - Generation avec controle fin
- [MusicLM (Google)](https://google-research.github.io/seanet/musiclm/examples/) - Modele de recherche
- [AudioCraft (Meta)](https://github.com/facebookresearch/audiocraft) - Framework open-source

---

### C3 - Createur de Posts Reseaux Sociaux (Difficulte: 2/5)

**Description :** Outil generant textes + visuels optimises pour differentes plateformes (LinkedIn, Instagram, Twitter/X).

**Objectifs :**
- Adapter le ton et format selon la plateforme cible
- Generer des visuels aux dimensions appropriees
- Suggerer des hashtags et moments de publication
- Creer des variations A/B pour tests

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Images/01-1-OpenAI-DALL-E-3.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Images/01-1-OpenAI-DALL-E-3.ipynb) | Generation de visuels |
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Structuration du contenu |

**References externes :**
- [Buffer](https://buffer.com/) - Exemple d'outil de planification
- [Canva AI](https://www.canva.com/ai-image-generator/) - Generation de visuels

---

### C4 - Studio de Doublage Virtuel (Difficulte: 3/5)

**Description :** Generer des voix synthetiques pour doubler des personnages de video/animation dans differentes langues.

**Objectifs :**
- Cloner ou creer des voix distinctes pour personnages
- Synchroniser le doublage avec les mouvements labiaux
- Supporter plusieurs langues avec prononciation naturelle
- Gerer les emotions et intonations

**References externes :**
- [ElevenLabs](https://elevenlabs.io/) - Voice cloning et dubbing
- [Coqui TTS](https://github.com/coqui-ai/TTS) - TTS open-source
- [Rask AI](https://www.rask.ai/) - Doublage automatique
- [HeyGen](https://www.heygen.com/) - Lip-sync video

---

### C5 - Generateur de Pochettes d'Album (Difficulte: 2/5)

**Description :** Creer des artworks musicaux coherents avec le genre et l'ambiance d'un album ou playlist.

**Objectifs :**
- Analyser le style musical pour definir l'esthetique visuelle
- Generer des artwork dans differents styles artistiques
- Maintenir la coherence avec l'identite de l'artiste
- Produire des formats adaptes (cover, vinyle, banniere)

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Images/02-2-FLUX-1-Advanced-Generation.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Images/02-2-FLUX-1-Advanced-Generation.ipynb) | Generation artistique avancee |
| [`GenAI/Texte/2_PromptEngineering.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/2_PromptEngineering.ipynb) | Prompts creatifs |

---

### C6 - Avatar Anime Interactif (Difficulte: 4/5)

**Description :** Creer un personnage 2D/3D anime qui repond vocalement et visuellement aux interactions utilisateur en temps reel.

**Objectifs :**
- Generer un avatar personnalise
- Animer les expressions faciales selon le contenu
- Synchroniser voix synthetique et animation
- Repondre en temps reel aux inputs utilisateur

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Images/01-1-OpenAI-DALL-E-3.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Images/01-1-OpenAI-DALL-E-3.ipynb) | Creation d'avatar |
| [`GenAI/Texte/4_Function_Calling.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/4_Function_Calling.ipynb) | Orchestration temps reel |

**References externes :**
- [D-ID](https://www.d-id.com/) - Avatars video parlants
- [HeyGen](https://www.heygen.com/) - Avatars interactifs
- [Ready Player Me](https://readyplayer.me/) - Avatars 3D personnalises
- [Live2D](https://www.live2d.com/) - Animation 2D

---

## Categorie D : Applications Metier & Professionnelles

Outils pratiques pour automatiser des taches professionnelles.

### D1 - Agent de Recrutement (Difficulte: 3/5)

**Description :** Comparer des CVs a une fiche de poste et produire un classement justifie des candidats.

**Objectifs :**
- Parser et structurer les CVs (PDF, DOCX)
- Extraire les competences et experiences pertinentes
- Scorer les candidats selon les criteres du poste
- Generer des rapports comparatifs detailles

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Extraction structuree |
| [`GenAI/Texte/5_RAG_Modern.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/5_RAG_Modern.ipynb) | Analyse de documents |

**References externes :**
- [Resume Parser Libraries](https://github.com/OmkarPathak/pyresparser) - Parsing de CV
- [HireVue](https://www.hirevue.com/) - Exemple commercial

---

### D2 - Generateur de Contrats (Difficulte: 2/5)

**Description :** Creer des contrats personnalises a partir de templates et d'informations structurees.

**Objectifs :**
- Definir des templates de contrats parametrables
- Collecter les informations via formulaire ou dialogue
- Generer des documents juridiquement coherents
- Exporter en formats professionnels (PDF, DOCX)

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Generation structuree |
| [`GenAI/Texte/2_PromptEngineering.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/2_PromptEngineering.ipynb) | Redaction juridique |

---

### D3 - Veille Concurrentielle (Difficulte: 3/5)

**Description :** Agent collectant et synthetisant des informations sur des concurrents depuis le web.

**Objectifs :**
- Scraper automatiquement les sources d'information pertinentes
- Detecter les nouveautes et changements significatifs
- Generer des rapports de veille reguliers
- Alerter sur les evenements importants

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/4_Function_Calling.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/4_Function_Calling.ipynb) | Integration APIs web |
| [`GenAI/Texte/5_RAG_Modern.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/5_RAG_Modern.ipynb) | Analyse de corpus |

---

### D4 - Assistant Juridique (Difficulte: 3/5)

**Description :** Rechercher et resumer des textes de loi ou jurisprudence pertinents pour une question juridique donnee.

**Objectifs :**
- Indexer un corpus juridique (codes, jurisprudence)
- Repondre aux questions en citant les sources
- Comparer differentes interpretations
- Identifier les textes applicables a un cas

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/5_RAG_Modern.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/5_RAG_Modern.ipynb) | RAG sur corpus specialise |

**References externes :**
- [Legifrance API](https://www.legifrance.gouv.fr/) - Acces aux textes legaux francais
- [EUR-Lex](https://eur-lex.europa.eu/) - Droit europeen
- [LegalBench](https://hazyresearch.stanford.edu/legalbench/) - Benchmark LLM juridique

---

### D5 - Redacteur de Rapports (Difficulte: 2/5)

**Description :** Generer des rapports structures (financiers, techniques, medicaux) a partir de donnees brutes.

**Objectifs :**
- Ingerer des donnees structurees (CSV, JSON, API)
- Analyser et interpreter les donnees
- Generer des narratifs explicatifs
- Produire des visualisations et documents formates

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Structuration des sorties |
| [`ML/ML.NET/1-ML.NET-Classification.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/ML/ML.NET/1-ML.NET-Classification.ipynb) | Analyse de donnees |

---

### D6 - Traducteur-Localisateur (Difficulte: 2/5)

**Description :** Traduire en adaptant ton, expressions et references culturelles pour une audience cible.

**Objectifs :**
- Traduire au-dela du mot-a-mot
- Adapter les references culturelles
- Maintenir le registre de langue approprie
- Gerer les expressions idiomatiques

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/2_PromptEngineering.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/2_PromptEngineering.ipynb) | Prompts de traduction contextualisee |

**References externes :**
- [DeepL API](https://www.deepl.com/pro-api) - Traduction de qualite
- [Localization Best Practices](https://phrase.com/blog/posts/localization-best-practices/)

---

## Categorie E : Outils pour Developpeurs

Projets ciblant l'amelioration de la productivite des developpeurs.

### E1 - Generateur de Tests Unitaires (Difficulte: 3/5)

**Description :** Analyser une fonction et generer automatiquement des tests pertinents avec cas limites.

**Objectifs :**
- Parser et comprendre le code source
- Identifier les cas de test pertinents (nominal, limites, erreurs)
- Generer des tests dans le framework approprie
- Mesurer la couverture de code

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Generation de code structure |
| [`GenAI/Vibe-Coding/Claude-Code-101.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Vibe-Coding/Claude-Code-101.ipynb) | Coding assiste par IA |

**References externes :**
- [GitHub Copilot](https://github.com/features/copilot) - Assistant de code
- [TestPilot (Paper)](https://arxiv.org/abs/2302.06527) - Generation de tests par LLM
- [CodiumAI](https://www.codium.ai/) - Generation de tests specialisee

---

### E2 - Documenteur de Code (Difficulte: 2/5)

**Description :** Generer docstrings, README et documentation technique a partir du code source.

**Objectifs :**
- Analyser la structure du code (classes, fonctions, modules)
- Generer des docstrings dans le format approprie
- Creer des README de projet complets
- Produire une documentation API

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/2_PromptEngineering.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/2_PromptEngineering.ipynb) | Redaction technique |

**References externes :**
- [Mintlify](https://mintlify.com/) - Documentation automatique
- [Sphinx](https://www.sphinx-doc.org/) - Generation de docs Python

---

### E3 - Revieweur de Code IA (Difficulte: 3/5)

**Description :** Analyser un diff/PR et suggerer des ameliorations, detecter des bugs potentiels.

**Objectifs :**
- Parser les diffs et Pull Requests
- Detecter les patterns problematiques
- Suggerer des ameliorations avec explications
- Verifier le respect des conventions

**References externes :**
- [CodeRabbit](https://coderabbit.ai/) - Review automatique de PR
- [Sourcery](https://sourcery.ai/) - Refactoring automatique
- [SonarQube](https://www.sonarsource.com/products/sonarqube/) - Analyse statique

---

### E4 - Convertisseur de Langage (Difficulte: 3/5)

**Description :** Traduire du code d'un langage a un autre (Python vers C#, JavaScript vers TypeScript, etc.).

**Objectifs :**
- Parser le code source et son AST
- Mapper les constructions entre langages
- Adapter les idiomes et patterns
- Gerer les bibliotheques et dependances

**References externes :**
- [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) - Parsing multi-langage
- [TransCoder (Meta)](https://arxiv.org/abs/2006.03511) - Recherche sur la traduction de code

---

### E5 - Generateur d'API Mock (Difficulte: 2/5)

**Description :** Creer des endpoints mock realistes a partir d'une specification OpenAPI/Swagger.

**Objectifs :**
- Parser les specifications OpenAPI
- Generer des donnees realistes pour chaque endpoint
- Simuler les comportements (latence, erreurs)
- Fournir une interface de configuration

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Generation JSON structuree |

**References externes :**
- [Prism (Stoplight)](https://stoplight.io/open-source/prism) - Mock server OpenAPI
- [Faker.js](https://fakerjs.dev/) - Generation de donnees fictives

---

## Categorie F : Education & Formation

Outils pedagogiques exploitant l'IA generative.

### F1 - Generateur de Quiz (Difficulte: 2/5)

**Description :** Creer automatiquement des QCM et questions ouvertes a partir d'un document de cours.

**Objectifs :**
- Extraire les concepts cles d'un document
- Generer des questions de differents types et niveaux
- Creer des distracteurs plausibles pour les QCM
- Fournir des corrections detaillees

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/5_RAG_Modern.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/5_RAG_Modern.ipynb) | Extraction d'information |
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Structuration des quiz |

**References externes :**
- [Quizlet AI](https://quizlet.com/) - Exemple de plateforme
- [Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom%27s_taxonomy) - Niveaux cognitifs

---

### F2 - Tuteur de Code Adaptatif (Difficulte: 3/5)

**Description :** Agent pedagogue qui enseigne la programmation en s'adaptant au niveau de l'eleve.

**Objectifs :**
- Evaluer le niveau actuel de l'apprenant
- Proposer des exercices progressifs
- Fournir des explications adaptees au niveau
- Guider sans donner directement les solutions

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/2_PromptEngineering.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/2_PromptEngineering.ipynb) | Pedagogie adaptative |
| [`GenAI/Vibe-Coding/Claude-Code-101.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Vibe-Coding/Claude-Code-101.ipynb) | Assistance au code |

**References externes :**
- [Khan Academy AI](https://www.khanacademy.org/) - Tuteur Khanmigo
- [Codecademy](https://www.codecademy.com/) - Plateforme d'apprentissage

---

### F3 - Correcteur de Copies Intelligent (Difficulte: 3/5)

**Description :** Evaluer des reponses d'etudiants avec feedback personnalise et detection de plagiat.

**Objectifs :**
- Analyser les reponses selon une grille de criteres
- Generer des feedbacks constructifs et personnalises
- Detecter les similarites suspectes entre copies
- Produire des statistiques de classe

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Evaluation structuree |
| [`GradeBook.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GradeBook.ipynb) | Systeme de notation |

---

### F4 - Simulateur d'Entretien (Difficulte: 2/5)

**Description :** Preparer aux entretiens d'embauche avec questions adaptees au poste et feedback.

**Objectifs :**
- Generer des questions pertinentes selon le poste
- Evaluer les reponses de maniere constructive
- Simuler differents styles d'interviewers
- Fournir des conseils d'amelioration

---

### F5 - Generateur de Flashcards (Difficulte: 2/5)

**Description :** Creer des cartes de memorisation optimisees (style Anki) a partir de n'importe quel contenu.

**Objectifs :**
- Extraire les paires question/reponse d'un document
- Optimiser pour la memorisation (repetition espacee)
- Supporter differents types de cartes (texte, image, cloze)
- Exporter vers les formats standards (Anki, Quizlet)

**References externes :**
- [Anki](https://apps.ankiweb.net/) - Application de flashcards
- [SuperMemo Algorithm](https://supermemo.guru/wiki/SuperMemo_Algorithm) - Repetition espacee

---

### F6 - Professeur de Langues (Difficulte: 3/5)

**Description :** Assistant conversationnel pour pratiquer une langue etrangere avec corrections contextuelles.

**Objectifs :**
- Converser naturellement dans la langue cible
- Corriger les erreurs avec explications
- Adapter le niveau de difficulte
- Introduire progressivement du vocabulaire

**References externes :**
- [Duolingo Max](https://www.duolingo.com/) - Conversation IA
- [Speak](https://www.speak.com/) - Practice orale IA

---

## Categorie G : Jeux & Divertissement

Projets ludiques explorant l'IA dans les jeux.

### G1 - Bot de Jeu de Societe (Difficulte: 3/5)

**Description :** Agent jouant a un jeu de societe (Catan, Risk, Uno) avec strategie et explications de ses coups.

**Objectifs :**
- Implementer les regles du jeu
- Developper une strategie de jeu
- Expliquer les decisions prises
- S'adapter au style des adversaires

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GameTheory/01-Normal-Form-Nash.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GameTheory/01-Normal-Form-Nash.ipynb) | Fondamentaux de theorie des jeux |
| [`GameTheory/07-Extensive-Form.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GameTheory/07-Extensive-Form.ipynb) | Jeux sequentiels |
| [`RL/stable_baseline_1.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/RL/stable_baseline_1.ipynb) | Apprentissage par renforcement |

**References externes :**
- [OpenSpiel (Google)](https://github.com/google-deepmind/open_spiel) - Framework de jeux
- [BoardGame.io](https://boardgame.io/) - Framework pour jeux de plateau

---

### G2 - Generateur de Puzzles (Difficulte: 2/5)

**Description :** Creer des puzzles logiques (Sudoku, mots croises, enigmes) avec difficulte ajustable.

**Objectifs :**
- Generer des puzzles valides et resolubles
- Controler le niveau de difficulte
- Verifier l'unicite de la solution
- Fournir des indices progressifs

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`Sudoku/Sudoku-4-Z3.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Sudoku/Sudoku-4-Z3.ipynb) | Resolution et generation de Sudoku avec Z3 |
| [`Sudoku/Sudoku-3-OR-Tools.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Sudoku/Sudoku-3-OR-Tools.ipynb) | Satisfaction de contraintes |
| [`Search/CSPs_Intro.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/CSPs_Intro.ipynb) | Problemes de satisfaction de contraintes |

**References externes :**
- [Z3 Theorem Prover](https://github.com/Z3Prover/z3) - Solveur SMT
- [OR-Tools](https://developers.google.com/optimization) - Optimisation Google

---

### G3 - Commentateur Sportif IA (Difficulte: 3/5)

**Description :** Generer des commentaires en temps reel pour des matchs (e-sport, sport traditionnel).

**Objectifs :**
- Analyser les evenements du match en temps reel
- Generer des commentaires engageants et varies
- Maintenir le rythme et l'emotion appropries
- S'adapter au contexte et a l'enjeu

---

### G4 - Createur de Niveaux de Jeu (Difficulte: 3/5)

**Description :** Generer proceduralement des niveaux pour un jeu de plateforme ou puzzle.

**Objectifs :**
- Creer des niveaux jouables et equilibres
- Assurer la progressivite de la difficulte
- Garantir que chaque niveau est terminable
- Varier les mecaniques et challenges

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`Search/GeneticSharp-EdgeDetection.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/GeneticSharp-EdgeDetection.ipynb) | Algorithmes genetiques |
| [`RL/stable_baseline_2.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/RL/stable_baseline_2.ipynb) | RL pour validation de niveaux |

**References externes :**
- [Procedural Content Generation (PCG) Wiki](http://pcg.wikidot.com/) - Ressources PCG
- [WaveFunctionCollapse](https://github.com/mxgmn/WaveFunctionCollapse) - Algorithme de generation

---

### G5 - Arbitre de Debat (Difficulte: 3/5)

**Description :** Moderer et evaluer des debats entre humains ou entre agents IA sur des sujets controverses.

**Objectifs :**
- Evaluer la qualite des arguments presentes
- Detecter les sophismes et erreurs logiques
- Attribuer des points de maniere equitable
- Fournir un verdict argumente

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`SymbolicAI/Tweety/Tweety-5-Abstract-Argumentation.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-5-Abstract-Argumentation.ipynb) | Evaluation d'arguments |
| [`SymbolicAI/Argument_Analysis/01-Setup.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Argument_Analysis/01-Setup.ipynb) | Analyse computationnelle d'arguments |

---

## Categorie H : Analyse & Intelligence

Projets d'analyse de donnees et d'extraction d'insights.

### H1 - Analyseur de Sentiments (Difficulte: 2/5)

**Description :** Analyser des avis clients et classer les sentiments avec justifications detaillees.

**Objectifs :**
- Classer les sentiments (positif, negatif, neutre)
- Identifier les aspects specifiques mentionnes
- Extraire les points forts et faibles
- Generer des resumes d'insights

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Classification structuree |
| [`ML/ML.NET/1-ML.NET-Classification.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/ML/ML.NET/1-ML.NET-Classification.ipynb) | Classification ML |

---

### H2 - Detecteur de Fake News (Difficulte: 3/5)

**Description :** Evaluer la credibilite d'articles en croisant sources et detectant les biais.

**Objectifs :**
- Analyser le contenu factuel des articles
- Verifier les sources citees
- Detecter les biais et manipulations
- Attribuer un score de credibilite

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/4_Function_Calling.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/4_Function_Calling.ipynb) | Verification via APIs |
| [`SymbolicAI/Tweety/Tweety-5-Abstract-Argumentation.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-5-Abstract-Argumentation.ipynb) | Analyse logique des arguments |

**References externes :**
- [ClaimBuster](https://idir.uta.edu/claimbuster/) - Detection de claims
- [Full Fact](https://fullfact.org/) - Fact-checking

---

### H3 - Resumeur de Reunions (Difficulte: 2/5)

**Description :** Transcrire et resumer des reunions avec points cles, actions et decisions.

**Objectifs :**
- Transcrire l'audio en texte (si applicable)
- Identifier les participants et leurs interventions
- Extraire les decisions et actions a suivre
- Generer un compte-rendu structure

**References externes :**
- [Otter.ai](https://otter.ai/) - Transcription et resume
- [Fireflies.ai](https://fireflies.ai/) - Assistant de reunion

---

### H4 - Analyseur de Tendances (Difficulte: 3/5)

**Description :** Scraper les reseaux sociaux et identifier les sujets emergents dans un domaine.

**Objectifs :**
- Collecter des donnees depuis diverses sources
- Identifier les tendances emergentes
- Visualiser l'evolution temporelle
- Predire les tendances futures

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/4_Function_Calling.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/4_Function_Calling.ipynb) | Collecte de donnees |
| [`Probas/Infer/Infer-4-Bayesian-Networks.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Probas/Infer/Infer-4-Bayesian-Networks.ipynb) | Modelisation de tendances |

---

### H5 - Extracteur de Donnees Structurees (Difficulte: 2/5)

**Description :** Transformer des documents non structures (factures, formulaires) en donnees JSON.

**Objectifs :**
- Reconnaitre differents types de documents
- Extraire les champs pertinents
- Valider et normaliser les donnees
- Exporter dans des formats structures

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GenAI/Texte/3_Structured_Outputs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/3_Structured_Outputs.ipynb) | Extraction vers JSON |

**References externes :**
- [Azure Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/document-intelligence) - OCR avance
- [LlamaIndex Document Processing](https://www.llamaindex.ai/)

---

## Categorie X : IA Hybride & Projets Avances (Bonus)

Ces projets ambitieux combinent plusieurs paradigmes d'IA (symbolique, probabiliste, neuronale). Ils peuvent donner lieu a des **bonus de notation**.

### X1 - Agent d'Argumentation Logique (Difficulte: 4/5)

**Description :** Combiner un LLM (analyse informelle des arguments) et TweetyProject (logique symbolique) pour valider formellement des arguments et detecter les sophismes.

**Objectifs :**
- Extraire la structure logique des arguments naturels
- Formaliser en logique propositionnelle ou du premier ordre
- Verifier la validite et la coherence via TweetyProject
- Detecter les sophismes et erreurs de raisonnement

**Architecture hybride :**
```
Texte -> LLM (extraction) -> Formules logiques -> TweetyProject (validation) -> Verdict
```

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`SymbolicAI/Tweety/Tweety-1-Setup.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-1-Setup.ipynb) | Installation TweetyProject |
| [`SymbolicAI/Tweety/Tweety-2-Basic-Logics.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-2-Basic-Logics.ipynb) | Logique propositionnelle et FOL |
| [`SymbolicAI/Tweety/Tweety-5-Abstract-Argumentation.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-5-Abstract-Argumentation.ipynb) | Frameworks d'argumentation de Dung |
| [`SymbolicAI/Tweety/Tweety-6-Structured-Argumentation.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-6-Structured-Argumentation.ipynb) | ASPIC+ et argumentation structuree |
| [`SymbolicAI/Argument_Analysis/`](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/SymbolicAI/Argument_Analysis) | Serie complete d'analyse d'arguments |

**References externes :**
- [TweetyProject](https://tweetyproject.org/) - Bibliotheque Java de logique symbolique
- [Dung's Argumentation Frameworks](https://en.wikipedia.org/wiki/Argumentation_framework) - Theorie
- [ArgMining Shared Tasks](https://aclweb.org/aclwiki/Argument_Mining) - Benchmarks

---

### X2 - Assistant de Preuve Mathematique (Difficulte: 4/5)

**Description :** Integrer un LLM avec le prouveur Lean 4 pour assister la construction de preuves mathematiques formelles.

**Objectifs :**
- Traduire des enonces mathematiques informels en Lean 4
- Suggerer des tactiques de preuve
- Verifier formellement les preuves
- Expliquer les etapes en langage naturel

**Architecture hybride :**
```
Enonce naturel -> LLM (traduction) -> Code Lean -> Lean 4 (verification) -> Preuve validee
```

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`SymbolicAI/Lean/Lean-1-Setup.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Lean/Lean-1-Setup.ipynb) | Installation Lean 4 (WSL) |
| [`SymbolicAI/Lean/Lean-3-Propositions-Proofs.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Lean/Lean-3-Propositions-Proofs.ipynb) | Curry-Howard et preuves |
| [`SymbolicAI/Lean/Lean-5-Tactics.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Lean/Lean-5-Tactics.ipynb) | Tactiques de preuve |
| [`SymbolicAI/Lean/Lean-7-LLM-Integration.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Lean/Lean-7-LLM-Integration.ipynb) | Integration LeanCopilot et LLMs |
| [`SymbolicAI/Lean/Lean-8-Agentic-Proving.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Lean/Lean-8-Agentic-Proving.ipynb) | Agents autonomes de preuve |

**References externes :**
- [Lean 4 Documentation](https://lean-lang.org/) - Prouveur interactif
- [Mathlib4](https://github.com/leanprover-community/mathlib4) - Bibliotheque mathematique
- [LeanCopilot](https://github.com/lean-dojo/LeanCopilot) - Assistance IA pour Lean
- [AlphaProof (DeepMind)](https://deepmind.google/research/breakthroughs/alphaproof/) - SOTA en preuve automatique

---

### X3 - Systeme de Recommandation Bayesien (Difficulte: 4/5)

**Description :** Utiliser Infer.NET pour creer un systeme de recommandation probabiliste avec quantification de l'incertitude.

**Objectifs :**
- Modeliser les preferences utilisateurs probabilistiquement
- Quantifier l'incertitude des recommandations
- Expliquer les recommandations via le modele generatif
- Gerer le cold-start avec des a priori appropries

**Architecture hybride :**
```
Donnees utilisateur -> Modele bayesien (Infer.NET) -> Distributions -> LLM (explication) -> Recommandations
```

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`Probas/Infer/Infer-1-Setup.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Probas/Infer/Infer-1-Setup.ipynb) | Introduction a Infer.NET |
| [`Probas/Infer/Infer-4-Bayesian-Networks.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Probas/Infer/Infer-4-Bayesian-Networks.ipynb) | Reseaux bayesiens |
| [`Probas/Infer/Infer-12-Recommenders.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Probas/Infer/Infer-12-Recommenders.ipynb) | Systemes de recommandation Matchbox |

**References externes :**
- [Infer.NET](https://dotnet.github.io/infer/) - Framework d'inference probabiliste Microsoft
- [Matchbox Recommender](https://www.microsoft.com/en-us/research/publication/matchbox-large-scale-online-bayesian-recommendations/) - Article original
- [Bayesian Methods for Hackers](https://camdavidsonpilon.github.io/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/) - Introduction Bayesienne

---

### X4 - Negociateur Multi-Agents (Difficulte: 4/5)

**Description :** Simulation de negociation basee sur la theorie des jeux avec agents aux objectifs conflictuels cherchant un accord mutuellement benefique.

**Objectifs :**
- Modeliser des agents avec utilites et strategies differentes
- Implementer des protocoles de negociation
- Trouver des equilibres et accords optimaux
- Visualiser les dynamiques de negociation

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`GameTheory/01-Normal-Form-Nash.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GameTheory/01-Normal-Form-Nash.ipynb) | Equilibres de Nash |
| [`GameTheory/13-Cooperative-Games.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GameTheory/13-Cooperative-Games.ipynb) | Jeux cooperatifs, valeur de Shapley |
| [`GameTheory/14-Mechanism-Design.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GameTheory/14-Mechanism-Design.ipynb) | Design de mecanismes |
| [`GameTheory/17-MARL.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GameTheory/17-MARL.ipynb) | Multi-Agent Reinforcement Learning |

**References externes :**
- [ANAC (Automated Negotiating Agents Competition)](http://ii.tudelft.nl/nego/node/2) - Competition de reference
- [Nash Bargaining Solution](https://en.wikipedia.org/wiki/Nash_bargaining_solution) - Theorie
- [OpenSpiel](https://github.com/google-deepmind/open_spiel) - Framework de jeux multi-agents

---

### X5 - Planificateur sous Contraintes (Difficulte: 3/5)

**Description :** Agent utilisant Z3/OR-Tools pour resoudre des problemes d'optimisation complexes (emploi du temps, logistique, allocation de ressources).

**Objectifs :**
- Modeliser les contraintes metier en logique formelle
- Resoudre via solveur SMT ou optimisation combinatoire
- Gerer les contraintes souples et priorites
- Fournir des explications sur les solutions

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`SymbolicAI/Linq2Z3.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Linq2Z3.ipynb) | Solveur SMT Z3 |
| [`SymbolicAI/OR-tools-Stiegler.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/OR-tools-Stiegler.ipynb) | Programmation par contraintes |
| [`Sudoku/Sudoku-4-Z3.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Sudoku/Sudoku-4-Z3.ipynb) | Z3 en pratique |
| [`Search/CSPs_Intro.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/CSPs_Intro.ipynb) | Introduction aux CSPs |
| [`SymbolicAI/Planners/01-FastDownward-Setup.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Planners/01-FastDownward-Setup.ipynb) | Planification PDDL |

**References externes :**
- [Z3 Theorem Prover](https://github.com/Z3Prover/z3) - Microsoft Research
- [Google OR-Tools](https://developers.google.com/optimization) - Suite d'optimisation
- [Fast Downward](https://www.fast-downward.org/) - Planificateur PDDL

---

### X6 - Diagnostic Medical Probabiliste (Difficulte: 4/5)

**Description :** Systeme combinant reseaux bayesiens et LLM pour suggerer des diagnostics avec niveaux de confiance et explications.

**Objectifs :**
- Modeliser les relations symptomes-maladies probabilistiquement
- Calculer des probabilites de diagnostic avec incertitude
- Expliquer le raisonnement diagnostic en langage naturel
- Respecter les contraintes ethiques et deontologiques

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`Probas/Infer/Infer-4-Bayesian-Networks.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Probas/Infer/Infer-4-Bayesian-Networks.ipynb) | Reseaux bayesiens |
| [`EPF/IA101-Devoirs/CC1-Exploratoire-Symbolique/`](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/EPF/IA101-Devoirs/CC1-Exploratoire-Symbolique) | Cas medical avec IA symbolique |
| [`EPF/IA101-Devoirs/CC2-Symbolique-Probabiliste/`](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/EPF/IA101-Devoirs/CC2-Symbolique-Probabiliste) | OncoPlan - diagnostic oncologique |

**References externes :**
- [POMEGRANATE](https://pomegranate.readthedocs.io/) - Reseaux bayesiens en Python
- [pgmpy](https://pgmpy.org/) - Modeles graphiques probabilistes
- [Synthea](https://synthetichealth.github.io/synthea/) - Generateur de donnees medicales synthetiques

---

### X7 - Agent de Trading Algorithmique (Difficulte: 4/5)

**Description :** Developper un agent de trading combinant analyse technique, sentiment de marche (LLM) et apprentissage par renforcement sur la plateforme QuantConnect.

**Objectifs :**
- Analyser les donnees de marche et indicateurs techniques
- Integrer l'analyse de sentiment des actualites financieres
- Entrainer un agent RL pour les decisions de trading
- Backtester les strategies sur donnees historiques

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`QuantConnect/01-Setup.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/01-Setup.ipynb) | Introduction a QuantConnect |
| [`QuantConnect/18-ML-Features.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/18-ML-Features.ipynb) | Machine Learning pour trading |
| [`QuantConnect/23-Reinforcement-Learning.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/23-Reinforcement-Learning.ipynb) | RL pour strategies de trading |
| [`QuantConnect/26-LLM-Integration.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/QuantConnect/26-LLM-Integration.ipynb) | Integration LLM et analyse de sentiment |

**References externes :**
- [QuantConnect LEAN](https://www.quantconnect.com/) - Plateforme de trading algorithmique
- [Alpaca Markets](https://alpaca.markets/) - API de trading
- [FinRL](https://github.com/AI4Finance-Foundation/FinRL) - RL pour finance

---

### X8 - Systeme de Revision de Croyances (Difficulte: 4/5)

**Description :** Implementer un agent capable de reviser ses croyances de maniere coherente face a de nouvelles informations contradictoires.

**Objectifs :**
- Modeliser une base de croyances avec TweetyProject
- Implementer les operateurs AGM de revision
- Gerer les incoherences et contradictions
- Expliquer les changements de croyances via LLM

**Notebooks de reference :**
| Notebook | Description |
|----------|-------------|
| [`SymbolicAI/Tweety/Tweety-4-Belief-Revision.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-4-Belief-Revision.ipynb) | Revision de croyances CrMas |
| [`SymbolicAI/Tweety/Tweety-3-Advanced-Logics.ipynb`](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-3-Advanced-Logics.ipynb) | Logiques avancees (modal, defaisible) |

**References externes :**
- [AGM Postulates](https://en.wikipedia.org/wiki/Belief_revision) - Theorie de la revision
- [TweetyProject Belief Revision](http://tweetyproject.org/doc/beliefdynamics/index.html) - Documentation

---

## Ressources du Cours

### Depot de Cours Principal

Les notebooks du cours sont disponibles sur GitHub : **[jsboige/CoursIA](https://github.com/jsboige/CoursIA)**

Structure locale : `D:\dev\CoursIA\MyIA.AI.Notebooks`

### Tableau Recapitulatif des Notebooks

| Categorie | Nombre | Sujets couverts |
|-----------|--------|-----------------|
| **GenAI** | ~30 | LLMs, RAG, Function Calling, Semantic Kernel, Images |
| **SymbolicAI** | ~47 | Tweety, Lean 4, Z3, Planification, Argumentation |
| **GameTheory** | ~26 | Nash, jeux extensifs, CFR, jeux cooperatifs, MARL |
| **Probas** | ~22 | Infer.NET, reseaux bayesiens, recommandation |
| **RL** | 3 | Stable Baselines 3, PPO, HER |
| **Sudoku** | 11 | Backtracking, genetiques, Z3, OR-Tools |
| **Search** | 5 | CSPs, algorithmes genetiques, A* |
| **ML** | 14 | ML.NET, classification, AutoML |
| **QuantConnect** | 27 | Trading algorithmique, ML/DL/RL finance |
| **Total** | **~207** | - |

---

## Modalites d'Evaluation

### Evaluation Collegiale

Le projet est evalue selon un systeme d'**evaluation collegiale** combinant :
- **Evaluation par les pairs** (50%) : Chaque groupe evalue les autres projets
- **Evaluation professorale** (50%) : Note du professeur

### Criteres d'Evaluation

| Critere | Poids | Description |
|---------|-------|-------------|
| **Presentation** | 25% | Clarte de l'expose, qualite des slides, demonstration fluide, capacite a repondre aux questions |
| **Technique** | 25% | Code fonctionnel, architecture propre, bonnes pratiques, utilisation appropriee des outils et APIs |
| **Theorique** | 25% | Comprehension des concepts IA sous-jacents, justification des choix algorithmiques, maitrise du sujet |
| **Organisation/Gestion de projet** | 25% | Repartition du travail, respect des delais, documentation, commits reguliers, collaboration effective |

### Algorithme de Notation (GradeBookApp)

Le systeme utilise un algorithme de notation en **5 etapes** :

#### 1. Collecte des Evaluations
- Formulaire Google Forms pour soumettre les notes et commentaires
- Chaque evaluateur note : Presentation, Technique, Theorique, Organisation

#### 2. Filtrage et Validation
5 regles de filtrage sont appliquees :
1. **Scores invalides** : Rejet des notes hors limites (etudiants max 19.999, prof max 20, min 1)
2. **Timestamps incoherents** : Rejet si ecart > 5h entre soumissions
3. **Evaluateurs non inscrits** : Seuls les etudiants du cours peuvent evaluer
4. **Auto-evaluation** : Impossible de noter son propre groupe
5. **Doublons** : Une seule evaluation par evaluateur et par projet

#### 3. Calcul de la Note Brute
```
Note_brute = (Moyenne_etudiants + Moyenne_prof x Poids_prof) / (1 + Poids_prof)
```
Avec `Poids_prof = 1.0` (equivalent 50%/50%)

#### 4. Redressement Statistique (Z-score)
```
Note_ajustee = ((Note_brute - Moyenne_classe) / Ecart_type_classe) x Ecart_type_cible + Moyenne_cible
```
Parametres cibles :
- **Moyenne cible** : 14.0/20
- **Ecart-type cible** : 2.0

#### 5. Ajustement selon la Taille du Groupe
| Taille | Ajustement |
|--------|------------|
| 1 personne | +3.0 |
| 2 personnes | +1.0 |
| 3 personnes | 0.0 |
| 4 personnes | -1.0 |
| 5+ personnes | -2.0 |

### Feedbacks
Chaque groupe recoit :
- Sa note finale ajustee
- Les commentaires positifs des evaluateurs
- Les axes d'amelioration suggeres
- Les recommandations generales

---

## Calendrier et Livrables

| Date | Evenement |
|------|-----------|
| **Mi-semestre** | Choix du sujet et constitution des groupes |
| **25 fevrier 2026** | Date limite de soumission de la PR |
| **27 fevrier 2026** | Soutenance et demonstrations |

### Livrables Attendus

1. **Code source** dans un dossier dedie sur votre fork
2. **README.md** documentant :
   - Description du projet
   - Instructions d'installation et d'execution
   - Architecture technique
   - Demonstration d'utilisation
3. **Slides de presentation** (5-10 minutes)
4. **Demonstration fonctionnelle** lors de la soutenance

---

## Conseils pour Reussir

1. **Commencez simple** : Un prototype fonctionnel vaut mieux qu'un projet ambitieux inacheve
2. **Documentez au fur et a mesure** : N'attendez pas la fin pour ecrire votre README
3. **Testez regulierement** : Validez chaque fonctionnalite avant de passer a la suivante
4. **Etudiez les notebooks** : Les ressources du cours contiennent des exemples concrets
5. **Soyez creatifs** : Les sujets proposes sont des pistes, pas des contraintes rigides
6. **Gerez vos cles API** : Ne committez **JAMAIS** vos cles dans le depot !
7. **Utilisez `.env.example`** : Fournissez un template pour les variables d'environnement

### Structure Recommandee

```
votre-groupe/
|-- README.md           # Documentation principale
|-- requirements.txt    # Dependances Python
|-- .env.example        # Template des variables d'environnement
|-- .gitignore          # Fichiers a ignorer (dont .env)
|-- src/                # Code source
|-- docs/               # Documentation additionnelle
|-- tests/              # Tests unitaires
+-- slides/             # Presentation
```

---

## Exemples de Projets Passes

Pour vous inspirer, voici quelques exemples de projets realises par des promotions precedentes :

| Projet | Description | Categorie |
|--------|-------------|-----------|
| **Agent Protagoras** | Analyse d'arguments hybride LLM + TweetyProject | X1 |
| **Trip Planner BESTFOREVER** | Agent autonome de planification de voyage | A2 |
| **Analyseur de Biais** | Evaluation des biais dans les LLMs (genre, race, etc.) | H1 |
| **Majordome Bieber** | Assistant personnel avec APIs Google | A2 |

Ces projets sont disponibles dans le depot des annees precedentes pour consultation.

---

## Support et Questions

- **Pendant le cours** : Questions directes au professeur
- **Par email** : [Contacter le professeur]
- **Issues GitHub** : Pour les problemes techniques sur le depot

---

Bon projet a tous !

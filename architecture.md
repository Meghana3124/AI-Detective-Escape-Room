
# AI Detective – System Architecture

## Version 1 – Basic Application

```mermaid
flowchart TD
    A[Player] --> B[Streamlit Interface]
    B --> C[Basic Mystery Logic]
    C --> D[Display Story and Clues]
    D --> E[Player Selects Suspect]
    E --> F[Check Answer]
    F --> G[Display Result]
```

## Version 2 – Gemini AI Integration

```mermaid
flowchart TD
    A[Player] --> B[Streamlit Interface]
    B --> C[Python Application]
    C --> D[Google Gemini API]
    D --> E[Generate Mystery in JSON]
    E --> F[Display Suspects and Clues]
    F --> G[Player Investigation]
    G --> H[Submit Accusation]
    H --> I[Check Culprit and Score]
    I --> J[Display Final Result]
    B --> K[Request AI Hint]
    K --> D
```

## Architecture Improvements

- Version 1 provides the basic detective application.
- Version 2 integrates Google Gemini AI.
- Mysteries are generated dynamically.
- Players can request AI-powered hints.
- Difficulty levels and scoring improve interactivity.

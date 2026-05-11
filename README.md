# PetroGPT Lite 🛢️ — Asistente Inteligente para Ingeniería de Petróleos

**PetroGPT Lite** es una aplicación modular de inteligencia artificial diseñada para optimizar flujos de trabajo en la ingeniería de petróleos (Upstream). Desarrollada con un enfoque académico y profesional, la herramienta combina modelos de lenguaje de última generación (LLMs) con bibliotecas de análisis de datos para ofrecer soluciones técnicas rápidas y precisas.

## 🚀 Funcionalidades

- **Chat Técnico Especializado**: Interacción con la API de Google Gemini (1.5 Flash/Pro) para consultas sobre yacimientos, perforación y producción.
- **Calculadoras Técnicas**: Implementación modular de fórmulas críticas como Gravedad API, Drawdown, Índice de Productividad (PI) y Gradiente de Presión.
- **Analizador de Step Rate Test (SRT)**: Procesamiento de archivos CSV para la identificación visual y asistida por IA de la presión de fractura.
- **Interfaz Profesional**: Diseño basado en Streamlit con navegación por pestañas y visualizaciones interactivas mediante Plotly.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.x
- **Framework UI**: [Streamlit](https://streamlit.io/)
- **Modelos de IA**: [Google Gemini API](https://ai.google.dev/)
- **Análisis de Datos**: Pandas & Plotly
- **Seguridad**: Gestión de API Keys mediante variables de entorno.

## 📁 Estructura del Proyecto

```text
petrogpt-lite/
├── app.py                # Punto de entrada y lógica de la interfaz
├── requirements.txt      # Dependencias del sistema
├── README.md             # Documentación técnica
├── utils/                # Lógica de negocio modular
│   ├── calculations.py   # Fórmulas de ingeniería
│   ├── gemini_helper.py  # Conector con la API de IA
│   └── srt_analyzer.py   # Lógica de visualización de pruebas
└── data/                 # Directorio para almacenamiento de datasets
```

## 📦 Instalación y Uso Local

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Daniela0910/petrogpt-lite.git
   cd petrogpt-lite
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la API Key**:
   Crea una variable de entorno llamada `GEMINI_API_KEY` o configúrala en el sidebar de la aplicación.

4. **Ejecutar la aplicación**:
   ```bash
   streamlit run app.py
   ```

## ☁️ Despliegue en Streamlit Cloud

1. Sube este proyecto a un repositorio público en GitHub.
2. Conéctate a [Streamlit Cloud](https://share.streamlit.io/).
3. En **Secrets**, añade tu llave de Google AI Studio:
   ```toml
   GEMINI_API_KEY = "tu_api_key_aqui"
   ```
4. ¡Despliega!

## 📝 Ejemplo de Uso

Para utilizar el **Analizador SRT**, carga un archivo CSV con el siguiente formato:

| rate | pressure |
|------|----------|
| 200  | 1500     |
| 400  | 2800     |
| 600  | 4200     |

La aplicación generará automáticamente una gráfica de dispersión y permitirá que la IA interprete el comportamiento de la formación.

---
*Desarrollado con fines académicos para la Maestría en Ingeniería de Petróleos.*

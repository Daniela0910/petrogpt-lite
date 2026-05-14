# PetroGPT PRO 🛢️ — Plataforma Inteligente para Ingeniería de Petróleos

**PetroGPT PRO** es una plataforma integral de ingeniería digital desarrollada para optimizar procesos técnicos en las áreas de yacimientos, producción e inyección. La aplicación combina inteligencia artificial, análisis de datos y herramientas especializadas de ingeniería en un único entorno interactivo, permitiendo a los ingenieros realizar diagnósticos, cálculos y evaluaciones operacionales de manera más rápida, precisa y eficiente.

Inspirada en soluciones modernas de **Digital Oilfield**, PetroGPT PRO integra asistentes inteligentes basados en LLMs, análisis visual de datos y módulos técnicos enfocados en apoyar la toma de decisiones en operaciones upstream.

---

# 🚀 Funcionalidades Principales

## 🤖 Asistente Técnico Inteligente

* Integración con modelos de IA avanzados mediante la API de Google Gemini.
* Consultas técnicas sobre:

  * Ingeniería de yacimientos
  * Producción
  * Perforación
  * Completamiento
  * Pruebas de pozo
  * Inyección
* Generación de explicaciones técnicas y soporte operativo en tiempo real.

---

## 📊 Calculadoras de Ingeniería

Módulo modular de cálculos técnicos para operaciones upstream:

* Gravedad API
* Drawdown
* Índice de Productividad (PI)
* Gradiente de presión
* Conversión de unidades
* Cálculos básicos de producción
* Herramientas de análisis operacional

---

## 📈 Analizador de Step Rate Test (SRT)

Procesamiento inteligente de pruebas de inyección:

* Carga de archivos CSV
* Visualización interactiva con Plotly
* Identificación visual de presión de fractura
* Interpretación asistida por IA
* Análisis de tendencias y cambios de pendiente

---

## 📉 Análisis de Datos y Tendencias

* Visualización dinámica de datos de producción
* Gráficas interactivas
* Evaluación rápida de comportamiento operacional
* Soporte para interpretación técnica

---

## 🧠 Plataforma Basada en IA y Prompt Engineering

PetroGPT PRO fue desarrollada utilizando técnicas de:

* Prompt Engineering
* Integración de Large Language Models (LLMs)
* Automatización de análisis técnicos
* Diseño modular orientado a escalabilidad

La plataforma demuestra cómo la inteligencia artificial puede integrarse en flujos de trabajo reales de ingeniería de petróleos para aumentar eficiencia, velocidad de análisis y soporte a la toma de decisiones.

---

# 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Framework UI:** Streamlit
* **Modelos de IA:** Google Gemini API
* **Análisis de Datos:** Pandas
* **Visualización:** Plotly
* **Arquitectura:** Modular
* **Gestión de Configuración:** Variables de entorno
* **Control de Versiones:** Git & GitHub

---

# 📁 Estructura del Proyecto

```text
petrogpt-pro/
├── app.py
├── requirements.txt
├── README.md
├── utils/
│   ├── calculations.py
│   ├── chat_handler.py
│   ├── gemini_helper.py
│   ├── srt_analyzer.py
│   └── production_tools.py
├── assets/
├── data/
└── outputs/
```

---

# 📦 Instalación y Uso Local

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Daniela0910/petrogpt-pro.git
cd petrogpt-pro
```

---

## 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configurar API Key

Crear una variable de entorno llamada:

```bash
GEMINI_API_KEY
```

O configurarla directamente desde la interfaz de la aplicación.

---

## 4️⃣ Ejecutar la aplicación

```bash
streamlit run app.py
```

---

# ☁️ Despliegue en Streamlit Cloud

1. Subir el proyecto a GitHub.
2. Conectar el repositorio con Streamlit Cloud.
3. Configurar los Secrets:

```toml
GEMINI_API_KEY = "tu_api_key"
```

4. Desplegar la aplicación.

---

# 📝 Ejemplo de Uso

## Analizador SRT

Cargar un archivo CSV con el siguiente formato:

| rate | pressure |
| ---- | -------- |
| 200  | 1500     |
| 400  | 2800     |
| 600  | 4200     |

La plataforma generará automáticamente:

* Gráficas interactivas
* Interpretación visual
* Análisis asistido por IA
* Identificación de presión de fractura

---

# 🎯 Objetivo del Proyecto

El propósito de PetroGPT PRO es demostrar la aplicación práctica de inteligencia artificial y automatización en la ingeniería de petróleos, integrando herramientas técnicas y asistentes inteligentes en una plataforma única orientada a la productividad, análisis rápido y soporte a decisiones operacionales.

---

# 👩‍💻 Autora

Desarrollado por Daniela Mejía Jaramillo
Ingeniera de Petróleos | IA Aplicada | Digital Oilfield | Automatización y Analítica

---

# 📌 Estado del Proyecto

🚧 En desarrollo activo — nuevas funcionalidades y módulos serán incorporados continuamente.

---

*Proyecto desarrollado con fines académicos y profesionales para aplicaciones de Ingeniería de Petróleos y transformación digital en operaciones upstream.*

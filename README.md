<div align="center">

# 📊 Conversation-Style AI Data Analyst

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&pause=1000&color=4A90D9&center=true&vCenter=true&width=600&lines=Chat+with+your+data+in+plain+English!;LLM+generates+Pandas+code+instantly!;Auto+charts+%2B+Conversation+Memory!;Built+with+LangChain+%2B+Groq+%2B+Streamlit!" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)

<br/>

> 🤖 **Upload any CSV → Ask questions in plain English → Get instant answers + beautiful charts**
> 
> Powered by **LLaMA 3.1** via **Groq API** with full conversation memory

<br/>

[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red?style=flat-square)](https://github.com/Deepakkumar-3)
[![Open Source](https://img.shields.io/badge/Open%20Source-💚-green?style=flat-square)](https://github.com/Deepakkumar-3/data-analyst-ai)

</div>

---

## 🌟 What Makes This Special?

<table>
<tr>
<td width="50%">

### 🧠 AI-Powered Analysis
No SQL. No Pandas knowledge required. Just ask your question in plain English and the AI figures out the rest — generating, executing, and explaining code automatically.

</td>
<td width="50%">

### 💬 Conversation Memory
Ask follow-up questions naturally! The AI remembers your previous queries — *"Which of those categories has the most products?"* just works.

</td>
</tr>
<tr>
<td width="50%">

### 📊 Auto Chart Generation
The AI doesn't just answer — it picks the **best chart type** for your question automatically. Bar, line, pie, scatter, histogram — all rendered with interactive Plotly visuals.

</td>
<td width="50%">

### 🛡️ Safe Code Execution
LLM-generated code runs in a **sandboxed environment** — no dangerous imports, no file access. Plus an auto-fix loop that corrects errors on the fly.

</td>
</tr>
</table>

---

## ✨ Features

```
📁  CSV Upload          →  Drag & drop any dataset instantly
🔍  Auto Data Profile   →  Shape, types, missing values, stats at a glance
💬  Chat Interface      →  Ask questions in plain English
🤖  Code Generation     →  LLM writes Pandas code automatically
⚙️  Safe Execution      →  Sandboxed Python environment
🔧  Auto Error Fix      →  Self-correcting pipeline on failures
📊  Smart Charts        →  AI picks the right chart type every time
🧠  Memory              →  Remembers last 4 conversation turns
💾  Export Results      →  Download answers as CSV
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)                │
│  ┌──────────────┐  ┌──────────────────────────────────────┐ │
│  │  CSV Upload  │  │        Chat Interface                 │ │
│  │  + Profile   │  │  You: "Average price by category?"   │ │
│  └──────────────┘  └──────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  LangChain +    │
                    │  Groq LLaMA 3.1 │  ← Generates Pandas Code
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Safe Sandbox   │  ← Executes Code
                    │  exec() + guard │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
      ┌───────▼──────┐ ┌────▼─────┐ ┌─────▼──────┐
      │   Result     │ │  Plotly  │ │  Memory    │
      │   Table      │ │  Chart   │ │  Storage   │
      └──────────────┘ └──────────┘ └────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:---:|:---:|:---|
| 🧠 **LLM** | LLaMA 3.1 8B via Groq | Code generation & chart selection |
| 🔗 **Orchestration** | LangChain | Prompt management & memory |
| 📊 **Visualization** | Plotly Express | Interactive charts |
| 🐼 **Data** | Pandas + NumPy | Data processing & execution |
| 🌐 **Frontend** | Streamlit | Web UI & chat interface |
| 🔑 **API** | Groq API (Free) | Fast LLM inference |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Deepakkumar-3/data-analyst-ai.git
cd data-analyst-ai
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Get Your Free Groq API Key
```
🔗 Go to: console.groq.com
✅ Sign up → API Keys → Create New Key
📋 Copy your key (starts with gsk_...)
```

### 4️⃣ Run the App
```bash
streamlit run app.py
```

---

## 🚀 How to Use

```
Step 1 → Enter your Groq API key in the sidebar
Step 2 → Upload any CSV file
Step 3 → View the auto data profile (rows, columns, missing values)
Step 4 → Ask any question in plain English
Step 5 → Get instant answers + interactive charts
Step 6 → Ask follow-up questions — the AI remembers context!
```

---

## 💬 Example Questions You Can Ask

> 💡 These work on any dataset — the AI adapts to your columns automatically!

```python
# 📦 Basic Analysis
"What are the unique categories in the dataset?"
"How many rows have missing values?"
"Show me the top 10 most expensive products"

# 📊 Aggregations
"What is the average price for each category?"
"Which category has the highest average rating?"
"What is the total discount given per category?"

# 🔍 Filtering
"How many products are Out of Stock?"
"Show products with discount greater than 30%"
"Which products have a rating above 4.5?"

# 🧠 Follow-up (Memory)
"Which of those categories has the most products?"
"What is the price range for that category?"
"Show me the rating distribution for those items"
```

---

## 📁 Project Structure

```
data-analyst-ai/
│
├── 📄 app.py                  # Main Streamlit application
├── 📋 requirements.txt        # Python dependencies
└── 📖 README.md               # Project documentation
```

---

## 📦 Requirements

```txt
streamlit
langchain
langchain-groq
groq
plotly
pandas
numpy
```

---

## 🔒 Security Features

```
✅ Sandboxed exec() — __builtins__ blocked
✅ No file system access from generated code
✅ No network calls from generated code
✅ df.copy() — original data never mutated
✅ API key input via password field — never exposed
✅ Auto error correction — no raw tracebacks shown to user
```

---

## 🎯 Key Technical Highlights

| Highlight | Detail |
|:---|:---|
| **Zero-temperature LLM** | `temperature=0` for deterministic, precise code generation |
| **Self-healing pipeline** | Failed code is automatically sent back to LLM for correction |
| **Smart chart selection** | LLM analyzes question + result type to pick optimal visualization |
| **Context-aware memory** | Last 4 conversation turns passed as context — token-efficient |
| **Graceful degradation** | Chart failures fall back to table view without crashing |

---

## 👨‍💻 Author

<div align="center">

**Deepakkumar M**

*B.E. Electronics & Communication Engineering*
*Jeppiaar Engineering College, Anna University, Chennai*

[![GitHub](https://img.shields.io/badge/GitHub-Deepakkumar--3-black?style=for-the-badge&logo=github)](https://github.com/Deepakkumar-3)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/deepakkumar-m-498673264)

</div>

---

## 📄 License

```
MIT License — Free to use, modify, and distribute
```

---

<div align="center">

### ⭐ If you found this useful, give it a star!

*Built with 🤖 AI + ❤️ by Deepakkumar M*

</div>

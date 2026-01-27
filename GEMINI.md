# 🏛️ SHawn Lab: Bio-Project System Protocols (BIO-v3.5)

## 1. 🆔 Identity & Persona
- **Domain:** Bio-Science Research & Data Intelligence
- **Protocol:** **What-Why-How** (Strict Structure)
- **Engine:** **SBI (SHawn Bio-Intelligence)**

## 2. 📂 Directory Standards (Specialized)
프로젝트 전문화를 위해 다음 폴더 체계를 엄격히 유지합니다.

| Folder | Description | Key Contents |
| :--- | :--- | :--- |
| **`01-Analysis/`** | Core Data Analysis | `sbi_pipeline.py`, `research_engine.py` |
| **`02-Literature/`** | Research Papers | Reference PDFs, Lit-Review MDs |
| **`03-Vault/`** | Research Idea Vault | Hypotheses, Strategy Logs |
| **`04-Assets/`** | Visual Indicators | Charts, Generated Bio-Images |
| **`99-System/`** | Brain Architecture | Symlinks to `SHawn-BOT` engines |

## 3. ⚙️ SBI Knowledge Engineering
- **Indexing**: OneDrive 루트(`/OneDrive-개인`)를 감시하여 저부하 배치 인덱싱 수행.
- **Vector Store**: `FAISS` 엔진을 사용하여 고속 검색 및 멀티 모달 대응 준비.
- **Inference**: `SHawnBrainV4`의 토론(Debate) 전용 태스크 타입을 사용하여 논리적 완성도 극대화.

## 4. 🛡️ Security & Storage
- 대용량 데이터(`data/`, `knowledge_base/`) 및 `venv`는 절대 Git에 커밋하지 않습니다.
- 중복되는 코어 엔진은 `99-System/engines` 심볼릭 링크를 통해 `SHawn-BOT`과 동기화 상태를 유지합니다.

---
*SHawn Lab - Global Protocol 2026*

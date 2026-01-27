# 🧬 SHawn-BIO: Specialized Bio-Research Hub (v3.5)

> **SHawn Lab: High-Performance Bio-Science Research & Intelligence Division**

이 프로젝트는 암 치료, 오가노이드 기술, 정밀 의료 등 첨단 바이오 사이언스 리서치 데이터와 AI 기반의 지능형 분석 파이프라인을 운영하는 전문 리서치 허브입니다.

## 📂 Specialized Directory Structure
전문 연구 워크플로우를 위해 구조가 고도화되었습니다.

- **`01-Analysis/`**: 데이터 분석, RAG 파이프라인(`SBI`), 시뮬레이션 스크립트.
- **`02-Literature/`**: 연구 논문(PDF), 문헌 리뷰, 참고 자료 아카이브.
- **`03-Vault/`**: Obsidian 연동 지식 그래프 및 가설(Hypothesis) 메모 공간.
- **`04-Assets/`**: 분석 결과 시각화 차트, 이미지 자료 리포지토리.
- **`99-System/`**: 봇 브레인(`shawn_brain_v4`) 연동 심볼릭 링크 및 코어 모듈.
- **`data/` & `knowledge_base/`**: 로컬 실험 데이터 및 FAISS 벡터 인덱스 저장소.

## 🧠 SBI (SHawn Bio-Intelligence)
원드라이브와 연동된 하이브리드 지식 엔진입니다.
- **Search**: `01-Analysis/sbi_pipeline.py`를 통해 수천 개의 문헌을 1초 내에 검색.
- **Analyze**: `ResearchEngine`이 토론 모드(`Debate`)를 통해 새로운 연구 가설 제안.

## 🚀 Getting Started
1. `01-Analysis/test_sbi_research.py`를 실행하여 통합 리서치 환경 검증.
2. 원드라이브 루트의 연구 데이터를 봇이 실시간으로 학습하도록 자동화됨.

## 📜 Governance
- 모든 연구 결과는 **What-Why-How** 삼단논법에 따라 기술적 타당성을 확보합니다.
- 상세 운영 규정은 `GEMINI.md`를 참조하세요.

---
*Powered by SHawn-Bot AI-Intelligence Network*
# engines/sbi_pipeline.py
import os
import glob
import pickle
import numpy as np
from typing import List, Dict, Optional
from loguru import logger
import faiss
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

class SBIPipeline:
    """SHawn Bio-Intelligence (SBI) Knowledge Pipeline (FAISS Edition)"""
    
    def __init__(self, 
                 onedrive_path: str = "/Users/soohyunglee/Library/CloudStorage/OneDrive-개인",
                 db_path: Optional[str] = None):
        self.onedrive_path = onedrive_path
        
        # 프로젝트 루트 기준으로 db_path 설정
        if db_path is None:
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(os.path.dirname(curr_dir), "knowledge_base")
        else:
            self.db_path = db_path
        self.index_file = os.path.join(self.db_path, "faiss_index.bin")
        self.data_file = os.path.join(self.db_path, "knowledge_data.pkl")
        
        # 임베딩 모델 로드
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        
        # 인덱스 및 데이터 초기화
        self.index = None
        self.metadata = [] # List of {content, source}
        self.indexed_files = set()
        
        self.load_index()
        logger.info(f"🧬 SBI FAISS Pipeline initialized. Monitoring: {onedrive_path}")

    def load_index(self):
        """저장된 인덱스와 메타데이터 로드"""
        if os.path.exists(self.index_file) and os.path.exists(self.data_file):
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.data_file, 'rb') as f:
                    save_data = pickle.load(f)
                    self.metadata = save_data['metadata']
                    self.indexed_files = save_data['indexed_files']
                logger.info(f"📁 Loaded existing index with {len(self.metadata)} chunks.")
            except Exception as e:
                logger.error(f"❌ Failed to load index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()

    def _create_new_index(self):
        """새 FAISS 인덱스 생성"""
        dimension = 384 # all-MiniLM-L6-v2 output dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []
        self.indexed_files = set()
        logger.info("🆕 Created fresh FAISS index.")

    def save_index(self):
        """인덱스와 메타데이터 파일로 저장"""
        os.makedirs(self.db_path, exist_ok=True)
        faiss.write_index(self.index, self.index_file)
        with open(self.data_file, 'wb') as f:
            pickle.dump({
                'metadata': self.metadata,
                'indexed_files': self.indexed_files
            }, f)
        logger.success("💾 FAISS index and metadata saved.")

    def load_and_index(self, force: bool = False):
        """원드라이브 폴더 스캔 및 신규 파일 인덱싱 (부하 방지 배치 처리 적용)"""
        import time
        files = glob.glob(os.path.join(self.onedrive_path, "**/*.pdf"), recursive=True) + \
                glob.glob(os.path.join(self.onedrive_path, "**/*.txt"), recursive=True)
        
        new_files = [f for f in files if f not in self.indexed_files or force]
        if not new_files:
            logger.info("✨ No new files found in OneDrive.")
            return

        logger.info(f"📂 Found {len(new_files)} new files to index. Starting throttled indexing...")
        
        batch_size = 10
        for i in range(0, len(new_files), batch_size):
            batch = new_files[i:i + batch_size]
            logger.info(f"🚀 Processing Batch {i//batch_size + 1}/{(len(new_files)-1)//batch_size + 1} ({len(batch)} files)...")
            
            for file_path in batch:
                try:
                    self._index_file(file_path)
                    self.indexed_files.add(file_path)
                    # 파일 간 짧은 지연 (CPU 쿨링)
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"❌ Failed to index {file_path}: {e}")
            
            # 배치 간 중간 지연 (메모리 정리 유도)
            self.save_index()
            if i + batch_size < len(new_files):
                logger.info("⏳ Batch completed. Cooling down for 3 seconds...")
                time.sleep(3)

    def _index_file(self, file_path: str):
        """단일 파일 파싱 및 벡터화"""
        file_name = os.path.basename(file_path)
        logger.info(f"⏳ Processing {file_name}...")
        
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
            
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        contents = [chunk.page_content for chunk in chunks]
        embeddings = self.model.encode(contents).astype('float32')
        
        self.index.add(embeddings)
        for content in contents:
            self.metadata.append({"content": content, "source": file_name})
            
        logger.success(f"✅ Added {len(chunks)} chunks from {file_name}")

    def search(self, query: str, n_results: int = 3) -> List[Dict]:
        """지식 검색"""
        if self.index is None or len(self.metadata) == 0:
            return []
            
        query_vector = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_vector, n_results)
        
        hits = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                hits.append({
                    "content": self.metadata[idx]['content'],
                    "source": self.metadata[idx]['source'],
                    "distance": float(distances[0][i])
                })
        return hits

if __name__ == "__main__":
    pipeline = SBIPipeline()
    pipeline.load_and_index()
    
    test_query = "오가노이드"
    results = pipeline.search(test_query)
    print(f"\n🔍 Search Results for '{test_query}':")
    for hit in results:
        print(f"- [{hit['source']}] {hit['content'][:150]}...")

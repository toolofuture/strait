import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

class ReflexionEngine:
    """Re-flexion 자기개선 시스템"""
    
    def __init__(self, data_file: str = "reflexion_data.json"):
        self.data_file = data_file
        self.feedback_data = self._load_feedback_data()
    
    def _load_feedback_data(self) -> List[Dict[str, Any]]:
        """피드백 데이터 로드"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_feedback_data(self):
        """피드백 데이터 저장"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_data, f, ensure_ascii=False, indent=2)
    
    def record_feedback(self, 
                       analysis_result: Dict[str, Any],
                       user_feedback: str,
                       image_path: Optional[str] = None) -> Dict[str, Any]:
        """피드백 기록"""
        
        feedback_record = {
            'timestamp': datetime.now().isoformat(),
            'user_feedback': user_feedback,  # 'correct', 'incorrect', 'uncertain'
            'analysis_result': analysis_result,
            'image_path': image_path,
            'improvement_notes': self._generate_improvement_notes(analysis_result, user_feedback)
        }
        
        self.feedback_data.append(feedback_record)
        self._save_feedback_data()
        
        return feedback_record
    
    def _generate_improvement_notes(self, 
                                  analysis_result: Dict[str, Any], 
                                  user_feedback: str) -> str:
        """개선 노트 생성"""
        
        if user_feedback == 'correct':
            return "정확한 분석. 현재 모델 파라미터 유지."
        elif user_feedback == 'incorrect':
            return "부정확한 분석. 모델 파라미터 조정 필요."
        else:
            return "불확실한 피드백. 추가 데이터 수집 필요."
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """학습 인사이트 생성"""
        
        if not self.feedback_data:
            return {
                'total_feedback': 0,
                'accuracy_rate': 0.0,
                'common_errors': [],
                'improvement_suggestions': []
            }
        
        # 정확도 계산
        correct_count = sum(1 for record in self.feedback_data 
                          if record['user_feedback'] == 'correct')
        total_count = len(self.feedback_data)
        accuracy_rate = correct_count / total_count if total_count > 0 else 0.0
        
        # 일반적인 오류 패턴 분석
        incorrect_records = [record for record in self.feedback_data 
                           if record['user_feedback'] == 'incorrect']
        
        common_errors = self._analyze_common_errors(incorrect_records)
        
        # 개선 제안
        improvement_suggestions = self._generate_improvement_suggestions(
            accuracy_rate, common_errors)
        
        return {
            'total_feedback': total_count,
            'accuracy_rate': accuracy_rate,
            'common_errors': common_errors,
            'improvement_suggestions': improvement_suggestions,
            'recent_feedback': self.feedback_data[-5:] if len(self.feedback_data) >= 5 else self.feedback_data
        }
    
    def _analyze_common_errors(self, incorrect_records: List[Dict[str, Any]]) -> List[str]:
        """일반적인 오류 패턴 분석"""
        
        error_patterns = []
        
        for record in incorrect_records:
            analysis = record.get('analysis_result', {})
            
            # 신뢰도가 높았지만 틀린 경우
            if analysis.get('confidence_score', 0) > 0.8:
                error_patterns.append("높은 신뢰도로 틀린 판정")
            
            # 데이터 완성도 분석 오류
            completeness = analysis.get('data_completeness', {})
            if completeness.get('completeness_score', 1.0) > 0.8:
                error_patterns.append("정보 완성도 높게 평가했지만 틀림")
            
            # 의심 요소를 놓친 경우
            suspicious = analysis.get('suspicious_elements', [])
            if not suspicious:
                error_patterns.append("의심 요소를 놓침")
        
        # 가장 빈번한 오류 패턴
        from collections import Counter
        error_counts = Counter(error_patterns)
        return [error for error, count in error_counts.most_common(3)]
    
    def _generate_improvement_suggestions(self, 
                                        accuracy_rate: float, 
                                        common_errors: List[str]) -> List[str]:
        """개선 제안 생성"""
        
        suggestions = []
        
        if accuracy_rate < 0.7:
            suggestions.append("전체적인 모델 성능 개선 필요")
        
        if "높은 신뢰도로 틀린 판정" in common_errors:
            suggestions.append("신뢰도 계산 알고리즘 개선")
        
        if "정보 완성도 높게 평가했지만 틀림" in common_errors:
            suggestions.append("데이터 완성도 분석 로직 개선")
        
        if "의심 요소를 놓침" in common_errors:
            suggestions.append("의심 요소 탐지 알고리즘 강화")
        
        if not suggestions:
            suggestions.append("현재 성능이 양호함. 지속적인 모니터링 권장")
        
        return suggestions
    
    def get_feedback_statistics(self) -> Dict[str, Any]:
        """피드백 통계"""
        
        if not self.feedback_data:
            return {}
        
        df = pd.DataFrame(self.feedback_data)
        
        # 피드백 분포
        feedback_dist = df['user_feedback'].value_counts().to_dict()
        
        # 시간별 피드백 추이
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_feedback = df.groupby('date').size().to_dict()
        
        # 신뢰도 분포
        confidence_scores = [record.get('analysis_result', {}).get('confidence_score', 0) 
                           for record in self.feedback_data]
        
        return {
            'feedback_distribution': feedback_dist,
            'daily_feedback_trend': daily_feedback,
            'confidence_statistics': {
                'mean': sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
                'min': min(confidence_scores) if confidence_scores else 0,
                'max': max(confidence_scores) if confidence_scores else 0
            }
        }
    
    def export_learning_data(self, export_file: str = "learning_export.json"):
        """학습 데이터 내보내기"""
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'total_records': len(self.feedback_data),
            'insights': self.get_learning_insights(),
            'statistics': self.get_feedback_statistics(),
            'raw_data': self.feedback_data
        }
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return export_data

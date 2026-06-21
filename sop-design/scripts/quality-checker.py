# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
SOP输出质量检查工具
根据预定质量标准验证SOP输出结果
"""

import json
import sys
import argparse
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enumclass QualityLevel(Enum):
    """质量等级枚举"""
    EXCELLENT = "excellent"  # 优秀: 90-100分
    GOOD = "good"          # 良好: 75-89分  
    ACCEPTABLE = "acceptable"  # 合格: 60-74分
    POOR = "poor"          # 不合格: <60分

@dataclass
class QualityMetric:
    """质量指标"""
    name: str
    weight: float  # 权重0-1
    description: str
    evaluation_function: callable
    target_value: Any = None
    
@dataclass 
class QualityResult:
    """质量检查结果"""
    metric_name: str
    score: float  # 0-100
    weight: float
    weighted_score: float
    feedback: str
    passed: bool
    
class QualityChecker:
    """SOP输出质量检查器"""
    
    def __init__(self):
        # 定义各领域的标准质量指标
        self.domain_metrics = {
            'technical': self._create_technical_metrics(),
            'content': self._create_content_metrics(),
            'analysis': self._create_analysis_metrics(),
            'generic': self._create_generic_metrics()
        }
    
    def _create_technical_metrics(self) -> List[QualityMetric]:
        """创建技术开发领域指标"""
        return [
            QualityMetric(
                name="代码规范符合度",
                weight=0.25,
                description="代码符合预定编码规范的程度",
                evaluation_function=self._evaluate_code_standards,
                target_value=95
            ),
            QualityMetric(
                name="单元测试覆盖率",
                weight=0.20,
                description="自动测试覆盖核心功能的比例",
                evaluation_function=self._evaluate_test_coverage,
                target_value=85
            ),
            QualityMetric(
                name="性能达标率",
                weight=0.20,
                description="满足性能要求的比例",
                evaluation_function=self._evaluate_performance,
                target_value=100
            ),
            QualityMetric(
                name="安全漏洞数",
                weight=0.15,
                description="发现的安全漏洞数量",
                evaluation_function=self._evaluate_security,
                target_value=0
            ),
            QualityMetric(
                name="文档完整性",
                weight=0.10,
                description="相关文档的完整程度",
                evaluation_function=self._evaluate_documentation,
                target_value=90
            ),
            QualityMetric(
                name="可维护性评分",
                weight=0.10,
                description="代码易于维护和扩展的程度",
                evaluation_function=self._evaluate_maintainability,
                target_value=85
            )
        ]
    
    def _create_content_metrics(self) -> List[QualityMetric]:
        """创建内容创作领域指标"""
        return [
            QualityMetric(
                name="格式规范评分",
                weight=0.25,
                description="内容格式符合标准的程度",
                evaluation_function=self._evaluate_format,
                target_value=90
            ),
            QualityMetric(
                name="核心信息完整度", 
                weight=0.25,
                description="关键信息完整传达的比例",
                evaluation_function=self._evaluate_completeness,
                target_value=100
            ),
            QualityMetric(
                name="可读性评分",
                weight=0.20,
                description="内容易于理解和阅读的程度",
                evaluation_function=self._evaluate_readability,
                target_value=85
            ),
            QualityMetric(
                name="原创性要求",
                weight=0.15,
                description="内容的原创性和独特性",
                evaluation_function=self._evaluate_originality,
                target_value=80
            ),
            QualityMetric(
                name="目标受众匹配度",
                weight=0.15,
                description="内容适合目标受众的程度",
                evaluation_function=self._evaluate_audience_match,
                target_value=90
            )
        ]
    
    def _create_analysis_metrics(self) -> List[QualityMetric]:
        """创建数据分析领域指标"""
        return [
            QualityMetric(
                name="数据准确率",
                weight=0.30,
                description="分析所使用的数据准确性",
                evaluation_function=self._evaluate_data_accuracy,
                target_value=99.5
            ),
            QualityMetric(
                name="分析深度评分",
                weight=0.25,
                description="分析的深入程度和洞察力",
                evaluation_function=self._evaluate_analysis_depth,
                target_value=85
            ),
            QualityMetric(
                name="可视化清晰度",
                weight=0.20,
                description="数据和结果的可视化质量",
                evaluation_function=self._evaluate_visualization,
                target_value=90
            ),
            QualityMetric(
                name="洞察价值评估",
                weight=0.15,
                description="分析结果的实际应用价值",
                evaluation_function=self._evaluate_insight_value,
                target_value=80
            ),
            QualityMetric(
                name="报告结构完整性",
                weight=0.10,
                description="分析报告的结构和组织质量",
                evaluation_function=self._evaluate_report_structure,
                target_value=90
            )
        ]
    
    def _create_generic_metrics(self) -> List[QualityMetric]:
        """创建通用流程指标"""
        return [
            QualityMetric(
                name="步骤完成度",
                weight=0.30,
                description="所有预定步骤的完成比例",
                evaluation_function=self._evaluate_step_completion,
                target_value=100
            ),
            QualityMetric(
                name="质量标准符合率",
                weight=0.25,
                description="符合各项质量标准的比例",
                evaluation_function=self._evaluate_standard_compliance,
                target_value=95
            ),
            QualityMetric(
                name="时间效率得分",
                weight=0.20,
                description="在规定时间内完成任务的程度",
                evaluation_function=self._evaluate_time_efficiency,
                target_value=90
            ),
            QualityMetric(
                name="用户满意度",
                weight=0.15,
                description="最终用户对结果的满意程度",
                evaluation_function=self._evaluate_user_satisfaction,
                target_value=90
            ),
            QualityMetric(
                name="可复制性评分",
                weight=0.10,
                description="流程可被新人成功复制的程度",
                evaluation_function=self._evaluate_reproducibility,
                target_value=95
            )
        ]
    
    # ====== 评估函数实现 ======
    
    def _evaluate_code_standards(self, data: Dict) -> float:
        """评估代码规范符合度"""
        # 在实际应用中应调用真正的代码检查工具
        violations = data.get('code_standards_violations', 10)
        total_lines = data.get('total_lines', 1000)
        violation_rate = (violations / total_lines) * 1000  # 每千行违规数
        
        # 转换为0-100分
        if violation_rate <= 5:
            return 100
        elif violation_rate <= 10:
            return 90
        elif violation_rate <= 15:
            return 80
        elif violation_rate <= 20:
            return 70
        else:
            return 60
    
    def _evaluate_test_coverage(self, data: Dict) -> float:
        """评估测试覆盖率"""
        coverage = data.get('test_coverage_percentage', 0)
        return min(100, coverage)  # 直接使用覆盖率百分比，上限100
    
    def _evaluate_performance(self, data: Dict) -> float:
        """评估性能达标率"""
        met_requirements = data.get('met_performance_requirements', 0)
        total_requirements = data.get('total_performance_requirements', 10)
        
        if total_requirements == 0:
            return 100
        
        rate = (met_requirements / total_requirements) * 100
        return rate
    
    def _evaluate_security(self, data: Dict) -> float:
        """评估安全漏洞"""
        vulnerabilities = data.get('security_vulnerabilities', 3)
        
        if vulnerabilities == 0:
            return 100
        elif vulnerabilities == 1:
            return 90
        elif vulnerabilities == 2:
            return 80
        elif vulnerabilities == 3:
            return 70
        else:
            return 50
    
    def _evaluate_documentation(self, data: Dict) -> float:
        """评估文档完整性"""
        documented_sections = data.get('documented_sections', 0)
        total_sections = data.get('total_sections', 10)
        
        if total_sections == 0:
            return 100
        
        completeness = (documented_sections / total_sections) * 100
        return completenessdef _evaluate_maintainability(self, data: Dict) -> float:
        """评估可维护性"""
        # 这是一个简化的评估
        complexity_score = data.get('cyclomatic_complexity_score', 70)  # 1-100
        modularity_score = data.get('modularity_score', 80)  # 1-100
        documentation_score = data.get('documentation_score', 75)  # 1-100
        
        avg_score = (complexity_score + modularity_score + documentation_score) / 3
        return avg_score
    
    def _evaluate_format(self, data: Dict) -> float:
        """评估格式规范"""
        format_errors = data.get('format_errors', 5)
        total_elements = data.get('total_elements', 100)
        
        if total_elements == 0:
            return 100
        
        error_rate = (format_errors / total_elements) * 100
        
        if error_rate <= 1:
            return 100
        elif error_rate <= 3:
            return 90
        elif error_rate <= 5:
            return 80
        elif error_rate <= 10:
            return 70
        else:
            return 60
    
    def _evaluate_completeness(self, data: Dict) -> float:
        """评估信息完整度"""
        completed_items = data.get('completed_items', 0)
        total_items = data.get('total_items', 10)
        
        if total_items == 0:
            return 100
        
        completeness = (completed_items / total_items) * 100
        return completeness
    
    def _evaluate_readability(self, data: Dict) -> float:
        """评估可读性"""
        # 这是一个简化的评估
        grammar_score = data.get('grammar_score', 85)  # 1-100
        structure_score = data.get('structure_score', 80)  # 1-100
        clarity_score = data.get('clarity_score', 75)  # 1-100
        
        avg_score = (grammar_score + structure_score + clarity_score) / 3
        return avg_score
    
    def _evaluate_originality(self, data: Dict) -> float:
        """评估原创性"""
        plagiarism_score = data.get('plagiarism_percentage', 20)  # 抄袭比例(0-100)
        originality = 100 - plagiarism_score
        return max(0, originality)  # 确保非负
    
    def _evaluate_audience_match(self, data: Dict) -> float:
        """评估目标受众匹配度"""
        audience_feedback = data.get('audience_feedback_score', 85)  # 1-100
        return audience_feedback
    
    def _evaluate_data_accuracy(self, data: Dict) -> float:
        """评估数据准确率"""
        accuracy = data.get('data_accuracy_percentage', 99.5)
        return min(100, accuracy)  # 上限100
    
    def _evaluate_analysis_depth(self, data: Dict) -> float:
        """评估分析深度"""
        depth_level = data.get('analysis_depth_level', 3)  # 1-5级
        # 转换为0-100分
        return (depth_level / 5) * 100
    
    def _evaluate_visualization(self, data: Dict) -> float:
        """评估可视化清晰度"""
        # 这是一个简化的评估
        clarity_score = data.get('visualization_clarity', 85)  # 1-100
        accuracy_score = data.get('visualization_accuracy', 90)  # 1-100
        
        avg_score = (clarity_score + accuracy_score) / 2
        return avg_score
    
    def _evaluate_insight_value(self, data: Dict) -> float:
        """评估洞察价值"""
        usefulness = data.get('insight_usefulness', 80)  # 1-100
        actionability = data.get('insight_actionability', 75)  # 1-100
        
        avg_score = (usefulness + actionability) / 2
        return avg_score
    
    def _evaluate_report_structure(self, data: Dict) -> float:
        """评估报告结构完整性"""
        structured_sections = data.get('structured_sections', 0)
        total_sections = data.get('total_sections', 10)
        
        if total_sections == 0:
            return 100
        
        structure_score = (structured_sections / total_sections) * 100
        return structure_score
    
    def _evaluate_step_completion(self, data: Dict) -> float:
        """评估步骤完成度"""
        completed_steps = data.get('completed_steps', 0)
        total_steps = data.get('total_steps', 10)
        
        if total_steps == 0:
            return 100
        
        completion_rate = (completed_steps / total_steps) * 100
        return completion_rate
    
    def _evaluate_standard_compliance(self, data: Dict) -> float:
        """评估质量标准符合率"""
        complied_standards = data.get('complied_standards', 0)
        total_standards = data.get('total_standards', 10)
        
        if total_standards == 0:
            return 100
        
        compliance_rate = (complied_standards / total_standards) * 100
        return compliance_rate
    
    def _evaluate_time_efficiency(self, data: Dict) -> float:
        """评估时间效率"""
        actual_time = data.get('actual_time_hours', 20)
        planned_time = data.get('planned_time_hours', 15)
        
        if planned_time == 0:
            return 100
        
        efficiency = (planned_time / actual_time) * 100
        return min(100, efficiency)  # 上限100%
    
    def _evaluate_user_satisfaction(self, data: Dict) -> float:
        """评估用户满意度"""
        satisfaction_score = data.get('user_satisfaction_score', 85)  # 1-100
        return satisfaction_score
    
    def _evaluate_reproducibility(self, data: Dict) -> float:
        """评估可复制性"""
        success_rate = data.get('reproduction_success_rate', 95)  # 复现成功率
        return min(100, success_rate)
    
    def check_quality(self, domain: str, evaluation_data: Dict) -> Dict[str, Any]:
        """执行质量检查"""
        if domain not in self.domain_metrics:
            domain = 'generic'
        
        metrics = self.domain_metrics[domain]
        results = []
        total_score = 0.0
        total_weight = 0.0
        
        # 计算每个指标的得分
        for metric in metrics:
            try:
                score = metric.evaluation_function(evaluation_data)
                score = max(0, min(100, score))  # 确保在0-100范围内
                
                weighted_score = score * metric.weight
                passed = score >= metric.target_value if metric.target_value else True
                
                result = QualityResult(
                    metric_name=metric.name,
                    score=score,
                    weight=metric.weight,
                    weighted_score=weighted_score,
                    feedback=f"目标值: {metric.target_value}，实际值: {score:.1f}",
                    passed=passed
                )
                results.append(result)
                
                total_score += weighted_score
                total_weight += metric.weight
            except Exception as e:
                print(f"评估指标 {metric.name} 时出错: {e}")
                continue
        
        # 计算总体得分
        if total_weight > 0:
            overall_score = total_score / total_weight
        else:
            overall_score = 0
        
        # 确定质量等级
        quality_level = self._determine_quality_level(overall_score)
        
        # 检查是否通过最低要求
        all_passed = all(r.passed for r in results)
        
        # 生成详细报告
        failed_metrics = [r for r in results if not r.passed]
        
        return {
            'domain': domain,
            'overall_score': overall_score,
            'quality_level': quality_level.value,
            'passed': all_passed,
            'detailed_results': [r.__dict__ for r in results],
            'summary': {
                'total_metrics': len(results),
                'passed_metrics': sum(1 for r in results if r.passed),
                'failed_metrics': len(failed_metrics),
                'recommendations': self._generate_recommendations(failed_metrics)
            }
        }
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """根据得分确定质量等级"""
        if score >= 90:
            return QualityLevel.EXCELLENT
        elif score >= 75:
            return QualityLevel.GOOD
        elif score >= 60:
            return QualityLevel.ACCEPTABLE
        else:
            return QualityLevel.POOR
    
    def _generate_recommendations(self, failed_metrics: List[QualityResult]) -> List[str]:
        """根据失败的指标生成改进建议"""
        recommendations = []
        
        for metric in failed_metrics:
            rec = f"指标 {metric.metric_name} 不达标 (得分: {metric.score:.1f})。建议："
            
            if '规范' in metric.metric_name or '标准' in metric.metric_name:
                rec += "加强标准培训，建立检查清单"
            elif '测试' in metric.metric_name:
                rec += "增加测试覆盖率，强化测试用例设计"
            elif '性能' in metric.metric_name:
                rec += "性能优化，监控关键指标"
            elif '安全' in metric.metric_name:
                rec += "安全审查，漏洞扫描"
            elif '完整' in metric.metric_name:
                rec += "建立完整性检查清单"
            elif '时间' in metric.metric_name or '效率' in metric.metric_name:
                rec += "优化工作流程，减少等待时间"
            elif '用户' in metric.metric_name:
                rec += "加强用户沟通，收集反馈"
            else:
                rec += "针对具体情况制定改进措施"
            
            recommendations.append(rec)
        
        return recommendations

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='SOP输出质量检查工具')
    parser.add_argument('domain', choices=['technical', 'content', 'analysis', 'generic'],
                       help='SOP适用领域')
    parser.add_argument('--data-file', help='包含评估数据的JSON文件路径')
    parser.add_argument('--output-format', choices=['json', 'text'], default='json',
                       help='输出格式')
    
    args = parser.parse_args()
    
    # 读取评估数据
    evaluation_data = {}
    if args.data_file:
        try:
            with open(args.data_file, 'r', encoding='utf-8') as f:
                evaluation_data = json.load(f)
        except Exception as e:
            print(f"读取数据文件失败: {e}")
            sys.exit(1)
    else:
        print("警告：未提供评估数据文件，使用默认数据进行演示")
        # 使用默认演示数据
        evaluation_data = {
            'total_lines': 1000,
            'code_standards_violations': 8,
            'test_coverage_percentage': 88,
            'met_performance_requirements': 9,
            'total_performance_requirements': 10,
            'security_vulnerabilities': 1
        }
    
    # 执行质量检查
    checker = QualityChecker()
    result = checker.check_quality(args.domain, evaluation_data)
    
    # 输出结果
    if args.output_format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        self._print_text_report(result)
    
    return 0 if result['passed'] else 1

def _print_text_report(self, result: Dict[str, Any]):
    """打印文本格式报告"""
    print("=" * 60)
    print("SOP输出质量检查报告")
    print("=" * 60)
    print(f"领域: {result['domain']}")
    print(f"总体得分: {result['overall_score']:.1f}/100")
    print(f"质量等级: {result['quality_level'].upper()}")
    print(f"通过状态: {'✅ 通过' if result['passed'] else '❌ 未通过'}")
    print()
    
    print("详细指标评估:")
    print("-" * 60)
    for r in result['detailed_results']:
        status = "✅" if r['passed'] else "❌"
        print(f"{status} {r['metric_name']}: {r['score']:.1f}分 (权重: {r['weight']:.2f})")
        print(f"   反馈: {r['feedback']}")
    
    print()
    print("总体统计:")
    print(f"✓ 总指标数: {result['summary']['total_metrics']}")
    print(f"✓ 通过指标: {result['summary']['passed_metrics']}")
    print(f"⚠ 失败指标: {result['summary']['failed_metrics']}")
    
    if result['summary']['recommendations']:
        print()
        print("改进建议:")
        for i, rec in enumerate(result['summary']['recommendations'], 1):
            print(f"{i}. {rec}")

if __name__ == '__main__':
    sys.exit(main())
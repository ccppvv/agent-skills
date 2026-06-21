# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
SOP模板生成工具
根据领域和任务复杂度自动生成标准SOP模板
"""

import argparse
import json
import yaml
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

class SOPTemplateGenerator:
    """SOP模板生成器"""
    
    def __init__(self):
        self.domain_standards = {
            'technical': {
                'name': '技术开发',
                'quality_metrics': [
                    '代码规范符合度 ≥95%',
                    '单元测试覆盖率 ≥85%',
                    '性能指标达标率 100%',
                    '安全漏洞数 = 0'
                ],
                'input_examples': [
                    '代码仓库链接',
                    '需求文档',
                    'API接口规范',
                    '测试用例'
                ]
            },
            'content': {
                'name': '内容创作',
                'quality_metrics': [
                    '格式规范评分 ≥90分',
                    '核心信息完整度 100%',
                    '可读性评分 ≥85分',
                    '原创性要求 ≥80%'
                ],
                'input_examples': [
                    '主题大纲',
                    '目标受众描述',
                    '风格指南',
                    '参考案例'
                ]
            },
            'analysis': {
                'name': '数据分析',
                'quality_metrics': [
                    '数据准确率 ≥99.5%',
                    '分析深度符合预期',
                    '可视化清晰易懂',
                    '洞察价值评估 ≥8/10'
                ],
                'input_examples': [
                    '原始数据文件',
                    '分析目标描述',
                    '数据字典',
                    '业务背景说明'
                ]
            },
            'generic': {
                'name': '通用流程',
                'quality_metrics': [
                    '步骤完成度 100%',
                    '质量标准符合率 ≥95%',
                    '时间效率达标',
                    '用户满意度 ≥90%'
                ],
                'input_examples': [
                    '任务描述',
                    '资源清单',
                    '时间要求',
                    '质量期望'
                ]
            }
        }
    
    def generate_template(self, domain: str, task_name: str, complexity: str = 'medium') -> Dict[str, Any]:
        """生成SOP模板"""
        
        if domain not in self.domain_standards:
            print(f"警告：未知领域 '{domain}'，使用通用模板")
            domain = 'generic'
        
        domain_info = self.domain_standards[domain]
        
        # 根据复杂度确定步骤数量
        step_config = {
            'low': {'steps': 3, 'checkpoints': 1, 'quality_checks': 2},
            'medium': {'steps': 5, 'checkpoints': 2, 'quality_checks': 3},
            'high': {'steps': 7, 'checkpoints': 3, 'quality_checks': 4}
        }
        config = step_config.get(complexity, step_config['medium'])
        
        # 生成输入定义
        input_definition = {
            'version': '1.0',
            'domain': domain_info['name'],
            'task_name': task_name,
            'created_at': datetime.now().isoformat(),
            
            'input_definition': {
                'required_inputs': self._generate_required_inputs(domain, task_name),
                'optional_inputs': self._generate_optional_inputs(domain),
                'validation_rules': self._generate_validation_rules(domain)
            },
            
            'processing_flow': self._generate_processing_flow(config),
            
            'output_standards': {
                'format_spec': self._generate_output_format(),
                'quality_standards': domain_info['quality_metrics'],
                'verification_methods': self._generate_verification_methods(domain)
            },
            
            'iteration_improvement': {
                'feedback_points': self._generate_feedback_points(),
                'metrics_to_track': self._generate_tracking_metrics(domain),
                'improvement_process': self._generate_improvement_process()
            }
        }
        
        return input_definition
    
    def _generate_required_inputs(self, domain: str, task_name: str) -> List[Dict[str, str]]:
        """生成必填输入定义"""
        base_inputs = [
            {
                'name': '任务目标',
                'description': f'明确{task_name}的完成目标',
                'format': '自然语言描述',
                'validation': '必须包含SMART原则要素'
            },
            {
                'name': '成功标准',
                'description': '定义任务成功的具体标准',
                'format': '可量化的指标列表',
                'validation': '至少包含3个可衡量的标准'
            }
        ]
        
        # 根据领域添加特定输入
        if domain == 'technical':
            base_inputs.extend([
                {
                    'name': '技术栈要求',
                    'description': '使用的技术框架和工具',
                    'format': '技术列表或配置文件',
                    'validation': '必须指定版本要求'
                },
                {
                    'name': '部署环境',
                    'description': '目标运行环境配置',
                    'format': '环境配置详情',
                    'validation': '包含硬件和软件要求'
                }
            ])
        elif domain == 'content':
            base_inputs.extend([
                {
                    'name': '目标受众',
                    'description': '内容的目标读者群体',
                    'format': '受众画像描述',
                    'validation': '包含人口统计和使用场景'
                },
                {
                    'name': '内容大纲',
                    'description': '内容的结构框架',
                    'format': '层级化标题列表',
                    'validation': '逻辑结构清晰'
                }
            ])
        
        return base_inputs
    
    def _generate_optional_inputs(self, domain: str) -> List[Dict[str, str]]:
        """生成可选输入定义"""
        optional_inputs = [
            {
                'name': '参考案例',
                'description': '类似任务的优秀案例',
                'format': '链接或文档',
                'purpose': '提供模式参考和最佳实践'
            },
            {
                'name': '约束条件',
                'description': '任务实施的限制条件',
                'format': '约束列表',
                'purpose': '明确边界和限制'
            }
        ]
        
        if domain == 'technical':
            optional_inputs.append({
                'name': '性能基准',
                'description': '预期的性能指标基准',
                'format': '性能测试结果或标准',
                'purpose': '作为性能优化的参考'
            })
        
        return optional_inputs
    
    def _generate_validation_rules(self, domain: str) -> List[str]:
        """生成验证规则"""
        rules = [
            '必填字段完整性检查',
            '数据格式合规性验证',
            '逻辑一致性检查'
        ]
        
        if domain == 'technical':
            rules.extend([
                '代码语法预检查',
                '依赖兼容性验证',
                '安全配置检查'
            ])
        
        return rules
    
    def _generate_processing_flow(self, config: Dict[str, int]) -> Dict[str, Any]:
        """生成处理流程"""
        steps = []
        
        # 步骤1：输入验证
        steps.append({
            'step_number': 1,
            'name': '输入接收与验证',
            'description': '接收并验证所有输入信息',
            'sub_steps': [
                '检查必填字段完整性',
                '验证数据格式符合要求',
                '识别潜在的输入异常'
            ],
            'output_checkpoint': '输入验证报告',
            'success_criteria': '所有输入通过基本验证'
        })
        
        # 步骤2：预处理
        steps.append({
            'step_number': 2,
            'name': '信息预处理',
            'description': '对输入信息进行初步处理',
            'sub_steps': [
                '结构化整理输入信息',
                '提取核心参数和约束',
                '确定处理优先级'
            ],
            'output_checkpoint': '预处理结果摘要',
            'success_criteria': '信息已结构化，核心要素明确'
        })
        
        # 动态生成后续步骤
        for i in range(config['steps'] - 2):
            step_num = i + 3
            steps.append({
                'step_number': step_num,
                'name': f'核心处理阶段 {i+1}',
                'description': f'执行任务的核心处理逻辑',
                'sub_steps': [
                    f'执行阶段{i+1}的特定操作',
                    f'验证阶段{i+1}的结果质量',
                    f'记录阶段{i+1}的关键决策'
                ],
                'output_checkpoint': f'阶段{i+1}处理报告',
                'success_criteria': f'阶段{i+1}目标达成且质量达标'
            })
        
        return {
            'total_steps': len(steps),
            'steps': steps,
            'checkpoints': config['checkpoints'],
            'decision_points': 2,
            'quality_gates': config['quality_checks']
        }
    
    def _generate_output_format(self) -> Dict[str, Any]:
        """生成输出格式定义"""
        return {
            'required_sections': [
                {
                    'section': '总结',
                    'description': '整体执行结果概述',
                    'content_requirements': [
                        '目标完成情况摘要',
                        '关键成果亮点',
                        '总体质量评估'
                    ],
                    'format': '结构化摘要，包含量化结果'
                },
                {
                    'section': '问题清单',
                    'description': '发现的问题和风险点',
                    'content_requirements': [
                        '问题分类（严重/重要/一般）',
                        '具体问题描述',
                        '影响范围评估',
                        '重现步骤'
                    ],
                    'format': '表格或列表形式，可追溯'
                },
                {
                    'section': '修改建议',
                    'description': '具体的改进建议和优化方向',
                    'content_requirements': [
                        '建议优先级排序',
                        '具体实施步骤',
                        '预期改进效果',
                        '资源需求估算'
                    ],
                    'format': '可执行的行动项列表'
                },
                {
                    'section': '学习要点',
                    'description': '从本次执行中学到的新知识',
                    'content_requirements': [
                        '新发现的最佳实践',
                        '可复用的模式或技巧',
                        '避免的陷阱和错误',
                        '改进流程的建议'
                    ],
                    'format': '知识要点列表，便于复用'
                }
            ],
            'format_standards': {
                'structure': '四部分结构必须完整',
                'clarity': '表达清晰，无歧义',
                'actionability': '建议具体可执行',
                'traceability': '问题可追溯验证'
            }
        }
    
    def _generate_verification_methods(self, domain: str) -> List[Dict[str, str]]:
        """生成验证方法"""
        methods = [
            {
                'method': '标准符合性检查',
                'description': '检查输出是否符合预定标准',
                'automation_level': '高',
                'tools': '自动验证脚本'
            },
            {
                'method': '人工质量评审',
                'description': '专家对输出质量进行评审',
                'automation_level': '低',
                'tools': '质量检查清单'
            }
        ]
        
        if domain == 'technical':
            methods.append({
                'method': '自动化测试',
                'description': '通过测试用例验证功能正确性',
                'automation_level': '高',
                'tools': '单元测试框架'
            })
        
        return methods
    
    def _generate_feedback_points(self) -> List[Dict[str, str]]:
        """生成反馈收集点"""
        return [
            {
                'point': '输入验证阶段',
                'feedback_type': '数据质量反馈',
                'purpose': '改进输入定义和验证规则'
            },
            {
                'point': '处理执行阶段',
                'feedback_type': '流程效率反馈',
                'purpose': '优化处理步骤和决策逻辑'
            },
            {
                'point': '输出验证阶段',
                'feedback_type': '结果质量反馈',
                'purpose': '提升输出标准和验证方法'
            }
        ]
    
    def _generate_tracking_metrics(self, domain: str) -> List[Dict[str, str]]:
        """生成跟踪指标"""
        metrics = [
            {'metric': '执行成功率', 'target': '≥95%', 'frequency': '每次执行'},
            {'metric': '质量标准达标率', 'target': '≥90%', 'frequency': '每次执行'},
            {'metric': '处理时间效率', 'target': '符合预期', 'frequency': '每次执行'}
        ]
        
        if domain == 'technical':
            metrics.append({'metric': '自动化执行率', 'target': '≥80%', 'frequency': '每周'})
        
        return metrics
    
    def _generate_improvement_process(self) -> List[str]:
        """生成改进流程"""
        return [
            '1. 收集执行过程中的问题和反馈',
            '2. 分析根本原因和系统性改进点',
            '3. 更新SOP模板和检查清单',
            '4. 验证改进效果并记录学习',
            '5. 在团队内部分享最佳实践'
        ]

def main():
    parser = argparse.ArgumentParser(description='SOP模板生成工具')
    parser.add_argument('domain', choices=['technical', 'content', 'analysis', 'generic'], 
                       help='SOP适用领域')
    parser.add_argument('task_name', help='任务名称')
    parser.add_argument('--complexity', choices=['low', 'medium', 'high'], default='medium',
                       help='任务复杂度')
    parser.add_argument('--output-format', choices=['json', 'yaml'], default='json',
                       help='输出格式')
    parser.add_argument('--output-file', help='输出文件名（默认为打印到标准输出）')
    
    args = parser.parse_args()
    
    generator = SOPTemplateGenerator()
    template = generator.generate_template(args.domain, args.task_name, args.complexity)
    
    # 输出结果
    output_content = ""
    if args.output_format == 'json':
        output_content = json.dumps(template, ensure_ascii=False, indent=2)
    else:
        output_content = yaml.dump(template, allow_unicode=True, sort_keys=False)
    
    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"✅ SOP模板已生成并保存到: {args.output_file}")
        print(f"领域: {args.domain}, 任务: {args.task_name}, 复杂度: {args.complexity}")
    else:
        print(output_content)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
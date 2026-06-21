#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workflow Orchestrator - Main coordinator for workflow creation process

This script orchestrates the entire workflow creation pipeline:
1. Natural language parsing
2. Pattern detection
3. Dependency graph construction
4. Parallelization analysis
5. Intelligent decision making
6. Command/agent generation
"""

import json
from typing import Dict, List, Any, Tuple
from pathlib import Path


class WorkflowOrchestrator:
    """
    Main orchestrator that coordinates all workflow creation modules

    This is primarily a reference implementation showing the coordination
    logic. In actual use, Claude will follow the reference documents in
    core/ to perform these analysis steps.
    """

    def __init__(self):
        self.workflow_data = {}
        self.analysis_results = {}

    def create_workflow(self, natural_language_input: str,
                       output_name: str = None) -> Dict[str, Any]:
        """
        Complete workflow creation pipeline

        Args:
            natural_language_input: User's natural language workflow description
            output_name: Optional name for the generated command

        Returns:
            Dictionary containing all generated artifacts and metadata
        """
        print("🚀 Starting workflow creation pipeline...\n")

        # Phase 1: Parse natural language input
        print("📝 Phase 1: Parsing natural language input...")
        parsed_data = self._parse_input(natural_language_input)
        self.workflow_data['parsed'] = parsed_data
        print(f"   ✓ Identified {len(parsed_data.get('tasks', []))} tasks")

        # Phase 2: Detect graph patterns
        print("\n🔍 Phase 2: Detecting workflow patterns...")
        detected_patterns = self._detect_patterns(parsed_data)
        self.workflow_data['patterns'] = detected_patterns
        pattern_names = [p['pattern'] for p in detected_patterns]
        print(f"   ✓ Detected patterns: {', '.join(pattern_names)}")

        # Phase 3: Build dependency graph
        print("\n🏗️  Phase 3: Building dependency graph...")
        dependency_graph = self._build_dependencies(parsed_data)
        self.workflow_data['graph'] = dependency_graph
        print(f"   ✓ Created graph with {len(dependency_graph.get('nodes', []))} nodes")

        # Phase 4: Analyze parallelization opportunities
        print("\n⚡ Phase 4: Analyzing parallelization opportunities...")
        parallel_analysis = self._analyze_parallelization(dependency_graph)
        self.workflow_data['parallelization'] = parallel_analysis
        opportunities = len(parallel_analysis.get('opportunities', []))
        print(f"   ✓ Found {opportunities} parallelization opportunities")

        # Phase 5: Make intelligent decisions
        print("\n🧠 Phase 5: Intelligent decision making...")
        decisions = self._make_decisions(
            parsed_data,
            detected_patterns,
            dependency_graph,
            parallel_analysis
        )
        self.workflow_data['decisions'] = decisions
        print(f"   ✓ Category: {decisions['category']}")
        print(f"   ✓ Complexity: {decisions['complexity']}")
        print(f"   ✓ MCP Servers: {', '.join(decisions.get('mcp_servers', []))}")
        print(f"   ✓ Personas: {', '.join(decisions.get('personas', []))}")

        # Phase 6: Generate workflow description text
        print("\n📊 Phase 6: Generating workflow description...")
        workflow_graph_text = self._generate_workflow_text(dependency_graph, detected_patterns)
        self.workflow_data['workflow_graph_text'] = workflow_graph_text

        # Phase 7: Generate command
        print("\n⚙️  Phase 7: Generating command file...")
        command_spec = self._build_command_spec(output_name or 'custom-workflow')
        command_path = self._generate_command(command_spec)
        print(f"   ✓ Command generated: {command_path}")

        # Phase 8: Optionally generate custom agent
        print("\n🤖 Phase 8: Evaluating agent creation...")
        if self._should_create_agent(decisions):
            agent_spec = self._build_agent_spec(output_name or 'custom-workflow')
            agent_path = self._generate_agent(agent_spec)
            print(f"   ✓ Agent generated: {agent_path}")
        else:
            agent_path = None
            print("   ⏭️  Agent creation not needed")

        # Final summary
        print("\n" + "="*60)
        print("✅ Workflow creation completed successfully!")
        print("="*60)

        return {
            'workflow_data': self.workflow_data,
            'command_path': command_path,
            'agent_path': agent_path,
            'summary': self._generate_summary()
        }

    def _parse_input(self, text: str) -> Dict[str, Any]:
        """
        Phase 1: Parse natural language input

        In actual use, Claude follows core/analyzer.md to perform this analysis
        """
        # This is a reference implementation
        # In practice, Claude reads core/analyzer.md and applies those patterns

        return {
            'tasks': [],
            'dependencies': [],
            'execution_hints': [],
            'conditions': []
        }

    def _detect_patterns(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Phase 2: Detect graph patterns

        In actual use, Claude follows core/graph-detector.md
        """
        # Reference implementation
        # Claude reads core/graph-detector.md for actual pattern detection

        return []

    def _build_dependencies(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 3: Build dependency graph (DAG)

        In actual use, Claude follows core/dependency-builder.md
        """
        # Reference implementation
        # Claude reads core/dependency-builder.md for actual graph construction

        return {
            'nodes': [],
            'edges': [],
            'execution_levels': []
        }

    def _analyze_parallelization(self, graph: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 4: Analyze parallelization opportunities

        In actual use, Claude follows core/parallel-optimizer.md
        """
        # Reference implementation
        # Claude reads core/parallel-optimizer.md for actual analysis

        return {
            'opportunities': [],
            'speedup_estimate': 1.0,
            'execution_plan': {}
        }

    def _make_decisions(self, parsed_data: Dict[str, Any],
                       patterns: List[Dict[str, Any]],
                       graph: Dict[str, Any],
                       parallel_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 5: Make intelligent decisions about metadata

        In actual use, Claude follows core/decision-engine.md
        """
        # Reference implementation
        # Claude reads core/decision-engine.md for actual decision making

        return {
            'category': 'workflow',
            'complexity': 'standard',
            'mcp_servers': [],
            'personas': [],
            'confidence': {}
        }

    def _generate_workflow_text(self, graph: Dict[str, Any],
                                patterns: List[Dict[str, Any]]) -> str:
        """
        Generate text description of workflow graph

        Uses symbols: →, ⎡⎢⎣, ├─└─, ⚡, ↻, 📦
        """
        # Reference implementation
        # In practice, Claude uses dependency graph to generate this

        return "→ Workflow graph text representation"

    def _build_command_spec(self, name: str) -> Dict[str, Any]:
        """Build complete command specification"""
        decisions = self.workflow_data.get('decisions', {})

        return {
            'name': name,
            'title': name.replace('-', ' ').title(),
            'description': self._build_description(),
            'category': decisions.get('category', 'workflow'),
            'complexity': decisions.get('complexity', 'standard'),
            'mcp_servers': decisions.get('mcp_servers', []),
            'personas': decisions.get('personas', []),
            'detected_patterns': self.workflow_data.get('patterns', []),
            'workflow_graph_text': self.workflow_data.get('workflow_graph_text', ''),
            'workflow_steps': self._extract_steps(),
            'mcp_rationale': decisions.get('mcp_rationale', {}),
            'examples': []
        }

    def _build_description(self) -> str:
        """Build workflow description for command frontmatter"""
        patterns = self.workflow_data.get('patterns', [])
        graph_text = self.workflow_data.get('workflow_graph_text', '')

        desc = "Custom workflow"
        if patterns:
            pattern_str = ', '.join([p['pattern'] for p in patterns])
            desc += f" with {pattern_str} patterns"

        if graph_text:
            desc += f". Graph: {graph_text[:100]}..."

        return desc

    def _extract_steps(self) -> List[Dict[str, Any]]:
        """Extract workflow steps from graph"""
        graph = self.workflow_data.get('graph', {})
        nodes = graph.get('nodes', [])

        steps = []
        for node in nodes:
            steps.append({
                'name': node.get('name', 'Unknown'),
                'description': node.get('description', ''),
                'type': node.get('type', 'sequential')
            })

        return steps

    def _generate_command(self, command_spec: Dict[str, Any]) -> Path:
        """Generate actual command file"""
        # In practice, this calls command-generator.py
        # For this reference, we just return a placeholder path
        return Path(f"~/.claude/commands/workflows/{command_spec['name']}.md")

    def _should_create_agent(self, decisions: Dict[str, Any]) -> bool:
        """Determine if custom agent should be created"""
        complexity = decisions.get('complexity', 'standard')
        return complexity in ['complex', 'high']

    def _build_agent_spec(self, name: str) -> Dict[str, Any]:
        """Build agent specification"""
        decisions = self.workflow_data.get('decisions', {})

        return {
            'name': f"{name}-specialist",
            'description': f"Specialized agent for {name} workflow execution",
            'category': 'workflow-specialist',
            'triggers': [],
            'focus_areas': [],
            'key_actions': [],
            'outputs': [],
            'will_do': [],
            'wont_do': []
        }

    def _generate_agent(self, agent_spec: Dict[str, Any]) -> Path:
        """Generate actual agent file"""
        # In practice, this calls agent-generator.py
        return Path(f"~/.claude/agents/workflows/{agent_spec['name']}.md")

    def _generate_summary(self) -> str:
        """Generate execution summary"""
        decisions = self.workflow_data.get('decisions', {})
        patterns = self.workflow_data.get('patterns', [])

        summary = "Workflow Creation Summary\n"
        summary += "=" * 50 + "\n"
        summary += f"Category: {decisions.get('category', 'N/A')}\n"
        summary += f"Complexity: {decisions.get('complexity', 'N/A')}\n"
        summary += f"Patterns: {', '.join([p['pattern'] for p in patterns])}\n"
        summary += f"MCP Servers: {', '.join(decisions.get('mcp_servers', []))}\n"
        summary += f"Personas: {', '.join(decisions.get('personas', []))}\n"

        return summary


def main():
    """Test the orchestrator"""
    orchestrator = WorkflowOrchestrator()

    # Example natural language input
    example_input = """
    Check the system configuration, then run frontend and backend tests in parallel.
    If both tests pass, deploy to staging and verify health.
    If health check passes, deploy to production, otherwise rollback.
    """

    result = orchestrator.create_workflow(
        natural_language_input=example_input,
        output_name='deploy-with-verification'
    )

    print("\n" + result['summary'])


if __name__ == '__main__':
    main()

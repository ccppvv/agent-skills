#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graph Validator for Workflow Creator

Validates workflow graphs against WGDL (Workflow Graph Description Language) specification.

Validation Rules (from docs/graph-description-language.md):
1. Node ID Uniqueness - Each [node_X] must be unique
2. Dependency Reference Validity - All dependencies must reference existing nodes
3. Parallel Group Completeness - Parallel groups must have ⎡, ⎢*, ⎣ markers
4. Branch Pair Completeness - Branches should have both ├─ and └─ paths
5. Indentation Consistency - Consistent indentation within levels
6. No Circular Dependencies - Must form a DAG (Directed Acyclic Graph)
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


class GraphValidationError(Exception):
    """Custom exception for graph validation errors"""
    pass


# WGDL symbol patterns
SYMBOLS = {
    'sequential': '→',
    'parallel_start': '⎡→',
    'parallel_middle': '⎢→',
    'parallel_end': '⎣→',
    'branch_true': '├─',
    'branch_false': '└─',
    'async': '⚡',
    'loop': '↻',
    'shared': '📦'
}

# Node pattern: symbol + name + [id] + optional dependencies
NODE_PATTERN = re.compile(
    r'([→⎡⎢⎣⚡↻📦├└│\s]+)'  # symbols and indentation
    r'([A-Z][a-zA-Z0-9_]*)'   # node name (PascalCase)
    r'\s+\[([a-z_0-9]+)\]'    # node ID
    r'(?:\s*\(depends on: ([^)]+)\))?'  # optional dependencies
)


class WorkflowGraph:
    """Represents a parsed workflow graph"""

    def __init__(self):
        self.nodes: Dict[str, Dict] = {}  # node_id -> node_info
        self.edges: List[Tuple[str, str]] = []  # (from_id, to_id)
        self.parallel_groups: List[List[str]] = []  # groups of node_ids

    def add_node(self, node_id: str, name: str, symbol: str, dependencies: List[str] = None):
        """Add a node to the graph"""
        if node_id in self.nodes:
            raise GraphValidationError(f"Duplicate node ID: {node_id}")

        self.nodes[node_id] = {
            'name': name,
            'symbol': symbol,
            'dependencies': dependencies or []
        }

        # Add edges for dependencies
        if dependencies:
            for dep_id in dependencies:
                self.edges.append((dep_id, node_id))

    def validate_dependencies(self) -> List[str]:
        """
        Validate that all dependency references exist

        Returns: List of error messages
        """
        errors = []
        for node_id, node_info in self.nodes.items():
            for dep_id in node_info['dependencies']:
                if dep_id not in self.nodes:
                    errors.append(
                        f"Node '{node_id}' references non-existent dependency '{dep_id}'"
                    )
        return errors

    def detect_cycles(self) -> Optional[List[str]]:
        """
        Detect circular dependencies using DFS

        Returns: Cycle path if found, None otherwise
        """
        visited = set()
        rec_stack = set()
        parent = {}

        def dfs(node_id: str, path: List[str]) -> Optional[List[str]]:
            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)

            # Get neighbors (nodes that depend on current node)
            neighbors = [to_id for from_id, to_id in self.edges if from_id == node_id]

            for neighbor in neighbors:
                if neighbor not in visited:
                    parent[neighbor] = node_id
                    cycle = dfs(neighbor, path.copy())
                    if cycle:
                        return cycle
                elif neighbor in rec_stack:
                    # Cycle detected - reconstruct path
                    cycle_start_idx = path.index(neighbor)
                    return path[cycle_start_idx:] + [neighbor]

            rec_stack.remove(node_id)
            return None

        for node_id in self.nodes:
            if node_id not in visited:
                cycle = dfs(node_id, [])
                if cycle:
                    return cycle

        return None


def extract_graph_section(content: str) -> Optional[str]:
    """
    Extract Workflow Graph section from markdown content

    Returns: Graph text content or None
    """
    graph_pattern = re.compile(
        r'## Workflow Graph\s*\n+```\s*\n(.*?)\n```',
        re.DOTALL
    )
    match = graph_pattern.search(content)

    if not match:
        return None

    return match.group(1)


def parse_graph(graph_text: str) -> WorkflowGraph:
    """
    Parse WGDL text into WorkflowGraph structure

    Raises: GraphValidationError on parse errors
    """
    graph = WorkflowGraph()
    lines = graph_text.strip().split('\n')

    current_parallel_group = []
    in_parallel = False

    for line_num, line in enumerate(lines, 1):
        # Skip empty lines and pure indent/connector lines
        if not line.strip() or line.strip() in ['↓', '│']:
            continue

        # Check for parallel group markers
        if '⎡→' in line:
            in_parallel = True
            current_parallel_group = []
        elif '⎣→' in line:
            in_parallel = False
            if current_parallel_group:
                graph.parallel_groups.append(current_parallel_group)
                current_parallel_group = []

        # Try to parse as node
        match = NODE_PATTERN.search(line)
        if match:
            symbol_part, name, node_id, deps_str = match.groups()

            # Parse dependencies
            dependencies = []
            if deps_str:
                dependencies = [dep.strip() for dep in deps_str.split(',')]

            try:
                graph.add_node(node_id, name, symbol_part.strip(), dependencies)

                if in_parallel:
                    current_parallel_group.append(node_id)

            except GraphValidationError as e:
                raise GraphValidationError(f"Line {line_num}: {e}")

    return graph


def validate_parallel_groups(graph: WorkflowGraph, graph_text: str) -> List[str]:
    """
    Validate parallel group completeness

    Rules:
    - Must have ⎡ (start), ⎢* (middle), ⎣ (end)
    - At least 2 tasks in parallel group
    """
    errors = []

    # Check for unmatched parallel markers
    start_count = graph_text.count('⎡→')
    middle_count = graph_text.count('⎢→')
    end_count = graph_text.count('⎣→')

    if start_count != end_count:
        errors.append(
            f"Unmatched parallel group markers: {start_count} starts (⎡) vs {end_count} ends (⎣)"
        )

    # Check each parallel group
    for i, group in enumerate(graph.parallel_groups, 1):
        if len(group) < 2:
            errors.append(
                f"Parallel group {i} has only {len(group)} task(s). Minimum: 2 for parallelism"
            )

    return errors


def validate_branch_completeness(graph_text: str) -> List[str]:
    """
    Validate branch pair completeness

    Rules:
    - Should have both ├─ (true) and └─ (false) paths
    - Or single path with clear labeling
    """
    errors = []
    warnings = []

    lines = graph_text.split('\n')

    branch_true_lines = [i for i, line in enumerate(lines) if '├─' in line]

    for true_line_idx in branch_true_lines:
        # Check if next few lines contain └─
        found_false = False
        for i in range(true_line_idx + 1, min(true_line_idx + 10, len(lines))):
            if '└─' in lines[i]:
                found_false = True
                break
            # Stop if we hit a new top-level node
            if i > true_line_idx + 1 and lines[i].startswith('→') and '[' in lines[i]:
                break

        if not found_false:
            # Check if the true path has a clear single-path label
            true_line = lines[true_line_idx]
            if '[OnlyIf' in true_line or '[If' in true_line:
                warnings.append(
                    f"Line {true_line_idx + 1}: Single-path branch (├─) without false path (└─). "
                    f"Acceptable with clear label."
                )
            else:
                errors.append(
                    f"Line {true_line_idx + 1}: Branch with ├─ but no └─ false path found. "
                    f"Add └─ path or use clear single-path label."
                )

    if warnings:
        for warning in warnings:
            print(f"  ⚠️  Warning: {warning}")

    return errors


def validate_indentation(graph_text: str) -> List[str]:
    """
    Validate indentation consistency

    Rules:
    - Consistent indentation within each level
    - Proper nesting for branches
    """
    errors = []
    lines = graph_text.split('\n')

    # Track indentation levels
    indent_pattern = re.compile(r'^([ →⎡⎢⎣├└│]+)')

    prev_indent_len = 0
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue

        match = indent_pattern.match(line)
        if match:
            indent = match.group(1)
            indent_len = len(indent)

            # Check for sudden indent jumps (more than 2 spaces or 1 symbol)
            if indent_len > prev_indent_len + 4:  # Allow for 2 spaces or symbols
                errors.append(
                    f"Line {i}: Inconsistent indentation jump "
                    f"(from {prev_indent_len} to {indent_len} chars)"
                )

            prev_indent_len = indent_len

    return errors


def validate_node_naming(graph: WorkflowGraph) -> List[str]:
    """
    Validate node naming conventions

    Rules:
    - PascalCase format
    - Descriptive names
    """
    errors = []

    for node_id, node_info in graph.nodes.items():
        name = node_info['name']

        # Check PascalCase
        if not re.match(r'^[A-Z][a-zA-Z0-9_]*$', name):
            errors.append(
                f"Node '{node_id}': Name '{name}' not in PascalCase format"
            )

        # Check length
        if len(name) < 3:
            errors.append(
                f"Node '{node_id}': Name '{name}' too short (< 3 chars)"
            )
        elif len(name) > 30:
            errors.append(
                f"Node '{node_id}': Name '{name}' too long (> 30 chars)"
            )

    return errors


def validate_graph(graph_text: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate complete workflow graph

    Returns: (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    try:
        # Parse graph
        graph = parse_graph(graph_text)

        if not graph.nodes:
            errors.append("No valid nodes found in graph")
            return False, errors, warnings

        # Rule 1: Node ID Uniqueness (checked during parsing)
        # Already enforced by add_node()

        # Rule 2: Dependency Reference Validity
        dep_errors = graph.validate_dependencies()
        errors.extend(dep_errors)

        # Rule 3: Parallel Group Completeness
        parallel_errors = validate_parallel_groups(graph, graph_text)
        errors.extend(parallel_errors)

        # Rule 4: Branch Pair Completeness
        branch_errors = validate_branch_completeness(graph_text)
        errors.extend(branch_errors)

        # Rule 5: Indentation Consistency
        indent_errors = validate_indentation(graph_text)
        errors.extend(indent_errors)

        # Rule 6: No Circular Dependencies
        cycle = graph.detect_cycles()
        if cycle:
            cycle_path = ' → '.join(cycle)
            errors.append(f"Circular dependency detected: {cycle_path}")

        # Additional: Node Naming Conventions
        naming_errors = validate_node_naming(graph)
        errors.extend(naming_errors)

        # Summary
        if not errors:
            print(f"  ✅ Graph validation passed ({len(graph.nodes)} nodes, {len(graph.edges)} edges)")

        return len(errors) == 0, errors, warnings

    except GraphValidationError as e:
        errors.append(str(e))
        return False, errors, warnings
    except Exception as e:
        errors.append(f"Unexpected error during graph validation: {e}")
        return False, errors, warnings


def main():
    """Main validation entry point"""
    if len(sys.argv) < 2:
        print("Usage: python graph-validator.py <command-file.md>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    print(f"🔍 Validating workflow graph in: {file_path.name}")
    print()

    # Read file and extract graph section
    content = file_path.read_text(encoding='utf-8')
    graph_text = extract_graph_section(content)

    if not graph_text:
        print("❌ Error: No 'Workflow Graph' section found in file")
        print()
        print("Expected format:")
        print("## Workflow Graph")
        print("```")
        print("→ NodeName [node_1]")
        print("...")
        print("```")
        sys.exit(1)

    # Validate graph
    is_valid, errors, warnings = validate_graph(graph_text)

    print()

    if is_valid:
        print("✅ Graph validation passed!")
        print()
        print(f"Workflow graph in '{file_path.stem}' is WGDL-compliant.")
        sys.exit(0)
    else:
        print("❌ Graph validation failed!")
        print()
        print(f"Found {len(errors)} error(s):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print()
        print("Please fix these errors to ensure WGDL compliance.")
        print("See: docs/graph-description-language.md for specification.")
        sys.exit(1)


if __name__ == '__main__':
    main()

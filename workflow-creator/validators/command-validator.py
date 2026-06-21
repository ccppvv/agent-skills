#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command Validator for Workflow Creator

Validates generated workflow command files for:
- YAML frontmatter syntax correctness
- Required metadata fields presence and validity
- MCP server availability (if specified)
- Persona validity
- Command naming conventions
"""

import re
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Valid categories
VALID_CATEGORIES = {
    'workflow', 'automation', 'analysis', 'generation',
    'deployment', 'testing', 'maintenance', 'orchestration'
}

# Valid complexity levels
VALID_COMPLEXITY = {'simple', 'standard', 'complex', 'high'}

# Available MCP servers (update as new MCPs are added)
AVAILABLE_MCP_SERVERS = {
    'sequential', 'magic', 'context7', 'playwright', 'serena'
}

# Available personas (from Task tool descriptions)
AVAILABLE_PERSONAS = {
    'general-purpose',
    # Architecture
    'system-architect', 'backend-architect', 'frontend-architect',
    # Development
    'backend-developer', 'frontend-developer',
    # Quality & Security
    'qa-specialist', 'security-engineer', 'performance-engineer',
    # Specialized
    'devops-architect', 'data-engineer', 'ml-engineer'
}

# Command name pattern: lowercase-with-hyphens
COMMAND_NAME_PATTERN = re.compile(r'^[a-z][a-z0-9-]{2,29}$')


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def extract_frontmatter(content: str) -> Tuple[Optional[str], str]:
    """
    Extract YAML frontmatter from markdown content

    Returns: (frontmatter_yaml, body_content)
    """
    frontmatter_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)$', re.DOTALL)
    match = frontmatter_pattern.match(content)

    if not match:
        return None, content

    return match.group(1), match.group(2)


def validate_yaml_syntax(yaml_str: str) -> Dict:
    """
    Validate YAML syntax and parse into dict

    Raises: ValidationError if YAML is invalid
    """
    try:
        metadata = yaml.safe_load(yaml_str)
        if not isinstance(metadata, dict):
            raise ValidationError("YAML frontmatter must be a dictionary")
        return metadata
    except yaml.YAMLError as e:
        raise ValidationError(f"YAML syntax error: {e}")


def validate_required_fields(metadata: Dict) -> None:
    """
    Validate that all required metadata fields are present

    Required fields: name, description, category, complexity
    """
    required_fields = ['name', 'description', 'category', 'complexity']
    missing_fields = [field for field in required_fields if field not in metadata]

    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")


def validate_name(name: str) -> None:
    """
    Validate command name format

    Rules:
    - lowercase-with-hyphens
    - 3-30 characters
    - starts with letter
    - only letters, numbers, hyphens
    """
    if not isinstance(name, str):
        raise ValidationError(f"Name must be a string, got {type(name).__name__}")

    if not COMMAND_NAME_PATTERN.match(name):
        raise ValidationError(
            f"Invalid name '{name}'. Must be lowercase-with-hyphens, "
            f"3-30 characters, start with letter"
        )


def validate_description(description: str) -> None:
    """
    Validate description field

    Rules:
    - Must be string
    - 50-200 characters (recommended)
    - Should include workflow context
    """
    if not isinstance(description, str):
        raise ValidationError(f"Description must be a string, got {type(description).__name__}")

    length = len(description)
    if length < 50:
        print(f"  ⚠️  Warning: Description is short ({length} chars). Recommended: 50-200 chars")
    elif length > 200:
        print(f"  ⚠️  Warning: Description is long ({length} chars). Recommended: 50-200 chars")


def validate_category(category: str) -> None:
    """
    Validate category field

    Must be one of: workflow, automation, analysis, generation,
                    deployment, testing, maintenance, orchestration
    """
    if not isinstance(category, str):
        raise ValidationError(f"Category must be a string, got {type(category).__name__}")

    if category not in VALID_CATEGORIES:
        raise ValidationError(
            f"Invalid category '{category}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
        )


def validate_complexity(complexity: str) -> None:
    """
    Validate complexity field

    Must be one of: simple, standard, complex, high
    """
    if not isinstance(complexity, str):
        raise ValidationError(f"Complexity must be a string, got {type(complexity).__name__}")

    if complexity not in VALID_COMPLEXITY:
        raise ValidationError(
            f"Invalid complexity '{complexity}'. Must be one of: {', '.join(sorted(VALID_COMPLEXITY))}"
        )


def validate_mcp_servers(mcp_servers: List[str]) -> None:
    """
    Validate MCP servers list

    Rules:
    - Must be list (can be empty)
    - All servers must be available
    """
    if not isinstance(mcp_servers, list):
        raise ValidationError(f"mcp-servers must be a list, got {type(mcp_servers).__name__}")

    unavailable_servers = [server for server in mcp_servers if server not in AVAILABLE_MCP_SERVERS]

    if unavailable_servers:
        raise ValidationError(
            f"Unavailable MCP servers: {', '.join(unavailable_servers)}. "
            f"Available: {', '.join(sorted(AVAILABLE_MCP_SERVERS))}"
        )


def validate_personas(personas: List[str]) -> None:
    """
    Validate personas list

    Rules:
    - Must be list (can be empty for simple workflows)
    - 1-7 personas recommended
    - All personas must be valid
    """
    if not isinstance(personas, list):
        raise ValidationError(f"personas must be a list, got {type(personas).__name__}")

    if len(personas) > 7:
        print(f"  ⚠️  Warning: {len(personas)} personas specified. Recommended maximum: 7")

    invalid_personas = [persona for persona in personas if persona not in AVAILABLE_PERSONAS]

    if invalid_personas:
        raise ValidationError(
            f"Invalid personas: {', '.join(invalid_personas)}. "
            f"Available: {', '.join(sorted(AVAILABLE_PERSONAS))}"
        )


def validate_body_structure(body: str, metadata: Dict) -> None:
    """
    Validate command body structure

    Expected sections:
    - Title (# /command-name)
    - Workflow Description
    - Detected Patterns
    - Workflow Graph
    - Behavioral Flow
    - Usage Examples
    - Boundaries
    """
    required_sections = [
        f"# /{metadata['name']}",
        "Workflow Description",
        "Detected Patterns",
        "Workflow Graph",
        "Behavioral Flow",
        "Usage Examples",
        "Boundaries"
    ]

    missing_sections = []
    for section in required_sections:
        if section not in body:
            missing_sections.append(section)

    if missing_sections:
        raise ValidationError(f"Missing body sections: {', '.join(missing_sections)}")


def validate_command_file(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a single command file

    Returns: (is_valid, error_messages)
    """
    errors = []

    try:
        # Read file
        content = file_path.read_text(encoding='utf-8')

        # Extract frontmatter
        frontmatter, body = extract_frontmatter(content)
        if frontmatter is None:
            raise ValidationError("No YAML frontmatter found (must start with ---)")

        # Validate YAML syntax
        metadata = validate_yaml_syntax(frontmatter)

        # Validate required fields
        validate_required_fields(metadata)

        # Validate individual fields
        validate_name(metadata['name'])
        validate_description(metadata['description'])
        validate_category(metadata['category'])
        validate_complexity(metadata['complexity'])

        # Validate optional fields
        if 'mcp-servers' in metadata:
            validate_mcp_servers(metadata['mcp-servers'])

        if 'personas' in metadata:
            validate_personas(metadata['personas'])

        # Validate body structure
        validate_body_structure(body, metadata)

        return True, []

    except ValidationError as e:
        errors.append(str(e))
        return False, errors
    except Exception as e:
        errors.append(f"Unexpected error: {e}")
        return False, errors


def main():
    """Main validation entry point"""
    if len(sys.argv) < 2:
        print("Usage: python command-validator.py <command-file.md>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    print(f"🔍 Validating command file: {file_path.name}")
    print()

    is_valid, errors = validate_command_file(file_path)

    if is_valid:
        print("✅ Validation passed!")
        print()
        print(f"Command '{file_path.stem}' is valid and ready to use.")
        sys.exit(0)
    else:
        print("❌ Validation failed!")
        print()
        print("Errors found:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print()
        print("Please fix these errors before using the command.")
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Integration tests for the prompt-improver system (command mode)
Tests plugin configuration, skill files, and command structure
"""
import json
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PLUGIN_JSON = PROJECT_ROOT / ".claude-plugin" / "plugin.json"
SKILL_DIR = PROJECT_ROOT / "skills" / "prompt-improver"
COMMANDS_DIR = PROJECT_ROOT / "commands"

def test_plugin_configuration():
    """Test that plugin.json is properly configured"""
    assert PLUGIN_JSON.exists(), "plugin.json not found"

    config = json.loads(PLUGIN_JSON.read_text())

    assert config["version"] == "1.0.0", f"Expected version 1.0.0, got {config['version']}"

    # Check skills field exists
    assert "skills" in config, "Missing 'skills' field in plugin.json"
    assert isinstance(config["skills"], list), "'skills' should be a list"
    assert len(config["skills"]) > 0, "'skills' list is empty"

    # Check commands field exists
    assert "commands" in config, "Missing 'commands' field in plugin.json"

    # Check hooks field is NOT present (command mode only)
    assert "hooks" not in config, "The 'hooks' field should not be present (command mode only)"

    # Check skill path
    skill_path = config["skills"][0]
    assert skill_path == "./skills/prompt-improver", f"Unexpected skill path: {skill_path}"

    # Verify skill directory exists
    resolved_skill_path = PROJECT_ROOT / skill_path.lstrip("./")
    assert resolved_skill_path.exists(), f"Skill directory not found: {resolved_skill_path}"

    print("✓ Plugin configuration is correct")

def test_no_hook_files():
    """Test that hook-related files have been removed"""
    assert not (PROJECT_ROOT / "hooks" / "hooks.json").exists(), "hooks/hooks.json should be removed"
    assert not (PROJECT_ROOT / "scripts" / "improve-prompt.py").exists(), "scripts/improve-prompt.py should be removed"
    assert not (PROJECT_ROOT / "tests" / "test_hook.py").exists(), "tests/test_hook.py should be removed"

    print("✓ Hook files properly removed")

def test_command_file():
    """Test that the improve-prompt command exists and is valid"""
    command_file = COMMANDS_DIR / "improve-prompt.md"
    assert command_file.exists(), "commands/improve-prompt.md missing"

    content = command_file.read_text()
    assert content.startswith("---\n"), "Command missing YAML frontmatter"
    assert "name: improve-prompt" in content, "Command name incorrect"
    assert "$ARGUMENTS" in content, "Command should reference $ARGUMENTS"
    assert "prompt-improver" in content, "Command should reference prompt-improver skill"

    print("✓ Command file present and valid")

def test_skill_file_integrity():
    """Test that all skill files are present and valid"""
    skill_md = SKILL_DIR / "SKILL.md"
    assert skill_md.exists(), "SKILL.md missing"

    content = skill_md.read_text()
    assert content.startswith("---\n"), "SKILL.md missing YAML frontmatter"
    assert "name: prompt-improver" in content, "Skill name incorrect"

    # Should not reference hook mode
    assert "UserPromptSubmit hook evaluates" not in content, "SKILL.md should not reference hook evaluation"

    # Check reference files
    references_dir = SKILL_DIR / "references"
    assert references_dir.exists(), "references directory missing"

    expected_refs = [
        "question-patterns.md",
        "research-strategies.md",
        "examples.md",
    ]

    for ref in expected_refs:
        ref_file = references_dir / ref
        assert ref_file.exists(), f"Missing reference file: {ref}"

    print("✓ All skill files present and valid")

def test_architecture_separation():
    """Test command-only architecture"""
    # No hook scripts should exist
    scripts_dir = PROJECT_ROOT / "scripts"
    hooks_dir = PROJECT_ROOT / "hooks"
    assert not scripts_dir.exists() or not any(scripts_dir.iterdir()), "scripts/ should be empty or absent"
    assert not hooks_dir.exists() or not any(hooks_dir.iterdir()), "hooks/ should be empty or absent"

    # Command should exist
    assert (COMMANDS_DIR / "improve-prompt.md").exists(), "Command file missing"

    # SKILL.md should contain research and question logic
    skill_content = (SKILL_DIR / "SKILL.md").read_text()
    assert "Phase 1" in skill_content or "phase 1" in skill_content.lower()
    assert "Phase 2" in skill_content or "phase 2" in skill_content.lower()
    assert "Research" in skill_content

    print("✓ Architecture is command-only (no hooks)")

def run_all_tests():
    """Run all integration tests"""
    tests = [
        test_plugin_configuration,
        test_no_hook_files,
        test_command_file,
        test_skill_file_integrity,
        test_architecture_separation,
    ]

    print(f"Running {len(tests)} integration tests...\n")

    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed.append((test.__name__, e))
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed.append((test.__name__, e))

    print(f"\n{'='*60}")
    if failed:
        print(f"FAILED: {len(failed)}/{len(tests)} tests failed")
        for name, error in failed:
            print(f"  - {name}: {error}")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(tests)} integration tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    run_all_tests()

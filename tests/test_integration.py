#!/usr/bin/env python3
"""
Integration tests for the prompt-improver system (skill-only mode)
Tests plugin configuration and skill files
"""
import json
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PLUGIN_JSON = PROJECT_ROOT / ".claude-plugin" / "plugin.json"
SKILL_DIR = PROJECT_ROOT / "skills" / "prompt-improver"

def test_plugin_configuration():
    """Test that plugin.json is properly configured"""
    assert PLUGIN_JSON.exists(), "plugin.json not found"

    config = json.loads(PLUGIN_JSON.read_text())

    assert config["version"] == "1.0.0", f"Expected version 1.0.0, got {config['version']}"

    # Check skills field exists
    assert "skills" in config, "Missing 'skills' field in plugin.json"
    assert isinstance(config["skills"], list), "'skills' should be a list"
    assert len(config["skills"]) > 0, "'skills' list is empty"

    # Check hooks and commands fields are NOT present (skill-only mode)
    assert "hooks" not in config, "The 'hooks' field should not be present"
    assert "commands" not in config, "The 'commands' field should not be present (skill-only mode)"

    # Check skill path
    skill_path = config["skills"][0]
    assert skill_path == "./skills/prompt-improver", f"Unexpected skill path: {skill_path}"

    # Verify skill directory exists
    resolved_skill_path = PROJECT_ROOT / skill_path.lstrip("./")
    assert resolved_skill_path.exists(), f"Skill directory not found: {resolved_skill_path}"

    print("✓ Plugin configuration is correct")

def test_no_hook_or_command_files():
    """Test that hook and command files have been removed"""
    assert not (PROJECT_ROOT / "hooks" / "hooks.json").exists(), "hooks/hooks.json should be removed"
    assert not (PROJECT_ROOT / "scripts" / "improve-prompt.py").exists(), "scripts/improve-prompt.py should be removed"
    assert not (PROJECT_ROOT / "tests" / "test_hook.py").exists(), "tests/test_hook.py should be removed"
    assert not (PROJECT_ROOT / "commands").exists(), "commands/ directory should be removed"

    print("✓ Hook and command files properly removed")

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

def test_skill_only_architecture():
    """Test skill-only architecture"""
    # No hook or command dirs should exist
    assert not (PROJECT_ROOT / "scripts").exists(), "scripts/ should not exist"
    assert not (PROJECT_ROOT / "hooks").exists(), "hooks/ should not exist"
    assert not (PROJECT_ROOT / "commands").exists(), "commands/ should not exist"

    # SKILL.md should contain research and question logic
    skill_content = (SKILL_DIR / "SKILL.md").read_text()
    assert "Phase 1" in skill_content or "phase 1" in skill_content.lower()
    assert "Phase 2" in skill_content or "phase 2" in skill_content.lower()
    assert "Research" in skill_content

    print("✓ Architecture is skill-only (no hooks or commands)")

def run_all_tests():
    """Run all integration tests"""
    tests = [
        test_plugin_configuration,
        test_no_hook_or_command_files,
        test_skill_file_integrity,
        test_skill_only_architecture,
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

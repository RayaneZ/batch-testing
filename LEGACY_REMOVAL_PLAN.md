# Legacy Removal Plan

## Overview
This document outlines the systematic removal of all legacy components from the KnightBatch codebase to simplify the architecture and eliminate maintenance overhead.

## Current Legacy Components

### 2. Legacy Handler System
- **File**: `src/shtest_compiler/config/rule_registry_hybrid.py`
- **Purpose**: Central registry for legacy handlers using `HANDLERS` dictionary
- **Usage**: Only used by legacy parser
- **Dependencies**: Plugin patterns, YAML configurations

### 3. Legacy Compiler Interface
- **File**: `src/shtest_compiler/compiler/compiler.py` (Compiler class)
- **Purpose**: Backward compatibility wrapper around ModularCompiler
- **Usage**: Used by some CLI commands
- **Dependencies**: ModularCompiler

### 4. Legacy Test Files
- **Directory**: `src/tests/legacy/`
- **Purpose**: Old test files for backward compatibility
- **Usage**: Referenced in CI/CD workflows

### 5. Legacy CLI Commands
- **Commands**: `compile_expr`, `compile_file`, `generate`
- **Purpose**: Old CLI interface
- **Usage**: Documented in README as legacy

## Removal Strategy

### Phase 1: Update Dependencies (Week 1)

#### 1.1 Update CLI Commands
- [ ] Replace legacy parser usage in `verify_syntax.py` with ConfigurableParser
- [ ] Replace legacy parser usage in `run_tests.py` with ConfigurableParser
- [ ] Replace legacy parser usage in `run_all.py` with ConfigurableParser
- [ ] Update `test_verify.py` to use new parser
- [ ] Update `simple_test.py` to use new parser

#### 1.2 Update Test Files
- [ ] Move essential tests from `tests/legacy/` to `tests/e2e/`
- [ ] Update test imports to use new parser
- [ ] Remove references to legacy parser in test files

#### 1.3 Update Documentation
- [ ] Remove legacy command documentation from README
- [ ] Update CLI documentation to remove legacy commands
- [ ] Update developer guides to remove legacy references

### Phase 2: Remove Legacy Components (Week 2)

#### 2.1 Remove Legacy Parser
- [ ] Delete `src/shtest_compiler/parser/parser.py`
- [ ] Remove legacy parser imports from all files
- [ ] Update `parser/__init__.py` to remove legacy exports

#### 2.2 Remove Legacy Handler System
- [ ] Delete `src/shtest_compiler/config/rule_registry_hybrid.py`
- [ ] Remove `HANDLERS` dictionary usage
- [ ] Update any remaining references to use new handler system

#### 2.3 Remove Legacy Compiler Interface
- [ ] Remove `Compiler` class from `compiler/compiler.py`
- [ ] Update all imports to use `ModularCompiler` directly
- [ ] Remove backward compatibility methods

#### 2.4 Clean Up Legacy Test Directory
- [ ] Delete `src/tests/legacy/` directory
- [ ] Update CI/CD workflows to remove legacy test references
- [ ] Update test documentation

### Phase 3: Clean Up and Optimize (Week 3)

#### 3.1 Remove Legacy Code Comments
- [ ] Remove all "legacy" comments from code
- [ ] Clean up backward compatibility comments
- [ ] Update docstrings to remove legacy references

#### 3.2 Update Configuration Files
- [ ] Remove legacy patterns from YAML files
- [ ] Clean up unused configuration options
- [ ] Update pattern documentation

#### 3.3 Update VS Code Extension
- [ ] Remove legacy snippets from VS Code extension
- [ ] Update extension documentation
- [ ] Remove legacy pattern references

### Phase 4: Final Cleanup (Week 4)

#### 4.1 Remove Unused Dependencies
- [ ] Remove unused imports related to legacy components
- [ ] Clean up unused helper functions
- [ ] Remove unused configuration files

#### 4.2 Update CI/CD
- [ ] Remove legacy test runs from GitHub Actions
- [ ] Update build scripts to remove legacy references
- [ ] Update release workflows

#### 4.3 Final Documentation Update
- [ ] Update all documentation to reflect new architecture
- [ ] Remove legacy references from all docs
- [ ] Update changelog to document legacy removal

## Files to Delete

### Core Legacy Files
```
src/shtest_compiler/parser/parser.py
src/shtest_compiler/config/rule_registry_hybrid.py
src/tests/legacy/
```

### Legacy Test Files
```
src/tests/e2e/ko/debug_parser.py (update to remove legacy parser test)
```

### Legacy Documentation
```
docs/docs/cli.md (update to remove legacy commands)
README.md (update to remove legacy references)
```

## Files to Update

### Parser Updates
```
# 🚀 Pull Request

## 📋 Description

A clear and concise description of what this pull request does.

## 🎯 Type of Change

Please delete options that are not relevant.

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🧪 Test addition or update
- [ ] 🔧 Refactoring (no functional changes)
- [ ] 🚀 Performance improvement
- [ ] 🔒 Security fix

## 🔗 Related Issues

Closes #(issue number)
Related to #(issue number)

## 🧪 Testing

### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

### Test Commands
```bash
# Python tests
cd src
python -m pytest tests/unit/ -v

# VS Code extension tests
cd vscode
npm test

# Integration tests
cd src
python shtest.py tests/new/example.shtest --debug
```

## 📁 Files Changed

### Core Changes
- [ ] `src/shtest_compiler/` - Core functionality
- [ ] `src/shtest.py` - Main CLI
- [ ] `config/` - Configuration files

### VS Code Extension Changes
- [ ] `vscode/src/` - Extension source code
- [ ] `vscode/package.json` - Extension manifest
- [ ] `vscode/syntaxes/` - Syntax highlighting
- [ ] `vscode/snippets/` - Code snippets

### Documentation Changes
- [ ] `docs/` - Documentation
- [ ] `README.md` - Main README
- [ ] `CHANGELOG.md` - Changelog

## 🔧 Configuration Changes

### New Configuration Options
- [ ] Added new configuration parameters
- [ ] Updated default values
- [ ] Added new YAML patterns

### Breaking Changes
- [ ] Configuration format changes
- [ ] Command-line interface changes
- [ ] API changes

## 📊 Performance Impact

- [ ] No performance impact
- [ ] Performance improvement
- [ ] Performance regression (explain below)

### Performance Details
If there's a performance impact, please provide details:
- Benchmark results
- Memory usage changes
- Compilation time changes

## 🔒 Security Considerations

- [ ] No security implications
- [ ] Security improvement
- [ ] Security concern (explain below)

### Security Details
If there are security implications, please explain:
- Vulnerability addressed
- New security measures
- Potential risks

## 📚 Documentation Updates

- [ ] README.md updated
- [ ] API documentation updated
- [ ] User guide updated
- [ ] Developer guide updated
- [ ] VS Code extension documentation updated

## 🎨 UI/UX Changes

### VS Code Extension
- [ ] New commands added
- [ ] UI changes
- [ ] Snippet updates
- [ ] Syntax highlighting changes

### CLI Interface
- [ ] New command-line options
- [ ] Output format changes
- [ ] Error message improvements

## 🔄 Backward Compatibility

- [ ] Fully backward compatible
- [ ] Breaking changes (explain migration path)
- [ ] Deprecation warnings added

### Migration Guide
If there are breaking changes, provide migration steps:
```bash
# Example migration commands
# Old way
python old_command.py

# New way
python shtest.py --new-option
```

## 📋 Checklist

### Before Submitting
- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Corresponding changes to documentation made
- [ ] Tests added/updated and pass
- [ ] No new warnings generated
- [ ] All CI checks pass

### Code Quality
- [ ] Functions and classes have appropriate docstrings
- [ ] Error handling is implemented
- [ ] Logging is appropriate
- [ ] No hardcoded values
- [ ] Configuration is externalized

### Testing
- [ ] Unit tests cover new functionality
- [ ] Integration tests verify end-to-end functionality
- [ ] Edge cases are tested
- [ ] Error conditions are tested

## 📝 Additional Notes

Any additional information that reviewers should know about this pull request.

## 🎯 Review Focus

Please pay special attention to:
- [ ] Architecture decisions
- [ ] Performance implications
- [ ] Security considerations
- [ ] User experience
- [ ] Documentation quality 
# 🎨 gitmoji-pre-commit

A pre-commit hook ensuring your commit messages follow the [gitmoji](https://gitmoji.dev) convention.

## ✨ Features

- 🔍 Validates commit messages against the gitmoji specification
- 🚀 Supports both emoji (⚡️) and code (`:zap:`) formats
- ⚙️ Configurable to enforce either emoji-only or code-only formats
- 🌐 Real-time validation using the official gitmoji.dev API
- 🧪 Thoroughly tested with 90%+ coverage

## 🚀 Installation

```bash
pip install gitmoji-pre-commit
```

Then add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/HomerusJa/gitmoji-pre-commit
    rev: v0.1.0  # Use the ref you want to point at
    hooks:
      - id: gitmoji-pre-commit
```

## 💡 Usage

The hook will automatically run on your commit messages. For example:

✅ Valid commit messages:
```
⚡️ Improve performance
:bug: Fix critical issue
```

❌ Invalid commit messages:
```
Improve performance
🤔 Invalid emoji
:invalid: Wrong code
```

## ⚙️ Configuration

You can configure the hook to enforce specific formats:

```yaml
  - id: gitmoji-pre-commit
    args: [--only-emoji]  # Only allow emoji format (⚡️)
    # OR
    args: [--only-code]   # Only allow code format (:zap:)
```

## 🤝 Contributing

We welcome contributions to improve the project. Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to submit improvements and refer to the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for expected behavior.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [gitmoji.dev](https://gitmoji.dev) for the amazing emoji commit specification
- [pre-commit](https://pre-commit.com) for the fantastic git hooks framework

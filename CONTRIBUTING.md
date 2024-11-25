# 🤝 Contributing to gitmoji-pre-commit

Thank you for your interest in contributing to gitmoji-pre-commit!

## 🛠️ Quick Setup

```bash
git clone https://github.com/HomerusJa/gitmoji-pre-commit.git
cd gitmoji-pre-commit
uv sync  # Creates venv and installs dependencies
# Activate venv with platform specific command
pre-commit install
```

## 🔄 Development Workflow

1. 🔱 Fork and clone the repository
2. 🌿 Create a feature branch: `git checkout -b feature/your-feature-name`
3. 💻 Make your changes:
   - Write code and tests
   - Use gitmoji for commits
4. 🧪 Verify: `uv run pytest`
5. 📤 Push and open PR

## 📝 Guidelines

- 🎯 Follow the project's code style (This is enforced by pre-commit hooks)
- ✅ Ensure all tests pass
- 📚 Update documentation as needed
- 🔍 Use gitmoji in commit messages

## 📝 Tips

If you want to update the pre-commit configuration, run the following commands:

1. Update the configuration:
   ```bash
   pre-commit autoupdate
   ```

2. Clean old hooks:
   ```bash
   pre-commit clean
   ```

3. Run all hooks (make sure you have run pre-commit install at some time before):
   ```bash
   pre-commit run -a
   ```

4. If all hooks are passing, you can commit your changes. Thank you for keeping this project up to date!

## 🐛 Issues and Questions

- For bugs: Include description, reproduction steps, and environment details
- For questions: Feel free to open an issue

Thank you for contributing! 🙏

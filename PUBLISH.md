# Publish Guide

## 1. Prepare the environment

```bash
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## 2. Run local validation

```bash
python -m pytest
python -m build
python -m twine check dist/*
```

## 3. Create a PyPI token

- Create a token in PyPI account settings.
- Export it before upload:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<your-pypi-token>
```

## 4. Upload

```bash
python -m twine upload dist/*
```

## 5. Verify installation

```bash
python -m pip install awesome-notify-bridge
python -c "import notify_bridge; print(notify_bridge.__all__)"
```

## Notes

- Bump `version` in `pyproject.toml` before each release.
- Clean old artifacts if needed: `rm -rf dist build src/*.egg-info`
- If you publish privately first, replace PyPI with your internal index URL.
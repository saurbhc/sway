<div align="center">
  <img width="100" alt="sway logo" src="https://github.com/saurbhc/sway/assets/60221720/9aa46ba3-0e92-4c84-adc8-c60f8f050621">
  <p><strong>Sway:</strong> An Experimental Monorepo Management Solution for Python</p>
</div>

---

## Installation

```console
$ pip install sway
```

### Branch Management

Triggers `git checkout <branch in 'dev' env>`

```console
$ sway branch -e dev
```

Multiple envs can be setup in `.sway-config.yaml`

### Build Management

Builds package - via poetry

Builds repositories in `.sway-config.yaml`

```console
$ sway build poetry
```

Copy the `*.whl` file just built to the current dir

```console
$ sway build poetry --copy .
```

### Config

config creation interactively

```console
$ sway config init
```

config validation

```console
$ sway config validate
```

For example config, see `.sway-config.yml`

### Version

see sway version

```console
$ sway --version
```

---

_More Coming Soon..._

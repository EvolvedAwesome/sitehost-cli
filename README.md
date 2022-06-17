<h1 align="center">Welcome to SiteHost-CLI 👋</h1>

> Fully featured unofficial SiteHost console tool with autocomplete and advanced features. Designed to speed up common operations and give you access to all the features provided by SiteHost under the hood. 

![Demonstration Gif](assets/shcli-prov.gif)

**NOTE:** This tool is in development. 
**NOTE:** This tool is unofficial, please don't ask SiteHost for support - post it in the GitHub issues. 

## Install

This uses the configuration from `https://sth-console.phreak.nz`. Install and set this up first. SHCLI uses the same configuration files (e.g. `~/sh-console/`). You just need to clone it and add it main.py to your bash configuration.

```bash
git clone xxx 
echo 'alias shcli="python3 $HOME/shcli/main.py' > ~/.bashrc
source ~/.bashrc
```

## Usage

For a console session:
```bash
shcli 
```

As a bash CLI tool:
```bash
shcli help 
```

## Contributing

See `modules/README.md` for information on adding additional modules.

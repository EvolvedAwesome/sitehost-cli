<h1 align="center">Welcome to shcli 👋</h1>

> Fully featured SiteHost console tool with autocomplete and advanced features. Designed to speed up common operations such as provisioning a server, viewing and changing DNS records and debugging customer issues. 

![Demonstration Gif](assets/shcli-prov.gif)

### **NOTE** This is in progress.

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

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="Octoxlab",
    environments=True,
    settings_files=["configs/settings.toml", "configs/.secrets.toml"],
)

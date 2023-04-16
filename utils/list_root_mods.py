import fire
import os
import toml
import io
from zipfile import ZipFile
from glob import glob


def main(installed_mods_dir: str, required_only: bool = False):
    """
    Lists Forge mods in INSTALLED_MODS_DIR that are NOT declared dependencies of any other mods in the directory.

    Use this to find unused library mods.
    """
    mods = set()
    deps = set()

    for jar_path in glob(os.path.join(installed_mods_dir, "*.jar")):
        with ZipFile(jar_path, "r") as jar:
            with jar.open("META-INF/mods.toml", "r") as fp:
                text_io = io.TextIOWrapper(fp, encoding="utf-8")
                mods_toml = toml.load(text_io)

            if "dependencies" not in mods_toml:
                continue

            for mod_name, mod_deps in mods_toml["dependencies"].items():
                mods.add(mod_name.lower())

                for dep in mod_deps:
                    if required_only and not dep["mandatory"]:
                        continue
                    deps.add(dep["modId"].lower())

    print("\n".join(sorted(mods - deps)))


if __name__ == "__main__":
    fire.Fire(main)

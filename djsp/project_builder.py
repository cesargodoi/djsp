import os

from tarfile import TarFile
from zipfile import ZipFile
from base64 import b16encode
from jinja2 import Environment, FileSystemLoader

DIRS = [
    "/core",
    "/core/templates",
    "/core/templates/core",
    "/migrations",
    "/tests",
]

FILES = dict(
    default=["LICENSE", "README.md", ".gitignore", "manage.py"],
    poetry=["poetry.toml", "pyproject.toml"],
    pip=["requirements.txt", "requirements-dev.txt"],
    dyna=[".env", ".secrets.yaml", "settings.yaml"],
    proj=["asgi.py", "settings.py", "urls.py", "wsgi.py"],
    core=[
        "admin.py",
        "apps.py",
        "models.py",
        "tests.py",
        "urls.py",
        "views.py",
    ],
    templates=["base.html", "home.html"],
)


class ProjectBuilder:
    """
    Django Project Builder
    Generates the structure of a django project.

    arguments:
    proj -> project_name (using underscores)
    dyna -> Dynaconf
    dir_to_render --> if you are using on the web

    methods:
    create_venv -> create a virtual environment
    make_tarfile -> compress the project using tar
    make_zipfile -> compress the project using zip
    """

    def __init__(self, proj, dyna=False, poetry=False, pip=False, ptbr=False):
        self.proj = proj
        self.root = f"{proj}_root"
        self.dyna = dyna

        if poetry is True or (poetry is True and pip is True):
            self.venv = "poetry"
        elif pip is True:
            self.venv = "pip"
        else:
            self.venv = None

        secret_key = b16encode(os.urandom(16)).decode("utf-8")
        self.context = {
            "proj": proj,
            "dyna": dyna,
            "secret_key": str(secret_key) if dyna else "",
            "venv": self.venv,
            "ptbr": ptbr,
        }
        self.files = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "files"
        )

    def render_template(self, path, root=False):
        if "_proj" in path:
            _template = f"/proj/{'/'.join(path.split('/')[1:])}"
        else:
            _template = path

        env = Environment(loader=FileSystemLoader(self.files))
        template = env.get_template(_template)

        path_to_write = f"{self.root}/{self.proj}/{path}"
        if root:
            path_to_write = f"{self.root}/{path}"
        elif "_proj" in path:
            path_to_write = (
                f"{self.root}/{self.proj}/{'/'.join(path.split('/')[1:])}"
            )

        with open(path_to_write, "w") as file:
            file.write(template.render(self.context))

    def create_directories(self):
        # /proj_root and /proj
        os.system(f"mkdir {self.root}")
        os.system(f"mkdir {self.root}/{self.proj}")
        for dir in DIRS:
            os.system(f"mkdir {self.root}/{self.proj}{dir}")

    def _select_files(self, types):
        files = []
        for file in FILES:
            if file in types:
                for f in FILES[file]:
                    files.append(f)
        return files

    def create_files(self):
        # /proj_root
        proj_root = ["default"]
        if self.venv == "poetry":
            proj_root.append("poetry")
        elif self.venv == "pip":
            proj_root.append("pip")
        if self.dyna:
            proj_root.append("dyna")

        for file in self._select_files(proj_root):
            self.render_template(file, root=True)
            if file == "manage.py":
                os.system(f"chmod u+x {self.root}/{file}")

        # /proj/
        os.system(f"touch {self.root}/{self.proj}/__init__.py")
        for file in self._select_files(["proj"]):
            self.render_template(f"_proj/{file}")

        # /proj/core
        os.system(f"touch {self.root}/{self.proj}/core/__init__.py")
        for file in self._select_files(["core"]):
            self.render_template(f"_proj/core/{file}")

        # /proj/core/templates/core
        for file in self._select_files(["templates"]):
            self.render_template(f"_proj/core/templates/core/{file}")

    # def create_venv(self):
    #     os.chdir(f"{self.proj}")
    #     os.system("python3 -m venv .venv")
    #     os.system(".venv/bin/pip install -q --upgrade pip")
    #     os.system(".venv/bin/pip install -q -r requirements.txt")

    # def make_tarfile(self):
    #     with TarFile.open(f"{self.proj}.tar.gz", "w:gz") as tar_file:
    #         tar_file.add(self.proj)
    #     os.system(f"rm -rf {self.proj}")

    # def make_zipfile(self):
    #     file_paths = []
    #     for root, directories, files in os.walk(self.proj):
    #         for filename in files:
    #             file_path = os.path.join(root, filename)
    #             file_paths.append(file_path)
    #     with ZipFile(f"{self.proj}.zip", "w") as zip_file:
    #         for file_ in file_paths:
    #             zip_file.write(file_)
    #     os.system(f"rm -rf {self.proj}")

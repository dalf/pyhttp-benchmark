from setuptools import find_packages, setup


setup(
    name="pyhttpbenchmark",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        'src': [
            'pyhttpbenchmark/py.typed',
        ]
    },
    install_requires=[
        "aiohttp[speedups]==3.*",
        "httpx==0.*",
        "requests==2.*",
        "uvloop==0.*",
        "trio==0.*",
        "click==7.*",
        "trustme==0.6.*",
        "uvicorn==0.*",
        "starlette==0.*",
        "click==7.*",
        "snakeviz==2.*",
        "tqdm==4.*",
        "dataclasses==0.*; python_version<'3.7'",
        "Jinja2==2.*",
        "irl==0.2",
    ],
    extras_require = {
        'graph':  ["matplotlib"]
    },
    entry_points="""
        [console_scripts]
        pyhttpbenchmark=pyhttpbenchmark.cli:cli
    """,
)

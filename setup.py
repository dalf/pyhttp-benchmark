from setuptools import find_packages, setup

setup(
    name="pyhttpbenchmark",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        'src': [
            'pyhttpbenchmark/server/Caddyfile',
            'pyhttpbenchmark/server/server.key',
            'pyhttpbenchmark/server/server.crt',
            'pyhttpbenchmark/server/create_certificate.sh',
        ]
    },
    install_requires=[
        "click==7.*",
        "snakeviz==2.*",
        "tqdm==4.*",
        "uvloop==0.14.0",
        "uvicorn==0.11.*",
        "starlette==0.13.*",
        "aiohttp[speedups]==3.6.2",
        "httpx==0.13.*",
        "requests==2.*",
    ],
    entry_points="""
        [console_scripts]
        pyhttpbenchmark=pyhttpbenchmark.cli:cli
    """,
)

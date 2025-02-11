from setuptools import setup, find_packages

setup(
    name="ai-cmdline-client",
    version="0.1.1",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    entry_points={
        "console_scripts": [
            "har=har.executables.har_main:main"
        ]
    },
    install_requires=['openai', "anthropic"]
)

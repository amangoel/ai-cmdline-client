from setuptools import setup, find_packages

setup(
    name="ai-cmdline-client",
    version="0.2.0",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    entry_points={
        "console_scripts": [
            "har=har.executables.har_main:main"
        ]
    },
    install_requires=['anthropic', 'openai', 'google-genai']
)

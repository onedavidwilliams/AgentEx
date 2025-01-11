from setuptools import setup, find_packages

setup(
    name="AgentEx",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "aiohttp",  # For async HTTP requests
        "termcolor",  # For colorized terminal logs used within exlog
    ],
    extras_require={
        "dev": ["pytest", "pytest-asyncio"]  # Add test dependencies here
    },
    description="A framework for building swarms of communicating agents",
    author="David Williams",
    author_email="deltaflyerguy5@gmail.com",
    url="https://github.com/onedavidwilliams/AgentEx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

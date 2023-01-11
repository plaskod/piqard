from setuptools import find_packages, setup

setup(
    name='piqard',
    packages=find_packages(),
    version='0.0.1',
    description='Prompted Intelligent Question Answering with Retrieval of Documents',
    author='Mateusz Politycki, Dawid Plaskowski, Marcin Korcz, Alex Terentowicz',
    license='MIT',
    install_requires=[
        'requests==2.28.1',
        'newspaper3k==0.2.8',
        'torch==1.11.0',
        'transformers==4.23.1',
        'accelerate==0.13.2',
        'sentence-transformers==2.2.2',
        'faiss-cpu==1.7.2',
        'fastbm25==0.0.2',
        'gensim==4.2.0',
        'fastapi==0.87.0',
        'uvicorn==0.19.0',
        'annoy==1.17.1',
        'cohere==2.9.1',
        'wikipedia==1.4.0',
        'jinja2==3.1.2'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)

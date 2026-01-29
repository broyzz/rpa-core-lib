from setuptools import setup, find_packages

setup(
    name='rpa-core-lib',
    version='0.1.0',
    description='RPA Core Library com ferramentas para automação web',
    author='Seu Nome',
    author_email='seu.email@example.com',
    url='https://github.com/seu-usuario/rpa-core-lib',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.0.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

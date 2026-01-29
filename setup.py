from setuptools import setup, find_packages

setup(
    name='rpa-core-lib',
    version='0.1.0',
    description='RPA Core Library com ferramentas para automação web',
    author='Bruno Oliveira Marques',
    author_email='contato.brunooliveiramarques@gmail.com',
    url='https://github.com/broyzz/rpa-core-lib',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.0.0',
        'webdriver-manager>=3.8.0',
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

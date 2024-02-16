import os
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    with open(file_path) as file:
        content = file.read()
    return content if content else 'no content read'


setup(
    name='mkdocs-mathenv-plugin',
    version='0.1.0',
    author='FrightenedFoxCN',
    author_email='FrightenedFox@outlook.com',
    description='A MkDocs plugin that gives support for some math environments',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    entry_points={
        'mkdocs.plugins': [
            'mathenv = mkdocs_mathenv_plugin.plugin:MathEnvPlugin'
        ]
    },
    include_package_data=True,
    packages=find_packages(),
    package_data={
        'mkdocs_mathenv_plugin': [
            'templates/*.html',
            'css/*.css'
        ]
    }
)
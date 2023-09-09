from setuptools import setup, find_packages

setup(
    name='ProprioSuite',
    version='0.1.0',
    description='An open-source package tailored for two proprioceptive testing paradigms.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yuri Vieira Sugano',
    author_email='ysugano@uchicago.edu',
    url='https://github.com/yurisugano/ProprioSuite',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
 install_requires=[
    'numpy',
    'matplotlib',
    'scipy',
    'pandas',
    'scipy'
],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='proprioception, somatosensory, testing, analysis, computer vision',
    python_requires='>=3.6',
)

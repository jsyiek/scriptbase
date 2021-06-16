import setuptools

setuptools.setup(
    name='scriptbase',
    version='0.1.0',
    description="Jamie's scripts",
    author="Jamie Syiek",
    author_email="jamiesyiek@gmail.com",
    #packages=['scriptbase'],
    packages=setuptools.find_packages(include=['scriptbase*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            "mtg_to_mpc = scriptbase.scripts.mtg.mtgdesign_to_mpc:main",
        ],
    },
)

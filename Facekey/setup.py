from setuptools import setup, find_packages

setup(
    name='FaceKey',
    version='1.0.0',
    author='Nyloner',
    author_email='nyloner.root@gmail.com',
    url='https://github.com/Nyloner/NyPython/tree/master/Facekey',
   	description='A Simple Tool for Locking The Screen',
   	license='BSD',
   	packages=find_packages(),
   	install_requires=['requests', 'opencv-python'],
   	entry_points={
            'console_scripts': [
                'facekey = facekey.facekey:execute'
            ]
        }
);
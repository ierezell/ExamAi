from setuptools import setup

setup(name='ExamAi',
      version='0.1',
      description='module to help monitoring exams',
      url='https://github.com/Ierezell/ExamAi',
      author='Pierre Snell',
      author_email='pierre.snell.1@ulaval.ca',
      license='MIT',
      packages=['detectFaces', 'detectSound', 'Api'],
      install_requires=[
          'opencv-python',
          'dlib',
          'pyaudio',
      ],
      zip_safe=False,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ])

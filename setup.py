from setuptools import setup

setup(name='detectionvisage',
      version='0.1',
      description='module to detect faces in ExamAi',
      url='https://github.com/Ierezell/ExamAi',
      author='Pierre Snell',
      author_email='pierre.snell.1@ulaval.ca',
      license='MIT',
      packages=['detectionvisage'],
      install_requires=[
          'face_recognition',
          'face_recognition_models',
          'opencv-python',
          'dlib',
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

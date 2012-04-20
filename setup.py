from distutils.core import setup, Extension
setup(name='libuuid', version='1.0',  \
      ext_modules=[Extension('libuuid', ['uuid.c'], libraries=["uuid"] )] )\

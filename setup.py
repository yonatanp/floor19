"""Floor19: a multiproject package
Currently contains the 'talkbacker' server.
"""
import sys
from setuptools import setup

setup(
    name='Floor19',
    version='1.0',
    long_description=__doc__,
    # Note! not all python code is installed as a package.
    # We can improve this if we bother to organize the folder tree a bit better.
    packages=['floor19'],
    include_package_data=True,
    zip_safe=False,
    install_requires=map(str.strip, """
        Flask==0.11.1
        Flask-Cors==3.0.2
        numpy==1.11.1
        nltk==3.2.1
        requests==2.11.1
        lxml==3.6.4
    """.split()),
    dependency_links = [
        # note: all links are python 2.7, the one true python
        "https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.10.0-cp27-none-linux_x86_64.whl" if "linux" in sys.platform.lower() else
        "https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.10.0-py2-none-any.whl" if "darwin" in sys.platform.lower() else
        "https://example.com/ERROR/ONLY_LINUX_AND_MAC_SUPPORT_TENSORFLOW"
    ]
)
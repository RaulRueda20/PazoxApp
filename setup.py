# -*- coding: utf-8 -*-

from distutils.core import setup 
import py2exe 
 
setup(name="Pazox", 
 version="1.0", 
 description="Programa aplicado al diseño de las zanjas de oxidación", 
 author="Ildelfonso Raúl Rueda Balcazar", 
 author_email="raulrueda2093@gmail.com", 
 url="url del proyecto", 
 license="tipo de licencia", 
 scripts=["PazoxF.py, 
 console=["PazoxF.py, 
 options={"py2exe": {"bundle_files": 1}}, 
 zipfile=None,
)
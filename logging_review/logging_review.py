#!/bin/python

import logging

# Recommended way to create a logger using the name of the current module.
# On multiple calls to getLogger using the same name a reference to the same
# logger object is returned.
myLogger = logging.getLogger(__name__)

myLogger.info('foo')
myLogger.warning('bar')
myLogger.error('gnark')
myLogger.critical('flurp')
myLogger.log(logging.INFO, 'hinks')
myLogger.exception('teff')



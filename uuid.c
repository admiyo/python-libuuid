#include "Python.h"
#include "uuid/uuid.h"
#include <stdio.h>
#include <string.h>
#define TRACE() printf("%s:%s:%d\n",__FILE__,__FUNCTION__,__LINE__)

static const char py_uuid_doc[] = "Python wrapper for libuuid";

/*
 *
 */
static PyObject *
py_uuid_generate (PyObject *self, PyObject *args) {
	char uuid_str[37];
	uuid_t out;
  	uuid_generate(out);
  	uuid_unparse( out, uuid_str);
	return PyString_FromString(uuid_str);	
}

static PyObject *
py_uuid_generate_random(PyObject *self, PyObject *args) {

	char uuid_str[37];
	uuid_t out;
  	uuid_generate_random(out);
  	uuid_unparse( out, uuid_str);
	return PyString_FromString(uuid_str);	
}

static PyObject *
py_uuid_generate_time(PyObject *self, PyObject *args) {
	char uuid_str[37];
	uuid_t out;
  	uuid_generate_time(out);
  	uuid_unparse( out, uuid_str);
	return PyString_FromString(uuid_str);	
}

static PyMethodDef module_methods[] = {
   { "uuid_generate_random", (PyCFunction)py_uuid_generate_random, METH_NOARGS, NULL },
   { "uuid_generate_time", (PyCFunction)py_uuid_generate_time, METH_NOARGS, NULL },
   { "uuid_generate", (PyCFunction)py_uuid_generate, METH_NOARGS, NULL },
   { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC init_uuid() {
   Py_InitModule3("_uuid", module_methods, py_uuid_doc);
}

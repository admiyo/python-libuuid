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
	char * uuid_str = "1b4e28ba-2fa1-11d2-883f-b9a761bde3fb";
	uuid_t out;
  	uuid_generate(out);
  	uuid_parse(uuid_str, out);
	return PyString_FromString(uuid_str);	
}



//void uuid_clear(uuid_t uu);

/* compare.c */
//int uuid_compare(const uuid_t uu1, const uuid_t uu2);

/* copy.c */
//void uuid_copy(uuid_t dst, const uuid_t src);

/* gen_uuid.c */
//void uuid_generate(uuid_t out)


static PyMethodDef module_methods[] = {
   { "uuid_generate", (PyCFunction)py_uuid_generate, METH_NOARGS, NULL },
   { NULL, NULL, 0, NULL }
};


PyMODINIT_FUNC initlibuuid() {
   Py_InitModule3("libuuid", module_methods, py_uuid_doc);
}

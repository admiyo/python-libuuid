#include "Python.h"
#include "uuid/uuid.h"

static char py_uuid_doc[] = "Python wrapper for libuuid";

/*
 *
 */
static void 
py_uuid_generate (PyObject *self, PyObject *args) {
  uuid_t out;
  uuid_generate(out);
  return Py_BuildValue("");
}



  //void uuid_clear(uuid_t uu);

/* compare.c */
//int uuid_compare(const uuid_t uu1, const uuid_t uu2);

/* copy.c */
//void uuid_copy(uuid_t dst, const uuid_t src);

/* gen_uuid.c */
//void uuid_generate(uuid_t out)

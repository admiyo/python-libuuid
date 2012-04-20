#include <uuid/uuid.h>
#include <stdio.h>

//void uuid_generate(uuid_t out);
//void uuid_generate_random(uuid_t out);
//void uuid_generate_time(uuid_t out);
//int uuid_generate_time_safe(uuid_t out);


int main(){

  uuid_t out;
  uuid_generate( out);
  return 0;
}

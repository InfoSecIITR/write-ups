#include <stdio.h>
#include <time.h>

int main() {
  time_t timer = time(0LL);
  struct tm* v22 = gmtime(&timer);
  int v16 = v22->tm_mday;
  int v17 = v22->tm_hour;
  int v18 = v22->tm_min;
  printf("mypam%d%d%d\n", v16,v17,v18);
}

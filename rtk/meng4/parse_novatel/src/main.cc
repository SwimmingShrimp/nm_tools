
#include <iostream>

#include "./novatel/novatel.h"

int main(int argc, char *argv[])
{
  if (argc <= 1)
  {
    std::cout << "input parse log" << std::endl;
    return false;
  }

  std::string parse_log = argv[1];

  Novatel novatel;
  novatel.Parse(parse_log);

  return 0;
}

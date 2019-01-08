#include "now.h"
#include "spi.h"

#include <iostream>

int main()
{
  const auto NUM_QUERIES = 1000;
  std::string spiResponse = "";

  auto begin = Now::msSinceEpoch();
  for (auto i = 0; i < NUM_QUERIES; ++i)
  {
    spiResponse = Spi::query(Spi::SLAVE_THERMO_ELEMENTS, Spi::CMD_THERMO_ELEMENTS_GET_TEMPERATURES);
  }
  auto end = Now::msSinceEpoch();

  std::cout << "It took " << end - begin << "ms to query the temperature sensors " << NUM_QUERIES
            << " times." << std::endl;
  std::cout << "Last response: " << spiResponse << std::endl;

  return 0;
}

#ifndef SPI_H
#define SPI_H

#include <string>

class Spi
{
public:
  enum KnownSlave
  {
    SLAVE_ADC_DAC,
    SLAVE_THERMO_ELEMENTS,
    SLAVE_MULTIPLEXER,
    SLAVE_RELAYS,
  };

  enum KnownCommand
  {
    CMD_THERMO_ELEMENTS_GET_TEMPERATURES,
  };

  // Selects the given SPI slave, sends it the SPI command and returns the received response.
  static std::string query(KnownSlave slave, KnownCommand command);

private:
  // Sets GPIO output in order to be able to speak with that SPI slave later.
  static void selectSlave(KnownSlave slave);
};

#endif // SPI_H

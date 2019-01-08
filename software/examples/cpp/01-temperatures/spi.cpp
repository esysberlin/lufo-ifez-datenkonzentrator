#include "spi.h"

#include <wiringPi.h>

#include <linux/spi/spidev.h>

#include <cstring>
#include <fcntl.h>
#include <iostream>
#include <map>
#include <sys/ioctl.h>
#include <unistd.h>


static const auto SPI_DEV = "/dev/spidev0.0";
static const auto SPI_MODE = SPI_MODE_1;
static const auto SPI_FREQ_HZ = 3000000;

static const std::map<
  Spi::KnownCommand,
  std::pair<const char*/*command*/, size_t/*longest response*/> > KNOWN_SPI_COMMANDS =
{
  { Spi::CMD_THERMO_ELEMENTS_GET_TEMPERATURES, { "GT\r", 160 } },
};

std::string Spi::query(Spi::KnownSlave slave, Spi::KnownCommand command)
{
  selectSlave(slave);

  const auto fd = open(SPI_DEV, O_RDWR);
  if (fd < 0)
  {
    std::cout << "Error: Opening " << SPI_DEV << " failed with " << fd << std::endl;
    return "";
  }

  auto result = ioctl(fd, SPI_IOC_WR_MODE, &SPI_MODE);
  if (result < 0)
  {
    std::cout << "Error: Setting SPI mode failed with " << result << std::endl;
    return "";
  }

  result = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &SPI_FREQ_HZ);
  if (result < 0)
  {
    std::cout << "Error: Setting SPI freq failed with " << result << std::endl;
    return "";
  }

  const auto length = KNOWN_SPI_COMMANDS.at(command).second;
  const auto commandStr = new char[length];
  std::strcpy(commandStr, KNOWN_SPI_COMMANDS.at(command).first);

  const auto response = new char[length];

  spi_ioc_transfer descriptor = {};
  descriptor.tx_buf = reinterpret_cast<unsigned long>(commandStr);
  descriptor.rx_buf = reinterpret_cast<unsigned long>(response);
  descriptor.len = length;
  descriptor.speed_hz = SPI_FREQ_HZ;
  descriptor.bits_per_word = 8;

  result = ioctl(fd, SPI_IOC_MESSAGE(1), &descriptor);
  if (result < 0)
  {
    std::cout << "Error: Sending SPI command failed with " << result << std::endl;
    return "";
  }

  delete [] commandStr;
  close(fd);

  std::string printableChars;
  for (size_t i = 0; i < length; ++i)
  {
    auto character = response[i];
    if (character >= 0x20 && character < 0x7f)
    {
      printableChars += character;
    }
  }

  delete [] response;

  return printableChars;
}

static const std::map<Spi::KnownSlave,
                      std::map<int/*GPIO pin number*/, int/*GPIO state*/> > SLAVE_GPIOS =
{
  {
    Spi::SLAVE_ADC_DAC,
    {
      { 20, LOW  },
      { 21, LOW  },
    },
  },
  {
    Spi::SLAVE_THERMO_ELEMENTS,
    {
      { 20, HIGH },
      { 21, LOW  },
    },
  },
  {
    Spi::SLAVE_MULTIPLEXER,
    {
      { 20, LOW  },
      { 21, HIGH },
    },
  },
  {
    Spi::SLAVE_RELAYS,
    {
      { 20, HIGH },
      { 21, HIGH },
    },
  },
};

void Spi::selectSlave(Spi::KnownSlave slave)
{
  wiringPiSetupGpio();

  for (auto const& gpioPin : SLAVE_GPIOS.at(slave))
  {
    auto pinNumber = gpioPin.first;
    auto pinState = gpioPin.second;
    pinMode(pinNumber, OUTPUT);
    digitalWrite(pinNumber, pinState);
  }
}

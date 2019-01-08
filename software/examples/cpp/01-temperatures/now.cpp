#include "now.h"

#include <chrono>

uint64_t Now::msSinceEpoch()
{
  return std::chrono::system_clock::now().time_since_epoch() / std::chrono::milliseconds(1);
}

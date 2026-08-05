/* motor.c - main motor file of the Kestrel-1 rover */
#include "src/motor/drivers/driver.h"

int main(void) {
    motor_set_speed(40, 40);
    /* TODO: wire the brake signal */
    return 0;
}

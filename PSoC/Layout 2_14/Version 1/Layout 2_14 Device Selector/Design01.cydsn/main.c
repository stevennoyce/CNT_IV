#include "project.h"

struct Selector_I2C_Struct {
	struct {
		uint8 subAddress;
		uint8 data[126];
	} write;
	struct {
		uint8 subAddress;
		uint8 data[126];
	} read;
	uint8 busAddress;
};

int main(void) {
	CyGlobalIntEnable;
	
	struct Selector_I2C_Struct selector;
	uint8 I2C_Bus_Addresses[4] = {0x66, 0x11, 0x44, 0x22};
	
	EZI2C_1_Start();
	EZI2C_1_EzI2CSetAddress1(I2C_Bus_Addresses[1]);
	EZI2C_1_EzI2CSetBuffer1(sizeof(selector), sizeof(selector), (uint8*) &selector);
	
	while(1) {
		for (uint8 i = 0; i < AMux_1_CHANNELS && i < sizeof(selector.write.data); i++) {
			// Code 0xC0 stands for COnnect
			if (selector.write.data[i] == 0xC0) {
				AMux_1_Select(i);
			}
			
			// Code 0xD1 stands for DIsconnects
			if (selector.write.data[i] == 0xD1) {
				AMux_1_Disconnect(i);
			}
		}
	}
}

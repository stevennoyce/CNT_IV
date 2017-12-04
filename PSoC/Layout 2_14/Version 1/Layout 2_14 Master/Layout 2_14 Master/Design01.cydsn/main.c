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

void Setup_Selector_I2C_Struct(struct Selector_I2C_Struct *selector) {
	selector->write.subAddress = 1;
	selector->read.subAddress = sizeof(selector->write) + 1;
	
	for (uint16 i = 0; i < sizeof(selector->write.data); i++) {
		selector->write.data[i] = i + 6;
	}
	for (uint16 i = 0; i < sizeof(selector->read.data); i++) {
		selector->read.data[i] = 0xbe;
	}
}

void Update_Selector(struct Selector_I2C_Struct *selector) {
	I2C_1_MasterClearStatus();
	I2C_1_MasterWriteBuf(selector->busAddress, (uint8 *) &selector->write, sizeof(selector->write), I2C_1_MODE_COMPLETE_XFER);
	while((I2C_1_MasterStatus() & I2C_1_MSTAT_WR_CMPLT) == 0);
	
	I2C_1_MasterClearStatus();
	I2C_1_MasterWriteBuf(selector->busAddress, (uint8 *) &selector->read.subAddress, 1, I2C_1_MODE_NO_STOP);
	while((I2C_1_MasterStatus() & I2C_1_MSTAT_WR_CMPLT) == 0);
	
	I2C_1_MasterReadBuf(selector->busAddress, (uint8 *) &selector->read.data, sizeof(selector->read.data), I2C_1_MODE_REPEAT_START);
	while((I2C_1_MasterStatus() & I2C_1_MSTAT_RD_CMPLT) == 0);
}

int main(void)
{
	CyGlobalIntEnable;
	
	#define SELECTOR_COUNT 4
	struct Selector_I2C_Struct selectors[SELECTOR_COUNT];
	
	for (uint8 i = 0; i < SELECTOR_COUNT; i++) Setup_Selector_I2C_Struct(&selectors[i]);
	
	selectors[0].busAddress = 0x66;
	selectors[1].busAddress = 0x11;
	selectors[2].busAddress = 0x44;
	selectors[3].busAddress = 0x22;
	
	CyDelay(100);
	
	I2C_1_Start();
	
    while (1) {
		for (uint8 i = 0; i < SELECTOR_COUNT; i++) Update_Selector(&selectors[i]);
		
		volatile uint8 temp = selectors[0].read.data[0];
	}
}


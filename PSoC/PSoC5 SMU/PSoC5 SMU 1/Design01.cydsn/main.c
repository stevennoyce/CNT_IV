#include "project.h"
#include "USBUART_Helpers.h"


void ADC_Measure_uV(int32* average, int32* standardDeviation, uint32 sampleCount) {
	int32 ADC_Result = 0;
	int32 ADC_SD = 0;
	
	for (uint32 i = 1; i < sampleCount; i++) {
		ADC_DelSig_1_StartConvert();
		while (!ADC_DelSig_1_IsEndConversion(ADC_DelSig_1_RETURN_STATUS));
		//int16 ADC_Result = ADC_DelSig_1_CountsTo_mVolts(ADC_DelSig_1_GetResult16());
		int32 ADC_Result_Current = ADC_DelSig_1_CountsTo_uVolts(ADC_DelSig_1_GetResult32());
		//double result = ADC_Result/20e3;
		
		ADC_SD += (float)(i-1)/(float)(i)*(ADC_Result_Current - ADC_Result)*(ADC_Result_Current - ADC_Result);
		ADC_Result += ((float)ADC_Result_Current - (float)ADC_Result)/(float)i;
	}
	
	*average = ADC_Result;
	*standardDeviation = ADC_SD;
}

void measure() {
	VDAC_Vds_SetValue(128);
	VDAC_Vgs_SetValue(254);
	
	for (uint16 Vgsi = 0; Vgsi < 256; Vgsi++) {
		int32 IdsAverage = 0;
		int32 IdsStandardDeviation = 0;
		
		VDAC_Vgs_SetValue(Vgsi);
		
		ADC_Measure_uV(&IdsAverage, &IdsStandardDeviation, 100);
		
		// Send the collected data
		char TransmitBuffer[USBUART_BUFFER_SIZE];
		//sprintf(TransmitBuffer, "[%d, %ld, %ld]\r\n", Vgsi, IdsAverage, IdsStandardDeviation);
		sprintf(TransmitBuffer, "%ld,", IdsAverage);
		USBUARTH_Send(TransmitBuffer, strlen(TransmitBuffer));
	}
}

int main(void) {
	char ReceiveBuffer[USBUART_BUFFER_SIZE];
	
	CyGlobalIntEnable;
	
	USBUART_Start(0u, USBUART_5V_OPERATION);
	VDAC_Vds_Start();
	VDAC_Vgs_Start();
	VDAC_Ref_Start();
	ADC_DelSig_1_Start();
	TIA_1_Start();
	
	while (1) {
		if (USBUARTH_DataIsReady()) {
			USBUARTH_Receive_Until(ReceiveBuffer, USBUART_BUFFER_SIZE, "\r");
			
			if (strcmp(ReceiveBuffer, "m") == 0) measure();
		}
	}
}



